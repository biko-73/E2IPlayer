# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Ovni-crea
from datetime import datetime

from Components.config import config
from Plugins.Extensions.IPTVPlayer.compat import e2Json_loads
from Plugins.Extensions.IPTVPlayer.libs.matrix.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.libs.matrix.lib.comaddon import VSlog
from Plugins.Extensions.IPTVPlayer.libs.matrix.lib.handler.premiumHandler import \
    cPremiumHandler
from Plugins.Extensions.IPTVPlayer.libs.matrix.lib.handler.requestHandler import \
    cRequestHandler


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'alldebrid', 'Alldebrid', 'violet')

    def setDisplayName(self, displayName):
        self._displayName = f'{displayName} [COLOR violet]{self._defaultDisplayName}/{self.getRealHost()}[/COLOR]'

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        if (token_Alldebrid := cPremiumHandler(self.getPluginIdentifier()).getToken()):
            if not (sUrl_Bypass := config.plugins.iptvplayer.urlmain_alldebrid.value):
                sUrl_Bypass = "https://api.alldebrid.com/v4/link/unlock?agent=vStream&apikey={0}&link={1}"
            sUrl_Bypass %= (token_Alldebrid, self._url)
        else:
            return False, False

        oRequest = cRequestHandler(sUrl_Bypass)
        sHtmlContent = e2Json_loads(oRequest.request())
        try:
            sHtmlContent = oRequest.request()
            sHtmlContent = e2Json_loads(sHtmlContent)
        except:
            VSlog(f'Hoster Alldebrid - json.loads : {sHtmlContent}')

        if 'error' in sHtmlContent:
            if sHtmlContent['error']['code'] in ('LINK_HOST_NOT_SUPPORTED', 'LINK_DOWN'):
                # si alldebrid ne prend pas en charge ce type de lien, on retourne le lien pour utiliser un autre hoster
                return False, self._url
            else:
                VSlog(f'Hoster Alldebrid - Error: {sHtmlContent["error"]["code"]}')
                return False, self._url   # quelque soit l'erreur, on retourne le lien pour utiliser un autre hoster

        api_call = HostURL = sHtmlContent["data"]["link"]
        try:
            mediaDisplay = HostURL.split('/')
            VSlog('Hoster Alldebrid - play : {}/ ... /{}'.format('/'.join(mediaDisplay[0:3]), mediaDisplay[-1]))
        except:
            VSlog(f'Hoster Alldebrid - play : {HostURL}')

        if api_call:
            return True, api_call

        return False, False

    def testPremium(self):
        if not (token_Alldebrid := cPremiumHandler(self.getPluginIdentifier()).getToken()):
            return

        from Plugins.Extensions.IPTVPlayer.libs.matrix.lib.comaddon import \
            dialog
        sUrl = f"https://api.alldebrid.com/v4/user?agent=myAppName&apikey={token_Alldebrid}"
        oRequest = cRequestHandler(sUrl)
        reponse = e2Json_loads(oRequest.request())
        if 'error' in reponse:
            dialog().VSok(reponse['error']['message'])
        elif reponse['status'] == 'success':
            userData = reponse['data']['user']
            timestamp = userData['premiumUntil']
            premiumUntil = datetime.fromtimestamp(timestamp)

            if userData['isTrial']:
                msg = "Version d'essai"
                msg += f"\r\nDate fin= {premiumUntil}"
                msg += f"\r\nSouscription = {userData["isSubscribed"]}"
                if 'remainingTrialQuota' in userData:
                    msg += f"\r\nQuota disponible (MB) = {userData["remainingTrialQuota"]}"
                dialog().VSok(msg)
                return

            msg = f'Compte premium = {userData["isPremium"]}\r\nDate fin = {premiumUntil}'
            dialog().VSok(msg)
        return
