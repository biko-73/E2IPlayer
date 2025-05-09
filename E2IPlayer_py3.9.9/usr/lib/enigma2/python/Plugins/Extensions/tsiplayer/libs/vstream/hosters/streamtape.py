#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.util import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.util import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
import re

class cHoster(iHoster):
    def __init__(self):
        self.__sDisplayName = 'Streamtape00001'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'streamtape'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        #sPattern1 = 'ById\(\'ideoo.+?=\s*["\']([^"\']+)[\'"].+?["\']([^"\']+)\'\)'
        #aResult = oParser.parse(sHtmlContent, sPattern1)

        #if (aResult[0] == True):
        #    url = aResult[1][0][1]
        #    api_call = 'https://streamtape.com/get_video' + url[url.find('?'):] + "&stream=1&"        
        
        sPattern1 = 'id="ideoolink.*?>(.*?)<'
        Liste_els = re.findall(sPattern1, sHtmlContent, re.S)
        if Liste_els:
            url = Liste_els[0]
            api_call = 'https:/' + url + "&stream=1&"             
        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self.__sUrl

        return False, False
