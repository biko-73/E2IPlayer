# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler


class cHosterHandler:

    def getUrl(self, oHoster):
        sUrl = oHoster.getUrl()
        VSlog("hosterhandler " + sUrl)
        oRequest = cRequestHandler(sUrl)
        sContent = oRequest.request()

        aMediaLink = cParser().parse(sContent, oHoster.getPattern())
        if (aMediaLink[0] == True):
            return True, aMediaLink[1][0]
        return False, ''

    def getHoster(self, sHosterFileName):
        exec("from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters." + sHosterFileName + " import cHoster")

        return cHoster()
