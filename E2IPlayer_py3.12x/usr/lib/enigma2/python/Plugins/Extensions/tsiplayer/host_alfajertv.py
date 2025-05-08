# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,gethostname,T
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta

import re

import requests
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import \
    TranslateTXT as _
from Plugins.Extensions.IPTVPlayer.libs import ph



def getinfo():
    info_={}
    name = 'FajerShow'
    hst = 'https://show.alfajertv.com'
    info_['old_host'] = hst
    hst_ = tshost(name)
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='1.0 16/07/2023'
    info_['dev']='MOHAMED_OS'
    info_['cat_id']='21'
    info_['desc']='أفلام, مسلسلات عربية و اجنبية'
    info_['icon']='https://i.ibb.co/jyTp1q8/alfajertv.png'
    info_['recherche_all']='1'
    return info_


class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{})
        self.MAIN_URL   =  getinfo()['host']

    def showmenu(self,cItem):
        TAB = [('رمـــضــان 2023','/genre/ramadan2023/','20',0),('أفــلام','','10',0),('مسـلسـلات','','11',0),('مسـرحـيـات','/genre/plays/','20',0)]
        self.add_menu(cItem,'','','','','','',TAB=TAB,search=False)
        self.addDir({'import':cItem['import'],'category' : 'search','title': _('Search'), 'search_item':True,'page':1,'hst':'tshost','icon':cItem['icon']})

    def showmenu1(self,cItem):
        self.add_menu(cItem,r'id="menu-item-12093"(.*?)id="menu-item-13336"',r'<a href="(.*?)">(.*?)</a>','','20',ord=[0,1],ind_0=cItem['sub_mode'],LINK='/movies/')

    def showmenu2(self,cItem):
        self.add_menu(cItem,r'id="menu-item-12097"(.*?)id="menu-item-12098"',r'<a href="(.*?)">(.*?)</a>','','20',ord=[0,1],ind_0=cItem['sub_mode'],LINK='/tvshows/')

    def getTag(self,url):
        if 'turkish-movies' in url or 'indian-series' in url or 'plays' in url or 'ramadan2023' in url:
            return True
        return False

    def showitms(self,cItem):
        getTag = self.getTag(cItem.get('url'))
        if getTag:
            URL = cItem.get('url')
        else:
            page = cItem.get('page',1)
            URL = cItem.get('url')+'page/'+str(page)
        sts, data = self.getPage(URL)
        if sts:
            data = re.findall(r'class="items">(.*?)"sidebar scrolling">', data, re.S)[0]
            if data:
                Liste_els = re.findall(r'src="(.*?)".*?alt="(.*?)".*?href="(.*?)"', data, re.S)
                for (image,titre,url)in Liste_els:
                    self.addDir({'import':cItem['import'],'category' : 'host2','title':ph.clean_html(titre),'icon':image,'desc':'','mode':'21','url':url,'good_for_fav':True})
        if getTag is False:
            self.addDir({'import':cItem['import'],'category' : 'host2','title':tscolor('\c00????00')+'Next Page >>'+tscolor('\c00??????'),'icon':cItem['icon'],'desc':'','mode':'20','url':cItem['url'],'page':page+1})


    def showelms(self,cItem):
        sts, data = self.getPage(cItem.get('url'))
        if sts:
            if 'tvshows' in cItem.get('url'):
                Liste_els = re.findall(r'"episodiotitle">.*?href="(.*?)">(.*?)</a>', data, re.S)
                if Liste_els:
                    for (url,titre) in Liste_els:
                        self.addVideo({'import':cItem['import'], 'hst':'tshost', 'url':url, 'title':ph.clean_html(titre), 'desc':'','icon':cItem['icon'],'good_for_fav':True})
            else:
                Liste_els = re.findall(r'"data">.*?<h1>(.*?)</h1>', data, re.S)
                if Liste_els:
                    for titre in Liste_els:
                        self.addVideo({'import':cItem['import'], 'hst':'tshost', 'url':cItem['url'], 'title':ph.clean_html(titre), 'desc':'','icon':cItem['icon'],'good_for_fav':True})

    def get_links(self,cItem):
        urlTab = []
        sts, data = self.getPage(cItem['url'])
        if sts:
            URL = self.MAIN_URL + '/wp-admin/admin-ajax.php'
            aResult = re.findall(r'data-type="(.*?)".*?data-post="(.*?)".*?data-nume="(.*?)"', data, re.S)
            if aResult:
                for (type_,post_,nume_) in aResult:
                    sHtmlContent = requests.post(URL, data={'action':'doo_player_ajax','post':post_,'nume':nume_,'type':type_}).text
                    siteUrl = re.findall(r"<iframe.*?src='(.*?)' frameborder",sHtmlContent,re.S)[0]
                    sTitel = re.findall(r"\//(.*?)\/",siteUrl,re.S)[0].replace('show.alfajertv.com','سيرفر فلسـطيـن')
                    urlTab.append({'name':sTitel, 'url':siteUrl, 'need_resolve':1})
        return urlTab

    def SearchResult(self,str_ch,page,extra):
        URL=self.MAIN_URL+'/?s='+str_ch
        sts, data = self.getPage(URL)
        if sts:
            data = re.findall(r'class="details">(.*?)"sidebar scrolling">', data, re.S)[0]
            if data:
                Liste_els = re.findall(r'src="(.*?)".*?alt="(.*?)".*?href="(.*?)"', data, re.S)
                for (image,titre,url)in Liste_els:
                    self.addDir({'import':extra,'category' : 'host2','title':ph.clean_html(titre),'icon':image,'mode':'21','url':url,'hst':'tshost'})