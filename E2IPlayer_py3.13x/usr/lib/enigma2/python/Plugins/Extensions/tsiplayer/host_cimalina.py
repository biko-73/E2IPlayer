# -*- coding: utf-8 -*-

from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost, gethostname, tshost, unifurl
import re

from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import \
    TranslateTXT as _
from Plugins.Extensions.IPTVPlayer.libs import ph



def getinfo():
    info_={}
    name = 'CimaLina'
    hst = 'https://cimalina.live'
    info_['old_host'] = hst
    hst_ = tshost(name)
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='1.0 29/07/2023'
    info_['dev']='MOHAMED_OS'
    info_['cat_id']='21'
    info_['desc']='أفلام, مسلسلات اجنبية'
    info_['icon']='https://i.ibb.co/T8dKp38/cimalina.png'
    info_['recherche_all']='1'
    return info_


class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'cimalina.cookie'})
        self.MAIN_URL       =  getinfo()['host']
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        self.HEADER = {'User-Agent': self.USER_AGENT, 'Connection': 'keep-alive', 'Accept-Encoding':'gzip', 'Content-Type':'application/x-www-form-urlencoded','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
        self.defaultParams = {'header':self.HEADER, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        self.cacheLinks = {}

    def showmenu(self,cItem):
        TAB = [('أفـــــلام','','10','film'),('مــسـلـسـلات','','10','serie')]
        self.add_menu(cItem,'','','','','',TAB=TAB,search=False)
        self.addDir({'import':cItem['import'],'category' : 'search','title': _('Search'), 'search_item':True,'page':1,'hst':'tshost','icon':cItem['icon']})

    def showmenu1(self,cItem):
        gnr = cItem['sub_mode']
        if gnr == 'film':
            self.CimaLina_TAB = [
                {'category':'host2','title': 'أفــلام أجنـبيـة','url':self.MAIN_URL+'/category/أفلام-أجنبية/', 'mode':'20'},
                {'category':'host2','title': 'أفــلام هنــديـة','url':self.MAIN_URL+'/category/أفلام-هندية/',  'mode':'20'},
                {'category':'host2','title': 'أفــلام آسـيـويـة','url':self.MAIN_URL+'/category/أفلام-اسيوية/',  'mode':'20'},
                {'category':'host2','title': 'أفــلام تـركـيـة','url':self.MAIN_URL+'/category/أفلام-تركية/',  'mode':'20'},
                {'category':'host2','title': 'أفــلام أنـمـي','url':self.MAIN_URL+'/category/أفلام-أنمي/', 'mode':'20'}]
        elif gnr == 'serie':
            self.CimaLina_TAB = [
                {'category':'host2','title': 'مسـلـسـلات أجنـبيـة','url':self.MAIN_URL+'/category/مسلسلات-أجنبية/', 'mode':'20'},
                {'category':'host2','title': 'مسـلـسـلات تـركـيـة','url':self.MAIN_URL+'/category/مسلسلات-تركية-مترجمة/',  'mode':'20'},
                {'category':'host2','title': 'مسـلـسـلات تـركـيـة مدبلجة','url':self.MAIN_URL+'/category/مسلسلات-تركية-مدبلجة/',  'mode':'20'},
                {'category':'host2','title': 'مسـلـسـلات آسـيـويـة','url':self.MAIN_URL+'/category/مسلسلات-اسيوية/',  'mode':'20'},
                {'category':'host2','title': 'مسـلـسـلات كــوريـــة','url':self.MAIN_URL+'/category/مسلسلات-كورية/',  'mode':'20'},
                {'category':'host2','title': 'مسـلـسـلات أنـمـي','url':self.MAIN_URL+'/category/مسلسلات-أنمي/', 'mode':'20'}]

        self.listsTab(self.CimaLina_TAB, {'import':cItem.get('import',''),'icon':cItem.get('icon','')})

    def showitms(self,cItem):
        page = cItem.get('page',1)
        URL = cItem.get('url','')+'page/'+str(page)+'/'
        sts, data = self.getPage(URL)
        if sts:
            Liste_els = re.findall(r'class="movie">.+?href="([^"]+)".+?src="([^"]+).+?class="dicr">(.+?)</', data, re.S)
            for (url,image,titre) in Liste_els:
                info  = self.std_title(ph.clean_html(titre),with_ep=True)
                self.addDir({'import':cItem['import'],'category' : 'host2','title':info.get('title_display'),'icon':self.std_url(image),'desc':info.get('desc'),'mode':'21','url':url,'good_for_fav':True,'EPG':True,'hst':'tshost','saison':info.get('saison'),'part':info.get('part')})
            self.addDir({'import':cItem['import'],'category' : 'host2','title':tscolor('\c00????00')+'Next Page >>'+tscolor('\c00??????'),'icon':cItem['icon'],'desc':'','mode':'20','url':cItem['url'],'page':page+1})


    def showelms(self,cItem):
        sNextPage = self.NextPage(cItem.get('url'))
        if sNextPage:
            page = cItem.get('page',1)
            URL = cItem.get('url','')+'page/'+str(page)+'/'
        else:
            URL = cItem.get('url')
        sts, data = self.getPage(URL)
        if sts:
            if 'selary' in URL:
                Liste_els = re.findall('class="movie">.+?href="([^"]+)".+?class="dicr">(.+?)</', data, re.S)
                if Liste_els:
                    for (url,titre) in Liste_els:
                        self.addVideo({'import':cItem['import'], 'hst':'tshost', 'url':url, 'title':self.std_extract(titre), 'desc':'','icon':cItem['icon'],'good_for_fav':True,'EPG':True,'hst':'tshost'})
                    if sNextPage:
                        self.addMore({'import':cItem['import'],'category' : 'host2','title':tscolor('\c00????00')+'Add More'+tscolor('\c00??????'),'icon':cItem['icon'],'desc':'','mode':'21','url':cItem['url'],'page':page+1})
            else:
                self.addVideo({'import':cItem['import'], 'hst':'tshost', 'url':cItem['url'], 'title':cItem['title'], 'desc':'','icon':cItem['icon'],'good_for_fav':True,'hst':'tshost'})

    def get_links(self,cItem):
        urlTab = []
        sts, data = self.getPage(cItem.get('url'))
        if sts:
            UrlData = re.findall(r'class="formWatch".+?action="([^"]+)".+?name="servers".+?value="([^"]+)">.+?name="downloads".+?value="([^"]+)">', data, re.S)
            for (Url,ServersID,DownloadsID) in UrlData:
                data = {'servers':ServersID,'downloads':DownloadsID,'submit':''}
                sts, data_ = self.getPage(Url,self.defaultParams,data)
                if sts:
                    url_dat = re.findall(r"data-server=.+?src='([^']+)'", data_, re.S)
                    for Url_ in url_dat:
                        urlTab.append({'name':'|Watch Server| '+ gethostname(unifurl(Url_)), 'url':unifurl(Url_), 'need_resolve':1,'type':'local'})

                    url_dat = re.findall(r'href="([^"]+)".+?class="fa fa-download', data_, re.S)
                    for Url_ in url_dat:
                        urlTab.append({'name':'|Downl Server| '+ gethostname(Url_), 'url':unifurl(Url_), 'need_resolve':1,'type':'local'})
            self.cacheLinks[str(cItem['url'])] = urlTab
        return urlTab


    def SearchResult(self,str_ch,page,extra):
        URL=self.MAIN_URL+'/search/'+str_ch+'/page/'+str(page)
        sts, data = self.getPage(URL)
        if sts:
            Liste_els = re.findall(r'class="movie">.+?href="([^"]+)".+?src="([^"]+).+?class="dicr">(.+?)</', data, re.S)
            for (url,image,titre) in Liste_els:
                info  = self.std_title(ph.clean_html(titre),with_ep=True)
                self.addDir({'import':extra,'category' : 'host2','title':info.get('title_display'),'icon':self.std_url(image),'desc':info.get('desc'),'mode':'21','url':url,'good_for_fav':True,'EPG':True,'hst':'tshost'})

    def getArticle(self,cItem):
        Desc = [('Year','href=".+?release-year.+?>(.+?)</','\n',''),('Generes','href=".+?genre.+?>(.+?)</','\n',''),('Story','class="StoryMovie">(.+?)</','\n','')]
        desc = self.add_menu(cItem,'','class="MovieDetails">(.+?)class="CategoriesBrowse ">','','desc',Desc=Desc)
        if desc =='': desc = cItem.get('desc','')
        return [{'title':cItem['title'], 'text': desc, 'images':[{'title':'', 'url':cItem.get('icon','')}], 'other_info':{}}]


    def NextPage(self,url):
        sts, data = self.getPage(url)
        if sts:
            matches = re.findall(r'class="navigation">', data, re.S)
            if matches:
                return True

