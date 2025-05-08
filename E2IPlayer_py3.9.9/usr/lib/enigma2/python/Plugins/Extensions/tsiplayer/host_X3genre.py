# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG,MergeDicts
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import GetIPTVSleep
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,gethostname,tscolor
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.urlparser    import urlparser as ts_urlparser

try:
    from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.requestHandler import cRequestHandler
    from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.config import GestionCookie
except:
    pass 
    
import re
import time


###################################################
#01# HOST https://akoam.net
###################################################
def getinfo():
    info_={}
    info_['name']=' >●★| Ramadan 2023 |★●<'
    info_['version']='4.0 22/03/2023'
    info_['dev']='RGYSoft'
    info_['cat_id']='21'
    info_['desc']='أفلام و مسلسلات رمضان 2023'
    info_['icon']='https://i.ibb.co/pQ8LgPr/Ramadan.png'
    #info_['recherche_all']='1'
    #info_['update']='Fix Links Extract'
    return info_


class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'tsiplayer.cookie'})
        #self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        #self.MAIN_URL = 'https://akwam.net'
        #self.HEADER = {'User-Agent': self.USER_AGENT, 'DNT':'1', 'Accept': 'text/html', 'Accept-Encoding':'gzip, deflate','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
        #self.AJAX_HEADER = MergeDicts(self.HEADER, {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'})
        #self.defaultParams = {'header':self.HEADER,'with_metadata':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        #self.cacheLinks = {}
        #self.getPage = self.cm.getPage

    def showmenu00(self,cItem):
        self.addDir({'import':cItem['import'],'category' :'host2','title':'رمضان 2020' ,'icon':cItem['icon'],'mode':'20','sub_mode':0})
        self.addDir({'import':cItem['import'],'category' :'host2','title':'رمضان 2019' ,'icon':cItem['icon'],'mode':'20','sub_mode':1})

    def showmenu0(self,cItem):
        sub_mode=cItem.get('sub_mode', 0)
        if sub_mode==0:
            self.addDir({'category': 'host2', 'title': tscolor('\c0000????')+'Assabile'  , 'mode': '00', 'url': '', 'import': 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_assabile import ', 'icon':cItem['icon'], 'type': 'category', 'desc': 'Quran Audio Library'})
            self.addDir({'category': 'host2', 'title': tscolor('\c0000????')+'MP3Quran'  , 'mode': '00', 'url': '', 'import': 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_mp3quran import ', 'icon':cItem['icon'], 'type': 'category', 'desc': 'Quran Audio Library'})
            self.addDir({'category': 'host2', 'title': 'Cima4u', 'mode': '30', 'url': '/category/مسلسلات-7series/مسلسلات-رمضان-2023/', 'name': 'category', 'import': 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_cima4u import ', 'type': 'category', 'icon':cItem['icon']})
            self.addDir({'category': 'host2', 'title': 'Akwam' , 'mode': '30', 'url': '/series?section=0&category=87&rating=0&year=2023&language=0&formats=0&quality=0', 'import': 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_akwam import ', 'icon':cItem['icon'], 'type': 'category', 'desc': ''})
            self.addDir({'category': 'host2', 'title': 'Extra-3sk' , 'mode': '20', 'url': '/category/ramadan-2023', 'sub_mode': '0', 'import': 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_extra3sk import ', 'type': 'category', 'icon':cItem['icon']})
            self.addDir({'category': 'host2', 'title': 'CimaNow'   , 'mode': '20', 'url': '/category/رمضان-2023/', 'mode': '20', 'import': 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_cimanow import ', 'type': 'category', 'icon':cItem['icon']})
            self.addDir({'category': 'host2', 'title': 'Wecima'    , 'mode': '20', 'url': '/category/مسلسلات/مسلسلات-رمضان-2023-series-ramadan-2023/', 'import': 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_mycima import ', 'icon':cItem['icon'], 'type': 'category', 'desc': ''})


            #self.addDir({'category': 'host2', 'title': 'Egybest'   , 'mode': '30', 'url': '/ramadan-2022/', 'import': 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_egybest import ', 'icon': 'https://i.ibb.co/z2SXTd8/souayah-Egy-Best-film.png', 'type': 'category', 'desc': '', 'page':1})
            #self.addDir({'category': 'host2', 'title': 'ArbLionz'  , 'mode': '20', 'url': '/category/series/arabic-series/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86-2022/', 'sub_mode': 'serie', 'import': 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_arablionz import ', 'icon': 'https://i.ibb.co/861LmCL/Sans-titre.png', 'type': 'category', 'page': 1, 'desc': '\xd9\x85\xd8\xb3\xd9\x84\xd8\xb3\xd9\x84\xd8\xa7\xd8\xaa \xd8\xb1\xd9\x85\xd8\xb6\xd8\xa7\xd9\x86'})
            #self.addDir({'category': 'host2', 'title': 'ArabSeed'  , 'mode': '20', 'url': '/category/%d8%a7%d9%84%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86-2022', 'name': 'category', 'import': 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_arabseed import ', 'type': 'category', 'icon': 'https://i.ibb.co/7S7tWYb/arabseed.png'})
            #self.addDir({'category': 'host2', 'title': 'Cimaclub'  , 'mode': '30', 'url': '/category/مسلسلات-رمضان-2022', 'import': 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_cimaclub import ', 'icon': 'https://i.pinimg.com/originals/f2/67/05/f267052cb0ba96d70dd21e41a20a522e.jpg', 'type': 'category', 'desc': ''})
            #self.addDir({'category': 'host2', 'title': 'EgyDead'   , 'mode': '20', 'url': '/tag/رمضان-2022/', 'mode': '20', 'import': 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_egydead import ', 'type': 'category', 'icon': 'https://i.ibb.co/yNNqyth/i6yz8Xs.png'})
            #self.addDir({'category': 'host2', 'title': 'Movizland' , 'mode': '30', 'url': '/category/series/arab-series/?release-year=2022', 'import': 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_movizland import ', 'icon': 'https://i.ibb.co/ZS8tq3z/movizl.png', 'type': 'category', 'desc': ''})
            #self.addDir({'category': 'host2', 'title': 'Shahid4u'  , 'mode': '20', 'url': '/category/رمضان-2022/', 'import': 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_shahid4u import ', 'icon': 'https://i.ibb.co/gtSXrs2/shahid4u.png', 'type': 'category', 'desc': ''})

        #elif sub_mode==1:
        #	self.addDir({'import':cItem['import'],'category' : 'host2','title':'By Filtre','desc':'','icon':cItem['icon'],'mode':'22','sub_mode':sub_mode})


    def start(self,cItem):
        mode=cItem.get('mode', None)
        if mode=='00':
            self.showmenu0(cItem)
        if mode=='20':
            self.showmenu1(cItem)
        return True

