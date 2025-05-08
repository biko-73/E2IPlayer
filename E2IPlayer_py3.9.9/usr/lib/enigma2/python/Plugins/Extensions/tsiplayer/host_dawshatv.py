# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,T
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Components.config import config
import re
import base64,urllib

def getinfo():
    info_={}
    name = 'Dawsha-TV'
    hst = 'https://w.dawsha-tv.com'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='2.0 18/07/2022'        
    info_['dev']='RGYSoft'
    info_['cat_id']='21'
    info_['desc']='افلام و مسلسلات'
    info_['icon']='https://i.ibb.co/Fm4LNfj/logo.png'
    info_['recherche_all']='1'
    return info_


class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':''})
        self.MAIN_URL = getinfo()['host']			
    
    def showmenu(self,cItem):
        TAB = [('مسلسلات رمضان 2021','/category/مسلسلات-رمضان-2021','20',''),('المسلسلات','','10',0),
               ('مسلسلات نتفلكس','/category/مسلسلات-نتفلكس','20',''),('مسلسلات كرتون انمي','/category/مسلسلات-كرتون-انمي','20',''),
               ('الافلام','','10',1),]
        self.add_menu(cItem,'','','','','',TAB=TAB,search=False)
        self.addDir({'import':cItem['import'],'category' :'host2','title':T('Search'),'icon':'https://i.ibb.co/dQg0hSG/search.png','mode':'51'})
  
    def showmenu1(self,cItem):
        self.add_menu(cItem,'<ul class="dropdown-menu(.*?)</ul','<li.*?href="(.*?)".*?>(.*?)</li>','','20',ind_0=cItem.get('sub_mode',0))		
  
    def showitms(self,cItem):
        page = cItem.get('page',1)
        if (page > 1):
            LINK = cItem['url']+'.html/page'+str(page)
        else:
            LINK = cItem['url']
        desc = [('Quality','quality">(.*?)</span>','',''),('Views','postViews">(.*?)</span>','',''),('Rate','postRate">(.*?)</span>','','')]
        next = [2,'20']
        self.add_menu(cItem,'','class="postBlock">.*?href="(.*?)".*?title="(.*?)"(.*?)url\(\'(.*?)\'','','21',ord=[0,1,3,2],Desc=desc,Next=next,u_titre=True,EPG=True,LINK=LINK)		

    def showelms(self,cItem):						
        if (cItem['url'].startswith('http')):
            self.add_menu(cItem,'','data-season="(.*?)".*?>(.*?)<','','21',ord=[0,1],EPG=True,add_vid=True,corr_=False)
            self.add_menu(cItem,'class="eplist(.*?)</ul>','title=.*?"(.*?)".*?epNum.*?href=.*?"(.*?)"','','video',ord=[1,0],EPG=True,add_vid=True)   
        else:
            addParams = dict(self.defaultParams)
            addParams['header']['X-Requested-With']='XMLHttpRequest'
            self.add_menu(cItem,'','epNum.*?href=.*?"(.*?)".*?title=.*?"(.*?)[\\"]','','video',post_data = {'Ajax':1,'seriesID':cItem['url']},ord=[0,1],corr_=False,add_vid=False,LINK=self.MAIN_URL+'/myajax/getEpisodesBySeries',addParams=addParams)	

    def get_links(self,cItem): 	
        urlTab = []
        url = cItem['url'].replace('episodes','watch_episodes').replace('/movies/','/watch_movies/')
        sts, data = self.getPage(url)
        if sts:        
            post_els = re.findall('postID.*?"(.*?)"', data, re.S)
            if post_els:
                postID = post_els[0]
                Liste_els = re.findall('"servList">(.*?)</ul', data, re.S)
                if Liste_els:
                    Liste_els = re.findall('<li.*?onclick=\'(.*?)\("(.*?)".{1,5}"(.*?)".*?server">(.*?)<', Liste_els[0], re.S)
                    for (fnc,id1,id2,titre) in Liste_els:
                        titre = self.cleanHtmlStr(titre).strip()
                        urlTab.append({'name':'|Watch Server| '+titre, 'url':'hst#tshost#'+url+'|'+fnc+'|'+id1+'|'+postID, 'need_resolve':1,'type':''})  
        return urlTab	


    def getVideos(self,videoUrl):
        urlTab = []	
        referer,fnc,id1,postID = videoUrl.split('|')
        url = self.MAIN_URL+'/myajax/'+fnc
        post_data = {'server':id1, 'postID':postID,'Ajax':1}
        addParams = dict(self.defaultParams)
        addParams['header']['Referer'] = self.MAIN_URL#referer
        addParams['header']['X-Requested-With'] = 'XMLHttpRequest'        
        sts, data = self.getPage(url,addParams,post_data=post_data)
        if sts:
            data = data.replace('\\','')
            printDBG('data===='+data)
            Liste_els_3 = re.findall('src="(.+?)"', data, re.S|re.IGNORECASE)	
            if Liste_els_3:
                URL = Liste_els_3[0]
                if URL.startswith('//'): URL='http:'+URL
                urlTab.append((URL,'1'))
        return urlTab	

    def SearchResult(self,str_ch,page,extra):
        desc = [('Quality','quality">(.*?)</span>','',''),('Views','postViews">(.*?)</span>','',''),('Rate','postRate">(.*?)</span>','','')]
        url = self.MAIN_URL+'/search/'+str_ch+'.html/page'+str(page)
        self.add_menu({'import':extra,'url':url},'','class="postBlock">.*?href="(.*?)".*?title="(.*?)"(.*?)url\(\'(.*?)\'','','21',ord=[0,1,3,2],Desc=desc,u_titre=True)		

    def SearchAll(self,str_ch,page=1,extra='',type_=''):
        elms = []
        url = self.MAIN_URL+'/search/'+str_ch+'.html/page'+str(page)
        sts, data = self.getPage(url)
        if sts:
            data_list0 = re.findall('class="postBlock">.*?href="(.*?)".*?title="(.*?)"(.*?)url\(\'(.*?)\'', data, re.S)
            if data_list0:
                for (url,titre,desc,image) in data_list0:
                    info   = self.std_title(titre,with_type=True)
                    elms.append({'import':extra,'category' : 'host2','url': url,'title':info.get('title_display'),'sTitle':info.get('title'),'desc':'','icon':image,'mode':'21','good_for_fav':True,'info':info}) 
                if 'rel="next">' in data:
                    elm = {'import':extra,'category' : 'host2','title':T('Next'),'url':'','desc':'next','icon':'','mode':'51','good_for_fav':True,'EPG':True,'hst':'tshost','page':page+1,'section':type_,'str_ch':str_ch}
                    elms.append(elm)    
        return elms


    def getArticle(self,cItem):
        Desc = [('Story','class="story">(.*?)</h3>','','')]
        desc = self.add_menu(cItem,'','postInfo">(.*?)</section>','','desc',Desc=Desc)	
        if desc =='': desc = cItem.get('desc','')
        return [{'title':cItem['title'], 'text': desc, 'images':[{'title':'', 'url':cItem.get('icon','')}], 'other_info':{}}]
