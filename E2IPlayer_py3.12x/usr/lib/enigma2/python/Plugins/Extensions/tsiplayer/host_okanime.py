# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,T
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads
import re
import urllib
def getinfo():
    info_={}
    info_['name']='Okanime.Com'
    info_['version']='1.2.1 16/09/2019'
    info_['dev']='RGYSoft'
    info_['cat_id']='22'
    info_['desc']='انمي مترجم'
    info_['icon']='https://i.ibb.co/88XFP0D/okanim.jpg'
    info_['recherche_all']='0'
    info_['update']='Add newest_animes'
    return info_
    
    
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'okanime.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        self.MAIN_URL = 'https://okanime.tv'
        self.HEADER = {'User-Agent': self.USER_AGENT}
        self.defaultParams = {'header':self.HEADER, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        #self.getPage = self.cm.getPage


    def getPage(self,baseUrl, addParams = {}, post_data = None):
        i=0
        while True:
            baseUrl=self.std_url(baseUrl)
            #printDBG('counttttt'+str(i))
            if addParams == {}: addParams = dict(self.defaultParams)
            sts, data = self.cm.getPage(baseUrl, addParams, post_data)
            #printDBG(str(sts))
            if sts:
                #printDBG(data)
                break
            else:
                i=i+1
                if i>2: break
        return sts, data

        
    def showmenu0(self,cItem):
        hst='host2'
        img_=cItem['icon']
        self.addMarker({'title':'أفلام','category' : 'host2','icon':img_} )									

        Cat_TAB = [
                    {'category':hst,'title': 'الترتيب حسب أحدث الافلام', 'mode':'30','url':self.MAIN_URL+'/partials/filter_movies?sort=movies.aired_year&direction=desc'},	
                    {'category':hst,'title': 'الترتيب حسب أحدث الاضافات', 'mode':'30','url':self.MAIN_URL+'/partials/filter_movies?sort=movies.published_at&direction=desc'},						
                    {'category':hst,'title': 'الترتيب حسب الأبجدية', 'mode':'30','url':self.MAIN_URL+'/partials/filter_movies?sort=title&direction=asc'},
                    {'category':hst,'title': 'الترتيب حسب تقييم الأعضاء', 'mode':'30','url':self.MAIN_URL+'/partials/filter_movies?sort=rating_caches.avg&direction=desc'},
                    ]
        self.listsTab(Cat_TAB, {'import':cItem['import'],'icon':img_})	
        self.addMarker({'title':'قائمة الانميات','category' : 'host2','icon':img_} )	
        Cat_TAB = [
                    {'category':hst,'title':'آخر الحلقات المضافة', 'mode':'30','url':self.MAIN_URL+'/dashboard/newest_animes?direction=asc','sub_mode':1},
                    {'category':hst,'title': 'الترتيب حسب أحدث الانميات', 'mode':'30','url':self.MAIN_URL+'/partials/filter_animes?sort=animes.aired_year&direction=desc'},
                    {'category':hst,'title': 'الترتيب حسب أحدث الاضافات', 'mode':'30','url':self.MAIN_URL+'/partials/filter_animes?sort=animes.published_at&direction=desc'},
                    {'category':hst,'title': 'الترتيب حسب الأبجدية', 'mode':'30','url':self.MAIN_URL+'/partials/filter_animes?sort=title&direction=asc'},
                    {'category':hst,'title': 'الترتيب حسب تقييم الأعضاء', 'mode':'30','url':self.MAIN_URL+'/partials/filter_animes?sort=rating_caches.avg&direction=desc'},
                    #{'category':'search','title': _('Search'), 'search_item':True,'page':1,'hst':'tshost'},
                    ]
        self.listsTab(Cat_TAB, {'import':cItem['import'],'icon':img_})		
        self.addDir({'import':cItem['import'],'category' :'host2','title':T('Search')  ,'icon':'https://i.ibb.co/dQg0hSG/search.png','mode':'51'})	
        
        
    def showitms(self,cItem):
        url1=cItem['url']
        gnr=cItem.get('sub_mode',0)
        page=cItem.get('page',1)
        url_=url1+'&page='+str(page)
        sts, data = self.getPage(url_)
        if sts:
            if gnr==0:
                pat = 'video-item">.*?data-src="(.*?)".*?href="(.*?)".*?<h6>(.*?)<'
            else:	
                pat = 'video-item">.*?data-src="(.*?)".*?href="(.*?)".*?video-title">(.*?)<'	
            films_list = re.findall(pat, data, re.S)		
            for (image,url,titre) in films_list:
                image = image.replace('.jpg.webp','.jpg')
                if not image.startswith('http'): image = self.MAIN_URL + image
                url=self.MAIN_URL+url
                titre=ph.clean_html(titre)
                if ('/movies/' in url) and ('/watch' not in url) :
                    url = url +'/watch'
                if ('/animes/' in url) and ('/episodes/' not in url):				
                    self.addDir({'import':cItem['import'],'good_for_fav':True,'EPG':True,'category' : 'host2','url': url,'title':titre,'desc':'','icon':image,'hst':'tshost','mode':'31'})		
                else:
                    self.addVideo({'import':cItem['import'],'good_for_fav':True,'EPG':True,'category' : 'host2','url': url,'title':titre,'desc':'','icon':image,'hst':'tshost'})		

            self.addDir({'import':cItem['import'],'title':'Page '+str(page+1),'page':page+1,'category' : 'host2','url':url1,'icon':cItem['icon'],'mode':'30','sub_mode':gnr} )									
            
    def showelms(self,cItem):
        urlo=cItem['url']
        url1=urlo
        sts, data = self.getPage(urlo)
        if sts:
            Liste_els = re.findall('ajax\({.*?url:.*?\'(.*?)\'', data, re.S)
            if Liste_els:
                url1=Liste_els[0]
                if not url1.startswith('http'): url1=self.MAIN_URL+url1
                sts, data = self.getPage(url1)
                if sts:
                    films_list1 = re.findall('class="item".*?href="(.*?)".*?src="(.*?)".*?subtitle">(.*?)<', data, re.S)				
                    for (url,image,titre) in films_list1:
                        if not url.startswith('http'): url=self.MAIN_URL+url
                        image = image.replace('.jpg.webp','.jpg')
                        if not image.startswith('http'): image = self.MAIN_URL + image
                        self.addVideo({'import':cItem['import'],'good_for_fav':True,'category' : 'host2','url': url,'title':ph.clean_html(titre),'desc':cItem['desc'],'icon':image,'hst':'tshost'} )		

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

        url_=self.MAIN_URL+'/partials/filter_animes?sort=animes.published_at&direction=desc&search='+str_ch+'&page='+str(page)
        sts, data = self.getPage(url_)
        if sts:
            count=0
            films_list = re.findall('video-item">.*?data-src="(.*?)".*?href="(.*?)".*?<h6>(.*?)<', data, re.S)		
            for (image,url,titre) in films_list:
                count = count + 1
                image = image.replace('.jpg.webp','.jpg')
                if not image.startswith('http'): image = self.MAIN_URL + image
                url=self.MAIN_URL+url
                titre=ph.clean_html(titre)
                if ('/movies/' in url) and ('/watch' not in url) :
                    url = url +'/watch'
                if ('/animes/' in url) and ('/episodes/' not in url):				
                    elms.append({'import':extra,'good_for_fav':True,'EPG':True,'category' : 'host2','url': url,'title':titre,'desc':'','icon':image,'hst':'tshost','mode':'31'})		
                else:
                    elms.append({'import':extra,'good_for_fav':True,'EPG':True,'category' : 'host2','url': url,'title':titre,'desc':'','icon':image,'hst':'tshost','type':'video'})		
            print(count)
            if count>14:
                elms.append({'import':extra,'category' : 'host2','title':T('Next'),'url':'','desc':'Next','icon':'','hst':'tshost','mode':'51','page':page+1,'str_ch':str_ch,'type_':''})
        return elms



    def SearchResult(self,str_ch,page,extra):
        url_=self.MAIN_URL+'/partials/filter_animes?sort=animes.published_at&direction=desc&search='+str_ch+'&page='+str(page)
        sts, data = self.getPage(url_)
        if sts:
            films_list = re.findall('video-item">.*?data-src="(.*?)".*?href="(.*?)".*?<h6>(.*?)<', data, re.S)		
            for (image,url,titre) in films_list:
                image = image.replace('.jpg.webp','.jpg')
                if not image.startswith('http'): image = self.MAIN_URL + image
                url=self.MAIN_URL+url
                titre=ph.clean_html(titre)
                if ('/movies/' in url) and ('/watch' not in url) :
                    url = url +'/watch'
                if ('/animes/' in url) and ('/episodes/' not in url):				
                    self.addDir({'import':extra,'good_for_fav':True,'EPG':True,'category' : 'host2','url': url,'title':titre,'desc':'','icon':image,'hst':'tshost','mode':'31'})		
                else:
                    self.addVideo({'import':extra,'good_for_fav':True,'EPG':True,'category' : 'host2','url': url,'title':titre,'desc':'','icon':image,'hst':'tshost'})		


    def get_links(self,cItem):
        urlTab = []	
        URL=cItem['url']
        sts, data = self.getPage(URL)
        if sts:
            Liste_els = re.findall('class="servers-list.*?data-provider_name="(.*?)".*?data-category="(.*?)".*?href="(.*?)"', data, re.S)
            for (host_,cat,url) in Liste_els:
                local=''
                if 'one plus' in host_.lower(): local='local'
                if 'server 7' in host_.lower():
                    host_ = '|'+cat.upper()+ ' S7'+'| Mp4upload'
                    local='local'
                elif 'server 2' in host_.lower():
                    host_ = '|'+cat.upper()+ ' S2'+'| OK.ru'
                    local='local'						
                else:
                    host_ = '|'+cat.upper()+'| '+host_	
                urlTab.append({'name':host_, 'url':'hst#tshost#'+url, 'need_resolve':1,'type':local})						
        return urlTab
        
        
    def getVideos(self,videoUrl):
        urlTab = []	
        sUrl = self.MAIN_URL+videoUrl
        sts, data = self.getPage(sUrl)
        if sts:
            srv = json_loads(data)
            URL = srv.get('data',{}).get('attributes',{}).get('url','')
            if URL.startswith('//'): URL = 'https:'+URL
            if '/cdn/' in URL:
                urlParams = dict(self.defaultParams)
                urlParams['header']['Referer']=self.MAIN_URL
                sts, data = self.getPage(URL,urlParams)
                if sts:
                    printDBG('data='+data)
                    srv_ = re.findall("'frame'..src.*?=.*?'(.*?)'", data, re.S)
                    if srv_:
                        URL_ = srv_[0]
                        urlTab.append((URL_,'1'))
            else:
                if URL!='': urlTab.append((URL,'1'))
        return urlTab

    def getArticle(self, cItem):
        printDBG("Animekom.getVideoLinks [%s]" % cItem) 
        otherInfo1 = {}
        desc = cItem['desc']
        sts, data = self.getPage(cItem['url'])
        if sts:
            lst_dat=re.findall('review-content">(.*?)</p', data, re.S)
            if lst_dat:
                desc=desc+'\\n'+ph.clean_html(lst_dat[0])

        icon = cItem.get('icon')
        title = cItem['title']			
        return [{'title':title, 'text': desc, 'images':[{'title':'', 'url':icon}], 'other_info':otherInfo1}]


    
    def start(self,cItem):      
        mode=cItem.get('mode', None)
        if mode=='00':
            self.showmenu0(cItem)
        elif mode=='30':
            self.showitms(cItem)			
        elif mode=='31':
            self.showelms(cItem)
        elif mode=='51':
            self.searchResult(cItem)
            name= 'searchResult'    			
