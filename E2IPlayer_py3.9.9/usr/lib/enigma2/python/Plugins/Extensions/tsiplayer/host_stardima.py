# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tshost,T

import re
import base64

def getinfo():
    info_={}
    name = 'Stardima.Com'
    hst = 'https://www.stardima.co'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='2.0 18/07/2022'        
    info_['dev']='RGYSoft'
    info_['cat_id']='22'
    info_['desc']='افلام و مسلسلات كرتون'
    info_['icon']='https://www.stardima.co/watch/wp-content/uploads/2021/12/logo.png'
    info_['recherche_all']='0'
    return info_


class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'stardima.cookie'})
        self.MAIN_URL = getinfo()['host']
        
    def showmenu(self,cItem):
        TAB = [('افلام','/watch/movies/','20',0),('مسلسلات - مواسم','/watch/seasons/','20',1),('مسلسلات - حلقات','/watch/episodes/','20',2)]#,('قنوات بث مباشر','','10',3)]
        self.add_menu(cItem,'','','','','',TAB=TAB,search=False)
        self.addDir({'import':cItem['import'],'category' :'host2','title':T('Search')  ,'icon':'https://i.ibb.co/dQg0hSG/search.png','mode':'51'})	

    
    def showmenu1(self,cItem):
        self.add_menu(cItem,'<ul class="sub-menu">(.*?)</ul>','<li.*?href="(.*?)".*?>(.*?)<','','video',ind_0=3,ord=[0,1])	
       
    def showitms(self,cItem):
        next = ['rel="next".*?href="(.*?)"','20']
        self.add_menu(cItem,'<header class="archive_post">(.*?)"pagination"','<article.*?class="item.*?src="(.*?)".*?alt="(.*?)"(.*?)href="(.*?)"(.*?)</article>','','21',ord=[3,1,0,2,4],Next=next,u_titre=True,bypass=True)		

    def showelms(self,cItem):
        printDBG('cItem='+str(cItem))
        self.add_menu(cItem,'<ul class=\'episodios\'>(.*?)</ul>','<li.*?src=\'(.*?)\'.*?numerando\'>(.*?)<.*?href=\'(.*?)\'(.*?)</li>','','video',ord=[2,1,0,3])	


    def SearchAll(self,str_ch,page=1,extra='',type_=''): 
        return self.get_items({'page':page,'import':extra,'str_ch':str_ch})
    
    def SearchAnims(self,str_ch,page=1,extra=''):
        elms = self.SearchAll(str_ch,page,extra=extra,type_='')
        return elms

    def get_items(self,cItem={}):
        elms    = []
        extra   = cItem.get('import')
        str_ch  = cItem.get('str_ch')
        page    = cItem.get('page', 1)

        url = self.MAIN_URL+'/watch/page/'+str(page)+'/?s='+str_ch
        sts, data = self.getPage(url)
        if sts:
            count=0
            films_list = re.findall('<article.*?href="(.*?)".*?src="(.*?)".*?alt="(.*?)"(.*?)</article>', data, re.S)		
            for (url,image,titre,desc) in films_list:
                desc  = self.extract_desc(desc,[('type','class="episodes">(.*?)</span>'),('type','class="movies">(.*?)</span>'),('year','class="year">(.*?)</span>'),('plot','class="contenido">(.*?)</div>')])
                info  = self.std_title(titre,with_type=True)
                desc  = info.get('desc')                    
                titre = info.get('title_display')
                image = self.std_url(image) 
                elms.append({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'desc':desc,'icon':image,'mode':'21','good_for_fav':True,'EPG':True,'hst':'tshost','info':info})		  
            films_list = re.findall("id='nextpagination'", data, re.S)	
            if films_list:
                elms.append({'import':extra,'category' : 'host2','title':T('Next'),'url':'','desc':'Next','icon':'','hst':'tshost','mode':'51','page':page+1,'str_ch':str_ch,'type_':''})
        return elms

    def SearchResult(self,str_ch,page,extra):
        url = self.MAIN_URL+'/watch/page/'+str(page)+'/?s='+str_ch
        desc = [('Type','class="episodes">(.*?)</span>','',''),('Type','class="movies">(.*?)</span>','',''),('Year','class="year">(.*?)</span>','',''),('Story','class="contenido">(.*?)</div>','\n','')]
        self.add_menu({'import':extra,'url':url},'','<article.*?href="(.*?)".*?src="(.*?)".*?alt="(.*?)"(.*?)</article>','','21',ord=[0,2,1,3],Desc=desc,u_titre=True)
        
    def get_links(self,cItem): 		
        urlTab=[]
        URL=cItem['url']	
        sts, data = self.getPage(URL)
        if sts:
            Liste_els = re.findall('<li id=\'player.*?class=\'(.*?)\'.*?data-type=\'(.*?)\'.*?data-post=\'(.*?)\'.*?data-nume=\'(.*?)\'', data, re.S)	        
            i = 0
            for (action,type_,post_,nume) in Liste_els:
                URL = 'hst#tshost#'+action+'|||'+type_+'|||'+post_+'|||'+nume
                titre = '|Watch Server| Server '+nume
                urlTab.append({'name':titre, 'url':URL, 'need_resolve':1})
            Liste_els = re.findall('<input rel="nofollow".*?.open\(\'(.*?)\'.*?value=\'(.*?)\'', data, re.S)	
            for (url,titre) in 	Liste_els:
                titre = titre.replace('إضغط هنا لتحميل الجودة ✔','Download Server')
                titre = titre.replace('إضغط هنا تحميل جودة ✔','Download Server')
                if '|' in titre:
                    titre = '|'+titre.split('|')[-1].strip()+'| '+titre.split('|')[0].strip()+'p'
                url = url.replace('https://freestore.app/?download=','https://www.stardima.net/player/download.php?slug=')
                urlTab.append({'name':titre, 'url':url, 'need_resolve':0,'type':'local'})	
        return urlTab	


    def getVideos1(self,videoUrl):
        urlTab = []
        action,type_,post_,nume = videoUrl.split('|||')
        url='https://www.stardima.co/wp-admin/admin-ajax.php'
        post_data ={'action':'doo_player_ajax','post':post_,'nume':nume,'type':type_}
        sts, data = self.getPage(url,post_data=post_data)
        if sts:
            Liste_els = re.findall('"embed_url":"(.*?)"', data, re.S|re.IGNORECASE)
            if Liste_els:
                URL_ = Liste_els[0].replace('\\','')
                urlTab.append((URL_,'1'))
        return urlTab	

    def getVideos(self,videoUrl):
        urlTab = []
        action,type_,post_,nume = videoUrl.split('|||')
        url='https://www.stardima.co/wp-json/dooplayer/v2/'+post_+'/'+type_+'/'+nume
        
        url_post = 'https://www.stardima.co/watch/wp-admin/admin-ajax.php'
        post_data = {'action':'doo_player_ajax','post':post_,'nume':nume,'type':type_}

        #sts, data = self.getPage(url)
        sts, data = self.getPage(url_post,post_data=post_data)
        if sts:
            Liste_els = re.findall('"embed_url":"(.*?)"', data, re.S|re.IGNORECASE)
            if Liste_els:
                URL_ = Liste_els[0].replace('\\','')
                if '/embed2/?id=' in URL_: URL_ = URL_.split('/embed2/?id=',1)[1]
                URL_=str(base64.b64decode(URL_))
                if '?id=' in URL_: URL_ = URL_.split('?id=',1)[1]
                print(URL_)
                urlTab.append((URL_,'1'))
        return urlTab	


    def showmenu11(self,cItem):
        abc = ['\xd8\xa3', '\xd8\xa8', '\xd8\xaa', '\xd8\xab', '\xd8\xac', '\xd8\xad', '\xd8\xae', '\xd8\xaf', '\xd8\xb0', '\xd8\xb1', '\xd8\xb2', '\xd8\xb3', '\xd8\xb4', '\xd8\xb5', '\xd8\xb6', '\xd8\xb7', '\xd8\xb8', '\xd8\xb9', '\xd8\xba', '\xd9\x81', '\xd9\x82', '\xd9\x83', '\xd9\x84', '\xd9\x85', '\xd9\x86', '\xd9\x87\xd9\x80', '\xd9\x88', '\xd9\x8a']
        i=0
        for letter in abc:
            i=i+1
            href='https://www.stardima.co/watch/browse-%s-videos-1-date.html' %str(i) 
            self.addDir({'import':cItem['import'],'category' : 'host2','title':letter,'url':href,'mode':'40'})			

    def showmenu21(self,cItem):
        sts, data = self.getPage(cItem['url'])
        if sts:
            Liste_els = re.findall('<li><a href="(.*?)">(.*?)</a></li>', data, re.S)	
            for href,title in Liste_els:
                try:href=href.split('.html')[0]+'.html'
                except:continue
                if not "videos-1-date.html" in href:
                    continue
                self.addDir({'import':cItem['import'],'category' : 'host2','title':title,'url':href,'mode':'20','good_for_fav':True})			       

        
    def showmenu31(self,cItem):
        sts, data = self.getPage('https://www.stardima.co/ads.php')
        if sts:
            Liste_els = re.findall('<li>.*?title="(.*?)".*?href="(.*?)".*?src="(.*?)"', data, re.S)	
            for (titre,url,image) in Liste_els:
                if '?cat=' in url:
                    x1,name_=url.split('?cat=')
                    url='https://www.stardima.co/watch/browse-'+name_+'-videos-1-date.html'
                if titre.strip()!='':
                    self.addDir({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'icon':image,'mode':'20','good_for_fav':True})			       

        
    def showmenu41(self,cItem):
        self.addDir({'import':cItem['import'],'category' : 'host2','icon':cItem['icon'],'title':'أ-ي',                                                                                                                         'mode':'30'})
        self.addDir({'import':cItem['import'],'category' : 'host2','icon':cItem['icon'],'title':'مسلسلات أنمي وكرتون مدبلجة','url':'https://www.stardima.co/watch/browse-cartoon_anime_dub_arabic-videos-1-date.html',         'mode':'40'})
        self.addDir({'import':cItem['import'],'category' : 'host2','icon':cItem['icon'],'title':'مسلسلات أنمي وكرتون مترجمة','url':'https://www.stardima.co/watch/browse-cartoon_anime_sub_arabic-videos-1-date.html',         'mode':'40'})
        self.addDir({'import':cItem['import'],'category' : 'host2','icon':cItem['icon'],'title':'نمي وكرتون مدبلجة عربي','url':'https://www.stardima.co/watch/browse-movie_anime_cartoon_dub_arabic-videos-1-date.html',      'mode':'20'})
        self.addDir({'import':cItem['import'],'category' : 'host2','icon':cItem['icon'],'title':'أفلام أنمي وكرتون مترجمة عربي','url':'https://www.stardima.co/watch/browse-movie_anime_cartoon_sub_arabic-videos-1-date.html','mode':'20'})
        self.addDir({'import':cItem['import'],'category' : 'host2','icon':cItem['icon'],'title':'أفلام أنمي وكرتون صامتة','url':'https://www.stardima.co/watch/browse-cartoon-anime-Silent-videos-1-date.html',                'mode':'20'})
        self.addDir({'import':cItem['import'],'category' : 'host2','icon':cItem['icon'],'title':'افلام عائلية','url':'https://www.stardima.co/watch/browse-movies-family-arabic-videos-1-date.html',                           'mode':'20'})
        self.addDir({'import':cItem['import'],'category' : 'host2','icon':cItem['icon'],'title':'Pixar Short Movies','url':'https://www.stardima.co/watch/browse-Pixar-Short-Movies-videos-1-date.html',                      'mode':'20'})
    
    def showanim1(self,cItem):
        page=cItem.get('page',1)
        url_or=cItem['url']	
        if '-1-date.html' in url_or:
            url=url_or.replace('1-date.html',str(page)+'-date.html')
        else:
            url=url_or+'?page='+str(page)
        sts, data = self.getPage(url)
        if sts:
            Liste_els = re.findall('class="thumbnail">.*?echo="(.*?)".*?<a href="(.*?)".*?title="(.*?)"', data, re.S)
            i=0	
            for (image,url,titre) in Liste_els:
                self.addVideo({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'icon':image,'hst':'tshost','good_for_fav':True})
                i=i+1
            if i>10:
                self.addDir({'import':cItem['import'],'category' : 'host2','title':'Page Suivante','url':url_or,'page':page+1,'mode':'20'})


    def SearchResult1(self,str_ch,page,extra):
        url_='https://www.stardima.co/page/'+str(page)+'/?s='+str_ch
        sts, data = self.getPage(url_)
        if sts:
            Liste_els = re.findall('class="thumbnail">.*?echo="(.*?)".*?<a href="(.*?)".*?title="(.*?)"', data, re.S)
            for (image,url,titre) in Liste_els:
                self.addVideo({'import':extra,'category' : 'host2','title':titre,'url':url,'icon':image,'hst':'tshost','good_for_fav':True})


        


    def get_links1(self,cItem): 	
        urlTab = []
        url=cItem['url']	
        sts, data = self.getPage(url)
        if sts:
            Liste_els = re.findall('contentURL" content="(.*?)"', data, re.S)
            if 	Liste_els:
                urlTab.append({'name':'|Watch Server| Main Server', 'url':Liste_els[0], 'need_resolve':0,'type':'local'})	
            
            Liste_els = re.findall('<input rel="nofollow".*?.open\(\'(.*?)\'.*?value=\'(.*?)\'', data, re.S)	
            for (url,titre) in 	Liste_els:
                titre = titre.replace('إضغط هنا لتحميل الجودة ✔','Download Server')
                titre = titre.replace('إضغط هنا تحميل جودة ✔','Download Server')
                if '|' in titre:
                    titre = '|'+titre.split('|')[-1].strip()+'| '+titre.split('|')[0].strip()+'p'
                urlTab.append({'name':titre, 'url':'hst#tshost#'+url, 'need_resolve':1,'type':'local'})	

        return urlTab	

    def getVideos1(self,videoUrl):
        urlTab = []
        videoUrl.split('|||')
        
        
        url='https://www.stardima.co/watch/'+videoUrl	
        sts, data = self.getPage(url)
        if sts:
            Liste_els = re.findall('videoUrl.*? value="(.*?)"', data, re.S)
            if 	Liste_els:
                URL_part=Liste_els[0].split('O0k0O', 1)
                new=''
                i=0
                for letter in URL_part[0]:
                    if (i % 2)==0:
                        new=new+letter
                    i=i+1	
                URL_b64=new+URL_part[1].replace('O0k0O','=')
                URL_=base64.b64decode(URL_b64)
                urlTab.append((URL_,'0'))	
        return urlTab	
            
