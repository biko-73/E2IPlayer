from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import dialog, xbmcgui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.packer import cPacker
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog
import re

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'hdup', 'hdup')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = ''

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()
       
        aResult = re.findall('(eval\(function\(p,a,c,k.*?)\s+<\/script>', sHtmlContent, re.DOTALL)
        if aResult:
           for i in aResult:
                sdata = cPacker().unpack(i)
                sPattern = 'file:"(.+?)",label:".+?"}'
                aResult = oParser.parse(sdata,sPattern)
                if aResult[0]:
                    api_call = aResult[1][0] 

        if api_call:
            return True, api_call

        return False, False
