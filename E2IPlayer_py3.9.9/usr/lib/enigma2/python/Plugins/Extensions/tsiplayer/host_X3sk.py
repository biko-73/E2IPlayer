# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,T
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads
from Plugins.Extensions.IPTVPlayer.libs import ph
import re,urllib,base64
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta

def getinfo():
    info_={}
    name = 'Esheeq.Com'
    hst = 'https://eceeq.org'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='2.0 18/07/2022'
    info_['dev']='RGYSoft'
    info_['cat_id']='21'
    info_['desc']='أفلام و مسلسلات تركية'
    info_['icon']='https://i.ibb.co/dBxJK7F/esseq.png'
    info_['recherche_all']='1'
    #info_['update']='Fix Links extractor'	

    return info_
    
    
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'_3sk.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        self.MAIN_URL = getinfo()['host']
        self.HEADER = {'User-Agent': self.USER_AGENT, 'Connection': 'keep-alive', 'Accept-Encoding':'gzip', 'Content-Type':'application/x-www-form-urlencoded','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
        self.defaultParams = {'header':self.HEADER, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}

    def showmenu(self,cItem):
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'اخر الحلقات'  ,'icon':cItem['icon'],'mode':'20','url':self.MAIN_URL+'/episodes/'})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'افلام'     ,'icon':cItem['icon'],'mode':'20','url':self.MAIN_URL+'/category/الأفلام-التركية/'})			
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'جميع المسلسلات','icon':cItem['icon'],'mode':'20','url':self.MAIN_URL+'/all-series/'})
        self.addDir({'import':cItem['import'],'category' :'host2','title':T('Search')  ,'icon':'https://i.ibb.co/dQg0hSG/search.png','mode':'51'})	
        header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'}

    def SearchAll(self,str_ch,page=1,extra='',type_=''): 
        return self.get_items({'page':page,'import':extra,'str_ch':str_ch,'type_':type_})

    def get_items(self,cItem={}):
        elms    = []
        extra   = cItem.get('import')
        str_ch   = cItem.get('str_ch')
        page    = cItem.get('page', 1)
        url_    = cItem.get('url', '')
        type_   = cItem.get('type_', '')      
        if url_ == '':
            with_type = True
            url0 = self.MAIN_URL+'/search/'+str_ch
        else:
            with_type = False
            url0 = url_
        if (page>1):
            url0 = url0+'/page/'+str(page)+'/'
        sts, data = self.getPage(url0)
        if sts:		
            i = 0
            pat = 'class="block-post.*?href="(.*?)".*?url\((.*?)\).*?class="title">(.*?)<'
            lst_data=re.findall(pat, data, re.S)
            for (url1,image,titre) in lst_data:
                with_ep = True
                titre = titre.replace('&#8211;','-').replace('&#8220;','').replace('&#8221;','').replace('  ',' ').replace('  ',' ').replace('  ',' ').strip()
                info  = self.std_title(titre,with_type=with_type,with_ep=with_ep)
                desc  = info.get('desc')                    
                titre = info.get('title_display')
                image = self.std_url(image)
                i = i+1
                if '?url=' in url1:
                    url_tmp = url1.split('?url=')[-1].replace('%3D','=')
                    url1 = base64.b64decode(url_tmp).decode("utf-8")
                if '/series/' in url1:
                    elms.append({'import':extra,'category' : 'host2','title':titre,'url':url1,'desc':desc,'icon':image,'hst':'tshost','good_for_fav':True,'mode':'20'})			
                else:
                    elms.append({'import':extra,'category' : 'host2','title':titre,'url':url1,'desc':desc,'icon':image,'hst':'tshost','good_for_fav':True,'type':'video'})	
        
        films_list = re.findall('class=\'current\'>.*?class=\'inactive\'>', data, re.S)	
        if films_list:
            if '/search/' in url0:
                mode = '51'
            else: mode = '20'
            elms.append({'import':extra,'category' : 'host2','title':T('Next'),'url':url_,'desc':'Next','icon':'','hst':'tshost','mode':mode,'page':page+1,'str_ch':str_ch,'type_':type_})
        return elms

    def showitms(self,cItem):
        extra   = cItem.get('import')
        str_ch  = cItem.get('str_ch')
        page    = cItem.get('page', 1)
        type_   = cItem.get('type_', '')  
        url_    = cItem.get('url', '')         
        elms = self.get_items({'url':url_,'page':page,'import':extra,'str_ch':str_ch,'type_':type_})
        for elm in elms:
            if elm.get('type','') == 'video':
                self.addVideo(elm)
            elif elm.get('type','') == 'marker':
                self.addMarker(elm)            
            else:
                self.addDir(elm)
                
    def get_links(self,cItem):
        param = dict(self.defaultParams)
        param['header']['Referer'] = self.MAIN_URL+'/' 	
        urlTab = []
        baseUrl=cItem['url']
        if '/vid/post.php?' not in baseUrl:
            sts, data = self.getPage(baseUrl)
            if sts:
                lst_data = re.findall('<a rel="nofollow".*?href="(.*?)"',data, re.S)			
                if lst_data:
                    baseUrl = lst_data[0]                
        
        #if 'dfdf/vid/post.php?' in baseUrl:
        if False:
            sts, data = self.getPage(baseUrl,param)
            if sts:	
                lst_data = re.findall('top_banner">.*?href="(.*?)"',data, re.S)			
                if lst_data:
                    baseUrl = lst_data[0]
        
        sts, data = self.getPage(baseUrl,param)
        if sts:	
            lst_data = re.findall('data-server="(.*?)"(.*?)</li>',data, re.S)
            if lst_data:
                for host,url in lst_data:
                    if '<em>ok</em>' in url: 
                        url = 'https://www.ok.ru/videoembed/'+host
                        host = 'OK.RU'
                    elif '<em>tune</em>' in url:
                        url = 'https://tune.pk/js/open/embed.js?vid='+host+'&userid=827492&_=1601112672793'
                        host = 'TUNE.PK'
                    elif '<em>turk</em>' in url:
                        url = 'https://arabveturk.com/embed-'+host+'.html'
                        host = 'ARABVETURK'
                    elif '<em>now</em>' in url:
                        url = 'https://extremenow.net/embed-'+host+'.html'
                        host = 'EXTREAMENOW'
                    elif '<em>youtube</em>' in url:
                        url = 'https://www.youtube.com/watch?v='+host
                        host = 'YOUTUBE'                         
                    elif '<em>pro</em>' in url:
                        url = 'https://protonvideo.to/iframe/'+host
                        host = 'PROTONVIDEO' 
                    elif '<em>box</em>' in url:
                        url = 'https://youdbox.org/embed-'+host+'.html'
                        host = 'YOUDBOX'                  
                    elif '<em>daily</em>' in url:
                        lst_data0 = re.findall('href="(.*?)"',url, re.S)	
                        if lst_data0:
                            url = lst_data0[0]
                            #if '?' in url: url = url.split('?',1)[0]
                            #url = url.replace('www.dailymotion.com/video/','www.dailymotion.com/embed/video/')
                        host = 'DAILYMOTION'
                    elif '<em>plus</em>' in url:
                        url = 'https://tuneplus.co/js/open/embed.js?vid='+host+'&userid=958509&_=1627365111402'
                        host = 'Tuneplus'  
                    urlTab.append({'url':url, 'name':host, 'need_resolve':1,type:''})
            else:
                lst_data = re.findall('iframe.*?src="(.*?)"',data, re.S)
                if lst_data: urlTab.append({'url':lst_data[0], 'name':'Iframe', 'need_resolve':1,type:''})	
        return urlTab	

    def getVideos(self,videoUrl):
        printDBG(videoUrl)
        urlTab = []	
        sts, data = self.getPage(videoUrl)
        if sts:	
            lst_url = re.findall('src=["\'](.*?)["\']',data, re.S|re.IGNORECASE)
            if lst_url:
                Url = lst_url[0]
                if Url.startswith('//'): Url='http:'+Url
                Url = strwithmeta(Url,{'Referer':''})
                urlTab.append((Url,'1'))
        return urlTab		 

    def SearchResult(self,str_ch,page,extra):
        url=self.MAIN_URL+'/search/'+str_ch+'/?page='+str(page)+'/'
        sts, data = self.getPage(url)
        if sts:
            lst_data=re.findall('class="block-post.*?href="(.*?)".*?title="(.*?)".*?url\((.*?)\)', data, re.S)
            for (url,titre,image) in lst_data:
                image=self.std_url(image)
                titre = ph.clean_html(titre)
                if '/series/' in url:
                    self.addDir({'import':extra,'category' : 'host2','title':titre,'url':url,'desc':'','icon':image,'hst':'tshost','good_for_fav':True,'mode':'30'})			
                else:
                    self.addVideo({'import':extra,'category' : 'host2','title':titre,'url':url,'desc':'','icon':image,'hst':'tshost','good_for_fav':True})	
