# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,gethostname,tscolor,tshost
import urllib
import re
from Components.config import config

def getinfo():
    info_={}
    name = 'Arabseed'
    hst = 'https://m15.asd.rest/main'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='2.0 05/05/2025'    
    info_['dev']='RGYSoft'
    info_['cat_id']='21'#'201'
    info_['desc']='أفلام و مسلسلات عربية و اجنبية'
    info_['icon']='https://i.ibb.co/7S7tWYb/arabseed.png'
    info_['recherche_all']='1'
    #info_['update']='Add Filter section'
    return info_
    
    
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'arabseed.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        self.MAIN_URL = getinfo()['host']
        self.SiteName   = 'Arabseed'
        self.HEADER = {'User-Agent': self.USER_AGENT, 'Connection': 'keep-alive', 'Accept-Encoding':'gzip', 'Content-Type':'application/x-www-form-urlencoded','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
        self.defaultParams = {'header':self.HEADER, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        #self.getPage = self.cm.getPage
        self.cacheLinks = {}
        
    def showmenu(self,cItem):
        hst='host2'
        self.Arablionz_TAB = [
                            {'category':hst, 'sub_mode':0, 'title': 'افلام',       'mode':'10'},
                            {'category':hst, 'sub_mode':1, 'title': 'نيتفليكس - Netfilx',       'mode':'10'},
                            {'category':hst, 'sub_mode':2, 'title': 'مسلسلات',     'mode':'10'},
                            {'category':hst, 'sub_mode':3, 'title': 'مصارعه','url':self.MAIN_URL+'/category/مصارعه/', 'mode':'20'},                       
                            {'category':hst, 'title': tscolor('\c0000????') + 'حسب التصنيف' , 'mode':'19','count':1,'data':'none','code':''},	
                            {'category':'search','title':tscolor('\c00????30') + _('Search'), 'search_item':True,'page':1,'hst':'tshost'},
                            ]		
        self.listsTab(self.Arablionz_TAB, {'import':cItem.get('import',''),'icon':cItem.get('icon','')})	

    def showmenu1(self,cItem):
        hst='host2'
        gnr=cItem['sub_mode']
        sts, data = self.getPage(self.MAIN_URL+'/main/')
        if sts:
            cat_film_data=re.findall('<ul class="sub-menu">(.*?)</ul>', data, re.S) 
            if cat_film_data:
                data2=re.findall('<li.*?href="(.*?)".*?>(.*?)<', cat_film_data[gnr], re.S)
                for (url,titre) in data2:
                    if not url.startswith('http'): url=self.MAIN_URL+url
                    self.addDir({'import':cItem.get('import',''),'category' : 'host2','url': url,'title':titre,'desc':'','icon':cItem.get('icon',''),'mode':'20'})	
        if gnr==2:
            self.addDir({'import':cItem.get('import',''), 'title': 'Ramadan 2022','category' : 'host2','url': self.MAIN_URL+'/category/%d8%a7%d9%84%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86-2022','desc':'','icon':cItem.get('icon',''),'mode':'20'})            
    def showfilter(self,cItem):
        count=cItem['count']
        data1=cItem['data']	
        codeold=cItem['code']	
        if count==1:
            sts, data = self.getPage(self.MAIN_URL+'/category/foreign-movies-3/')
            if sts:
                data1=re.findall('TaxPageFilterItem.*?<ul>(.*?)</ul', data, re.S)
            else:
                data1=None
        if count==5:
            mode_='20'
        else:
            mode_='19'
        if data1:
            lst_data1 = re.findall('<li.*?data-tax="(.*?)".*?data-term="(.*?)">(.*?)</li>',data1[count-1], re.S)	
            for (x1,x2,x3) in lst_data1:
                #if  ((('–' not in x2) and ('-' not in x2)) or('Sci-Fi' in x2))and ('null' not in x2)and ('كريستينا' not in x2):
                if not((x1 == 'category') and (x2.strip()=='')):
                    code=codeold+x1+'='+x2.strip()+'&'
                else:
                    code=codeold
                self.addDir({'import':cItem.get('import',''),'category' :'host2', 'url':code, 'title':ph.clean_html(x3), 'desc':code, 'icon':cItem.get('icon',''), 'mode':mode_,'count':count+1,'data':data1,'code':code, 'sub_mode':'item_filter','page':-1})					
        
    def showitms(self,cItem):
        desc = [('Info','Ribbon">(.*?)</div>','',''),('Story','Story">(.*?)</div>','','')]
        next = ['next page-numbers.*?href="(.*?)"','20']
        if cItem['url'].startswith('http') or (cItem['url'].startswith('/')):
            self.add_menu(cItem,'Blocks">(.*?)</ul>','class="MovieBlock.*?href="(.*?)".*?(?:image=|data-src=)"(.*?)"(.*?)<h4>(.*?)</h4>(.*?)</a>','','21',ind_0 = -1,ord=[0,3,1,2,4],Desc=desc,Next=next,u_titre=True,EPG=True)		
        else:
            LINK = self.MAIN_URL+'/wp-content/themes/Elshaikh2021/Ajaxat/Home/FilteringShows.php'
            post_data ={}
            if '&' in cItem['url']:
                prams = cItem['url'].split('&')
            else:
                prams = cItem['url']
            for param in prams:
                if '=' in param:
                    pram_x1,param_x2 = param.split('=')
                    post_data[pram_x1]=param_x2
            self.add_menu(cItem,'Blocks">(.*?)</ul>','class="MovieBlock.*?href="(.*?)".*?(?:image=|img src=)"(.*?)"(.*?)<h4>(.*?)</h4>(.*?)</a>','','21',LINK = LINK,post_data=post_data,ind_0 = -1,ord=[0,3,1,2,4],Desc=desc,Next=next,u_titre=True,EPG=True)		
 
    def showelms(self,cItem):
        self.add_menu(cItem,'','(Trailer).*?src="(.*?)"','','video',post_data = {'href':cItem['url']},ord=[1,0],corr_=False,add_vid=False,LINK=self.MAIN_URL+'/wp-content/themes/Elshaikh2021/Ajaxat/Home/LoadTrailer.php',hst='none')	
        self.add_menu(cItem,'class="ContainerEpisodesList(.*?)</div>','href="(.*?)".*?>(.*?)</a>','','video',u_titre=True,EPG=True)		



    def SearchResult(self,str_ch,page,extra):
        elms = []
        url = self.MAIN_URL+'/find/?find='+str_ch+'&offset='+str(page)
        desc = [('Info','Ribbon">(.*?)</div>','',''),('Story','Story">(.*?)</div>','','')]
        data = self.add_menu({'import':extra,'url':url},'','class="MovieBlock.*?href="(.*?)".*?(?:image=|img src=)"(.*?)"(.*?)<h4>(.*?)</h4>(.*?)</a>','','21',ind_0 = -1,ord=[0,3,1,2,4],Desc=desc,u_titre=True,year_op=1,EPG=True)		
        return data[2]

    def MediaBoxResult1(self,str_ch,year_,extra):
        urltab=[]
        str_ch_o = str_ch
        str_ch = urllib.quote(str_ch_o+' '+year_)	
        url_=self.MAIN_URL+'/?s='+str_ch+'&page='+str(1)
        sts, data = self.getPage(url_)
        if sts:		
            data1=re.findall('class="BlockItem.*?href="(.*?)".*?src="(.*?)".*?Title">(.*?)<(.*?)</div>', data, re.S)		
            i=0
            for (url,image,titre,desc) in data1:
                desc=ph.clean_html(desc)
                titre=ph.clean_html(titre)
                desc0,titre = self.uniform_titre(titre,year_op=1)
                if desc.strip()!='':
                    desc = tscolor('\c00????00')+'Desc: '+tscolor('\c00??????')+desc
                desc=desc0+desc	
                titre0='|'+tscolor('\c0060??60')+'ArabSeeD'+tscolor('\c00??????')+'| '+titre				
                
                urltab.append({'titre':titre,'import':extra,'good_for_fav':True,'EPG':True,'category' : 'host2','url': url,'title':titre0,'desc':desc,'icon':image,'mode':'31','hst':'tshost'})			
        return urltab
        
    def get_links(self,cItem): 	
        urlTab = []	
        #print('get_links')
        if config.plugins.iptvplayer.ts_dsn.value:
            urlTab = self.cacheLinks.get(str(cItem['url']), [])		
        if urlTab == []:		
            url=cItem['url']
            sts, data = self.getPage(url)
            if sts:
                print('url='+url)
                
                server_data = re.findall('WatchButtons">.*?<a href="(.*?)"', data, re.S)
                if server_data:
                    URL = server_data[0]
                    #print('url='+URL)
                    addParams = dict(self.defaultParams)
                    addParams['header']['Referer'] = self.MAIN_URL
                    sts, data = self.getPage(URL,addParams)
                    if sts:
                        print(data)
                        server_data = re.findall('<ul>(.*?)</ul>', data, re.S)
                        if server_data:
                            server_data = re.findall('3>(.*?)</h3>(.*?)<h', data+'<h', re.S)
                            for (label,data) in server_data:
                                label = label.replace('مشاهدة','').strip()
                                server_data = re.findall('data-link="(.*?)".*?>(.*?)</li>', data, re.S)
                                for (URL_,Titre) in server_data:
                                    Titre = Titre.replace('سيرفر عرب سيد','Local Server').replace('سيرفر','Server')
                                    urlTab.append({'name':'['+label+'] '+self.cleanHtmlStr(Titre).strip(), 'url':URL_, 'need_resolve':1})
                            
            if config.plugins.iptvplayer.ts_dsn.value:
                self.cacheLinks[str(cItem['url'])] = urlTab
        return urlTab
            
    def getVideos(self,videoUrl):
        urlTab = []	
        code1,code2,qu=videoUrl.split('|')
        url=self.MAIN_URL+'/wp-content/themes/ArbSeed/Server.php'
        url=self.MAIN_URL+'/wp-content/themes/Elshaikh2021/Ajaxat/Single/Server.php'
        post_data = {'post_id':code2,'server':code1,'qu':qu}
        sts, data = self.getPage(url,post_data=post_data)
        if sts:
            print(data)
            Liste_els = re.findall('src.*?["\'](.*?)["\']', data, re.S|re.IGNORECASE)
            if Liste_els:
                URL_ = Liste_els[0]
                if URL_.startswith('//'): URL_ = 'http:'+URL_
                urlTab.append((URL_,'1'))
        return urlTab	
        
    def getArticle(self, cItem):
        otherInfo1 = {}
        desc = cItem['desc']
        sts, data = self.getPage(cItem['url'])
        if sts:
            lst_dat=re.findall('class="HoldINfo(.*?)class="topBar', data, re.S)
            if lst_dat:
                lst_dat0=re.findall("<li>(.*?):(.*?)</li>", lst_dat[0], re.S)
                for (x1,x2) in lst_dat0:
                    if 'الجودة'     in x1: otherInfo1['quality'] = ph.clean_html(x2)
                    if 'تاريخ'      in x1: otherInfo1['year'] = ph.clean_html(x2)				
                    if 'اللغة'      in x1: otherInfo1['language'] = ph.clean_html(x2)	
                    if 'النوع'      in x1: otherInfo1['genres'] = ph.clean_html(x2)				
                    if 'الدولة'      in x1: otherInfo1['country'] = ph.clean_html(x2)	
                    if 'السنه'      in x1: otherInfo1['year'] = ph.clean_html(x2)	                         
            lst_dat=re.findall('StoryLine">(.*?)</div>', data, re.S)
            if lst_dat: desc = ph.clean_html(lst_dat[0])
        
        icon = cItem.get('icon')
        title = cItem['title']	
        
        return [{'title':title, 'text': desc, 'images':[{'title':'', 'url':icon}], 'other_info':otherInfo1}]

   

