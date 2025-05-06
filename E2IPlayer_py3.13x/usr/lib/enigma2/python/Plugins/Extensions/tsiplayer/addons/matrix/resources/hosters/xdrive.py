# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://xdrive.cc/embed/xxxxxx/blabla.mp4 >fstreamvk

from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'xdrive', 'Xdrive')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = '<source src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
