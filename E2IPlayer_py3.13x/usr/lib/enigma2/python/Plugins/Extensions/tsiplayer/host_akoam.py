# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG,MergeDicts
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import GetIPTVSleep
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,gethostname,tscolor,tshost
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.urlparser    import urlparser as ts_urlparser
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.utils import Quote,Unquote  
  
import re
import time


###################################################
#01# HOST https://akoam.net
###################################################	
def getinfo():
    info_={}
    name = 'Akwam (Old)'
    hst = tshost(name)	
    if hst=='': hst = 'https://ak.sv/old/'
    info_['host']= hst
    info_['name']=name
    info_['version']='1.9.3 01/05/2025'
    info_['dev']='RGYSoft'
    info_['cat_id']='21'
    info_['desc']='أفلام, مسلسلات و انمي عربية و اجنبية'
    info_['icon']='https://i.ibb.co/pLWdJQn/akoam.png'
    info_['recherche_all']='1'
    #info_['update']='Fix Links Extract'
    return info_
    
    
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'rmdan.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        self.MAIN_URL = getinfo()['host']
        #self.COOKIE_FILE1 = '/media/hdd/IPTVCache/cookies/rmdan2.cookie'
        self.HEADER = {'User-Agent': self.USER_AGENT, 'DNT':'1', 'Accept': 'text/html', 'Accept-Encoding':'gzip, deflate','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
        self.AJAX_HEADER = MergeDicts(self.HEADER, {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'})
        self.defaultParams = {'header':self.HEADER,'with_metadata':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        #self.defaultParams1 = {'header':self.HEADER,'with_metadata':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE1}

        self.ts_urlpars = ts_urlparser()
 

    def getPage(self,baseUrl, addParams = {}, post_data = None):
        baseUrl = self.std_url(baseUrl)
        i=0
        while True:
            printDBG('counttttt'+str(i))
            if addParams == {}: addParams = dict(self.defaultParams)
            origBaseUrl = baseUrl
            baseUrl = self.cm.iriToUri(baseUrl)
            addParams['cloudflare_params'] = {'cookie_file':self.COOKIE_FILE, 'User-Agent':self.USER_AGENT}
            sts, data = self.cm.getPageCFProtection(baseUrl, addParams, post_data)
            printDBG(str(sts))
            if sts:
                if sts and 'class="loading"' in data:
                    GetIPTVSleep().Sleep(5)
                    continue
                break
            else:
                i=i+1
                if i>2: break
        return sts, data


 
    def showmenu0(self,cItem):

        self.addDir({'import':cItem['import'],'category' :'host2','title':'الأفلام'   ,'icon':cItem['icon'],'mode':'20','sub_mode':'0'})
        self.addDir({'import':cItem['import'],'category' :'host2','title':'المسلسلات','icon':cItem['icon'],'mode':'20','sub_mode':'1'})	
        self.addDir({'import':cItem['import'],'category' :'host2','title':'الأنمي'   ,'url':self.MAIN_URL+'/cat/83/%D8%A7%D9%84%D8%A7%D9%86%D9%85%D9%8A','icon':cItem['icon'],'mode':'21'})
        self.addDir({'import':cItem['import'],'category' :'host2','title':'آخر'     ,'icon':cItem['icon'],'mode':'20','sub_mode':'2'})	
        self.addDir({'import':cItem['import'],'category' :'search','title':tscolor('\c00????30') + _('Search'),'search_item':True,'page':1,'hst':'tshost','icon':cItem['icon']})

    def showmenu1(self,cItem):
        sub_mode=cItem.get('sub_mode', '0')
        sts, data = self.getPage(self.MAIN_URL)
        if sts:
            lst_data = re.findall('<ul class="partions"(.*?)</ul>',data, re.S)
            if  lst_data:
                lst_data1 = re.findall('data-title="(.*?)".*?href="(.*?)">(.*?)<',lst_data[0], re.S)
                for (desc,url,titre) in lst_data1:
                    if titre not in ['البرامج','الألعاب','الاجهزة اللوحية','اسلاميات و اناشيد','الكتب و الابحاث','الصور و الخلفيات','الانمي']:
                        if ((sub_mode=='0') and ('فلام' in titre)):
                            self.addDir({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'desc':'','icon':cItem['icon'],'mode':'21'})	
                        elif ((sub_mode=='1') and ('المسلسلات' in titre)):
                            self.addDir({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'desc':'','icon':cItem['icon'],'mode':'21'})				
                        elif ((sub_mode=='2') and ('المسلسلات' not in titre) and ('فلام' not in titre)):
                            self.addDir({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'desc':'','icon':cItem['icon'],'mode':'30'})				


    def showmenu2(self,cItem):
        sub_mode=cItem.get('sub_mode', '0')
        url0=cItem['url']	
        titre0=cItem['title']
        self.addDir({'import':cItem['import'],'category' : 'host2','title':' الكل - '+titre0,'url':url0,'desc':'','icon':cItem['icon'],'mode':'30'})
                            
        sts, data = self.getPage(url0)
        if sts:
            lst_data = re.findall('لأقسام الفرعية</span>(.*?)</ul>',data, re.S)
            if  lst_data:
                lst_data1 = re.findall('href="(.*?)">(.*?)<',lst_data[0], re.S)
                for (url,titre) in lst_data1:
                    self.addDir({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'desc':'','icon':cItem['icon'],'mode':'30'})

    def showitms(self,cItem):
        page = cItem.get('page', 1)
        url0=cItem['url']
        url1=url0+'/page/'+str(page)
        sts, data = self.getPage(url1)
        if sts:
            lst_data=re.findall('class="subject_box shape".*?href="(.*?)".*?src="(.*?)".*?<h3>(.*?)<.*?desc">(.*?)<', data, re.S)
            count=0			
            for (url1,image,name_eng,desc) in lst_data:
                if 'توضيح هام لمتابعي' not in name_eng:
                    name_eng=ph.clean_html(name_eng.strip())
                    desc0,name_eng = self.uniform_titre(name_eng)
                    if desc.strip()!='':
                        desc = tscolor('\c00????00')+'Info: '+tscolor('\c00??????')+desc
                    desc=desc0+desc
                    self.addDir({'import':cItem['import'],'category' : 'host2','title':name_eng,'url':url1.strip(),'desc':desc,'icon':image,'mode':'31','good_for_fav':True,'EPG':True,'hst':'tshost'})
                    printDBG('name='+ph.clean_html(name_eng.strip())+' url=#'+url1+'#')
                    count=count+1
            if count>38:	
                self.addDir({'import':cItem['import'],'category' : 'host2','title':'Page Suivante','url':cItem['url'],'page':page+1,'mode':'30'})

    def std_host_name(self,name_):
        if self.ts_urlpars.checkHostSupportbyname(name_):
            if '|' in name_:
                name_=name_.replace(name_.split('|')[-1],tscolor('\c0090??20')+name_.split('|')[-1].replace('embed.','').title())
            else:
                name_=tscolor('\c0090??20')+name_.replace('embed.','').title()
        elif self.ts_urlpars.checkHostNotSupportbyname(name_):
            if '|' in name_:
                name_=name_.replace(name_.split('|')[-1],tscolor('\c00??1020')+name_.split('|')[-1].replace('embed.','').title())
            else:
                name_=tscolor('\c00??5050')+name_.replace('embed.','').title()					
        return name_


    def showelms(self,cItem):
        hostMap = {'1477487990':'Vidtodo','1558278006':'Uqload','1423075862':'Dailymotion','1458117295':'Openload.co', '1477487601':'Estream.to', '1505328404':'Streamango', '1423080015':'Flashx.tv', '1430052371':'Ok.ru', '1477488213':'Thevid.tv'}
        url0=cItem['url']	
        desc=cItem['desc']
        try:	
            printDBG(' url2=#'+url0+'#')		
            sts, data = self.getPage(url0)
            if sts:
                trailer_data=re.findall('class="sub_trailer">.*?class="youtube-player.*?id="(.*?)"', data, re.S)
                if trailer_data:
                    self.addVideo({'category' : 'host2','title':'TRAILER','url':'https://www.youtube.com/watch?v='+trailer_data[0],'desc':'','icon':cItem['icon'],'hst':'none'})	
                if ('الانتقال إلي التصميم الجديد' in data) or ('على التصميم الجديد' in data):
                    lst_data=re.findall('sub_extra_desc">.*?href="(.*?)"', data, re.S)
                    if not lst_data: lst_data=re.findall('class="sub_desc">.*?href="(.*?)"', data, re.S)
                    if lst_data:
                        Url=lst_data[0]
                        import_ = 'from Plugins.Extensions.IPTVPlayer.tsiplayer.host_akwam import '
                        titre = tscolor('\c0000??00')+ '[New Site] '+tscolor('\c00??????')+cItem['title']
                        self.addDir({'import':import_,'category' : 'host2','title': titre ,'url':Url ,'desc':cItem['desc'],'icon':cItem['icon'],'hst':'tshost','mode':'31'})
                            
                elif 'sub_episode_links">' in data:
                    lst_data=re.findall('_episode_links">(.*?)title">(.*?)<.*?(?:<h5>|sub-no-file)(.*?)<div class="sub', data, re.S)			
                    for (inf,titre1,data1) in lst_data:
                        img_data=re.findall('src="(.*?)"', inf, re.S)
                        img_ = cItem['icon']
                        if img_data: img_ = img_data[0]
                        
                        self.addMarker({'title':tscolor('\c0000????')+titre1.strip(),'icon':img_})
                        if 'box epsoide_box\'>' in data1:
                            dat_1,dat_2=data1.split('box epsoide_box\'>',1)
                        else:
                            dat_1=data1
                            dat_2=''
                        lst_dat=re.findall('href=[\'"](.*?)[\'"]', dat_1, re.S)					
                        if lst_dat:
                            self.addVideo({'import':cItem['import'],'category' : 'host2','title':tscolor('\c0060??60')+'Akoam','url':lst_dat[0],'desc':desc,'icon':img_,'hst':'tshost','good_for_fav':True,'url0':url0})				
                        lst_dat=re.findall('/files/(.*?)\..*?href=[\'"](.*?)[\'"]', dat_2, re.S)					
                        if lst_dat:
                            for (hst1,urll) in lst_dat:
                                titre='رابط مشاهدة'
                                if hst1 in hostMap: titre=hostMap[hst1]
                                self.addVideo({'import':cItem['import'],'category' : 'host2','title':self.std_host_name(titre),'url':urll,'desc':desc,'icon':img_,'hst':'tshost','good_for_fav':True,'url0':url0})	
                        
                else:
                    lst_data=re.findall('\'sub_direct_links\'>(.*?)clear">', data, re.S)
                    if lst_data:
                        for (data1) in lst_data:
                            if 'sub_direct_links\'>' in data1:
                                dat_1,dat_2=data1.split('sub_direct_links\'>')
                            else:
                                dat_1,dat_2=data1,''
                            lst_dat=re.findall('href=[\'"](.*?)[\'"]', dat_1, re.S)					
                            if lst_dat:
                                self.addMarker({'title':tscolor('\c0000????')+'تحميل و المشاهدة الخاص ','icon':cItem['icon']})
                                self.addVideo({'import':cItem['import'],'category' : 'host2','title':tscolor('\c0060??60')+'Akoam','url':lst_dat[0],'desc':desc,'icon':cItem['icon'],'hst':'tshost','good_for_fav':True,'url0':url0})	
                                
                            lst_dat=re.findall('/files/(.*?)\..*?href=[\'"](.*?)[\'"]', dat_2, re.S)					
                            if lst_dat:
                                self.addMarker({'title':tscolor('\c0000????')+' روابط المشاهدة','icon':cItem['icon']})
                                for (hst1,urll) in lst_dat:
                                    titre='رابط مشاهدة'
                                    if hst1 in hostMap: titre=hostMap[hst1]
                                    self.addVideo({'import':cItem['import'],'category' : 'host2','title':self.std_host_name(titre),'url':urll,'desc':desc,'icon':cItem['icon'],'hst':'tshost','good_for_fav':True,'url0':url0})	
            #self.addVideo({'import':cItem['import'],'category' : 'host2','title':'Test Akoem link sans ads','url':'https://ak.sv/old/download/bccb31112557/It-Must-Be-Heaven-2019-720P-WEB-DL-akoam-net-mkv','desc':'','icon':cItem['icon'],'hst':'tshost','good_for_fav':True,'url0':url0})	
        except:
            self.addMarker({'title':tscolor('\c00??0000')+' ليس هناك سرفرات مشاهدة','icon':cItem['icon']})

    def SearchResult(self,str_ch,page,extra):
        url_=self.MAIN_URL+'/search/'+str_ch+'/page/'+str(page)
        sts, data = self.getPage(url_)
        if sts:
            lst_data=re.findall('<div class="tags_box">.*?href="(.*?)".*?url\((.*?)\).*?<h1>(.*?)<', data, re.S)			
            for (url1,image,name_eng) in lst_data:
                name_eng=ph.clean_html(name_eng.strip())
                desc0,name_eng = self.uniform_titre(name_eng)
                self.addDir({'import':extra,'category' : 'host2','title':name_eng,'url':url1,'desc':desc0,'icon':image,'mode':'31','good_for_fav':True,'EPG':True,'hst':'tshost'})

    def MediaBoxResult(self,str_ch,year_,extra):
        urltab=[]
        str_ch = str_ch+' '+year_
        str_ch = Quote(str_ch)
        url_=self.MAIN_URL+'/search/'+str_ch+'/page/1'
        sts, data = self.getPage(url_)
        if sts:
            lst_data=re.findall('<div class="tags_box">.*?href="(.*?)".*?url\((.*?)\).*?<h1>(.*?)<', data, re.S)			
            for (url1,image,name_eng) in lst_data:
                name_eng=ph.clean_html(name_eng.strip())
                desc0,titre0 = self.uniform_titre(name_eng,1)
                if ' 3D' not in name_eng:
                    name_eng='|'+tscolor('\c0060??60')+'Akwam (OLD)'+tscolor('\c00??????')+'| '+titre0
                    urltab.append({'titre':titre0,'import':extra,'category' : 'host2','title':name_eng,'url':url1,'desc':desc0,'icon':image,'mode':'31','good_for_fav':True,'EPG':True,'hst':'tshost'})
        return urltab



    def get_links(self,cItem): 	
        urlTab = []
        URL=cItem['url']
        URL = URL.replace('download','watching')
        printDBG('url='+URL)
        self.cm.clearCookie(self.COOKIE_FILE, removeNames=['golink'])
        sts, data = self.getPage(URL)
        if sts:
            try:
                cookies_ = self.cm.getCookieItems(self.COOKIE_FILE)
                printDBG('cookies_='+str(cookies_))
                if 'golink' in cookies_:        
                    link_from_cookie = json_loads(Unquote(cookies_['golink']))['route'].replace('download','watching')
                    printDBG('link_from_cookie='+link_from_cookie)
                    paramsUrl = dict(self.defaultParams)
                    paramsUrl['header']['Referer'] = cItem['url']
                    sts, data = self.getPage(link_from_cookie,paramsUrl)
            except:
                printDBG('except01')
            url_dat=re.findall('<iframe[^>]+?src=[\'"]([^"^\']+?)[\'"]', data, re.S | re.IGNORECASE)
            if not url_dat:
                lst_dat=re.findall('file:.{,3}?"(.*?)"', data, re.S)	
                if lst_dat:
                    urlTab.append({'name':'direct_link', 'url':lst_dat[0]})
            else:
                urL_=url_dat[0]
                if 'mellowads' not in urL_:
                    printDBG('11')
                    if urL_.startswith('//'):
                        urL_='http:'+urL_
                    if not urL_.startswith('http'):
                        urL_='http://'+urL_	
                    urlTab.append({'name':'link', 'url':urL_, 'need_resolve':1})						
                    
            if len(urlTab) == 0:
                paramsUrl = dict(self.defaultParams)
                URL = URL.replace('watching','download')
                paramsUrl['header']['Referer'] = URL
                paramsUrl['header']['X-Requested-With'] = 'XMLHttpRequest'
                sts, data = self.getPage(URL,paramsUrl,post_data={})
                if sts:
                    url_dat0=re.findall('direct_link":"(.*?)"', data, re.S | re.IGNORECASE)
                    if url_dat0:
                        urlTab.append({'name':'direct_link', 'url':url_dat0[0].replace('\\','')}) 
        return urlTab
        
     

    def getArticle(self,cItem):
        printDBG("AkoAm.getVideoLinks [%s]" % cItem) 
        otherInfo1 = {}
        title = cItem['title']
        icon = cItem.get('icon','')
        desc = cItem.get('desc','')
        sts, data = self.getPage(cItem['url'])
        if sts:
            lst_dat=re.findall("'sub_mainInfo'>(.*?)</di", data, re.S)
            lst_dat0=re.findall("<li>(.*?)<i>(.*?)</i>.*?</li", lst_dat[0], re.S)
            for (x1,x2) in lst_dat0:
                if 'المدة الزمنية' in x1: otherInfo1['duration'] = x2
                if 'سنة الانتاج' in x1: otherInfo1['year'] = x2
                if 'اللغة' in x1: otherInfo1['language'] = x2			
                if 'جودة الصورة' in x1: otherInfo1['quality'] = x2	
                if 'الترجمة' in x1: otherInfo1['translation'] = x2
                if 'المصدر' in x1: otherInfo1['station'] = x2
                if 'نوع الملف' in x1: otherInfo1['type'] = x2
                if 'محتوى الفيلم' in x1: otherInfo1['category'] = x2
                
            lst_dat0=re.findall('imdb">.*?<span>(.*?)</', lst_dat[0], re.S)
            if lst_dat0: otherInfo1['imdb_rating'] = lst_dat0[0].replace('\n','')
            
            lst_dat=re.findall('"sub_desc">(.*?)</div>', data, re.S)
            lst_dat0=re.findall("<span.*?>(.*?)</span>(.*?)(<br />.<br />|RRR)", lst_dat[0]+'RRR', re.S)
            for (x1,x2,x3) in lst_dat0:		
                if 'بطولة' in x1: otherInfo1['actors'] = ph.clean_html(x2)
                if 'ﺇﺧﺮاﺝ' in x1: otherInfo1['director'] = ph.clean_html(x2)	
                if 'ﺗﺄﻟﻴﻒ' in x1: otherInfo1['writers'] = ph.clean_html(x2)	
                if 'تصنيف' in x1: otherInfo1['genre'] = ph.clean_html(x2)
                
            if lst_dat0: desc = ph.clean_html(lst_dat0[0][1])
            else: desc = cItem['desc']

            lst_dat0=re.findall('main_img".*?src="(.*?)"', lst_dat[0], re.S)
            if lst_dat0: icon = lst_dat0[0]
            else: icon = cItem.get('icon')
        
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
            self.showelms(cItem)				
        return True

