#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://mixloads.com/embed-xxx.html sur topreplay
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.xbmc import xbmcgui

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mixloads', 'Mixloads')

    def _getMediaLinkForGuest(self): 
        VSlog(self._url)       
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = '{file:"([^"]+)",label:"([^"]+)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            url=[]
            qua=[]
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            if len(url) == 1:
                api_call = url[0]

            elif len(url) > 1:
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Quality', qua)
                if (ret > -1):
                    api_call = url[ret]

        if api_call:
            return True, api_call

        return False, False
