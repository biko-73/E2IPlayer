# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.packer import cPacker
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'flix555', 'Flix555')

    def _getMediaLinkForGuest(self):
        api_call = False
        VSlog(self._url)

        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        # Attention sous titre present aussi

        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])

            sPattern = '{sources:\[{file:"([^"]+)",label:"([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
                api_call = aResult[1][0][0]

        if api_call:
            return True, api_call

        return False, False
