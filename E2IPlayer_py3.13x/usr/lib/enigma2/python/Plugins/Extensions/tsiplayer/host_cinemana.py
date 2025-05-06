# -*- coding: utf-8 -*-


from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import \
    TranslateTXT as _
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost, gethostname, tshost, unifurl
import re


def getinfo():
    info_={}
    name = 'Cinemana'
    hst = 'https://cinemana.vip/main'
    info_['old_host'] = hst
    hst_ = tshost(name)
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='1.1 01/08/2023'
    info_['dev']='MOHAMED_OS'
    info_['cat_id']='21'
    info_['desc']='أفلام, مسلسلات عربية و اجنبية'
    info_['icon']='https://i.ibb.co/fH4LnHX/cinemana.png'
    info_['recherche_all']='1'
    return info_


class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{})
        self.MAIN_URL   =  getinfo()['host']
        self.HTTP_HEADER = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0','referer' : self.MAIN_URL}

    def showmenu(self,cItem):
        TAB = [('أفــلام','/movies/','20','film'),('مسـلسـلات','/search/?search=مسلسل','20','serie')]
        self.add_menu(cItem,'','','','','',TAB=TAB,search=False)
        self.addDir({'import':cItem['import'],'category' : 'search','title': _('Search'), 'search_item':True,'page':1,'hst':'tshost','icon':cItem['icon']})

    def showitms(self,cItem):
        gnr = cItem['sub_mode']
        if gnr == 'serie':
            URL = cItem.get("url")
        else:
            page = cItem.get('page',1)
            URL = cItem.get('url','')+'page/'+str(page)

        sts, data = self.getPage(URL)
        if sts:
            data = re.findall(r'<div class="ArcPage">(.*?)<center>', data, re.S)
            if data:
                Liste_els = re.findall(r'ItemBlock">.+?<a href="(.+?)".+?url\((.+?)\).+?<h3>(.+?)</h3>', data[0], re.S)
                for (url,image,titre) in Liste_els:
                    info  = self.std_title(ph.clean_html(titre),with_ep=True)
                    self.addDir({'import':cItem['import'],'category' : 'host2','title':info.get('title_display'),'desc':info.get('desc'),'icon':self.std_url(image),'mode':'21','url':url,'good_for_fav':True,'EPG':True,'hst':'tshost'})
        if 'page' in URL:
            self.addDir({'import':cItem['import'],'category' : 'host2','title':tscolor('\c00????00')+'Next Page >>'+tscolor('\c00??????'),'icon':cItem['icon'],'desc':'','mode':'20','url':cItem['url'],'page':page+1})

    def showelms(self,cItem):
            self.addVideo({'import':cItem['import'],'category' : 'host2','title':cItem['title'],'url':cItem['url'] ,'desc':'','icon':cItem['icon'],'good_for_fav':True,'EPG':True,'hst':'tshost'})


    def get_links(self,cItem):
        urlTab = []
        sts, data = self.getPage(cItem['url'])
        if sts:
            SiteUrl_ = self.MAIN_URL + '/wp-content/themes/EEE/Inc/Ajax/Single/Server.php'
            Sid = re.findall(r'<a data-like="likeCount" data-id="([^"]+)', data, re.S)
            server_tab = re.findall(r'data-server="(.+?)"', data, re.S)
            for server in server_tab:
                sts, data = self.getPage(SiteUrl_,self.HTTP_HEADER,{'post_id':Sid[0],'server':server})
                if sts:
                    siteUrl = re.findall(r'<iframe.+?src="([^"]+)"', data, re.S)
                    url = siteUrl[0].replace("\n","")
                    urlTab.append({'name':gethostname(url), 'url':url, 'need_resolve':1})
        return urlTab

    def SearchResult(self,str_ch,page,extra):
        URL=self.MAIN_URL+'?s='+str_ch+'&type=all&paged='+str(page)
        sts, data = self.getPage(URL)
        if sts:
            data = re.findall(r'<div class="ArcPage">(.*?)<center>', data, re.S)
            if data:
                Liste_els = re.findall(r'ItemBlock">.+?<a href="(.+?)".+?url\((.+?)\).+?<h3>(.+?)</h3>', data[0], re.S)
                for (url,image,titre) in Liste_els:
                    info  = self.std_title(ph.clean_html(titre),with_ep=True)
                    self.addDir({'import':extra,'category' : 'host2','title':info.get('title_display'),'desc':info.get('desc'),'icon':self.std_url(image),'mode':'21','url':url,'good_for_fav':True,'EPG':True,'hst':'tshost'})

    def getArticle(self,cItem):
        Desc = [('Rate','class="Rate">.*?<span> \/([^/]+)</','\n',''),('Generes','watch=genre.*?>(.*?)</a>','\n',''),('Year','watch=release-year.*?>(.*?)</a>','\n',''),
                    ('Quality','watch=quality.*?>(.*?)</a>','\n',''),('Story','class="Story">(.*?)</','\n','')]
        desc = self.add_menu(cItem,'','class="SingleAside">(.*?)</aside>','','desc',Desc=Desc)
        if desc =='': desc = cItem.get('desc','')
        return [{'title':cItem['title'], 'text': desc, 'images':[{'title':'', 'url':cItem.get('icon','')}], 'other_info':{}}]
