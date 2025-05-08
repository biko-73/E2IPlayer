# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tshost,T
import re

def getinfo():
    info_={}
    name = 'TukTukCinema'
    hst = 'https://tuktukcinema.pro'
    info_['old_host'] = hst
    hst_              = tshost(name)	
    if hst_!='': hst  = hst_
    info_['host']     = hst
    info_['name']     = name
    info_['version']  = '2.0 18/07/2022'
    info_['dev']      = 'RGYSoft'
    info_['cat_id']   = '21'
    info_['desc']     = 'هنا معلومات عن الموقع'
    info_['icon']     = hst+'/wp-content/uploads/2021/01/lela.png'
    return info_
   
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{})
        self.MAIN_URL      = getinfo()['host']
              
    def showmenu(self,cItem):
        TAB = [('افلام','','10',0),('مسلسلات','','10',1),('انميات','','10',2),('برامج تلفزيونية','','10',3)]
        printDBG('showmenu')
        self.add_menu(cItem,'','','','','',TAB=TAB,search=False)        
        self.addDir({'import':cItem['import'],'category' :'host2','title':T('Search')  ,'icon':'https://i.ibb.co/dQg0hSG/search.png','mode':'50'})	


    def showmenu1(self,cItem):
        printDBG('showmenu1')
        self.add_menu(cItem,'<ul class="sub-menu">(.*?)</ul>','<li.*?href="(.*?)".*?>(.*?)<','','20',ind_0=cItem.get('sub_mode',0),ord=[0,1])
        
    def showitms(self,cItem):
        desc = [('Genre','class="Genres">(.*?)</ul>','','')]
        next = ['class="next.page-numbers".href="(.*?)"','20']
        self.add_menu(cItem,'','class="Block--Item">.*?href="(.*?)".*?data-src="(.*?)"(.*?)<h3>(.*?)</h3>','','21',ord=[0,3,1,2],Desc=desc,Next=next,u_titre=True,EPG=True)		

    def showelms(self,cItem):
        sts, data = self.getPage(cItem.get('url',''))
        if sts:
            if '/watch/' in data: 
                self.addVideo({'category':'host2','good_for_fav':True, 'title':cItem['title'],'url':cItem['url'], 'desc':cItem.get('desc',''),'import':cItem['import'],'icon':cItem['icon'],'hst':'tshost'})						
            self.add_menu(cItem,'<section class="allepcont(.*?)</section>','<a href="(.*?)".*?alt="(.*?)".*?data-src="(.*?)"',data,'video',ord=[0,1,2],Titre='الحلقات',u_titre=True,EPG=True,add_vid=False)		
            self.add_menu(cItem,'<section class="allseasonss"(.*?)</section>','Block--Item">.*?href="(.*?)".*?alt="(.*?)".*?data-srccs="(.*?)"',data,'21',ord=[0,1,2],Titre='المواسم',u_titre=True,EPG=True,add_vid=False)		

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

    def get_items(self,cItem={}):
        elms    = []
        extra   = cItem.get('import')
        str_ch   = cItem.get('str_ch')
        page    = cItem.get('page', 1)
        url_    = cItem.get('url', '')
        type_   = cItem.get('type_', '')      
        if url_ == '':
            with_type = True
            if type_!='': 
                url0 = self.MAIN_URL+'/?s='+str_ch + '+' + type_
            else:
                url0 = self.MAIN_URL+'/?s='+str_ch
        else:
            with_type = False
            url0 = url_
        if (page>1):
            url0 = url0+'&page='+str(page)
        sts, data = self.getPage(url0)
        if sts:
            lst_data=re.findall('class="Block--Item">.*?href="(.*?)".*?title="(.*?)".*?img src="(.*?)"(.*?)</a>', data, re.S)
            for (url,titre,image,desc) in lst_data:  
                desc  = self.extract_desc(desc,[('genre','catssection">(.*?)</div'),('plot','<p>(.*?)</p>')])
                info  = self.std_title(titre,desc=desc,with_type=with_type)
                desc  = info.get('desc')                    
                titre = info.get('title_display')
                image = self.std_url(image) 
                elms.append({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'desc':desc,'icon':image,'mode':'21','good_for_fav':True,'sub_mode':'1','EPG':True,'hst':'tshost','info':info})		  
        films_list = re.findall('class="next page-numbers"', data, re.S)	
        if films_list:
            if '/?s=' in url0:
                mode = '51'
            else: mode = '20'
            elms.append({'import':extra,'category' : 'host2','title':T('Next'),'url':url_,'desc':'Next','icon':'','hst':'tshost','mode':mode,'page':page+1,'str_ch':str_ch,'type_':type_})
        return elms




    def get_links(self,cItem): 	
        urlTab = []	
        URL=cItem['url']
        if not URL.endswith('/watch/'):
            if not URL.endswith('/'): URL = URL+'/watch/'
            else: URL = URL+'watch/'
        sts, data = self.getPage(URL)
        if sts:
            Liste_els = re.findall('<li data-link="(.*?)".*?>(.*?)</li>', data, re.S)
            for (url,titre) in Liste_els:
                titre = self.cleanHtmlStr(titre)
                url = url+'|Referer='+URL
                urlTab.append({'name':titre, 'url':url, 'need_resolve':1})	
        return urlTab


    def getArticle(self,cItem):
        Desc = [('Genre','catssection">(.*?)</div','',''),('Story','<p>(.*?)</p>','\n','')]
        desc = self.add_menu(cItem,'','class="story">(.*?)</article>','','desc',Desc=Desc)	
        if desc =='': desc = cItem.get('desc','')
        return [{'title':cItem['title'], 'text': desc, 'images':[{'title':'', 'url':cItem.get('icon','')}], 'other_info':{}}]


    def SearchResult(self,str_ch,page,extra):
        url=self.MAIN_URL+'/?s='+str_ch+'&page='+str(page)
        desc = [('Genre','class="Genres">(.*?)</ul>','','')]
        self.add_menu({'import':extra,'url':url},'','class="Block--Item">.*?href="(.*?)".*?title="(.*?)".*?img src="(.*?)"(.*?)</a>','','21',ord=[0,1,2,3],Desc=desc,u_titre=True,EPG=True)		