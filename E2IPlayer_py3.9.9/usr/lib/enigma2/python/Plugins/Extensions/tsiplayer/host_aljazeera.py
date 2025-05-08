# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass, tshost
import re

from Plugins.Extensions.IPTVPlayer.libs import ph




def getinfo():
    info_={}
    name = 'Aljazeera'
    hst = 'https://www.aljazeera.net'
    info_['old_host'] = hst
    hst_ = tshost(name)
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='1.1 24/07/2023'
    info_['dev']='MOHAMED_OS'
    info_['cat_id']='21'
    info_['desc']='افلام وثائقية'
    info_['icon']='https://i.ibb.co/4Jf9Yct/aljazeera.png'
    info_['recherche_all']='0'
    return info_


class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{})
        self.MAIN_URL   =  getinfo()['host']

    def showmenu(self,cItem):
        TAB = [('افلام وثائقية','/programs/investigative/','20',0),('مسلسلات وثائقية','/programs/documentaries/','20',0),('برامج تلفزيونية','/programs/newsmagazineshows/','20',0)]
        self.add_menu(cItem,'','','','','','',TAB=TAB,search=False)

    def showitms(self,cItem):
        sts, data = self.getPage(cItem.get('url'))
        if sts:
            Liste_els = re.findall(r'loading="lazy" src="(.+?)" srcSet.+?<h3 class="program-card__title"><a href="(.+?)"><span>(.+?)</span></a></h3><p', data, re.S)
            for (image,url,titre)in Liste_els:
                image_ = self.MAIN_URL+image.split("?")[0]
                info  = self.std_title(ph.clean_html(titre))
                self.addDir({'import':cItem['import'],'category' : 'host2','title':info.get('title_display'),'icon':self.std_url(image_),'desc':info.get('desc'),'mode':'21','url':self.MAIN_URL+url,'good_for_fav':True,'hst':'tshost'})


    def showelms(self,cItem):
        sts, data = self.getPage(cItem.get('url'))
        if sts:
            Liste_els = re.findall(r'loading="lazy" src="(.+?)" srcSet.+?u-clickable-card__link" href="(.+?)"><span>(.+?)</span>', data, re.S)
            if Liste_els:
                for (image,url,titre) in Liste_els:
                    image_ = self.MAIN_URL+image.split("?")[0]
                    sTitel = titre.replace(cItem['title'],"").replace("-","")
                    self.addVideo({'import':cItem['import'], 'hst':'tshost', 'url':self.MAIN_URL+url, 'title':sTitel, 'desc':'','icon':self.std_url(image_),'good_for_fav':True,'EPG':True,'hst':'tshost'})

    def get_links(self,cItem):
        urlTab = []
        sts, data = self.getPage(cItem['url'])
        if sts:
            siteUrl = re.findall(r'"embedUrl": "(.+?)"', data, re.S)[0]
            sTitel= re.findall(r'embedUrl.+?\.(.+?)\/', data, re.S)[0]
            urlTab.append({'name':sTitel, 'url':siteUrl, 'need_resolve':1})
        return urlTab

    def getArticle(self,cItem):
        Desc = [('Story','class="article-excerpt">(.*?)</','\n','')]
        desc = self.add_menu(cItem,'','article-header">(.*?)article-content-read-more','','desc',Desc=Desc)
        if desc =='': desc = cItem.get('desc','')
        return [{'title':cItem['title'], 'text': desc, 'images':[{'title':'', 'url':cItem.get('icon','')}], 'other_info':{}}]