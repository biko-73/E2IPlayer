# -*- coding: utf-8 -*-

_p = '</span'
_o = 'eplist'
_n = 'list_episodes'
_m = 'title=[\'\"]([^\"^\']+?)[\'\"]'
_l = 'search_history'
_k = 'search_item'
_j = 'history'
_i = 'proxy_1'
_h = '<ul'
_g = 'القصه'
_f = '</h3'
_e = 'story'
_d = '<h3'
_c = '<li'
_b = 'search'
_a = 'explore_item'
_Z = 'title_display'
_Y = 'tvshow'
_X = 'ramadan'
_W = 'asia'
_V = '</ul'
_U = 'prev_title'
_T = '<div'
_S = '</li'
_R = 'None'
_Q = 'name'
_P = 'prev_url'
_O = 'series'
_N = 'EPG'
_M = 'movies'
_L = 'good_for_fav'
_K = 'media_type'
_J = None
_I = '</a'
_H = 'desc'
_G = 'category'
_F = 'url'
_E = 'icon'
_D = 'title'
_C = False
_B = True
_A = '>'
from Components.config import ConfigSelection, ConfigText, config, getConfigListEntry
from Plugins.Extensions.IPTVPlayer.compat import urllib_quote_plus
from Plugins.Extensions.IPTVPlayer.components.ihost import CBaseHostClass, CHostBase
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import TranslateTXT as _
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import MergeDicts, ParseColor, printDBG, printExc
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
config.plugins.iptvplayer.extrask_proxy = ConfigSelection(default=_R, choices=[(_R, _(_R)), (_i, _('Alternative proxy server (1)')), ('proxy_2', _('Alternative proxy server (2)'))])
config.plugins.iptvplayer.extrask_alt_domain = ConfigText(default='', fixed_size=_C)

def GetConfigList():
    A = []
    if config.plugins.iptvplayer.extrask_proxy.value == _R:
        A.append(getConfigListEntry(_('Alternative domain:'), config.plugins.iptvplayer.extrask_alt_domain))
    return A

def gettytul():
    return 'Extra 3sk'

class Extra3sk(CBaseHostClass):
    def __init__(A):
        CBaseHostClass.__init__(A, {_j: 'extrask', 'cookie': 'extrask.cookie'})
        A.MAIN_URL = _J
        A.DEFAULT_ICON_URL = 'https://i.ibb.co/WVmn0BT/Extra-3sk.png'
        A.HEADER = A.cm.getDefaultHeader()
        A.AJAX_HEADER = A.HEADER
        A.AJAX_HEADER.update({'X-Requested-With': 'XMLHttpRequest'})
        A.defaultParams = {'header': A.HEADER, 'use_cookie': _B, 'load_cookie': _B, 'save_cookie': _B, 'cookiefile': A.COOKIE_FILE}

    def getProxy(B):
        A = config.plugins.iptvplayer.extrask_proxy.value
        if A!= _R:
            if A == _i:
                A = config.plugins.iptvplayer.alternative_proxy1.value
                return A

    def getPage(B, baseUrl, addParams={}, post_data=_J):
        A = addParams
        if A == {}:
            C, A = (dict(B.defaultParams), B.getProxy())
            A = MergeDicts(A, {'http_proxy': C}) if C!= _J else A
        E, F = B.cm.urlEncodeSafe(baseUrl)
        return (E, F)

    def selectDomain(A):
        C = ['https://bebllash.com/']
        B = config.plugins.iptvplayer.extrask_alt_domain.value.strip()
        if A.cm.isValidUrl(B):
            if B[(-1)]!= '/':
                B += '/'
            C.insert(0, B)
        for B in C:
            D, E = A.getPage(B)
            if D:
                if 'قصة عشق اكسترا / EXTRA' in E:
                    A.setMainUrl(A.cm.meta[_F])
                    break
            else:  # inserted
                if A.MAIN_URL!= _J:
                    pass  # postinserted
                else:  # inserted
                    break
        if A.MAIN_URL == _J:
            A.MAIN_URL = C[0]
        return None

    def getFullIconUrl(B, url):
        A = url
        A = CBaseHostClass.getFullIconUrl(B, A.strip())
        if A == '':
            pass  # postinserted
        return ''

    def listMainMenu(A, cItem):
        printDBG('Extra 3sk.listMainMenu')
        B = [{_G: _M, _D: _('الأفـــلام'), _E: A.DEFAULT_ICON_URL, _K: _M}, {_G: _O, _D: _('مســلـســلات'), _E: A.DEFAULT_ICON_URL, _K: _O}, {_G: _W, _D: _('مســلـســلات آسـيويـة'), _E: A.DEFAULT_ICON_URL, _K: _W}, {_G: _Y, _D: _('بـــرامج'), _E: A.DEFAULT_ICON_URL, _K: _Y}, {_G: _b, _D: _('Search'), _k: _B}, {_G: _l, _D: _('Search history')}]

    def listCatItems(A, cItem, nextCategory):
        B = cItem
        printDBG(f'Extra 3sk.listCatItems cItem[{B}]')
        D, (G, H) = (A.currItem.get(_G, ''), A.getPage(A.getMainUrl()))
        if not G:
            pass  # postinserted
        return None

    def listItems(A, cItem, nextCategory):
        P = 'page'
        printDBG(f'Extra 3sk.listItems cItem[{B}]')
        J, B.get(_K, ''), Q, B[_F], K = (B.get(P, 1), J, B.get(_K, ''), Q, B[_F], K, A.getPage(K))
        if not R:
            pass  # postinserted
        return None

    def exploreItems(A, cItem):
        M = '#89CFFF'
        printDBG(f'Extra 3sk.exploreItems cItem[{B}]')
        N, G = A.getPage(B[_F])
        if not N:
            pass  # postinserted
        return None

    def listSeriesEpisodes(A, cItem):
        B = cItem
        printDBG(f'Extra 3sk.listSeriesEpisodes cItem[{B}]')
        I, E = A.getPage(B[_F])
        if not I:
            pass  # postinserted
        return None

    def listSearchResult(B, cItem, searchPattern, searchType):
        C, searchType, A = (searchPattern, C, searchType)
        printDBG(f'Extra 3sk.listSearchResult cItem[{cItem}], searchPattern[{C}] searchType[{A}]')
        if A == 'all':
            D = B.getFullUrl(f'/?s={urllib_quote_plus(C)}')
        E = {_Q: _G, _K: A, _L: _C, _F: D}

    def getLinksForVideo(A, cItem):
        D = cItem
        printDBG(f'Extra 3sk.getLinksForVideo [{D}]')
        H, J = ([], f'{D[_F]}?do=views')
        if not E:
            pass  # postinserted
        return None

    def getVideoLinks(B, videoUrl):
        A = videoUrl
        printDBG(f'Extra 3sk.getVideoLinks [{A}]')
        return B.up.getVideoLinkExt(A) if B.cm.isValidUrl(A) else None

    def getArticleContent(A, cItem):
        M = 'genre'
        L = 'quality'
        K = 'year'
        J = 'country'
        I = 'writer'
        F = '<a>'
        printDBG(f'Extra 3sk.getArticleContent [{E}]')
        C = {}
        G = E[_P] if _P in E else E
        N, O = A.getPage(G)
        return None

    def handleService(A, index, refresh=0, searchPattern='', searchType=''):
        I = 'listItems'
        C, D, index = (F, searchPattern, E, refresh, D, index)
        printDBG('handleService start')
        CBaseHostClass.handleService(A, C, D, E, F)
        if A.MAIN_URL == _J:
            A.selectDomain()
        B, G = (A.currItem.get(_Q, ''), A.currItem.get(_G, ''))
        printDBG(f'handleService: |||||||||||||||||||||||||||||||||||| name[{G}], category[{B}] ')
        A.currList = []
        if G is _J and (not B):
            A.listMainMenu({_Q: _G, 'type': _G})
        CBaseHostClass.endHandleService(A, C, D)

class IPTVHost(CHostBase):
    def __init__(A):
        CHostBase.__init__(A, Extra3sk(), _B, [])

    def getSearchTypes(B):
        A = []
        A.append(('Movies', _M))
        A.append(('Tv Series', _O))
        return A

    def withArticleContent(B, cItem):
        A = cItem
        if _P in A or A.get(_G, '') == _a:
            return _B