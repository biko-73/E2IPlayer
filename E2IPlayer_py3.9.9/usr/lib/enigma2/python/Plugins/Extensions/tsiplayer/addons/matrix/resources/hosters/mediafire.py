#-*- coding: utf-8 -*-

from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog, xbmcgui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.packer import cPacker
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import dialog
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.xbmc import xbmcgui
import re

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mediafire', 'mediafire')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
    
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
            #(.+?)([^<]+)
        oParser = cParser()
        sPattern =  'aria-label="Download file".+?href="(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            api_call = aResult[1][0]
        if api_call:
            return True, api_call + '|User-Agent=' + UA
                     
            
        return False, False
