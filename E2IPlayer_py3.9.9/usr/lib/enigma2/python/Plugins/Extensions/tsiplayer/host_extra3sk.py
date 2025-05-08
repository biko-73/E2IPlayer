# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,T
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads
from Plugins.Extensions.IPTVPlayer.libs import ph
import re,urllib,base64

def getinfo():
    info_={}
    name ='Extra-3sk.Info'
    hst = 'https://w.extrask.live'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='2.0 18/07/2022'   
    info_['dev']='RGYSoft'
    info_['cat_id']='21'
    info_['desc']='أفلام و مسلسلات تركية'
    info_['icon']='https://i.ibb.co/qR294FT/extra.png'
    info_['recherche_all']='0'
    #info_['update']='Fix Links extractor'	

    return info_


    
    
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'extra_3sk.cookie'})
        self.USER_AGENT     = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        self.MAIN_URL       = getinfo()['host']
        self.TrySetMainUrl  = True
        self.HEADER         = {'User-Agent': self.USER_AGENT, 'Connection': 'keep-alive', 'Accept-Encoding':'gzip', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
        self.defaultParams  = {'header':self.HEADER,'with_metadata':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE} 


    def showmenu(self,cItem):
        sts, data = self.getPage(self.MAIN_URL)
        if sts:
            lst_data=re.findall('dropdown">.*?title="(.*?)".*?<ul role="menu"(.*?)</u', data, re.S)
            for (titre,data0) in lst_data:
                self.addDir({'import':cItem['import'],'category' : 'host2','title': titre,'icon':cItem['icon'],'mode':'10','url':data0,'sub_mode':'0'})
        self.addDir({'import':cItem['import'],'category' :'host2','title':T('Search')  ,'icon':'https://i.ibb.co/dQg0hSG/search.png','mode':'50'})	
                
            
         
    def showmenu1(self,cItem):
        data = cItem.get('url','')
        lst_data=re.findall('<li id="menu.*?href="(.*?)".*?>(.*?)<', data, re.S)
        for (url,titre) in lst_data:
            self.addDir({'import':cItem['import'],'category' : 'host2','title': titre,'icon':cItem['icon'],'mode':'20','url':url,'sub_mode':'0'})


    def showitms(self,cItem):
        for elm in self.get_items(cItem):
            self.addDir(elm)

    def showelms(self,cItem):
        url0 = cItem.get('url', '')
        sts, data = self.getPage(url0)
        if sts:
            lst_data0 = re.findall('class="epNum.*?href="(.*?)".*?title.*?<span>(.*?)<', data, re.S)
            if lst_data0:
                for (url,ep) in lst_data0:
                    ep = self.std_episode('الحلقة'+ep,cItem)
                    self.addVideo({'import':cItem['import'],'category' : 'host2','title':ep,'url':url,'desc':'','icon':'','mode':'21','good_for_fav':True,'EPG':True,'hst':'tshost','type':'video'})
            else:
                title = cItem['info'].get('title')
                self.addVideo({'import':cItem['import'],'category' : 'host2','title':title,'url':cItem['url'],'desc':cItem['desc'],'icon':cItem['icon'],'mode':'21','good_for_fav':True,'EPG':True,'hst':'tshost','type':'video'})

    def get_items(self,cItem={}):
        elms    = []
        extra   = cItem.get('import')
        str_ch   = cItem.get('str_ch')
        page    = cItem.get('page', 1)
        url_    = cItem.get('url', '')
        type_   = cItem.get('type_', '')      
        if url_.startswith('/'): url0 = self.MAIN_URL + url_
        if url_=='':
            with_type = True
            if type_ != '':
                url0 = self.MAIN_URL+'/search/'+str_ch+' '+type_
            else:
                url0 = self.MAIN_URL+'/search/'+str_ch
        else:
            with_type = False
            url0 = url_
        if (page>1):
            url0=url0+'/page/'+str(page)+'/'
            url0=url0.replace('//page/','/page/')
            
        sts, data = self.getPage(url0)
        if sts:
            lst_data0=re.findall('<article class="post">.*?href="(.*?)".*?title="(.*?)".*?image:url\((.*?)\)(.*?)</article>', data, re.S)
            for (url,titre,image,desc) in lst_data0:
                desc   = self.extract_desc(desc,[('rating','class="imdb">(.*?)</div>'),('views','class="views">(.*?)</div>')])
                if 'الحلقة' in titre:
                    data_list = re.findall('EP_([ 0-9]{1,5})', titre.replace('الحلقة','_EP_'), re.S)
                    if data_list:
                        episode = data_list[0]
                        desc['episode'] = episode.strip()
                    titre = titre.split('الحلقة',1)[0].strip()
                info  = self.std_title(titre,desc=desc,with_type=with_type)
                desc  = info.get('desc')                    
                titre  = info.get('title_display')
                image=self.std_url(image)
                elms.append({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'desc':desc,'icon':image,'mode':'21','good_for_fav':True,'sub_mode':'1','EPG':True,'hst':'tshost','info':info})	
            films_list = re.findall('<a class="next', data, re.S)	
            if films_list:
                if '/search/' in url0:
                    mode = '51'
                else: mode = '20'
                elms.append({'import':extra,'category' : 'host2','title':T('Next'),'url':url_,'desc':'Next','icon':'','hst':'tshost','mode':mode,'page':page+1,'str_ch':str_ch,'type_':type_})
        return elms


    def showsearch(self,cItem):
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث في الموقع','icon':'https://i.ibb.co/2nztSQz/all.png','mode':'51','section':''})        
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن فيلم','icon':'https://i.ibb.co/k56BbCm/aflam.png','mode':'51','section':'فيلم'})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن مسلسل','icon':'https://i.ibb.co/3M38qkV/mousalsalat.png','mode':'51','section':'مسلسل'})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن انمي','icon':'https://i.ibb.co/3M38qkV/mousalsalat.png','mode':'51','section':'انمي'})

    def SearchAll(self,str_ch,page=1,extra='',type_=''): 
        return self.get_items({'page':page,'import':extra,'str_ch':str_ch,'type_':type_})
    
    def SearchMovies(self,str_ch,page=1,extra=''):
        elms = self.SearchAll(str_ch,page,extra=extra,type_='فيلم')
        return elms

    def SearchSeries(self,str_ch,page=1,extra=''):
        elms = self.SearchAll(str_ch,page,extra=extra,type_='مسلسل')
        return elms
    
    def SearchAnims(self,str_ch,page=1,extra=''):
        elms0 = self.SearchAll(str_ch,page,extra=extra,type_='كرتون')
        elms1 = self.SearchAll(str_ch,page,extra=extra,type_='انمي')
        return elms0+elms1    


    def getArticle(self, cItem):
        otherInfo1 = {}
        desc= cItem['desc']	
        sts, data = self.getPage(cItem['url'])
        if sts:
            lst_dat=re.findall("<span>سنة الاصدار : </span>(.*?)</li>", data, re.S)
            if lst_dat: otherInfo1['year'] = ph.clean_html(lst_dat[0])		
            lst_dat=re.findall("</i> دول الانتاج  : </span>(.*?)</li>", data, re.S)
            if lst_dat: otherInfo1['country'] = ph.clean_html(lst_dat[0])				
            lst_dat=re.findall("</i> النوع : </span>(.*?)</li>", data, re.S)
            if lst_dat: otherInfo1['genres'] = ph.clean_html(lst_dat[0])			
            lst_dat=re.findall("<span>IMDB</span>(.*?)</a>", data, re.S)
            if lst_dat: otherInfo1['rating'] = ph.clean_html(lst_dat[0])				
            lst_dat=re.findall('class="story">(.*?)</li>', data, re.S)
            if lst_dat: desc = ph.clean_html(lst_dat[0])			
            

        icon = cItem.get('icon')
        title = cItem['title']		
        return [{'title':title, 'text': desc, 'images':[{'title':'', 'url':icon}], 'other_info':otherInfo1}]
        
        
    def get_links(self,cItem): 	
        #self.set_MAIN_URL()
        urlTab = []
        baseUrl=cItem['url']
        post_data = {'wtchBtn':''}
        sts, data = self.getPage(baseUrl+'?do=views')
        if sts:	
            #printDBG('data='+data)
            _data_ = re.findall('postID.*?"(.*?)"',data, re.S)
            if _data_: 
                code =  _data_[0]          
                __data = re.findall('tabs-server">(.*?)</ul',data, re.S)
                if __data:
                    _data = re.findall('<li.*?id="(.*?)".*?id,(.*?)\).*?>(.*?)</li>',__data[0], re.S)
                    for (q,n,titre) in _data:
                        titre = self.cleanHtmlStr(titre)
                        titre = titre.replace('سيتم عرضة بعد الانتهاء من معالجة الفيديو','').strip()
                        q = q.strip()
                        n = n.strip()
                        post_data = code+'|'+n
                        urlTab.append({'name':titre, 'url':'hst#tshost#'+baseUrl+'?do=views'+'|'+post_data, 'need_resolve':1,'type':''})					
        return urlTab	
        

    def getVideos(self,videoUrl):
        urlTab = []
        referer,q,n=videoUrl.split('|')  
        if ',' in  n:
            url=self.MAIN_URL+'/wp-content/themes/vo2020/temp/ajax/iframe2.php?id='+q+'&video='+n.split(',',1)[0] +'&serverId='+n.split(',',1)[1]        
        else:
            url=self.MAIN_URL+'/wp-content/themes/vo2020/temp/ajax/iframe.php?id='+q+'&video='+n
        header = {'Host': self.MAIN_URL.replace('https://','').replace('http://',''), 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0','Accept': '*/*',\
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',\
        'X-Requested-With': 'XMLHttpRequest','Origin': self.MAIN_URL,'Connection': 'keep-alive','Referer': referer}
        params = dict(self.defaultParams) 
        params['header']=header
        sts, data = self.getPage(url,params)
        if sts:
            printDBG('data='+data)
            Liste_els = re.findall('src=["\'](.*?)["\']', data, re.IGNORECASE)		
            if 	Liste_els:
                URL_= Liste_els[0]
                if URL_.startswith('//'): URL_='http:'+URL_
                urlTab.append((URL_,'1'))		
        return urlTab
            
    def start1(self,cItem):      
        mode=cItem.get('mode', None)
        if mode=='00':
            self.showmenu0(cItem)
        if mode=='20':
            self.showmenu1(cItem)
        if mode=='30':
            self.showitms(cItem)			
        if mode=='31':
            self.showelms(cItem)			

