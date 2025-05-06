# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import GetCacheSubDir
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.xbmc import xbmc
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.xbmc import xbmcgui
import re,os.path,sys,json

# class addon(xbmcaddon.Addon):
class none_(object):
    def __new__(cls, *args):
        return object.__new__(cls)
    def __init__(self, *args):
        pass
    def __getattr__(self, name):
        return self
    def __call__(self, *args, **kwargs):
        return self
    def __int__(self):
        return 0
    def __float__(self):
        return 0
    def __str__(self):
        return '0'
    def __nonzero__(self):
        return False
    def __getitem__(self, key):
        return self
    def __setitem__(self, key, value):
        pass
    def __delitem__(self, key):
        pass
    def __len__(self):
        return 3
    def __iter__(self):
        return iter([self, self, self])


        
class listitem():
    #ListItem([label, label2, iconImage, thumbnailImage, path])
    def __init__(self, label = '', label2 = '', iconImage = '', thumbnailImage = '', path = ''):
        self.items = {}
        self.type  = 'none'

    def setInfo(self,type_, infoLabels):
        self.type  = type_
        self.items.update(infoLabels)

    def setArt(self,artLabels):
        self.items.update(artLabels)

    def setProperty(self, key, value):
        self.items.update({key:value})
    
    def getProperty(self, key):
        return self.items.get(key,'')
    
    def addContextMenuItems(self, items):
        pass

    def getItems(self):
        return self.items

class addon():
    def __init__(self, addonId = None):
        self.addonId = addonId
        self.settings = {}
        self.openSettings()

    def openSettings(self):
        settings_path = '/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/matrix/resources/settings.json'
        with open(settings_path) as json_file:
            self.settings = json.load(json_file)      
        #return None
    
    def getSetting(self, key):
        out = self.settings.get(key,None)
        if out == None:
            VSlog('settings:'+key+' notfound')
            return "false"
        return str(out)
     
    def setSetting(self, key, value):
        if key == 'ZT':
            f = open(GetCacheSubDir('Tsiplayer')+'zt.url', "w")
            f.write(value)
            f.close()
        return None
     
    def getAddonInfo(self, info):
        return None
     
    def VSlang(self, lang):
        #lng = 'French'
        lng = 'English'
        f = open('/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/matrix/resources/language/'+lng+'/strings.po', "r")
        data = f.read()     
        str_out = str(lang)
        lst_data=re.findall('msgctxt.*?"(.*?)".*?msgid.*?"(.*?)".*?msgstr.*?"(.*?)".*?', data, re.S)
        for (msgctxt,msgid,msgstr) in lst_data:
            if (msgctxt.replace('#','').strip() == str(lang)):
                if msgstr.strip() != '':
                    str_out = msgstr
                else:
                    str_out = msgid
                break
        return str_out

class dialog():       
    def VSselectqual(self, list_qual, list_url):
        VSlog('start:'+str(list_url))
        if len(list_url) == 0:
            return ''
        if len(list_url) == 1:
            return list_url[0]
        ret = 0
        i=0
        urlout = ''
        for url in list_url:
            urlout=urlout+url+'|tag:'+list_qual[i]+'||'
            i=i+1
        VSlog('start:'+str(urlout))
        return urlout

    def VSinfo(self, desc, title='vStream', iseconds=0, sound = False):
        return ''
        
    def VSerror(self, e):
        printDBG('VSerror: '+str(e))
        return

    def VSok(self, e):
        printDBG('VSok: '+str(e))
        return
    
class progress():
    def VScreate(self, title='vStream', desc='', large=False):
        return self
    def VSupdate(self, dialog, total, text='', search = False):
        count=0
    def VSupdatesearch(self, dialog, total, text=''):
        count=0
    def VSclose(self, dialog=''):
        return
    def iscanceled(self):
        return False


class window():
    def __init__(self, winID):
        pass
        
    def getProperty(self,prop):
        return 'false'

    def clearProperty(self,prop):
        return ''        

    def setProperty(self,prop,val):
        return ''         

class siteManager():
    
    SITES = 'sites'
    ACTIVE = 'active'
    LABEL = 'label'
    URL_MAIN = 'url'    
    
    def __init__(self):
        self.defaultPath = VSPath('/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/matrix/resources/sites.json')
        self.defaultData = None
        
    def isActive(self,txt):
        return 'true'

    def isEnable(self,txt):
        return 'true'

    def _getDefaultProp(self, sourceName):

        # Chargement des properties par défaut
        if not self.defaultData:
            self.defaultData = json.load(open(self.defaultPath))

        # Retrouver la prop par défaut
        sourceData = self.defaultData[self.SITES].get(sourceName) if self.defaultData and self.SITES in self.defaultData else None
        
        # pas de valeurs par défaut, on en crée à la volée
        if not sourceData:
            return {}

        return sourceData
        
    def getDefaultProperty(self, sourceName, propName):
        defaultProps = self._getDefaultProp(sourceName)
        if propName not in defaultProps:
            return False
        return defaultProps.get(propName)

    def getUrlMain(self, sourceName):
        return str(self.getDefaultProperty(sourceName, self.URL_MAIN))   
    
        

def VSProfil():
    return 'Master user'

def CountdownDialog():
    return False
        
def VSlog(e, level=''):
    printDBG('VSlog: '+str(e))
    return

def IsPython3():
    if sys.version_info[0] < 3:
        return False
    else:
        return True

def isKrypton():
    if IsPython3():
        return False
    else:
        return True

def isMatrix():
    if IsPython3():
        return True
    else:
        return False

def isNexus():
    return False


def VSPath(path):
    path = path.replace('special://temp/',GetCacheSubDir('Tsiplayer'))
    path = path.replace('special://home/userdata/addon_data/plugin.video.matrix/',GetCacheSubDir('Tsiplayer'))
    return path

def VSupdate():
    return ''