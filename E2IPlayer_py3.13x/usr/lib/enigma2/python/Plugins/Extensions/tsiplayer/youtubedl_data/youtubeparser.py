# -*- coding: utf-8 -*-
###################################################
# LOCAL import
###################################################
from Plugins.Extensions.IPTVPlayer.libs.youtube_dl.extractor.youtube import YoutubeIE
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, printExc, IsExecutable
from Plugins.Extensions.IPTVPlayer.libs.pCommon import common, CParsingHelper
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import TranslateTXT as _
from Plugins.Extensions.IPTVPlayer.libs.urlparserhelper import decorateUrl
from Plugins.Extensions.IPTVPlayer.libs.urlparserhelper import getDirectM3U8Playlist, getMPDLinksWithMeta
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads, dumps as json_dumps
from Plugins.Extensions.IPTVPlayer.libs import ph
###################################################

###################################################
# FOREIGN import
###################################################
import re
import urllib
import codecs
try:
    from urlparse import urlparse, urlunparse, parse_qsl
except:
    from urllib.parse import urlparse, urlunparse, parse_qsl
from datetime import timedelta
from Components.config import config, ConfigSelection, ConfigYesNo
###################################################

###################################################
# Config options for HOST
###################################################
config.plugins.iptvplayer.ytformat = ConfigSelection(default="mp4", choices=[("flv, mp4", "flv, mp4"), ("flv", "flv"), ("mp4", "mp4")])
config.plugins.iptvplayer.ytDefaultformat = ConfigSelection(default="720", choices=[("0", _("the worst")), ("144", "144p"), ("240", "240p"), ("360", "360p"), ("720", "720p"), ("1080", "1080p"), ("9999", _("the best"))])
config.plugins.iptvplayer.ytUseDF = ConfigYesNo(default=True)
config.plugins.iptvplayer.ytAgeGate = ConfigYesNo(default=False)
config.plugins.iptvplayer.ytShowDash = ConfigSelection(default="auto", choices=[("auto", _("Auto")), ("true", _("Yes")), ("false", _("No"))])
config.plugins.iptvplayer.ytSortBy = ConfigSelection(default="", choices=[("", _("Relevance")), ("video_date_uploaded", _("Upload date")), ("video_view_count", _("View count")), ("video_avg_rating", _("Rating"))])


class YouTubeParser():

    def __init__(self):
        self.cm = common()
        self.HTTP_HEADER = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
                            'X-YouTube-Client-Name': '1',
                            'X-YouTube-Client-Version': '2.20201112.04.01',
                            'X-Requested-With': 'XMLHttpRequest'
                            }
        self.http_params = {'header': self.HTTP_HEADER, 'return_data': True}
        self.postdata = {}
        self.sessionToken = ""

        return

    def checkSessionToken(self, data):
        if not self.sessionToken:
            token = self.cm.ph.getSearchGroups(data, '''"XSRF_TOKEN":"([^"]+?)"''')[0]
            if token:
                printDBG("Update session token: %s" % token)
                self.sessionToken = token
                self.postdata = {"session_token": token}

    def findKeys(self, node, kv):
        if isinstance(node, list):
            for i in node:
                for x in self.findKeys(i, kv):
                    yield x
        elif isinstance(node, dict):
            if kv in node:
                yield node[kv]
            for j in node.values():
                for x in self.findKeys(j, kv):
                    yield x

    def getVideoData(self, videoJson):

        videoId = videoJson.get("videoId", "")
        if videoId:
            url = 'http://www.youtube.com/watch?v=%s' % videoId
            try:
                title = videoJson['title']['runs'][0]['text']
            except:
                title = videoJson['title']['simpleText']

            badges = []
            bb = videoJson.get("badges", [])
            for b in bb:
                try:
                    bLabel = b["metadataBadgeRenderer"]["label"]
                    badges.append(bLabel.upper())
                except:
                    pass

            if badges:
                title = title + " [" + (' , '.join(badges)) + "]"

            icon = self.getThumbnailUrl(videoJson)

            desc = []
            try:
                duration = videoJson["lengthText"]["simpleText"]
                if duration:
                    desc.append(_("Duration: %s") % duration)
            except:
                pass

            try:
                views = videoJson["viewCountText"]["simpleText"]
                if views:
                    desc.append(views)
            except:
                pass

            try:
                time = videoJson["publishedTimeText"]["simpleText"]
                if time:
                    desc.append(time)
            except:
                time = ''

            try:
                owner = videoJson["ownerText"]["runs"][0]["text"]
            except:
                try:
                    owner = videoJson["longBylineText"]["runs"][0]["text"]
                except:
                    owner = ""

            if desc:
                desc = " | ".join(desc) + "\n" + owner
            else:
                desc = owner

            try:
                desc = desc + "\n" + videoJson["descriptionSnippet"]["runs"][0]["text"]
            except:
                pass

            return {'type': 'video', 'category': 'video', 'title': title, 'url': url, 'icon': icon, 'time': time, 'desc': desc}
        else:
            return {}


    def getThumbnailUrl(self, thumbJson, maxWidth=1000, hq=False):
        printDBG('---------- thumbJson='+str(thumbJson))
        url = ''
        try:
            thumbJson2 = []
            try:
                thumbJson2 = thumbJson["thumbnail"]["thumbnails"]
            except Exception:
                pass
            if len(thumbJson2) == 0:
                thumbJson2 = thumbJson["thumbnails"][0]['thumbnails']
                print(thumbJson2)
            thumbJson = thumbJson2
            width = 0
            i = 0

            while i < len(thumbJson):
                img = thumbJson[i]
                width = img['width']
                if width < maxWidth:
                    url = img['url']
                i = i + 1

            if hq or (not config.plugins.iptvplayer.allowedcoverformats.value) or config.plugins.iptvplayer.allowedcoverformats.value != 'all':
                #if 'hqdefault' in url:
                #    url = url.replace('hqdefault', 'hq720')
                if '?' in url:
                    url = url.split('?')[0]
        except Exception:
            printExc()
        printDBG('---------- thumbJson='+str(url))
        return url

    def updateQueryUrl(self, url, queryDict):
        urlParts = urlparse(url)
        query = dict(parse_qsl(urlParts[4]))
        query.update(queryDict)
        new_query = urllib.urlencode(query)
        new_url = urlunparse((urlParts[0], urlParts[1], urlParts[2], urlParts[3], new_query, urlParts[5]))
        return new_url
        
    def getSearchResult1(self, pattern, searchType, page, nextPageCategory, sortBy='', url=''):
        printDBG('YouTubeParser.getSearchResult pattern[%s], searchType[%s], page[%s]' % (pattern, searchType, page))
        currList = []

        try:
            #url = 'http://www.youtube.com/results?search_query=%s&filters=%s&search_sort=%s&page=%s' % (pattern, searchType, sortBy, page)

            nextPage = {}
            nP = {}
            nP_new = {}
            r2 = []

            if url:
                # next page search
                sts, data = self.cm.getPage(url, self.http_params, self.postdata)

                if sts:
                    response = json_loads(data)

            else:
                # new search
                # url = 'http://www.youtube.com/results?search_query=%s&filters=%s&search_sort=%s' % (pattern, searchType, sortBy)
                url = 'https://www.youtube.com/results?search_query=' + pattern + '&sp='
                if searchType == 'video':
                    url += 'EgIQAQ%253D%253D'
                if searchType == 'channel':
                    url += 'EgIQAg%253D%253D'
                if searchType == 'playlist':
                    url += 'EgIQAw%253D%253D'
                if searchType == 'live':
                    url += 'EgJAAQ%253D%253D'

                sts, data = self.cm.getPage(url, self.http_params)

                if sts:
                    self.checkSessionToken(data)
                    data2 = self.cm.ph.getDataBeetwenMarkers(data, "window[\"ytInitialData\"] =", "};", False)[1]
                    if len(data2) == 0:
                        data2 = self.cm.ph.getDataBeetwenMarkers(data, "var ytInitialData =", "};", False)[1]

                    response = json_loads(data2 + "}")

            if not sts:
                return []

            #printDBG("--------------------")
            #printDBG(json_dumps(response))
            #printDBG("--------------------")

            # search videos
            r2 = list(self.findKeys(response, 'videoRenderer'))

            printDBG("---------------------")
            printDBG(json_dumps(r2))
            printDBG("---------------------")

            for item in r2:
                params = self.getVideoData(item)

                if params:
                    printDBG(str(params))
                    currList.append(params)

            # search channels

            r2 = list(self.findKeys(response, 'channelRenderer'))

            printDBG("---------------------")
            printDBG(json_dumps(r2))
            printDBG("---------------------")

            for item in r2:
                params = self.getChannelData(item)

                if params:
                    printDBG(str(params))
                    currList.append(params)

            #search playlists

            r2 = list(self.findKeys(response, 'playlistRenderer'))

            printDBG("---------------------")
            printDBG(json_dumps(r2))
            printDBG("---------------------")

            for item in r2:
                params = self.getPlaylistData(item)

                if params:
                    printDBG(str(params))
                    currList.append(params)

            nP = list(self.findKeys(response, "nextContinuationData"))
            nP_new = list(self.findKeys(response, "continuationEndpoint"))

            if nP:
                nextPage = nP[0]
                #printDBG("-------------------------------------------------")
                #printDBG(json_dumps(nextPage))
                #printDBG("-------------------------------------------------")

                ctoken = nextPage["continuation"]
                itct = nextPage["clickTrackingParams"]
                try:
                    label = nextPage["label"]["runs"][0]["text"]
                except:
                    label = _("Next Page")

                urlNextPage = self.updateQueryUrl(url, {'pbj': '1', 'ctoken': ctoken, 'continuation': ctoken, 'itct': itct})
                params = {'type': 'more', 'category': "search_next_page", 'title': label, 'page': str(int(page) + 1), 'url': urlNextPage}
                printDBG(str(params))
                currList.append(params)

            elif nP_new:
                printDBG("-------------------------------------------------")
                printDBG(json_dumps(nP_new))
                printDBG("-------------------------------------------------")
                nextPage = nP_new[0]

                ctoken = nextPage["continuationCommand"]["token"]
                itct = nextPage["clickTrackingParams"]
                label = _("Next Page")

                urlNextPage = self.updateQueryUrl(url, {'pbj': '1', 'ctoken': ctoken, 'continuation': ctoken, 'itct': itct})
                params = {'type': 'more', 'category': "search_next_page", 'title': label, 'page': str(int(page) + 1), 'url': urlNextPage}
                printDBG(str(params))
                currList.append(params)

        except Exception:
            printExc()

        return currList

    def getSearchResult(self, pattern, searchType, page, nextPageCategory, sortBy='A', url=''):
        printDBG('YouTubeParser.getSearchResult pattern[%s], searchType[%s], page[%s]' % (pattern, searchType, page))
        currList = []

        try:
            #url = 'http://www.youtube.com/results?search_query=%s&filters=%s&search_sort=%s&page=%s' % (pattern, searchType, sortBy, page)

            nextPage = {}
            nP = {}
            nP_new = {}
            r2 = []

            if url:
                # next page search
                url = strwithmeta(url)
                if 'post_data' in url.meta:
                    http_params = dict(self.http_params)
                    http_params['header']['Content-Type'] = 'application/json'
                    http_params['raw_post_data'] = True
                    sts, data = self.cm.getPage(url, http_params, url.meta['post_data'])
                else:
                    sts, data = self.cm.getPage(url, self.http_params, self.postdata)

                if sts:
                    response = json_loads(data)

            else:
                # new search
                # url = 'http://www.youtube.com/results?search_query=%s&filters=%s&search_sort=%s' % (pattern, searchType, sortBy)
                url = 'https://www.youtube.com/results?search_query=' + pattern + '&sp='
                if searchType == 'video':
#                    url += 'EgIQAQ%253D%253D'
                    url += 'CA%sSAhAB' % sortBy
                if searchType == 'channel':
#                    url += 'EgIQAg%253D%253D'
                    url += 'CA%sSAhAC' % sortBy
                if searchType == 'playlist':
#                    url += 'EgIQAw%253D%253D'
                    url += 'CA%sSAhAD' % sortBy
                if searchType == 'live':
                    url += 'EgJAAQ%253D%253D'

                sts, data = self.cm.getPage(url, self.http_params)

                if sts:
                    self.checkSessionToken(data)
                    data2 = self.cm.ph.getDataBeetwenMarkers(data, "window[\"ytInitialData\"] =", "};", False)[1]
                    if len(data2) == 0:
                        data2 = self.cm.ph.getDataBeetwenMarkers(data, "var ytInitialData =", "};", False)[1]

                    response = json_loads(data2 + "}")

            if not sts:
                return []

#            printDBG("-------- response ------------")
#            printDBG(json_dumps(response))
#            printDBG("------------------------------")

            # search videos
            r2 = list(self.findKeys(response, 'videoRenderer'))

            printDBG("---------------------")
            printDBG(json_dumps(r2))
            printDBG("---------------------")

            for item in r2:
                params = self.getVideoData(item)

                if params:
                    printDBG(str(params))
                    currList.append(params)

            # search channels

            r2 = list(self.findKeys(response, 'channelRenderer'))

            printDBG("---------------------")
            printDBG(json_dumps(r2))
            printDBG("---------------------")

            for item in r2:
                params = self.getChannelData(item)

                if params:
                    printDBG(str(params))
                    currList.append(params)

            #search playlists

            r2 = list(self.findKeys(response, 'playlistRenderer'))

            printDBG("---------------------")
            printDBG(json_dumps(r2))
            printDBG("---------------------")

            for item in r2:
                params = self.getPlaylistData(item)

                if params:
                    printDBG(str(params))
                    currList.append(params)

            nP = list(self.findKeys(response, "nextContinuationData"))
            nP_new = list(self.findKeys(response, "continuationEndpoint"))

            if nP:
                nextPage = nP[0]
#                printDBG("-------------- nextPage -------------------------")
#                printDBG(json_dumps(nextPage))
#                printDBG("-------------------------------------------------")

                ctoken = nextPage["continuation"]
                itct = nextPage["clickTrackingParams"]
                try:
                    label = nextPage["label"]["runs"][0]["text"]
                except:
                    label = _("Next Page")

                urlNextPage = self.updateQueryUrl(url, {'pbj': '1', 'ctoken': ctoken, 'continuation': ctoken, 'itct': itct})
                params = {'type': 'more', 'category': "search_next_page", 'title': label, 'page': str(int(page) + 1), 'url': urlNextPage}
                printDBG(str(params))
                currList.append(params)

            elif nP_new:
                printDBG("-------------------------------------------------")
                printDBG(json_dumps(nP_new))
                printDBG("-------------------------------------------------")
                nextPage = nP_new[0]

                ctoken = nextPage["continuationCommand"]["token"]
                itct = nextPage["clickTrackingParams"]
                label = _("Next Page")

                urlNextPage = "https://www.youtube.com/youtubei/v1/search?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
                post_data = {'context': {'client': {'clientName': 'WEB', 'clientVersion': '2.20201021.03.00', }}, }
                post_data['continuation'] = ctoken
                post_data['context']['clickTracking'] = {'clickTrackingParams': itct}
                post_data = json_dumps(post_data).encode('utf-8')
                urlNextPage = strwithmeta(urlNextPage, {'post_data': post_data})
                params = {'type': 'more', 'category': "search_next_page", 'title': label, 'page': str(int(page) + 1), 'url': urlNextPage}
                printDBG(str(params))
                currList.append(params)

        except Exception:
            printExc()

        return currList
        
    def getPlaylistData(self, plJson):

        plId = plJson.get("playlistId", "")
        if plId:
            url = "https://www.youtube.com/playlist?list=%s" % plId
            title = plJson['title']['simpleText']
            icon = self.getThumbnailUrl(plJson)

            videoCount = plJson['videoCount']
            desc = _("videos: %s") % videoCount
            try:
                by = plJson["longBylineText"]["runs"][0]["text"]
                desc = desc + "\n" + by
            except:
                pass
            return {'type': 'category', 'category': 'playlist', 'title': title, 'url': url, 'icon': icon, 'time': '', 'desc': desc}
        else:
            return {}

    def getVideosFromPlaylist(self, url, category, page, cItem):
        printDBG('YouTubeParser.getVideosFromPlaylist')
        currList = []
        try:
            sts, data = self.cm.getPage(url, self.http_params)
            if sts:
                self.checkSessionToken(data)

                data2 = self.cm.ph.getDataBeetwenMarkers(data, "window[\"ytInitialData\"] =", "};", False)[1]
                if len(data2) == 0:
                    data2 = self.cm.ph.getDataBeetwenMarkers(data, "var ytInitialData =", "};", False)[1]

                response = json_loads(data2 + "}")

                r1 = response['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents']

                r2 = []
                for i in range(len(r1)):
                    r2.extend(r1[i]['itemSectionRenderer']['contents'])

                for r3 in r2:
                    pl = r3.get('playlistVideoListRenderer', '')
                    if pl:
                        pl2 = pl.get('contents', [])

                        for p in pl2:
                            videoJson = p.get('playlistVideoRenderer', '')
                            if videoJson:
                                params = self.getVideoData(videoJson)
                                if params:
                                    try:
                                        params['title'] = "%s. - %s " % (videoJson["index"]["simpleText"], params['title'])
                                    except:
                                        pass
                                    printDBG(str(params))
                                    currList.append(params)

        except Exception:
            printExc()

        return currList

    def getChannelData(self, chJson):

        chId = chJson.get("channelId", "")
        if chId:
            url = 'https://www.youtube.com/channel/%s' % chId
            title = chJson['title']['simpleText']

            icon = self.getThumbnailUrl(chJson)

            try:
                desc = chJson["descriptionSnippet"]["runs"][0]["text"]
            except:
                desc = ""

            return {'type': 'category', 'category': 'channel', 'title': title, 'url': url, 'icon': icon, 'time': '', 'desc': desc}

        else:
            return {}
            
    def getVideosFromChannelList(self, url, category, page, cItem):
        printDBG('YouTubeParser.getVideosFromChannelList page[%s]' % (page))
        currList = []

        try:
            url = strwithmeta(url)
            if 'post_data' in url.meta:
                http_params = dict(self.http_params)
                http_params['header']['Content-Type'] = 'application/json'
                http_params['raw_post_data'] = True
                sts, data = self.cm.getPage(url, http_params, url.meta['post_data'])
            else:
                sts, data = self.cm.getPage(url, self.http_params)

            if sts:
                if 'browse' in url:
                    # next pages
                    response = json_loads(data)['onResponseReceivedActions']

                    rr = {}
                    for r in response:
                        if r.get("appendContinuationItemsAction", ""):
                            rr = r
                            break

                    if not rr:
                        return []

                    r1 = rr["appendContinuationItemsAction"]
                    r4 = r1.get("continuationItems", [])

                else:
                    # first page of videos
                    self.checkSessionToken(data)
                    data2 = self.cm.ph.getDataBeetwenMarkers(data, "window[\"ytInitialData\"] =", "};", False)[1]
                    if len(data2) == 0:
                        data2 = self.cm.ph.getDataBeetwenMarkers(data, "var ytInitialData =", "};", False)[1]

                    response = json_loads(data2 + "}")

                    r1 = response['contents']['twoColumnBrowseResultsRenderer']['tabs']

                    r2 = {}
                    for tab in r1:
                        try:
                            if tab['tabRenderer']['content']:
                                r2 = tab['tabRenderer']['content']
                        except:
                            pass

                        if r2:
                            break

                    r3 = r2['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
                    r4 = r3[0]['gridRenderer'].get('items', '')

                nextPage = ''
                for r5 in r4:
                    videoJson = r5.get("gridVideoRenderer", "")
                    nP = r5.get('continuationItemRenderer', '')
                    if videoJson:
                        params = self.getVideoData(videoJson)
                        if params:
                            printDBG(str(params))
                            currList.append(params)
                    if nP != '':
                        nextPage = nP

                if nextPage:
                    ctoken = nextPage["continuationEndpoint"]["continuationCommand"].get('token', '')
                    ctit = nextPage["continuationEndpoint"]["clickTrackingParams"]
                    try:
                        label = nextPage["nextContinuationData"]["label"]["runs"][0]["text"]
                    except:
                        label = _("Next Page")

                    urlNextPage = "https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
                    post_data = {'context': {'client': {'clientName': 'WEB', 'clientVersion': '2.20201021.03.00', }}, }
                    post_data['continuation'] = ctoken
                    post_data['context']['clickTracking'] = {'clickTrackingParams': ctit}
                    post_data = json_dumps(post_data).encode('utf-8')
                    urlNextPage = strwithmeta(urlNextPage, {'post_data': post_data})
                    params = {'type': 'more', 'category': category, 'title': label, 'page': str(int(page) + 1), 'url': urlNextPage}
                    printDBG(str(params))
                    currList.append(params)

        except Exception:
            printExc()

        return currList