# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import addon, dialog, listitem, xbmc
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.tmdb import cTMDb
from datetime import date, datetime

import unicodedata
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.xbmc import xbmcvfs
import time
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import GetCacheSubDir

# -----------------------
#     Cookies gestion
# ------------------------


class GestionCookie():
    #PathCache = 'special://userdata/addon_data/plugin.video.vstream'
    PathCache = GetCacheSubDir('Tsiplayer')[:-1]
    def MakeListwithCookies(self,c):
        t = {}
        c = c.split(';')
        for i in c:
            j = i.split('=',1)
            if len(j) > 1:
                t[j[0]] = j[1]
            
        return t
        

    def DeleteCookie(self, Domain):
        Name = '/'.join([self.PathCache, 'cookie_%s.txt']) % (Domain)
        xbmcvfs.delete(Name)

    def SaveCookie(self, Domain, data):
        Name = '/'.join([self.PathCache, 'cookie_%s.txt']) % (Domain)

        # save it
        # file = open(Name, 'w')
        # file.write(data)
        # file.close()

        f = xbmcvfs.File(Name, 'w')
        f.write(data)
        f.close()

    def Readcookie(self, Domain):
        Name = '/'.join([self.PathCache, 'cookie_%s.txt']) % (Domain)

        # try:
        #     file = open(Name,'r')
        #     data = file.read()
        #     file.close()
        # except:
        #     return ''

        try:
            f = xbmcvfs.File(Name)
            data = f.read()
            f.close()
        except:
            return ''

        return data

    def AddCookies(self):
        cookies = self.Readcookie(self.__sHosterIdentifier)
        return 'Cookie=' + cookies
        
    def MixCookie(self,ancien_cookies, new_cookies):
        t1 = self.MakeListwithCookies(ancien_cookies)
        t2 = self.MakeListwithCookies(new_cookies)
        #Les nouveaux doivent ecraser les anciens
        for i in t2:
            t1[i] = t2[i]
                
        cookies = ''
        for c in t1:
            cookies = cookies + c + '=' + t1[c] + ';'
        cookies = cookies[:-1]
        return cookies

# -------------------------------
#     Configuration gestion
# -------------------------------

class cConfig():

    # def __init__(self):

        # import xbmcaddon
        # self.__oSettings = xbmcaddon.Addon(self.getPluginId())
        # self.__aLanguage = self.__oSettings.getLocalizedString
        # self.__setSetting = self.__oSettings.setSetting
        # self.__getSetting = self.__oSettings.getSetting
        # self.__oVersion = self.__oSettings.getAddonInfo('version')
        # self.__oId = self.__oSettings.getAddonInfo('id')
        # self.__oPath = self.__oSettings.getAddonInfo('path')
        # self.__oName = self.__oSettings.getAddonInfo('name')
        # self.__oCache = xbmc.translatePath(self.__oSettings.getAddonInfo('profile'))
        # self.__sRootArt = os.path.join(self.__oPath, 'resources' , 'art', '')
        # self.__sIcon = os.path.join(self.__oPath,'resources', 'art','icon.png')
        # self.__sFanart = os.path.join(self.__oPath,'resources','art','fanart.jpg')
        # self.__sFileFav = os.path.join(self.__oCache,'favourite.db').decode('utf-8')
        # self.__sFileDB = os.path.join(self.__oCache,'vstream.db').decode('utf-8')
        # self.__sFileCache = os.path.join(self.__oCache,'video_cache.db').decode('utf-8')

    def isDharma(self):
        return self.__bIsDharma

    def getSettingCache(self):
        return False

    def getAddonPath(self):
        return False

    def getRootArt(self):
        return False

    def getFileFav(self):
        return False

    def getFileDB(self):
        return False

    def getFileCache(self):
        return False


def WindowsBoxes(sTitle, sFileName, metaType, year=''):
    return False
