#coding: utf-8
import re

from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'verystream', 'VeryStream')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        api_call = ''

        sPattern =  'id="videolink">([^<>]+)<\/p>'
        aResult = re.findall(sPattern, sHtmlContent)

        if (aResult):

            api_call = 'https://verystream.com/gettoken/' + aResult[0] + '?mime=true'

        if api_call:
            return True, api_call

        return False, False
