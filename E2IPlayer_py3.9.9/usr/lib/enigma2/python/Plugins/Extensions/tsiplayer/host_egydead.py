# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,T

import re
import base64,urllib

def getinfo():
    info_={}
    name = 'EgyDead.live'
    hst = 'https://egydead.fyi'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='2.0 02/05/2025'        
    info_['dev']='RGYSoft'
    info_['cat_id']='21'
    info_['desc']='أفلام, مسلسلات و انمي عربية و اجنبية'
    info_['icon']='https://i.ibb.co/yNNqyth/i6yz8Xs.png'
    info_['recherche_all']='1'
    #info_['update']='Fix Links Extract'
    return info_


class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{})
        self.MAIN_URL = getinfo()['host']
        
    def showmenu(self,cItem):
        self.add_menu(cItem,'<div class="mainMenu">(.*?)</div>','(href="#">|<a>)(.*?)<.*?<ul class(.*?)</ul>','','data_out0:10',ord=[1,2],search=False,del_=['اغاني'])	
        self.addDir({'import':cItem['import'],'category' :'host2','title':T('Search')  ,'icon':'https://i.ibb.co/dQg0hSG/search.png','mode':'50'})	


    def showmenu1(self,cItem):
        self.add_menu(cItem,'','<li.*?href="(.*?)".*?>(.*?)<',cItem.get('data_out',''),'20',del_=['برامج','العاب'])
        #self.addDir({'import':cItem['import'],'category' :'host2', 'url':'/tag/رمضان-2022/', 'title':'رمضان 2022', 'desc':'', 'icon':cItem['icon'], 'mode':'20'})					
#        self.addDir({'import':cItem['import'],'category' :'host2', 'url':'/series-category/مسلسلات-رمضان-2022/', 'title':'رمضان 2022', 'desc':'', 'icon':cItem['icon'], 'mode':'20'})					

    def get_items(self,url_,url_org,extra,page,cItem={}):
        print('url_='+url_)
        elms = []
        if '/episode/' in url_: 
            sts, data = self.getPage(url_,post_data={'View':'1'})
            type_= 'video'
        else:   
            sts, data = self.getPage(url_)
            type_= ''
        if sts:
            if '/search/' in url_:
                pat0 = 'class="posts-list">(.*?)</ul>'
                with_type=True
            else:
                pat0 = '(?:class="salery-list">|class="episodes-list">|class="seasons-list">|class="cat-page">).*?class="TitleMaster">(.*?)(?:<div class="cat-page">|class="pagination">|<em>ذات صله</em>|class="TitleMaster">)'            
                with_type = False
            films_list0 = re.findall(pat0, data, re.S)	
            if films_list0:
                pat = 'class="movieItem">.*?href="(.*?)".*?title="(.*?)".*?src="(.*?)"(.*?)</li>'
                films_list = re.findall(pat, films_list0[0], re.S)		
                if films_list:
                    for (url,titre,image,desc) in films_list:
                        desc   = self.extract_desc(desc,[('episode','number_episode">(.*?)</span>'),('info','class="label">(.*?)</span>')])
                        info   = self.std_title(titre,desc=desc,with_type=with_type)
                        desc   = info.get('desc')
                        titre  = info.get('title_display')
                        image = self.std_url(image)
                        elm    = {'import':extra,'category' : 'host2','title':titre,'url':url,'desc':desc,'icon':image,'mode':'21','good_for_fav':True,'EPG':True,'hst':'tshost','info':info,'type':type_}
                        elms.append(elm)
            if elms == []:
                films_list = re.findall('class="EpsList">(.*?)</div>', data, re.S)		
                if films_list:                    
                    films_list = re.findall('<li.*?href="(.*?)".*?>(.*?)<', films_list[0], re.S)
                    for (url,ep) in films_list:
                        ep = ep.replace('حلقه','حلقة')
                        ep = self.std_episode(ep,cItem)
                        type_= 'video'
                        elm    = {'import':extra,'category' : 'host2','title':ep,'url':url,'desc':'','icon':'','mode':'21','good_for_fav':True,'EPG':True,'hst':'tshost','type':'video'}
                        elms.append(elm)
                else:
                    titre = cItem.get('sTitle',cItem.get('info',{}).get('title',cItem.get('title','')))
                    elm    = {'import':extra,'category' : 'host2','title':titre,'url':cItem.get('url',''),'desc':'','icon':'','good_for_fav':True,'EPG':True,'hst':'tshost','type':'video'}
                    elms.append(elm)
            
            if (elms != []) and (type_!='video'):
                films_list = re.findall('<a class="next', data, re.S)	
                if films_list:
                    if '/search/' in url_:
                        mode = '51'
                    else: mode = '20'
                    elms.append({'import':extra,'category' : 'host2','title':T('Next'),'url':url_org,'desc':'Next','icon':'','hst':'tshost','mode':mode,'page':page+1,'str_ch':url_org})
        return elms


    def showitms(self,cItem):
        page = cItem.get('page', 1)
        
        if page==1:
            Url = cItem['url']
        else:
            Url = cItem['url']+'?page='+str(page)+'/'
        for elm in self.get_items(Url,cItem['url'],cItem['import'],page):
            self.addDir(elm)

    def showelms(self,cItem):
        url = cItem['url']
        #[('','video',''),('/assembly/','20','URL'),('/season/','20','URL'),('/serie/','20','URL')]
        #if ('/assembly/' in url) or ('/season/' in url) or ('/serie/' in url):
        for elm in self.get_items(cItem['url'],cItem['url'],cItem['import'],1,cItem):
            if elm.get('type','') == 'video':
                self.addVideo(elm)
            else: self.addDir(elm)     
                            


    def get_links(self,cItem): 		
        post_data={'View':'1'}
        local = [('youdbox.','Youdbox','0'),('youtube.','TRAILER Youtube','0'),]
        result0 = self.add_menu(cItem,'','(trailerPopup)">.*?src="(.*?)"','','serv',local=local,ord=[1,0])						
        result1 = self.add_menu(cItem,'<ul class="serversList(.*?)</ul>','<li.*?data-link="(.*?)".*?>(.*?)</li>','','serv',post_data=post_data,local=local,LINK=cItem['url']+'?View=1')
        return result0[1]+result1[1]	
            
    def SearchResult(self,str_ch,page,extra):
        url = self.MAIN_URL+'/page/'+str(page)+'/?s='+str_ch
        desc = [('Episode','number_episode">(.*?)</span>','',''),('Info','class="label">(.*?)</span>','','')]
        self.add_menu({'import':extra,'url':url},'','class="movieItem">.*?href="(.*?)".*?title="(.*?)".*?src="(.*?)"(.*?)</li>','',[('','video',''),('/assembly/','20','URL'),('/season/','20','URL'),('/serie/','20','URL')],ord=[0,1,2,3],Desc=desc,EPG=True)

    def getArticle(self,cItem):
        Desc = [('Genre','<span>النوع : </span>(.*?)</li>','',''),('Quality','<span>الجوده : </span>(.*?)</li>','',''),('Country','<span>البلد : </span>(.*?)</li>','',''),('Year','<span>السنه : </span>(.*?)</li>','',''),('Date','<span>تاريخ الاصدار : </span>(.*?)</li>','',''),('Duration','<span>مده العرض : </span>(.*?)</li>','',''),('Story','<span>القصه</span>(.*?)</div>','\n','')]
        desc = ''
        desc = self.add_menu(cItem,'','extra-content">(.*?)<form','','desc',Desc=Desc)	
        if desc =='': desc = cItem.get('desc','')
        return [{'title':cItem['title'], 'text': desc, 'images':[{'title':'', 'url':cItem.get('icon','')}], 'other_info':{}}]

    def showsearch(self,cItem):
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث في الموقع','icon':'https://i.ibb.co/2nztSQz/all.png','mode':'51','section':''})        
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن فيلم','icon':'https://i.ibb.co/k56BbCm/aflam.png','mode':'51','section':'فيلم'})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن مسلسل','icon':'https://i.ibb.co/3M38qkV/mousalsalat.png','mode':'51','section':'مسلسل'})

    def SearchAll(self,str_ch,page=1,extra='',type_=''): 
        if type_ == '': 
            url_=self.MAIN_URL+'/search/'+str_ch+'/page/'+str(page)+'/'
        else:
            url_=self.MAIN_URL+'/search/'+str_ch+'+'+type_+'/page/'+str(page)+'/'
        elms = self.get_items(url_,str_ch,extra,page)
        return elms


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

        
