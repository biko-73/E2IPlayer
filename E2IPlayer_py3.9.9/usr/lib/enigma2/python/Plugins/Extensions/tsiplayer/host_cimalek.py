# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,gethostname,T
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Components.config import config
import re
import base64

from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import \
    TranslateTXT as _
from Plugins.Extensions.IPTVPlayer.libs import ph




def getinfo():
    info_={}
    name = 'Cimalek'
    hst = 'https://cimalek.art'
    info_['old_host'] = hst
    hst_ = tshost(name)
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='1.0 15/07/2023'
    info_['dev']='MOHAMED_OS'
    info_['cat_id']='21'
    info_['desc']='أفلام, مسلسلات عربية و اجنبية'
    info_['icon']='https://i.ibb.co/rdBFg9h/cimalek.png'
    info_['recherche_all']='1'
    return info_


class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'cimalek.cookie'})
        self.MAIN_URL       =  getinfo()['host']
        self.USER_AGENT     = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0'
        self.HEADER         = {'User-Agent': self.USER_AGENT, 'Connection': 'keep-alive', 'Accept-Encoding':'gzip', 'Content-Type':'application/json; charset=UTF-8','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
        self.defaultParams  = {'header':self.HEADER, 'with_metadata':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}

    def showmenu(self,cItem):
        TAB = [('أفــلام','','10',0),('مسـلسـلات','','11',0),('الـمـواسـم','/seasons/','20',0),('الحــلـقــات','/episodes/','20',0),('المـضـاف حـديـثا','','13',0),('الاكـثـر مـشـاهـدة','/trending/','20',0)]
        self.add_menu(cItem,'','','','','',TAB=TAB,search=False)
        self.addDir({'import':cItem['import'],'category' : 'search','title': _('Search'), 'search_item':True,'page':1,'hst':'tshost','icon':cItem['icon']})

    def showmenu1(self,cItem):
        self.add_menu(cItem,'<i class="fa fa-film(.*?)class="fa fa-desktop">','<li.*?href="(.*?)".*?>(.*?)</li>','','20',ord=[0,1],ind_0=cItem['sub_mode'],LINK='/movies/')

    def showmenu2(self,cItem):
        self.add_menu(cItem,'class="fa fa-desktop(.*?)200163','<li.*?href="(.*?)".*?>(.*?)</li>','','20',ord=[0,1],ind_0=cItem['sub_mode'],LINK='/series/')

    def showmenu3(self,cItem):
        self.add_menu(cItem,'class="cat-trending">(.*?)</div>','<a href="(.*?)".*?<span>(.*?)</span>','','20',ord=[0,1],ind_0=cItem['sub_mode'],LINK='/recent/')

    def showitms(self,cItem):
        page = cItem.get('page',1)
        URL = cItem.get('url','')+'page/'+str(page)
        sts, data = self.getPage(URL)
        if sts:
            data = re.findall('"film_list-wrap">(.*?)class="fcmpbox">|class="pagination">', data, re.S)
            if data:
                Liste_els = re.findall('<a href="(.*?)">.*?data-src="(.*?)".*?alt="(.*?)">', data[0], re.S)
                for (url,image,titre) in Liste_els:
                    titre = ph.clean_html(titre).replace("مسلسل","").replace("انمي","").replace("الموسم",tscolor('\c00????00')+"Season"+tscolor('\c00??????')).replace("الحلقة",tscolor('\c0000????')+"EP"+tscolor('\c00??????')).replace("مشاهدة","").replace("فيلم","")
                    self.addDir({'import':cItem['import'],'category' : 'host2','title':titre,'icon':image,'mode':'21','url':url,'good_for_fav':True})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':tscolor('\c00????00')+'Next Page >>'+tscolor('\c00??????'),'icon':cItem['icon'],'desc':'','mode':'20','url':cItem['url'],'page':page+1})


    def showelms(self,cItem):
        sts, data = self.getPage(cItem.get('url'))
        if sts:
            if 'series' in cItem.get('url') or 'seasons' in cItem.get('url') or 'episodes' in cItem.get('url'):
                info_data=re.findall('class="film-poster">.*?rating">(.*?)</span>.*?item quality">(.*?)<a.*?type=(.*?)".*?tick-item">(.*?)</a></span>', data, re.S)
            else:
                info_data=re.findall('class="film-poster">.*?rating">(.*?)</span>.*?tick-quality">(.*?)</a>.*?"item year">.*?type=(.*?)".*?quality">(.*?)</a>', data, re.S)
            if info_data:
                for (rating,quality,type_,year) in info_data:
                    type1 = type_.replace("movies","فــيــلـم").replace("series","مـسـلــســل")
                    desc = tscolor('\c00????00')+'Rating: '+tscolor('\c00??????')+ph.clean_html(rating)+'\n'+tscolor('\c00????00')+'Quality: '+tscolor('\c00??????')+ph.clean_html(quality)+'\n'\
                        + tscolor('\c00????00')+'Type: '+tscolor('\c00??????')+ph.clean_html(type1)+'\n'+tscolor('\c00????00')+'Year: '+tscolor('\c00??????')+ph.clean_html(year)+'\n'
            info_desc=re.findall('film-description.*?text">(.*?)</div>', data, re.S)
            if info_desc:
                desc =  desc +tscolor('\c00????00')+'Desc: '+tscolor('\c00??????')+ph.clean_html(info_desc[0])+'\n'
            if 'series' in cItem.get('url') or 'seasons' in cItem.get('url'):
                Liste_els = re.findall("class='episodesList.*?href='(.*?)'.*?class='serie'>(.*?)</", data, re.S)
                if Liste_els:
                    for (url,titre) in Liste_els:
                        Stitel = ph.clean_html(titre).replace("(","").replace(")","")
                        self.addVideo({'import':cItem['import'], 'hst':'tshost', 'url':url+'watch/', 'title':Stitel, 'desc':desc,'icon':cItem['icon'],'good_for_fav':True})
            else:
                Liste_els = re.findall(r'dynamic-name">(.*?)</h2>.*?WatchButtons">.*?<a href="(.+?)"', data, re.S)
                if Liste_els:
                    for (titre,url) in Liste_els:
                        self.addVideo({'import':cItem['import'], 'hst':'tshost', 'url':url, 'title':ph.clean_html(titre), 'desc':desc,'icon':cItem['icon'],'good_for_fav':True})

    def get_links(self,cItem):
        urlTab = []
        URL = self.MAIN_URL+'/wp-json/lalaplayer/v2/'
        sts, data = self.getPage(cItem.get('url'))
        if sts:
            sitData = re.findall(r'class="player-servers">(.*?)class="module_single_sda">', data, re.S)
            if sitData:
                url_ = re.findall(r"data-type='([^']+)'\sdata-post='([^']+)'\sdata-nume='([^']+)'.*?<li>(.+?)</li>", data, re.S)
                if url_:
                    for Sdata in url_:
                        sts,GetUrl = self.getPage(URL+'?p='+Sdata[1]+'&t='+Sdata[0]+'&n='+Sdata[2],addParams =self.defaultParams)
                        if sts:
                            sitLink = re.findall(r'embed_url":"([^"]+)"', GetUrl.replace("\\",""), re.S)
                            sts,url_data = self.getPage(sitLink[0],addParams =self.defaultParams)
                            if sts:
                                find_url = re.findall(r'"file":"(.+?)","label":', url_data, re.S)
                                if find_url and find_url[0].startswith(('https',"http")):
                                    urlTab.append({'name':Sdata[-1].replace("_"," "), 'url':find_url[0].replace("\\",""), 'need_resolve':0})
        return urlTab

    def SearchResult(self,str_ch,page,extra):
        URL=self.MAIN_URL+'/search/'+str_ch+'/page/'+str(page)
        sts, data = self.getPage(URL)
        if sts:
            data = re.findall(r'"film_list-wrap">(.*?)class="fcmpbox">', data, re.S)
            if data:
                Liste_els = re.findall(r'<a href="(.*?)">.*?data-src="(.*?)".*?alt="(.*?)">', data[0], re.S)
                for (url,image,titre) in Liste_els:
                    titre = ph.clean_html(titre).replace("مسلسل","").replace("انمي","").replace("الموسم",tscolor('\c00????00')+"Season"+tscolor('\c00??????')).replace("الحلقة",tscolor('\c0000????')+"EP"+tscolor('\c00??????')).replace("مشاهدة","").replace("فيلم","")
                    self.addDir({'import':extra,'category' : 'host2','title':titre,'icon':image,'mode':'21','url':url,'hst':'tshost'})