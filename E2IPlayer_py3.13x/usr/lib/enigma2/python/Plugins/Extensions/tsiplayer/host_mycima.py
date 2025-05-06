# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tshost,T
import re

def getinfo():
    info_={}
    name='WeCima'
    hst = 'https://wecima.click'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='2.0 18/07/2022'    
    info_['dev']='RGYSoft'
    info_['cat_id']='21'
    info_['desc']='افلام و مسلسلات كرتون'
    info_['icon']='https://i.ibb.co/18mqGhF/my-cima.png'
    info_['recherche_all']='1'
    return info_

class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'mycima.cookie'})
        self.MAIN_URL   = getinfo()['host']
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.011'
        self.HEADER     = {'User-Agent': self.USER_AGENT, 'Connection': 'keep-alive', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Content-Type':'application/x-www-form-urlencoded','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
        self.defaultParams = {'header':self.HEADER, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
                
    def showmenu(self,cItem):
        TAB = [('أفلام','','10',0),('مسلسلات','','10',1),('أنمي','','10',2),('المزيد','','10',3),('نوع العرض','','11',0)]
        self.add_menu(cItem,'','','','','',TAB=TAB,search=False)
        self.addDir({'import':cItem['import'],'category' :'host2','title':T('Search')  ,'icon':'https://i.ibb.co/dQg0hSG/search.png','mode':'50'})	
    
    def showmenu1(self,cItem):
        self.add_menu(cItem,'<ul class="sub-menu">(.*?)</ul','<li.*?href="(.*?)".*?>(.*?)</li>','','20',ind_0=cItem.get('sub_mode',0))		

    def showmenu2(self,cItem):
        self.add_menu(cItem,'<list--filterbox>(.*?)</list--filterbox>','data-term="(.*?)">(.*?)</item>','','20',pref_=self.MAIN_URL + '/AjaxCenter/Filtering/genre/')	

    def showsearch(self,cItem):
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث في الموقع','icon':'https://i.ibb.co/2nztSQz/all.png','mode':'51','section':''})        
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن فيلم','icon':'https://i.ibb.co/k56BbCm/aflam.png','mode':'51','section':'films'})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن مسلسل','icon':'https://i.ibb.co/3M38qkV/mousalsalat.png','mode':'51','section':'series'})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث في انمي','icon':'https://i.ibb.co/2nztSQz/all.png','mode':'51','section':'anime'})        


    def SearchAll(self,str_ch,page=1,extra='',type_=''): 
        if type_=='':
            elms = []
            r1 = self.get_items({'page':page,'import':extra,'str_ch':str_ch,'type_':''})
            r2 = self.get_items({'page':page,'import':extra,'str_ch':str_ch,'type_':'series'})
            r3 = self.get_items({'page':page,'import':extra,'str_ch':str_ch,'type_':'anime'}) 
            for elm in r1+r2+r3:
                if elm['title'] != T('Next'):
                    elms.append(elm)
            return elms         
        elif type_== 'films': type_ = ''
        return self.get_items({'page':page,'import':extra,'str_ch':str_ch,'type_':type_})
    
    def SearchMovies(self,str_ch,page=1,extra=''):
        elms = self.SearchAll(str_ch,page,extra=extra,type_='films')
        return elms

    def SearchSeries(self,str_ch,page=1,extra=''):
        elms = self.SearchAll(str_ch,page,extra=extra,type_='series')
        return elms
    
    def SearchAnims(self,str_ch,page=1,extra=''):
        elms = self.SearchAll(str_ch,page,extra=extra,type_='anime')
        return elms

    def get_items(self,cItem={}):
        elms     = []
        extra    = cItem.get('import')
        str_ch   = cItem.get('str_ch')
        page     = cItem.get('page', 1)
        url_     = cItem.get('url', '')
        type_    = cItem.get('type_', '')      
        if url_ == '':
            with_type = True
            if type_=='': 
                url0 = self.MAIN_URL+'/search/'+str_ch+'/'
                if (page>1):
                    url0 = url0+'/page/'+str(page)+'/'
            else:
                url0 = self.MAIN_URL+'/search/'+str_ch+'/list/'+type_+'/'
                if (page>1):
                    url0 = url0+'?page_number='+str(page)+'/'
        else:
            with_type = False
            url0 = url_
            if (page>1): url0 = url0+'/page/'+str(page)+'/'
        sts, data = self.getPage(url0)
        if sts:
            Liste_films_data = re.findall('<div class="Grid--WecimaPosts"(.*?)(?:class="pagination">|class="RightUI">)', data, re.S)
            if Liste_films_data:
                Liste_films_data = re.findall('class="GridItem".*?href="(.*?)".*?image:url\((.*?)\).*?</span>(.*?)</strong>(.*?)</ul>', data, re.S)
                for (url,image,titre,desc) in Liste_films_data:
                    #desc  = self.extract_desc(desc,[('rating','StarsIMDB">(.*?)</div>'),('genre','fa-film">(.*?)</li>'),('quality','desktop">(.*?)</li>'),('age','<span>الإشراف العائلي : </span>(.*?)<'),('country','<span>دولة الإنتاج : </span>(.*?)<'),('year','<span>سنة الإنتاج : </span>(.*?)<')])
                    info  = self.std_title(titre,with_type=with_type)
                    desc  = info.get('desc')                    
                    titre = info.get('title_display')
                    image = self.std_url(image) 
                    elms.append({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'desc':desc,'icon':image,'mode':'21','good_for_fav':True,'EPG':True,'hst':'tshost','info':info})		  
            films_list = re.findall('<a class="next', data, re.S)	
            if films_list:
                if '/search/' in url0:
                    mode = '51'
                else: mode = '20'
                if type_ == '': type_ ='films'
                print(type_)
                elms.append({'import':extra,'category' : 'host2','title':T('Next'),'url':url_,'desc':'Next','icon':'','hst':'tshost','mode':mode,'page':page+1,'str_ch':str_ch,'section':type_})
        return elms


    def showitms(self,cItem):
        if '/Filtering/genre/' in cItem['url']: 
            URL=''
            page = cItem.get('page',1)
            if page!=1: URL = cItem['url'] + '/offset/'+str((page-1)*30)+'/'
            self.add_menu(cItem,'','GridItem.*?href=."(.*?)".*?title=."(.*?)".*?url.(.*?)\)','','21',Next=[2,'20'],ord=[0,1,2],u_titre=True,EPG=True,LINK=URL)               
        else:
            Next = ['class="next page.*?href="(.*?)"','20']
            self.add_menu(cItem,'<div class="Grid--WecimaPosts">(.*?)(?:class="pagination">|class="RightUI">)','class="GridItem".*?href="(.*?)".*?image:url\((.*?)\).*?</span>(.*?)</strong>(.*?)</ul>','','21',Next=Next,ord=[0,2,1,3],u_titre=True,EPG=True)
    
    def showelms(self,cItem):
        self.add_menu(cItem,'class="List--Seasons--Episodes">(.*?)</div>','href="(.*?)".*?>(.*?)<','','21', Titre='Seasons',EPG=True)
        self.add_menu(cItem,'class="Episodes--Seasons--Episodes(.*?)</singlesection','href="(.*?)".*?>(.*?)</episodeTitle>','','video', Titre='Episodes',EPG=True)

    def SearchResult(self,str_ch,page,extra):
        url = self.MAIN_URL+'/search/'+str_ch+'/page/'+str(page)
        self.add_menu({'import':extra,'url':url},'<div class="Grid--MycimaPosts">(.*?)(?:class="pagination">|class="RightUI">)','class="GridItem".*?href="(.*?)".*?image:url\((.*?)\).*?</span>(.*?)</strong>(.*?)</ul>','','21',ord=[0,2,1,3],u_titre=True,EPG=True)

    def getArticle(self,cItem):
        Desc = [('Title','<span>الإسم بالعربي</span>(.*?)</li>','',''),('Country/Lang','<span>البلد و اللغة</span>(.*?)</li>','',''),('Time','<span>المدة</span>(.*?)</li>','',''),
                ('Genre','<span>النوع</span>(.*?)</li>','',''),('Quality','<span>الجودة</span>(.*?)</li>','',''),('Time','<span>مدة الحلقة</span>(.*?)</li>','',''),
                ('Category','<span>التصنيف</span>(.*?)</li>','',''),('Story','StoryMovieContent">(.*?)</div>','\n','')]
        desc = self.add_menu(cItem,'','','','desc',Desc=Desc)	
        if desc =='': desc = cItem.get('desc','')
        return [{'title':cItem['title'], 'text': desc, 'images':[{'title':'', 'url':cItem.get('icon','')}], 'other_info':{}}]

    def get_links(self,cItem): 		
        local = [('mycima.','MyCima','1'),]
        result = self.add_menu(cItem,'WatchServersList">(.*?)</ul','<li.*?url="(.*?)".*?>(.*?)</li>','','serv',local=local)						
        return result[1]	

    def getVideos(self,videoUrl):
        result = self.add_menu({'url':videoUrl},'sources: \[(.*?)\]','format:.*?["\'](.*?)["\'].*?src:.*?["\'](.*?)["\']','','link4',ord=[1,0])	
        if result[1] ==[]: result = self.add_menu({'url':videoUrl},'','source.*?(src)="(.*?)"',result[0],'link4',ord=[1,0])	
        return result[1]	
        
