#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog
# from resources.lib.packer import cPacker

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'downace', 'Downace')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        #sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        #aResult = oParser.parse(sHtmlContent,sPattern)
        #if aResult[0]:
        #    sHtmlContent = cPacker().unpack(aResult[1][0])

        sPattern = 'controls preload="none" src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0] #pas de choix qualité trouvé pour le moment

        if api_call:
            return True, api_call

        return False, False
