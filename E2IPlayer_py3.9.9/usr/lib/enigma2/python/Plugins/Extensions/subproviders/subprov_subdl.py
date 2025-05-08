# -*- coding: utf-8 -*-


import re

from Components.config import config
from Plugins.Extensions.IPTVPlayer.compat import e2Json_loads, urllib_urlencode
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import \
    TranslateTXT as _
from Plugins.Extensions.IPTVPlayer.components.isubprovider import (
    CBaseSubProviderClass, CSubProviderBase)
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import (
    GetSubtitlesDir, RemoveDisallowedFilenameChars, byteify, printDBG)
from Plugins.Extensions.IPTVPlayer.tools.manipulateStrings import iterDictItems


def GetConfigList():
    optionList = []
    return optionList


def GetLanguageTab():
    tab = {
        "AR": "Arabic",
        "BR_PT": "Brazillian Portuguese",
        "DA": "Danish",
        "NL": "Dutch",
        "EN": "English",
        "FA": "Farsi_Persian",
        "FI": "Finnish",
        "FR": "French",
        "ID": "Indonesian",
        "IT": "Italian",
        "NO": "Norwegian",
        "RO": "Romanian",
        "ES": "Spanish",
        "SV": "Swedish",
        "VI": "Vietnamese",
        "SQ": "Albanian",
        "AZ": "Azerbaijani",
        "BE": "Belarusian",
        "BN": "Bengali",
        "ZH_BG": "Big 5 code",
        "BS": "Bosnian",
        "BG": "Bulgarian",
        "BG_EN": "Bulgarian_English",
        "MY": "Burmese",
        "CA": "Catalan",
        "ZH": "Chinese BG code",
        "HR": "Croatian",
        "CS": "Czech",
        "NL_EN": "Dutch_English",
        "EN_DE": "English_German",
        "EO": "Esperanto",
        "ET": "Estonian",
        "KA": "Georgian",
        "DE": "German",
        "EL": "Greek",
        "KL": "Greenlandic",
        "HE": "Hebrew",
        "HI": "Hindi",
        "HU": "Hungarian",
        "HU_EN": "Hungarian_English",
        "IS": "Icelandic",
        "JA": "Japanese",
        "KO": "Korean",
        "KU": "Kurdish",
        "LV": "Latvian",
        "LT": "Lithuanian",
        "MK": "Macedonian",
        "MS": "Malay",
        "ML": "Malayalam",
        "MNI": "Manipuri",
        "PL": "Polish",
        "PT": "Portuguese",
        "RU": "Russian",
        "SR": "Serbian",
        "SI": "Sinhala",
        "SK": "Slovak",
        "SL": "Slovenian",
        "TL": "Tagalog",
        "TA": "Tamil",
        "TE": "Telugu",
        "TH": "Thai",
        "TR": "Turkish",
        "UK": "Ukranian",
        "UR": "Urdu"
    }
    return tab


class SubDLProvider(CBaseSubProviderClass):
    LANGUAGE_CACHE = []

    def __init__(self, params={}):
        self.MAIN_URL = 'https://subdl.com/'
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        self.HTTP_HEADER = {'User-Agent': self.USER_AGENT, 'Referer': self.MAIN_URL, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate'}

        self.MAIN_API = 'https://api.subdl.com/api/v1/subtitles'

        params['cookie'] = 'subdl.cookie'
        CBaseSubProviderClass.__init__(self, params)

        self.defaultParams = {'header': self.HTTP_HEADER, 'with_metadata': True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        self.languages = []

        self.dInfo = params['discover_info']
        self.searchTypes = [{'title': _('Search only in Movies'), 'search_only_movies': 'on'}, {'title': _('Search only in TV Series'), 'search_only_tv_series': 'on'}]

    def getPage(self, baseUrl, addParams={}, post_data=None):
        if addParams == {}:
            addParams = dict(self.defaultParams)

        sts, data = self.cm.getPage(baseUrl, addParams, post_data)
        return sts, data

    def initSubProvider(self, cItem):
        printDBG("SubDLProvider.initSubProvider")
        GetLanguage = GetLanguageTab()

        sts, data = self.getPage('https://subdl.strem.bar/language_list.json')
        try:
            jsonData = byteify(e2Json_loads(data))
        except:
            jsonData = byteify({})

        for key, value in iterDictItems(jsonData):
            self.languages.append({'title': value, 'sub_language_id': key})

        if len(self.languages) == 0 or not sts:
            for key, value in iterDictItems(GetLanguage):
                self.languages.append({'title': value, 'sub_language_id': key})

    def listSearchTypes(self, cItem, nextCategory):
        printDBG("SubDLProvider.listLanguages")
        cItem = dict(cItem)
        cItem['category'] = nextCategory
        self.listsTab(self.searchTypes, cItem)

    def listLanguages(self, cItem, nextCategory):
        printDBG("SubDLProvider.listLanguages")
        cItem = dict(cItem)
        cItem['category'] = nextCategory
        self.listsTab(self.languages, cItem)

    def listDownloadItems(self, cItem, nextCategory):
        printDBG("SubDLProvider.listDownloadItems")

        keywords = self.params['confirmed_title']
        subLanguageID = cItem.get('sub_language_id', '')
        searchOnlyTVSeries = cItem.get('search_only_tv_series', '')
        searchOnlyMovies = cItem.get('search_only_movies', '')

        if searchOnlyMovies:
            Type = 'movie'
        elif searchOnlyTVSeries:
            Type = 'tv'

        query = {'api_key': config.plugins.iptvplayer.subdl_api.value, 'type': Type, 'languages': subLanguageID, 'film_name': keywords, 'subs_per_page': 30}
        sts, data = self.getPage(f'{self.MAIN_API}?{urllib_urlencode(query)}')
        if not sts:
            return

        try:
            jsonData = byteify(e2Json_loads(data))
        except:
            jsonData = byteify({})

        if jsonData.get('status', False):

            for result in jsonData["results"]:
                slug = result["slug"]
                for subtitle in jsonData["subtitles"]:
                    if slug in subtitle["name"]:

                        params = dict(cItem)
                        params.update({'category': nextCategory, 'lang': subtitle['language'], 'title': f'[{subtitle['language']}] {subtitle['release_name']}', 'imdbid': result["imdb_id"], 'subId': result["sd_id"], 'url': self.getFullUrl(subtitle['url'], "https://dl.subdl.com"), 'desc': ''})
                        self.addDir(params)

    def getSubtitlesList(self, cItem, nextCategory):
        printDBG("SubDLProvider.getSubtitlesList")

        imdbid = cItem['imdbid']
        subId = cItem['subId']
        urlParams = dict(self.defaultParams)
        tmpDIR = self.downloadAndUnpack(cItem['url'], urlParams)
        if None == tmpDIR:
            return

        cItem = dict(cItem)
        cItem.update({'category': nextCategory, 'path': tmpDIR, 'imdbid': imdbid, 'sub_id': subId})
        self.listSupportedFilesFromPath(cItem)

    def listSubsInPackedFile(self, cItem, nextCategory):
        printDBG("SubDLProvider.listSubsInPackedFile")
        tmpFile = cItem['file_path']
        tmpDIR = tmpFile[:-4]

        if not self.unpackArchive(tmpFile, tmpDIR):
            return

        cItem = dict(cItem)
        cItem.update({'category': nextCategory, 'path': tmpDIR})
        self.listSupportedFilesFromPath(cItem)

    def _getFileName(self, title, lang, subId, imdbid):
        title = RemoveDisallowedFilenameChars(title).replace('_', '.')
        if (match := re.search(r'[^.]', title)):
            title = title[match.start():]

        fileName = f"{title}_{lang}_0_{subId}_{imdbid}"
        fileName += '.srt'
        return fileName

    def downloadSubtitleFile(self, cItem):
        printDBG("SubDLProvider.downloadSubtitleFile")
        retData = {}
        title = cItem['title']
        lang = cItem['lang']
        subId = cItem['sub_id']
        imdbid = cItem['imdbid']
        inFilePath = cItem['file_path']

        outFileName = self._getFileName(title, lang, subId, imdbid)
        outFileName = GetSubtitlesDir(outFileName)

        printDBG(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        printDBG(inFilePath)
        printDBG(outFileName)
        printDBG(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        if self.converFileToUtf8(inFilePath, outFileName, lang):
            retData = {'title': title, 'path': outFileName, 'lang': lang, 'imdbid': imdbid, 'sub_id': subId}

        return retData

    def handleService(self, index, refresh=0):
        printDBG('handleService start')

        CBaseSubProviderClass.handleService(self, index, refresh)

        name = self.currItem.get("name", '')
        category = self.currItem.get("category", '')

        printDBG(f"handleService: name[{name}], category[{category}] ")
        self.currList = []

    # MAIN MENU
        if name == None:
            self.initSubProvider(self.currItem)
            if len(self.languages):
                self.listSearchTypes(self.currItem, 'list_languages')
        elif category == 'list_languages':
            self.listLanguages(self.currItem, 'search_subtitles')
        elif category == 'search_subtitles':
            self.listDownloadItems(self.currItem, 'list_subtitles')
        elif category == 'list_subtitles':
            self.getSubtitlesList(self.currItem, 'list_sub_in_packed_file')
        elif category == 'list_sub_in_packed_file':
            self.listSubsInPackedFile(self.currItem, 'list_sub_in_packed_file')

        CBaseSubProviderClass.endHandleService(self, index, refresh)


class IPTVSubProvider(CSubProviderBase):

    def __init__(self, params={}):
        CSubProviderBase.__init__(self, SubDLProvider(params))
