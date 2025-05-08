#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.gui.gui import cGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, GetCacheSubDir
import urllib
import pickle
import time
#pour les sous titres
#https://github.com/amet/service.subtitles.demo/blob/master/service.subtitles.demo/service.py
#player API
#http://mirrors.xbmc.org/docs/python-docs/stable/xbmc.html#Player

class cPlayer():
    def __init__(self, *args):
        VSlog('player initialized')

    def clearPlayList(self):
        return ''

    def __getPlayList(self):
        return ''

    def addItemToPlaylist(self, oGuiElement):
        oGui = cGui()
        VSlog('addItemToPlaylist')
        oListItem =  oGui.createListItem(oGuiElement)
        self.__addItemToPlaylist(oGuiElement, oListItem)

    def __addItemToPlaylist(self, oGuiElement, oListItem):
        printDBG('addTsiplayerWrite0001:')
        sPluginPath='Tsiplayer'    
        sId        = oGuiElement.getSiteName()
        sLabel     = oGuiElement.getTitle()
        sFunction  = 'play'
        sIcon      = oGuiElement.getIcon()
        
        sMediaUrl  = oGuiElement.getMediaUrl()
        sSiteUrl   = oGuiElement.getSiteUrl() 
        printDBG('sMediaUrl:'+sMediaUrl)        
        #PIK = self.MyPath() + "VStream_listing.dat"
        
        #data = [oGuiElement, '']
        #with open(PIK, "a+") as f:
        #    pickle.dump(data, f)        
        #return ''

        #PIK = self.MyPath() + ("tmdb/VStream_listing_%s.dat" % sId)
        #time_now = round(time.time() * 1000)
        #data = [oGuiElement, '',time_now]
        #with open(PIK, "a+b") as f:
        #    pickle.dump(data, f)  
        
    def MyPath(self):
        return GetCacheSubDir('Tsiplayer')
        
    def AddSubtitles(self, files):
        return ''

    def run(self, oGuiElement, sTitle, sUrl):
        return ''

    def startPlayer(self, window=False):
        return ''

    def onPlayBackEnded(self):
        return ''

    def onPlayBackStopped(self):
        return ''

    def onPlayBackStarted(self):
        return ''

    def __getWatchlist(self, sAction):
        return ''

    def __getPlayerType(self):
        return False

    def enable_addon(self,addon):
        return ''
