# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,T

import re
import base64,urllib

def getinfo():
    info_={}
    name='Lodynet'
    hst = 'https://lodynet.link'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='2.0 18/07/2022'    
    info_['dev']='RGYSoft'
    info_['cat_id']='21'
    info_['desc']='افلام و مسلسلات كرتون'
    info_['icon']='https://www.lodynet.co/wp-content/uploads/2015/12/logo-1.png'
    info_['recherche_all']='0'
    return info_


class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{})
        self.MAIN_URL = getinfo()['host']
        
    def showmenu(self,cItem):
        TAB = [('مسلسلات','','10',0),('افلام','','10',1),('برامج و حفلات','/category/البرامج-و-حفلات-tv/','20','')]
        self.add_menu(cItem,'','','','','',TAB=TAB,search=False)
        self.addDir({'import':cItem['import'],'category' :'host2','title':T('Search')  ,'icon':'https://i.ibb.co/dQg0hSG/search.png','mode':'50'})	

    def showsearch(self,cItem):
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث في الموقع','icon':'https://i.ibb.co/2nztSQz/all.png','mode':'51','section':''})        
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن فيلم','icon':'https://i.ibb.co/k56BbCm/aflam.png','mode':'51','section':'فيلم'})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن مسلسل','icon':'https://i.ibb.co/3M38qkV/mousalsalat.png','mode':'51','section':'مسلسل'})

    def SearchAll(self,str_ch,page=1,extra='',type_=''): 
        return self.get_items({'page':page,'import':extra,'str_ch':str_ch,'type_':type_})
    
    def SearchMovies(self,str_ch,page=1,extra=''):
        elms = self.SearchAll(str_ch,page,extra=extra,type_='فيلم')
        return elms

    def SearchSeries(self,str_ch,page=1,extra=''):
        elms = self.SearchAll(str_ch,page,extra=extra,type_='مسلسل')
        return elms


    def showmenu1(self,cItem):
        gnr = cItem.get('sub_mode','')
        if gnr == 0 : TAB = [('مسلسلات هندية','/category/مسلسلات-هنديه/','20',''),('مسلسلات هندية مدبلجة','/category/1dubbed-indian-series/','20',''),
                            ('مسلسلات تركية','/category/مشاهدة-مسلسلات-تركية/','20',''),('مسلسلات تركية مدبلجة','/category/مشاهدة-مسلسلات-تركية-مدبلجة/','20',''),('مسلسلات كورية','/category/مشاهدة-مسلسلات-كورية/','20',''),
                            ('مسلسلات صينية مترجمة','/category/مسلسلات-صينية-مترجمة/','20',''),('مسلسلات تايلاندية','/مشاهدة-مسلسلات-تايلندية/','20',''),('مسلسلات مكسيكية','/category/مسلسلات-مكسيكية-a/','20','')]
        elif gnr == 1 : TAB = [('افلام هندية','/category/افلام-هندية/','20',''),('أفلام هندية مدبلجة','/category/أفلام-هندية-مدبلجة/','20',''),('افلام تركية مترجم','/category/افلام-تركية-مترجم/','20',''),
                            ('افلام اسيوية','/category/افلام-اسيوية-a/','20',''),('افلام اجنبي','/category/افلام-اجنبية-مترجمة-a/','20',''),('انيمي','/category/انيمي/','20','')]
        self.add_menu(cItem,'','','','','',TAB=TAB)

    def get_items(self,cItem={}):
        elms    = []
        extra   = cItem.get('import')
        str_ch   = cItem.get('str_ch')
        page    = cItem.get('page', 1)
        url_    = cItem.get('url', '')
        type_   = cItem.get('type_', '')      
        if url_ == '':
            with_type = True
            if type_=='مسلسل': 
                url0 = self.MAIN_URL+'/search/'+str_ch+'/?series=1'
            elif type_!='': 
                url0 = self.MAIN_URL+'/search/'+str_ch + '+' + type_
            else:
                url0 = self.MAIN_URL+'/search/'+str_ch
            if (page>1):
                url0 = url0+'/page/'+str(page)
        else:
            with_type = False
            url0 = url_
            if (page>1):
                url0=url0+'/page/'+str(page)
        sts, data = self.getPage(url0)
        if sts:
            lst_data=re.findall('class="LodyBlock.*?href="(.*?)".*?>(.*?)<img.*?src="(.*?)".*?<h2>(.*?)</h2>(.*?)</li>', data, re.S)
            for (url,desc1,image,titre,desc2) in lst_data:  
                desc  = self.extract_desc(desc1+desc2,[('info','Ribbon">(.*?)</div>'),('time','<time>(.*?)</time>')])
                info  = self.std_title(titre,desc=desc,with_type=with_type)
                desc  = info.get('desc')                    
                titre = info.get('title_display')
                image = self.std_url(image) 
                elms.append({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'desc':desc,'icon':image,'mode':'21','good_for_fav':True,'sub_mode':'1','EPG':True,'hst':'tshost','info':info})		  
        films_list = re.findall('(<a class="next|>الصفحة التالية</a>)', data, re.S)	
        if films_list:
            if '/search/' in url0:
                mode = '51'
            else: mode = '20'
            elms.append({'import':extra,'category' : 'host2','title':T('Next'),'url':url_,'desc':'Next','icon':'','hst':'tshost','mode':mode,'page':page+1,'str_ch':str_ch,'type_':type_})
        return elms

    def showitms(self,cItem):
        desc = [('Info','Ribbon">(.*?)</div>','',''),('Time','<time>(.*?)</time>','','')]
        next = ['class="next page.*?href="(.*?)"','20']
        self.add_menu(cItem,'','class="LodyBlock.*?href="(.*?)".*?>(.*?)<img.*?src="(.*?)".*?<h2>(.*?)</h2>(.*?)</li>','','21',ord=[0,3,2,1,4],Desc=desc,Next=next,u_titre=True,EPG=True)		

    def showelms(self,cItem):
        desc = [('Episode','NumberLayer">(.*?)</div>','',''),('Time','<time>(.*?)</time>','','')]
        next = ['class="next page-numbers.*?href="(.*?)"','21']
        self.add_menu(cItem,'CategorySubLinks">(.*?)class="pagination">','class="LodyBlock.*?href="(.*?)".*?<img.*?src="(.*?)"(.*?)<h2>(.*?)</h2>(.*?)</li>','','video',ord=[0,3,1,2,4],Next=next,Desc=desc,u_titre=True,EPG=True,add_vid=False)		
        self.add_menu(cItem,'<div class="EpisodesList">(.*?)</div','<a class=.*?href="(.*?)".*?<span>(.*?)</em>','','video',ord=[0,1],EPG=True)		
            
    def SearchResult(self,str_ch,page,extra):
        url = self.MAIN_URL+'/search/'+str_ch+'/page/'+str(page)
        desc = [('Info','Ribbon">(.*?)</div>','',''),('Time','<time>(.*?)</time>','','')]
        self.add_menu({'import':extra,'url':url},'','class="LodyBlock.*?href="(.*?)".*?>(.*?)<img.*?src="(.*?)".*?<h2>(.*?)</h2>(.*?)</li>','','21',ord=[0,3,2,1,4],Desc=desc,u_titre=True)

    def getArticle(self,cItem):
        Desc = [('Date','PublishDate">(.*?)</div>','',''),('Story','BoxContentInner">(.*?)</div>','\n','')]
        desc = self.add_menu(cItem,'','DetailsBox">(.*?)<ul','','desc',Desc=Desc)	
        if desc =='': desc = cItem.get('desc','')
        return [{'title':cItem['title'], 'text': desc, 'images':[{'title':'', 'url':cItem.get('icon','')}], 'other_info':{}}]

    def get_links(self,cItem): 		
        local = [('vidlo.us','LoDyTo','0'),]
        result = self.add_menu(cItem,'ServersList">(.*?)</ul','<li.*?data-embed="(.*?)".*?>(.*?)</li>','','serv',local=local)						
        return result[1]	
        
