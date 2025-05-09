# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://streamz.cc/xxx
import re

from Plugins.Extensions.IPTVPlayer.libs.matrix.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.libs.matrix.lib.comaddon import VSlog
from Plugins.Extensions.IPTVPlayer.libs.matrix.lib.handler.requestHandler import \
    cRequestHandler
from Plugins.Extensions.IPTVPlayer.libs.matrix.lib.packer import cPacker
from Plugins.Extensions.IPTVPlayer.libs.matrix.lib.parser import cParser

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'


def getheader(url, c):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.disableRedirect()
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Cookie', c)
    sHtmlContent = oRequestHandler.request()
    return oRequestHandler.getResponseHeader()['Location']


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'streamz', 'Streamz')

    def _getMediaLinkForGuest(self):
        oParser = cParser()
        VSlog(self._url)
        api_call = False

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()

        urlDownload = oRequest.getRealUrl()
        host = f"https://{urlDownload.split('/')[2]}"

        cookie = oRequest.GetCookies()

        # By-pass fake video
        # Get url
        urlJS = f'{host}/js/count.js'
        oRequest = cRequestHandler(urlJS)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.enableCache(False)
        JScode = oRequest.request()

        JScode = JScode.replace(' ', '')

        r = r"if\(\$\.adblock!=null\){\$\.get\('([^']+)',{([^}]+)}"
        aResult = oParser.parse(JScode, r)
        if not aResult[0]:
            return False, False

        data = aResult[1][0][1].split(':')
        Fakeurl = f'{aResult[1][0][0]}?{data[0]}={data[1].replace("'", "")}'

        # Request URL
        oRequest = cRequestHandler(Fakeurl)
        oRequest.addHeaderEntry('User-Agent', UA)
        try:
            tmp = oRequest.request()
        except:
            pass
        sPattern = r'(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for i in aResult[1]:
                decoded = cPacker().unpack(i)

                if "videojs" in decoded:
                    decoded = decoded.replace('\\', '')

                    r = re.search(r"""src:['"]([^"^']+?)['"]""", decoded, re.DOTALL)
                    if r:
                        url = r.group(1)

            VSlog(url)
            url = url.replace("getlink-", "getmp4-")

            api_call = getheader(url, cookie)

        VSlog(api_call)

        if api_call:
            return True, f'{api_call}|User-Agent={UA}&Referer={self._url}'

        return False, False
