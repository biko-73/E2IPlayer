#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
# from resources.lib.packer import cPacker
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'jawcloud', 'Jawcloud')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call =''

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        #VSlog(str(self._url))

        oParser = cParser()
        sPattern = '<source.+?src="(.+?)"'

        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0]):
            api_call = aResult[1][0]

        #VSlog(str(api_call))

        if api_call:
            return True, api_call

        return False, False
