#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://www.holavid.com/embed-cje1dkndj6cd.html
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.packer import cPacker
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import dialog
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'holavid', 'holavid')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)

        sUrl = self._url

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        if 'File was deleted' in sHtmlContent:
            VSlog("File was deleted")

        oParser = cParser()
        sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent,sPattern)

        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])

            sPattern = '.mpd"},{file:"([^<]+)",label:"'
            aResult = oParser.parse(sHtmlContent,sPattern)
            if aResult[0]:
                api_call = aResult[1][0] + '|AUTH=TLS&verifypeer=false' 
                
        if api_call:
            return True, api_call

        return False, False
