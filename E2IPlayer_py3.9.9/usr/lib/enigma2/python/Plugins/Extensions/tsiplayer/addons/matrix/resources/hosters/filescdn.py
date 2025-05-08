#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.gui.gui import cGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import dialog
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.packer import cPacker
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog

from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.xbmc import xbmcgui

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filescdn', 'filescdn')
        
    def __getIdFromUrl(self):
        sPattern = "v=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(self._url, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def _getMediaLinkForGuest(self):
        VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        
        api_call = ''
        #type1
        oParser = cParser()
        sPattern = 'file: "(.+?)",'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0]
            
        #type2?   
        sPattern =  "<script type='text/javascript'>(.+?)</script>"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            stri = cPacker().unpack(aResult[1][0])
            sPattern =  'name="src"value="(.+?)"/><embed id="np_vid"type="(.+?)"'
            aResult = oParser.parse(stri, sPattern)
            if (aResult[0] == True):
                url=[]
                qua=[]
                
                for aEntry in aResult[1]:
                    url.append(aEntry[0])
                    qua.append(aEntry[1][:3] + '*' + aEntry[1][3:])

            api_call = dialog().VSselectqual(qua, url)

            if (api_call):
                return True, api_call

        return False, False
