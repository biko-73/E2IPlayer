# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,T
from Components.config import config
import base64,urllib
import re

def getinfo():
    info_={}
    name = 'Faselhd.Co'
    hst = 'https://www.faselhds.care'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='2.0 18/07/2022'        
    info_['dev']='RGYSoft'
    info_['cat_id']='21'
    info_['desc']='أفلام و مسلسلات اسياوية و اجنبية'
    info_['icon']='https://i.ibb.co/XDQ5v3G/facel.png'
    info_['recherche_all']='1'
    #info_['update']='Add Local M3u8 and T7meel servers '	
    return info_
    
    
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'faselhd.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        self.MAIN_URL = getinfo()['host']
        self.HEADER = {'User-Agent': self.USER_AGENT, 'Connection': 'keep-alive', 'Accept-Encoding':'gzip', 'Content-Type':'application/x-www-form-urlencoded','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
        self.defaultParams = {'header':self.HEADER,'with_metadata':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        self.defaultParams0 = {'header':self.HEADER,'no_redirection':True,'with_metadata':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        
        #self.getPage = self.cm.getPage
         
    def showmenu0(self,cItem):		
        Fasel_TAB=[ {'category':'host2' ,'mode':'30' ,'url':self.MAIN_URL+'/most_recent','title': 'الأحدث'},			
                    {'category':'host2' ,'mode':'20'               ,'title': 'الأفلام' },
                    {'category':'host2' ,'mode':'20' ,'sub_mode':1 ,'title': 'المسلسلات' },
                    {'category':'host2' ,'mode':'20' ,'sub_mode':2 ,'title': 'البرامج التلفزيونية' },	
                    {'category':'host2' ,'mode':'20' ,'sub_mode':3 ,'title': 'القسم الاسيوي' },						
                    {'category':'host2' ,'mode':'20' ,'sub_mode':4 ,'title': 'الأنمي' },	
                    #{'category':'host2' ,'mode':'19' ,'title': tscolor('\c00????00')+'Filter' },	   
                    {'category':'host2', 'title': tscolor('\c0000????') + 'حسب التصنيف' , 'mode':'19','count':1,'data':'none','code':''},	                    
                    #{'category':'search'  ,'title': _('Search'),'search_item':True,'page':1,'hst':'tshost'},
                    ]
        self.listsTab(Fasel_TAB, {'import':cItem['import'],'name':'host2','icon':cItem['icon']})
        self.addDir({'import':cItem['import'],'category' :'host2','title':T('Search')  ,'icon':'https://i.ibb.co/dQg0hSG/search.png','mode':'50'})	
			
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

    def get_items(self,cItem={}):
        elms    = []
        extra   = cItem.get('import')
        str_ch   = cItem.get('str_ch')
        page    = cItem.get('page', 1)
        url_    = cItem.get('url', '')
        type_   = cItem.get('type_', '')      
        if url_ == '':
            with_type = True
            if (page>1):
                url0 = self.MAIN_URL+'/page/'+str(page)
            else:
                url0 = self.MAIN_URL+'/'
            url0 = url0 + '?s=' + str_ch
            if type_ != '':
                url0 = url0 +' '+type_
        else:
            with_type = False
            url0 = url_
            if (page>1):
                url0=url0+'/page/'+str(page)
        sts, data = self.getPage(url0)
        if sts:
            lst_data0=re.findall('postDiv.{0,2}">.*?href="(.*?)".*?-src="(.*?)"(.*?)h1">(.*?)<', data, re.S)
            for (url,image,desc,titre) in lst_data0:
                desc  = self.extract_desc(desc,[('quality','quality">(.*?)</span>'),('category','class="cat">(.*?)<span class')])
                info  = self.std_title(titre,desc=desc,with_type=with_type)
                desc  = info.get('desc')                    
                titre = info.get('title_display')
                image = self.std_url(image) 
                elms.append({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'desc':desc,'icon':image,'mode':'31','good_for_fav':True,'sub_mode':'1','EPG':True,'hst':'tshost','info':info})		
        films_list = re.findall('>&rsaquo;</a>', data, re.S)	
        if films_list:
            if '?s=' in url0:
                mode = '51'
            else: mode = '30'
            elms.append({'import':extra,'category' : 'host2','title':T('Next'),'url':url_,'desc':'Next','icon':'','hst':'tshost','mode':mode,'page':page+1,'str_ch':str_ch,'type_':type_})
        return elms


    def getPage0(self, baseUrl, addParams = {}, post_data = None):
        baseUrl=self.std_url(baseUrl)
        if addParams == {}: addParams = dict(self.defaultParams0)
        sts,data = self.cm.getPage(baseUrl, addParams, post_data)
        printDBG(str(data.meta))
        code = data.meta.get('status_code','')  
        while ((code == 302) or (code == 301)):
            new_url = data.meta.get('location','')
            if not new_url.startswith('http'):
                new_url = self.MAIN_URL + new_url
            new_url=self.std_url(new_url)
            sts,data = self.cm.getPage(new_url, addParams, post_data)
            code = data.meta.get('status_code','')
            printDBG(str(data.meta))
        return sts, data


    def showmenu1(self,cItem):
        gnr=cItem.get('sub_mode',0)
        sts, data = self.getPage0(self.MAIN_URL)
        if sts:
            lst_data = re.findall('role="menu">(.*?)</div',data, re.S)
            if lst_data:
                data = lst_data[gnr]
                lst_data = re.findall('href="(.*?)".*?>(.*?)<',data, re.S)
                for (url,titre) in lst_data:
                    if ('/oscars-winners' not in url) and ('/movies_coming_soon' not in url) and ('/reviews' not in url):
                        self.addDir({'import':cItem['import'],'category' :'host2', 'url':url, 'title':titre, 'desc':'', 'icon':cItem['icon'], 'mode':'30'})

    def showfilter(self,cItem):
        count=cItem['count']
        data1=cItem['data']	
        codeold=cItem['code']	
        if count==1:
            sts, data = self.getPage(self.MAIN_URL+'/all-movies')
            if sts:
                data1=re.findall('<select name="(.*?)".*?>(.*?)</div>', data, re.S)
            else:
                data1=None
        if count==5:
            mode_='30'
        else:
            mode_='19'
        if data1:
            #self.addMarker({'title': tscolor('\c00????30') + ph.clean_html(data1[count-1][1][0][1]),'icon':cItem['icon']})
            lst_data1 = re.findall('<option value="(.*?)".*?>(.*?)<',data1[count-1][1], re.S)	
            
            nb= 1
            for (x1,x2) in lst_data1:
                #if  ((('–' not in x2) and ('-' not in x2)) or('Sci-Fi' in x2))and ('null' not in x2)and ('كريستينا' not in x2):
                #if not((x1 == 'category') and (x2.strip()=='')):
                titre_ = ph.clean_html(x2)
                if nb==1:
                    self.addMarker({'title': tscolor('\c00????30') + ph.clean_html(x2),'icon':cItem['icon']})
                    titre_= 'الكل'
                code=codeold+data1[count-1][0]+'='+x1.strip()+'&'
                self.addDir({'import':cItem['import'],'category' :'host2', 'url':code, 'title':titre_, 'desc':code, 'icon':cItem['icon'], 'mode':mode_,'count':count+1,'data':data1,'code':code, 'sub_mode':'item_filter'})					
                nb=nb+1
    def showitms(self,cItem):
        printDBG('showitms='+cItem['url'])
        page=cItem.get('page',1)
        desc = [('Quality','quality">(.*?)</span>','',''),('Category','class="cat">(.*?)<span class','','')]            
        next = ['rel="next".*?href="(.*?)"','20']        
        if (cItem['url'].startswith('http') or cItem['url'].startswith('/')):        
            self.add_menu(cItem,'','"postDiv.*?href="(.*?)".*?-src="(.*?)"(.*?)h1">(.*?)<','',[('','31',''),('/collections/','30','URL')],ord=[0,3,1,2],Next=[1,'30'],u_titre=True,EPG=True,Desc=desc)		
        else:
            LINK = self.MAIN_URL+'/wp-admin/admin-ajax.php'          
            post_data ={}
            if '&' in cItem['url']:
                prams = cItem['url'].split('&')
            else:
                prams = cItem['url']
            for param in prams:
                if '=' in param:
                    pram_x1,param_x2 = param.split('=')
                    post_data[pram_x1]=param_x2
            post_data['action']='fillter_all_movies'
            post_data['pagenum']=page+1
            self.add_menu(cItem,'','postDiv.{0,2}">.*?href="(.*?)".*?src="(.*?)"(.*?)h1">(.*?)<','','31',LINK = LINK,post_data=post_data,ord=[0,3,1,2],u_titre=True,EPG=True,Desc=desc)		
            self.addDir({'import':cItem['import'],'category':'host2', 'url':cItem['url'], 'title':tscolor('\c0000??00')+'Page Suivante', 'page':page+1, 'desc':'Page Suivante', 'icon':cItem['icon'], 'mode':'30'})					
        
    def showelms(self,cItem):
        url=cItem['url']
        printDBG('showelms='+url)
        if not url.startswith('http'): 
            post_data = {'seasonID':url}
            url = self.MAIN_URL+'/series-ajax/?_action=get_season_list&_post_id='+url
            sts, data = self.getPage(url,self.defaultParams,post_data = post_data)
            if (sts) and (data==''):
                url = self.MAIN_URL+'/series-ajax/?_action=get_asian_season_list&_post_id='+url
                sts, data = self.getPage(url,self.defaultParams,post_data = post_data)                
            printDBG('data_meta='+str(data.meta))
            printDBG('data='+data)
        else:
            sts, data = self.getPage(url)
        if sts:
            lst_data=re.findall('class="posterImg">.{0,20}href="(.*?)"', data, re.S)			
            if lst_data: self.addVideo({'import':cItem['import'],'good_for_fav':True,'name':'categories','category' : 'video','url': lst_data[0],'title':'Trailer','desc':'','icon':cItem['icon'],'hst':'none'})						

            lst_data=re.findall('class="seasonDiv.*?href="(.*?)".*?-src="(.*?)"(.*?)title">(.*?)<', data, re.S)			
            if lst_data:
                for (url1,image,desc,titre) in lst_data:
                    self.addDir({'import':cItem['import'],'good_for_fav':True,'EPG':True, 'hst':'tshost', 'category':'host2', 'url':url1, 'title':titre, 'desc':'', 'icon':image, 'mode':'31'} )	
            else:
                lst_data=re.findall('class="epAll"(.*?)</div', data, re.S)	
                if lst_data:
                    lst_data = re.findall('href="(.*?)".*?>(.*?)<',lst_data[0], re.S)
                    for (url1,titre) in lst_data:
                        self.addVideo({'import':cItem['import'], 'hst':'tshost', 'url':url1, 'title':titre.strip(), 'desc':cItem['desc'], 'icon':cItem['icon']})
                else:
                    self.addVideo({'import':cItem['import'], 'hst':'tshost', 'url':cItem['url'], 'title':cItem['title'], 'desc':cItem['desc'], 'icon':cItem['icon']})
        
    def SearchResult(self,str_ch,page,extra):   
        url = self.MAIN_URL+'/page/'+str(page)+'?s='+str_ch
        desc = [('Quality','quality">(.*?)</span>','',''),('Category','class="cat">(.*?)<span class','','')]            		 
        self.add_menu({'import':extra,'url':url},'','postDiv.{0,2}">.*?href="(.*?)".*?-src="(.*?)"(.*?)h1">(.*?)<','','31',ord=[0,3,1,2],u_titre=True,EPG=True,Desc=desc)		

        
    def MediaBoxResult(self,str_ch,year_,extra):
        urltab=[]
        str_ch_o = str_ch
        str_ch = urllib.quote(str_ch_o+' '+year_)
        result = self.SearchResult(str_ch,1,'')
        for elm in result:
            titre     = elm['title']
            url       = elm['url']
            desc      = elm.get('desc','')
            image     = elm.get('icon','')
            mode      = elm.get('mode','') 
            if str_ch_o.lower().replace(' ','') == titre.replace('-',' ').replace(':',' ').lower().replace(' ',''):
                trouver = True
            else:
                trouver = False
            name_eng='|'+tscolor('\c0060??60')+'FaselHD'+tscolor('\c00??????')+'| '+titre				
            element = {'titre':titre,'import':extra,'good_for_fav':True,'EPG':True, 'hst':'tshost', 'category':'host2', 'url':url, 'title':name_eng, 'desc':desc, 'icon':image, 'mode':mode}
            if trouver:
                urltab.insert(0, element)					
            else:
                urltab.append(element)	
        return urltab	        
        
 
        
    def get_links(self,cItem): 	
        urlTab = []	
        URL=cItem['url']
        sts, data = self.getPage(URL)
        if sts:
            Liste_els = re.findall('class="signleWatch(.*?)div', data, re.S)
            if Liste_els:
                Liste_els = re.findall('<li.*?href.*?["\'](.*?)["\'].*?>(.*?)</li', Liste_els[0], re.S)
                for (url,titre) in Liste_els:
                    titre = self.cleanHtmlStr(titre)
                    local = ''
                    if ('سيرفر #01' in titre) or ('سيرفر الجودة الأصلية' in titre):
                        titre = '|Server 01| FaselHD'
                        local = 'local'
                    elif 'سيرفر #07' in titre: titre = '|Server 07| Vidfast.Co'	
                    elif 'سيرفر المشاهدة #01' in titre: titre = '|Server 01| FaselHd'
                    elif 'سيرفر المشاهدة #02' in titre: titre = '|Server 02| FaselHd'
                    if 'moshahda.online' in url:
                        urlTab.append({'name':'|Local| Moshahda', 'url':url, 'need_resolve':1,'type':'local'})	
                    else:
                        if url.startswith('http'):
                            urlTab.append({'name':titre, 'url':'hst#tshost#'+url, 'need_resolve':1,'type':local})	
            Liste_els = re.findall('downloadLinks.*?href="(.*?)"', data, re.S)
            if Liste_els:   
                urlTab.append({'name':'|Download| Ta7meel', 'url':Liste_els[0], 'need_resolve':1,'type':'local'})	    
        return urlTab
         
    def getVideos(self,videoUrl):
        urlTab = []
        addParams = dict(self.defaultParams)
        addParams['header']['Referer'] = self.MAIN_URL
        sts, data = self.cm.getPage(videoUrl,addParams)
        if sts:			
            if 'adilbo_HTML_encoder' in data:
                printDBG('ttttttttttttttttttttttttttt'+data)
                t_script = re.findall('<script.*?;.*?\'(.*?);', data, re.S)	
                t_int = re.findall('/g.....(.*?)\)', data, re.S)	
                if t_script and t_int:
                    script = t_script[0].replace("'",'')
                    script = script.replace("+",'')
                    script = script.replace("\n",'')
                    sc = script.split('.')
                    page = ''
                    for elm in sc:
                        #printDBG('decode'+elm)
                        c_elm = base64.b64decode(elm+'==').decode("utf-8")
                        t_ch = re.findall('\d+', c_elm, re.S)
                        if t_ch:
                            nb = int(t_ch[0])+int(t_int[0])
                            page = page + chr(nb)
                    t_url = re.findall('file":"(.*?)"', page, re.S)	
                    if t_url:	
                        urlTab.append((t_url[0].replace('\\',''),'3'))
            else:
                Liste_els_3 = re.findall('<iframe.*?src="(.*?)"', data, re.S)	
                if Liste_els_3:
                    urlTab.append((Liste_els_3[0],'1'))
                else:
                    Liste_els_3 = re.findall('file: "(.*?)"', data, re.S)	
                    if Liste_els_3:			
                        meta = {'iptv_proto':'m3u8','Referer':videoUrl}
                        url_=strwithmeta(Liste_els_3[0], meta)
                        urlTab.append((url_,'3'))
                    else:
                        Liste_els_3 = re.findall('file":"(.*?)"', data, re.S)	
                        if Liste_els_3:			
                            meta = {'iptv_proto':'m3u8','Referer':videoUrl}
                            url_=strwithmeta(Liste_els_3[0].replace('\\',''), meta)
                            urlTab.append((url_,'3'))
        return urlTab
        
    def getArticle(self, cItem):
        printDBG("FaselhdCOM.getArticleContent [%s]" % cItem)
        retTab = []
        otherInfo = {}
        title = ''
        desc = ''
        icon = ''
        sts, data = self.cm.getPage(cItem['url'])
        if sts:
            url = self.cm.ph.getDataBeetwenNodes(data, ('<meta', '>', 'refresh'), ('<', '>'))[1]
            url = self.getFullUrl(self.cm.ph.getSearchGroups(url, '''url=['"]([^'^"]+?)['"]''', 1, True)[0])

            if self.cm.isValidUrl(url):
                sts, tmp = self.getPage(url)
                if sts: data = tmp

            data = self.cm.ph.getDataBeetwenNodes(data, ('<header', '>'), ('<style', '>'))[1]
            #desc = self.cleanHtmlStr(self.cm.ph.getDataBeetwenMarkers(data, '<p', '</p>')[1])
            Liste_els_3 = re.findall('singleDesc">(.*?)</div>', data, re.S)	
            if Liste_els_3:	desc = self.cleanHtmlStr(Liste_els_3[0])		
            title = self.cleanHtmlStr(self.cm.ph.getDataBeetwenMarkers(data, '<h1', '</h1>')[1])
            icon  = self.getFullIconUrl(self.cm.ph.getSearchGroups(data, '''\ssrc=['"]([^'^"]+?)['"]''')[0])

            keysMap = {'دولة المسلسل':   'country',
                       'حالة المسلسل':   'status',
                       'اللغة':          'language',
                       'توقيت الحلقات':  'duration',
                       'الموسم':         'seasons',
                       'الحلقات':        'episodes',

                       'تصنيف الفيلم':   'genres',
                       'مستوى المشاهدة': 'age_limit',
                       'سنة الإنتاج':     'year',
                       'مدة الفيلم':     'duration',
                       'تقييم IMDB':     'imdb_rating',
                       'بطولة':          'actors',
                       'جودة الفيلم':    'quality'}
            data = self.cm.ph.getAllItemsBeetwenNodes(data, ('<i', '>', 'fa-'), ('</span', '>'))
            for item in data:
                tmp = self.cleanHtmlStr(item).split(':')
                marker = tmp[0].strip()
                value  = tmp[-1].strip().replace(' , ', ', ')
                
                printDBG(">>>>>>>>>>>>>>>>>> marker[%s] -> value[%s]" % (marker, value))
                
                #marker = self.cm.ph.getSearchGroups(item, '''(\sfa\-[^'^"]+?)['"]''')[0].split('fa-')[-1]
                #printDBG(">>>>>>>>>>>>>>>>>> " + marker)
                if marker not in keysMap: continue
                if value == '': continue
                otherInfo[keysMap[marker]] = value

        if title == '': title = cItem['title']
        if desc == '':  desc = cItem.get('desc', '')
        if icon == '':  icon = cItem.get('icon', self.DEFAULT_ICON_URL)

        return [{'title':self.cleanHtmlStr( title ), 'text': self.cleanHtmlStr( desc ), 'images':[{'title':'', 'url':self.getFullUrl(icon)}], 'other_info':otherInfo}]

    
    def start(self,cItem):      
        mode=cItem.get('mode', None)
        if mode=='00':
            self.showmenu0(cItem)
        if mode=='20':
            self.showmenu1(cItem)
        if mode=='19':
            self.showfilter(cItem)            
        if mode=='30':
            self.showitms(cItem)			
        if mode=='31':
            self.showelms(cItem)
        if mode=='32':
            self.showitms3(cItem)
        elif mode=='50':
            self.showsearch(cItem)
            name= 'showsearch'   
        elif mode=='51':
            self.searchResult(cItem)
            name= 'searchResult'     
