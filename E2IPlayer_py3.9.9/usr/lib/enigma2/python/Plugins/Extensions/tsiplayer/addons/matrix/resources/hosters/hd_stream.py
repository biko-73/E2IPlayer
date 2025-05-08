# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom
# Hoster pour les liens https://hd-stream.xyz/embed/
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.packer import cPacker
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import dialog
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'hd_stream', 'HDStream')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = False

        oRequestHandler = cRequestHandler(self._url)
        sHtmlContent = oRequestHandler.request()

        oParser = cParser()
        sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:

            sHtmlContent = cPacker().unpack(aResult[1][0])
            sPattern = 'file":"([^"]+)".+?"label":"([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
                url = []
                qua = []

                for aEntry in aResult[1]:
                    url.append(aEntry[0])
                    qua.append(aEntry[1])

                api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
