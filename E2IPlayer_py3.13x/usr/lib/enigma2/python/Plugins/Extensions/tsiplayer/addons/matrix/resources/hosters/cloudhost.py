# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# ==>otakufr

from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'cloudhost', 'Cloudhost')

    def _getMediaLinkForGuest(self, api_call=None):
        VSlog(self._url)
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = '<source src="([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
