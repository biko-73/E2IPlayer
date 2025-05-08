# -*- coding: utf-8 -*-

from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.search import cSearch

def showSearch():
    oSearch = cSearch()
    exec("oSearch.searchGlobal()")
    return True
