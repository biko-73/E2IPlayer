# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.vstream.resources.lib.comaddon import \
    addon
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.vstream.resources.lib.gui.gui import \
    cGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.vstream.resources.lib.handler.outputParameterHandler import \
    cOutputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.vstream.resources.lib.handler.pluginHandler import \
    cPluginHandler


def globalSources():
    oGui           = cGui()
    oPluginHandler = cPluginHandler()
    aPlugins = oPluginHandler.getAvailablePlugins(force=True)

    if len(aPlugins) == 0:
        addons = addon()
        addons.openSettings()
        oGui.updateDirectory()
    else:
        for aPlugin in aPlugins:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            icon = 'sites/%s.png' % (aPlugin[1])
            # icon = 'https://imgplaceholder.com/512x512/transparent/fff?text=%s&font-family=Roboto_Bold' % aPlugin[1]
            oGui.addDir(aPlugin[1], 'load', aPlugin[0], icon, oOutputParameterHandler)
    oGui.setEndOfDirectory()
    return