# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,T
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.utils import Quote,IsPython3 
from Components.config import config
import re


def getinfo():
    info_={}
    name = 'Cimaclub.Com'
    hst = 'https://cimaclub.us'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='2.0 18/07/2022'        
    info_['dev']='RGYSoft'
    info_['cat_id']='21'
    info_['desc']='أفلام, مسلسلات و انمي عربية و اجنبية'
    info_['icon']='https://i.pinimg.com/originals/f2/67/05/f267052cb0ba96d70dd21e41a20a522e.jpg'
    info_['recherche_all']='1'
    #info_['update']='New Template'
    return info_
    
    
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'cimaclub.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        self.MAIN_URL = getinfo()['host']
        self.HTTP_HEADER = {'User-Agent': self.USER_AGENT, 'DNT':'1', 'Accept': 'text/html', 'Accept-Encoding':'gzip, deflate', 'Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
        self.AJAX_HEADER = dict(self.HTTP_HEADER)
        self.AJAX_HEADER.update( {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'} )
        if IsPython3():
            no_redirection=False
        else:
            no_redirection=True
            
        self.defaultParams = {'header':self.HTTP_HEADER, 'with_metadata':True,'no_redirection':no_redirection, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        
        self.defaultParams2 = {'header':self.AJAX_HEADER, 'with_metadata':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}

    def showmenu0(self,cItem):
        hst='host2'
        img_=cItem['icon']
        Cimaclub_TAB=[
                      #{'category':hst,'title': tscolor('\c0000????') + 'Ramadan 2022' ,'mode':'30', 'url': self.MAIN_URL+'/category/مسلسلات-رمضان-2022'},	
                      {'category':hst,'title': tscolor('\c00????00') +'Main'    ,'mode':'20'  ,'sub_mode':'filter'},	
                      {'category':hst,'title': 'Films'    ,'mode':'20'  ,'sub_mode':'film'},
                      {'category':hst,'title': 'Series'   ,'mode':'20'  ,'sub_mode':'serie'},
                      {'category':hst,'title': 'Other'    ,'mode':'20'  ,'sub_mode':'other'},
                      {'category':hst,'title': tscolor('\c0000??00') + 'Filter'       ,'mode':'21', 'url': self.MAIN_URL+'/getposts?'},					  
                      #{'category':'search'  ,'title':tscolor('\c0000????') +  _('Search'),'search_item':True,'page':1,'hst':'tshost'},
                      {'category':hst,'title':T('Search') ,'icon':'https://i.ibb.co/dQg0hSG/search.png','mode':'51'},
                    ]
        self.listsTab(Cimaclub_TAB, {'icon':img_,'import':cItem['import']})

    def showmenu2(self,cItem):
        count=cItem.get('count',0)
        data1=cItem.get('data','')	
        codeold=cItem['url']	
        if count==0:
            sts, data = self.getPage_(self.MAIN_URL)
            if sts:
                data1=re.findall('class="dropdown-list(.*?)</ul>', data, re.S)
            else:
                data1=None
        if count==3:
            mode_='30'
        else:
            mode_='21'
        if data1:
            lst_data1 = re.findall('<li.*?data-tax="(.*?)".*?data-cat="(.*?)".*?bold">(.*?)<',data1[count], re.S)	
            for (x1,x2,x3) in lst_data1:
                code=codeold+x1+'='+x2+'&'
                self.addDir({'import':cItem['import'],'category' :'host2', 'url':code, 'title':x3, 'desc':x1, 'icon':cItem['icon'], 'mode':mode_,'count':count+1,'data':data1,'code':code, 'sub_mode':'item_filter'})					

    def showmenu1(self,cItem):
        gnr2=cItem['sub_mode']			 
        url=self.MAIN_URL
        img=cItem['icon']
        if gnr2=='filter':
            Cimaclub_filter=[{'category':'host2', 'title': 'الاحدث'       , 'url':self.MAIN_URL+'/getposts?type=one&data=latest', 'desc':'', 'icon':img, 'mode':'30', 'page':1},
                             {'category':'host2', 'title': 'المثبت'      , 'url':self.MAIN_URL+'/getposts?type=one&data=pin'   , 'desc':'', 'icon':img, 'mode':'30', 'page':0},						  
                             {'category':'host2', 'title': 'الاكثر مشاهدة', 'url':self.MAIN_URL+'/getposts?type=one&data=view'                                 , 'desc':'', 'icon':img, 'mode':'30', 'page':1},						  
                             {'category':'host2', 'title': 'الأعلى تقييماً', 'url':self.MAIN_URL+'/getposts?type=one&data=rating'                                   , 'desc':'', 'icon':img, 'mode':'30', 'page':1},	 
                            ]
            self.listsTab(Cimaclub_filter, {'name':'categories','import':cItem['import']})
        else:
            sts, data = self.getPage_(url)
            if sts:
                lst_data = re.findall('<ul(.*?)</ul>',data, re.S)
                if lst_data:
                    if gnr2=='film':
                        data1= lst_data[0]
                    elif gnr2=='serie':
                        #self.addDir({'category' :'host2', 'url':self.MAIN_URL+'/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b9%d8%b1%d8%a8%d9%8a/%d8%b1%d9%85%d8%b6%d8%a7%d9%86-2019/', 'title':'رمضان 2019', 'desc':'رمضان 2019', 'icon':img, 'mode':'30','page':1,'import':cItem['import']})					
                        data1= lst_data[1]		
                    elif gnr2=='other':
                        data1= lst_data[2]
                    lst_data1 = re.findall('<li.*?href="(.*?)".*?>(.*?)<',data1, re.S)
                    for (url1,titre1) in lst_data1:
                        if ('الرئيسية' not in titre1) and ('الأفلام' != titre1.strip()) and ('للكبار' not in titre1):
                            self.addDir({'import':cItem['import'],'category' :'host2', 'url':url1, 'title':titre1, 'desc':titre1, 'icon':img, 'mode':'30', 'page':1})
                    if gnr2=='film000':
                        lst_data0 = re.findall('FooterMenu">(.*?)</ul>',data, re.S)
                        if lst_data0:
                            lst_data01 = re.findall('<li.*?href="(.*?)">(.*?)<',lst_data0[0], re.S)
                            for (url11,titre11) in lst_data01:
                                if ('الرئيسية' not in titre11) and ('الطلبات' not in titre11) and ('سلاسل' not in titre11):
                                    self.addDir({'import':cItem['import'],'category' :'host2', 'url':url11, 'title':titre11, 'desc':titre11, 'icon':img, 'mode':'30', 'page':1})
                                
                        self.addMarker({'title':tscolor('\c0000??00')+'Films by Filtre (coming soon)','icon':'','desc':''})				
                        lst_data2 = re.findall('tax="genre">.*?<ul(.*?)</ul>',data, re.S)
                        if lst_data2:
                            lst_data3 = re.findall('<li.*?href="(.*?)">(.*?)</li>',lst_data2[0], re.S)
                            for (url3,titre3) in lst_data3:
                                if url3=='#':url3=self.MAIN_URL					
                                self.addDir({'import':cItem['import'],'category' :'host2', 'url':url3, 'title':ph.clean_html(titre3), 'desc':ph.clean_html(titre3), 'icon':img, 'mode':'30','page':1})					
        
    def showitms(self,cItem):
        page=cItem.get('page',1)
        printDBG('url0='+cItem['url'])
        url0=cItem['url'].replace('&amp%3B','&').replace('&amp;','&')
        printDBG('url00='+url0)
        url=url0
        if page!=0:
            if '?' in url0:
                url=url0+'&page='+str(page)
            else:
                url=url0+'?page='+str(page)
        url=url.replace('&&','&')	
        #sts, data = self.cm.getPage(url)	
        if (not url.startswith('http')): url = self.MAIN_URL + url
        sts, data = self.getPage_(url)	
        if sts:		
            lst_data=re.findall('class="content-box">.*?href="(.*?)".*?src="(.*?)"(.*?)<h3>(.*?)</h3>', data, re.S)
            for (url1,image,desc0,name_eng) in lst_data:
                #name_eng=name_eng.replace(' اون لاين','')
                #name_eng=name_eng.replace('مسلسل ','')
                #name_eng=name_eng.replace('فيلم ','')
                desc1 =''
                lst_inf=re.findall('ti-eye">(.*?)</', desc0, re.S)
                if lst_inf: desc1 = desc1 + tscolor('\c00????00')+'Views: '+tscolor('\c00??????')+ph.clean_html(lst_inf[0])+'\n'
                lst_inf=re.findall('ti-star">(.*?)</', desc0, re.S)
                if lst_inf: desc1 = desc1 + tscolor('\c00????00')+'Rate: '+tscolor('\c00??????')+ph.clean_html(lst_inf[0])+'\n'				
                desc00,name_eng = self.uniform_titre(name_eng)
                if '://'in image: image = image.split('://')[0]+'://'+Quote(image.split('://')[1])
                else: image = cItem['image']
                desc=desc00+desc1
                self.addDir({'import':cItem['import'],'good_for_fav':True,'category':'host2', 'url':url1,'data_post':'', 'title':ph.clean_html(name_eng), 'desc':desc, 'icon':image, 'mode':'31','EPG':True,'hst':'tshost'} )							
            if page!=0:
                self.addDir({'import':cItem['import'],'category':'host2', 'url':url0, 'title':tscolor('\c0000??00')+'Page Suivante', 'page':page+1, 'desc':'Page Suivante', 'icon':cItem['icon'], 'mode':'30'})	

    def showelems(self,cItem):
        url0=cItem['url']	
        data_post=cItem.get('data_post','')
        titre=cItem['title']			
        lst=[]
        tab=[] 
        #sts, data = self.cm.getPage(url0)	
        sts, data = self.getPage_(url0)
        if sts:
            tr_data=re.findall('TrailerPopup">.*?src="(.*?)"', data, re.S)		
            if tr_data:			
                if tr_data[0].strip() != 'https://www.youtube.com/embed/':
                    params = {'import':cItem['import'],'good_for_fav':True,'category' : 'video','url': tr_data[0],'title':'Trailer','desc':'','icon':cItem['icon'],'hst':'none'} 
                    self.addVideo(params)		
            cat_data=re.findall('(?:<ul class="Seasons|<ul class="Episodes).*?<h2>(.*?)</h2>(.*?)</ul>', data, re.S)		
            if cat_data:
                for (titre_,data_) in cat_data:
                    self.addMarker({'title':tscolor('\c0000??00')+titre_,'icon':cItem['icon'],'desc':''})	
                    cat_data2=re.findall('<li.*?href="(.*?)".*?>(.*?)</li>', data_, re.S)	
                    for (url_,titre0_) in cat_data2:	
                        if '/season/' in url_:
                            self.addDir({'import':cItem['import'],'good_for_fav':True,'category':'host2', 'url':url_,'data_post':'', 'title':ph.clean_html(titre0_), 'desc':'', 'icon':cItem['icon'], 'mode':'31','EPG':True,'hst':'tshost'} )							
                        else:
                            params = {'import':cItem['import'],'good_for_fav':True,'category' : 'video','url': url_,'title':ph.clean_html(titre0_),'desc':'','icon':cItem['icon'],'hst':'tshost'} 
                            self.addVideo(params)				
            else:
                cat_data=re.findall('holder-block">.*?<h2(.*?)</h2>(.*?)</div>', data, re.S)		
                if cat_data:
                    for (titre_,data_) in cat_data:
                        self.addMarker({'title':tscolor('\c0000??00')+ph.clean_html('<'+titre_),'icon':cItem['icon'],'desc':''})	
                        cat_data2=re.findall('href="(.*?)".*?>(.*?)</a>', data_, re.S)	
                        for (url_,titre0_) in cat_data2:	
                            if '/season/' in url_:
                                self.addDir({'import':cItem['import'],'good_for_fav':True,'category':'host2', 'url':url_,'data_post':'', 'title':ph.clean_html(titre0_), 'desc':'', 'icon':cItem['icon'], 'mode':'31','EPG':True,'hst':'tshost'} )							
                            else:
                                params = {'import':cItem['import'],'good_for_fav':True,'category' : 'video','url': url_,'title':ph.clean_html(titre0_),'desc':'','icon':cItem['icon'],'hst':'tshost'} 
                                self.addVideo(params)				
                else:
                    params = {'import':cItem['import'],'good_for_fav':True,'category' : 'video','url': url0,'title':titre,'desc':'','icon':cItem['icon'],'desc':cItem['desc'],'hst':'tshost'} 
                    self.addVideo(params)						

    def SearchResult(self,str_ch,page,extra):
        HTTP_HEADER = {'User-Agent': self.USER_AGENT}
        defaultParams = {'header':HTTP_HEADER,'with_metadata':True }
        url_=self.MAIN_URL+'/search?s='+str_ch+'&page='+str(page)
        
        sts, data = self.getPage_(url_,defaultParams)
        if data:
            lst_data=re.findall('class="content-box">.*?href="(.*?)".*?src="(.*?)"(.*?)<h3>(.*?)</h3>', data, re.S)
            for (url1,image,desc0,name_eng) in lst_data:
                #name_eng=name_eng.replace(' اون لاين','')
                #name_eng=name_eng.replace('مسلسل ','')
                #name_eng=name_eng.replace('فيلم ','')
                desc1 =''
                lst_inf=re.findall('ti-eye">(.*?)</', desc0, re.S)
                if lst_inf: desc1 = desc1 + tscolor('\c00????00')+'Views: '+tscolor('\c00??????')+ph.clean_html(lst_inf[0])+'\n'
                lst_inf=re.findall('ti-star">(.*?)</', desc0, re.S)
                if lst_inf: desc1 = desc1 + tscolor('\c00????00')+'Rate: '+tscolor('\c00??????')+ph.clean_html(lst_inf[0])+'\n'				
                desc00,name_eng = self.uniform_titre(name_eng)
                if '://'in image: image = image.split('://')[0]+'://'+Quote(image.split('://')[1])
                else: image = cItem['image']
                desc=desc00+desc1
                self.addDir({'import':extra,'good_for_fav':True,'category':'host2', 'url':url1,'data_post':'', 'title':ph.clean_html(name_eng), 'desc':desc, 'icon':image, 'mode':'31','EPG':True,'hst':'tshost'} )							
    
    def SearchAll(self,str_ch,page=1,extra='',type_=''):
        elms = []
        HTTP_HEADER = {'User-Agent': self.USER_AGENT}
        defaultParams = {'header':HTTP_HEADER,'with_metadata':True }
        url_=self.MAIN_URL+'/search?s='+str_ch+'&page='+str(page)
        sts, data = self.getPage_(url_,defaultParams)
        if data:
            lst_data=re.findall('class="content-box">.*?href="(.*?)".*?src="(.*?)"(.*?)<h3>(.*?)</h3>', data, re.S)
            for (url1,image,desc0,name_eng) in lst_data:
                #name_eng=name_eng.replace(' اون لاين','')
                #name_eng=name_eng.replace('مسلسل ','')
                #name_eng=name_eng.replace('فيلم ','')
                desc1 =''
                lst_inf=re.findall('ti-eye">(.*?)</', desc0, re.S)
                if lst_inf: desc1 = desc1 + tscolor('\c00????00')+'Views: '+tscolor('\c00??????')+ph.clean_html(lst_inf[0])+'\n'
                lst_inf=re.findall('ti-star">(.*?)</', desc0, re.S)
                if lst_inf: desc1 = desc1 + tscolor('\c00????00')+'Rate: '+tscolor('\c00??????')+ph.clean_html(lst_inf[0])+'\n'				
                desc00,name_eng = self.uniform_titre(name_eng)
                if '://'in image: image = image.split('://')[0]+'://'+Quote(image.split('://')[1])
                else: image = cItem['image']
                desc=desc00+desc1
                elms.append({'import':extra,'good_for_fav':True,'category':'host2', 'url':url1,'data_post':'', 'title':ph.clean_html(name_eng), 'desc':desc, 'icon':image, 'mode':'31','EPG':True,'hst':'tshost'})
        if 'rel="next"' in data:
            elm = {'import':extra,'category' : 'host2','title':T('Next'),'url':'','desc':'next','icon':'','mode':'51','good_for_fav':True,'EPG':True,'hst':'tshost','page':page+1,'section':type_,'str_ch':str_ch}
            elms.append(elm)  
        return elms


    def get_links(self,cItem): 	
        urlTab = []	
        URL=cItem['url'].replace('/post/','/watch/').replace('/film/','/watch/').replace('/episode/','/watch/')	
        sts, data = self.getPage_(URL)
        if sts:
            server_id_data = re.findall('_post_id=(.*?)"', data, re.S)
            if server_id_data:
                server_id = server_id_data[0]
                server_data = re.findall('class="servers-tabs">(.*?)</ul>', data, re.S)
                if server_data:
                    server_data = re.findall('<li.*?data-embedd="(.*?)".*?>(.*?)</li>', server_data[0], re.S)
                    for (id,titre) in server_data:
                        url_ = self.MAIN_URL+'/ajaxCenter?_action=getserver&_post_id='+server_id+'&serverid='+id
                        local = ''
                        if 'سيرفر سيما' in titre:
                            titre = 'CimaClub'
                            local = 'local'
                        urlTab.append({'name':ph.clean_html(titre), 'url':'hst#tshost#'+url_+'|'+cItem['url'], 'need_resolve':1,'type':local})
        return urlTab
         
    def getVideos(self,videoUrl):
        urlTab = []	
        URL,referer=videoUrl.split('|')			
        sts, data = self.getPage(URL,self.defaultParams2)
        if sts:
            urlTab.append((data.strip(),'1'))
        return urlTab
                
    def getArticle(self, cItem):
        otherInfo1 = {}
        desc = cItem.get('desc','')
        sts, data = self.getPage_(cItem['url'])
        if sts:
            lst_dat=re.findall('class="half-tags">(.*?)</ul>', data, re.S)
            if lst_dat: 
                if ph.clean_html(lst_dat[0])!='':
                    desc = desc+tscolor('\c00????00')+'Category: '+tscolor('\c00??????')+ph.clean_html(lst_dat[0]).replace('بتصنيف','')+'\n'
            lst_dat=re.findall('class="media-p">(.*?)</div>', data, re.S)
            if lst_dat: 
                if ph.clean_html(lst_dat[0])!='':
                    desc = desc+tscolor('\c00????00')+'Story: '+tscolor('\c00??????')+ph.clean_html(lst_dat[0])					
                    
        icon = cItem.get('icon')
        title = cItem['title']		
        return [{'title':title, 'text': desc, 'images':[{'title':'', 'url':icon}], 'other_info':otherInfo1}]

    
    def start(self,cItem):      
        mode=cItem.get('mode', None)
        if mode=='00':
            self.showmenu0(cItem)
        if mode=='20':
            self.showmenu1(cItem)
        if mode=='21':
            self.showmenu2(cItem)			
        if mode=='30':
            self.showitms(cItem)			
        if mode=='31':
            self.showelems(cItem)
        if mode=='51':
            self.searchResult(cItem)	
        return True	
