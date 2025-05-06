# -*- coding: utf-8 -*-

from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.vstream.resources.lib.search import \
    cSearch


def showSearch():
    oSearch = cSearch()
    exec("oSearch.searchGlobal()")
    return True
