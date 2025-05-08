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
    name = 'CartoonArbi'
    hst = 'https://www.arteenz.com'
    info_['old_host'] = hst
    hst_ = tshost(name)
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='1.1 24/07/2023'
    info_['dev']='MOHAMED_OS'
    info_['cat_id']='22'
    info_['desc']='افلام و مسلسلات كرتون'
    info_['icon']='https://i.ibb.co/6nsRSXN/cartoonrbi.png'
    info_['recherche_all']='0'
    return info_


class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{})
        self.MAIN_URL   =  getinfo()['host']

    def showmenu(self,cItem):
        TAB = [('أفـــلام','/films.html','20',0),('مســلســلات','/cats.html','20',0)]
        self.add_menu(cItem,'','','','','','',TAB=TAB,search=False)

    def showitms(self,cItem):
        page = cItem.get('page',1)
        URL = cItem.get('url','').replace(".html","")+'-pages-'+str(page)+".html"
        sts, data = self.getPage(URL)
        if sts:
            Liste_els = re.findall(r'cartoon_cat_pic">.+?href="([^<]+)" title="([^<]+)">.+?src="([^<]+)" alt', data, re.S)
            for (url,titre,image)in Liste_els:
                info  = self.std_title(ph.clean_html(titre))
                self.addDir({'import':cItem['import'],'category' : 'host2','title':info.get('title_display'),'icon':image,'desc':info.get('desc'),'mode':'21','url':url,'good_for_fav':True,'hst':'tshost'})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':tscolor('\c00????00')+'Next Page >>'+tscolor('\c00??????'),'icon':cItem['icon'],'desc':'','mode':'20','url':cItem['url'],'page':page+1})


    def showelms(self,cItem):
        URL = cItem.get('url')

        if "cartooncat" in URL:
            page = cItem.get('page',1)
            url_ = URL.replace("cartooncat","cartoonpagecat").replace(".html","")+'-'+str(page)+".html"
            sts, data = self.getPage(url_)
        else:
            sts, data = self.getPage(URL)

        if sts:
            if "cartooncat" in URL:
                Liste_els = re.findall(r'cartoon_eps_pic">.+?href="(.+?)".+?title="(.+?)">', data, re.S)
                for (url,titer) in Liste_els:
                    self.addVideo({'import':cItem['import'], 'hst':'tshost', 'url':url.replace("cartoon","watch-"), 'title':"الحلقة " + titer.split(" ")[-1], 'desc':'','icon':cItem['icon'],'good_for_fav':True,'EPG':True,'hst':'tshost'})
                self.addDir({'import':cItem['import'],'category' : 'host2','title':tscolor('\c00????00')+'Next Page >>'+tscolor('\c00??????'),'icon':cItem['icon'],'desc':'','mode':'21','url':cItem['url'],'page':page+1})
            else:
                self.addVideo({'import':cItem['import'], 'hst':'tshost', 'url':cItem['url'], 'title':cItem['title'], 'desc':'','icon':cItem['icon'],'good_for_fav':True,'EPG':True,'hst':'tshost'})

    def get_links(self,cItem):
        urlTab = []
        sts, data = self.getPage(cItem['url'])
        if sts:
            sData = re.findall(r"data:.+?&p=(.+?)'", data, re.S)[0]
            siteData = re.findall(r"server_ch([^<]+),'(.+?)'", data, re.S)
            for (id_,key_) in siteData:
                siteUrl = self.MAIN_URL + '/plugins/servers.php?server=' +id_.replace("(","")+'&url='+key_+'&p='+sData
                sts, data = self.getPage(siteUrl)
                if sts:
                    videoUrl = re.findall(r'<iframe.+?src="(.+?)"', data, re.S)[0]
                    sts, data = self.getPage(videoUrl)
                    if sts:
                        siteData = re.findall(r'<iframe.+?src="(.+?)"', data, re.S)[0]
                        if 'arteenz' in siteData:
                            sts, data = self.getPage(siteData)
                            if sts:
                                siteUrl = re.findall(r'file:"(.+?)"', data, re.S)[0]
                        else:
                            siteUrl = siteData.replace('preview?pli=1#t=1','').replace('https://docs.google.com','https://drive.google.com')
                        sTitel = siteUrl.split("/")[2].rsplit('.',1)[0].capitalize()

                        urlTab.append({'name':sTitel, 'url':siteUrl, 'need_resolve':1})
        return urlTab

    def getArticle(self,cItem):
        Desc = [('Time','esp_time">(.*?)</','\n',''),('Year','esp_date">.+?\|(.*?)-','\n',''),('Generes','esp_cat">.+?>(.+?)</','\n',''),('Story','class="ico_story">.+?;">(.+?)</','\n','')]
        desc = self.add_menu(cItem,'','class="game_name_c">(.+?)class="ico_download">','','desc',Desc=Desc)
        if desc =='': desc = cItem.get('desc','')
        return [{'title':cItem['title'], 'text': desc, 'images':[{'title':'', 'url':cItem.get('icon','')}], 'other_info':{}}]