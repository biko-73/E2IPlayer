# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,gethostname,T
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Components.config import config
import re
import base64
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.utils import Quote
from Plugins.Extensions.IPTVPlayer.components.e2ivkselector import GetVirtualKeyboard
from Plugins.Extensions.IPTVPlayer.p2p3.pVer import isPY2
def getinfo():
    info_={}
    name='ArabScieNces'
    hst = 'https://arabsciences.com/'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='1.0 8/07/2023'        
    info_['dev']='AbouYacine'
    info_['cat_id']='21'
    info_['desc']='افلام وثائقية'
    info_['icon']='https://i0.wp.com/arabsciences.com/wp-content/uploads/2016/01/logo_arabsciences512.png'
    info_['recherche_all']='0'
    return info_
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'arabsciences.cookie'})
        self.MAIN_URL = getinfo()['host']

    def showmenu(self,cItem):          
        self.addDir({'import':cItem['import'],'category' :'host2', 'title':'الصنف الاول', 'desc':'', 'icon':getinfo()['icon'], 'mode':'40'})					
        self.addDir({'import':cItem['import'],'category' :'host2', 'title':' الصنف الثاني ', 'desc':'', 'icon':getinfo()['icon'], 'mode':'41'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'title':'الصنف الثالث', 'desc':'', 'icon':getinfo()['icon'], 'mode':'42'})
		
    def showmenu16(self,cItem):#2
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/cultures/', 'title':'ثقافات', 'desc':'', 'icon':'', 'mode':'20'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/countries/', 'title':'البلدان', 'desc':'', 'icon':'', 'mode':'20'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/islam/', 'title':'الإسلام', 'desc':'', 'icon':'', 'mode':'20'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/nature/', 'title':'الطبيعة', 'desc':'', 'icon':'', 'mode':'20'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/politics/', 'title':'سياسة', 'desc':'', 'icon':'', 'mode':'20'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/engineering/', 'title':'هندسة', 'desc':'', 'icon':'', 'mode':'20'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/catastrophe/', 'title':'كوارث', 'desc':'', 'icon':'', 'mode':'20'})

    def showmenu17(self,cItem):#3
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/tv-channels/natgeoad/', 'title':'ناشونال جيوغرافيك ابو ظبي', 'desc':'', 'icon':'', 'mode':'20'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/tv-channels/dw-arabic/', 'title':'DW (عربية)', 'desc':'', 'icon':'', 'mode':'20'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/tv-channels/jazeeradoc-tv-channels/', 'title':'الجزيرة الوثائقية', 'desc':'', 'icon':'', 'mode':'20'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/tv-channels/alarabyatv/', 'title':'قناة العربية', 'desc':'', 'icon':'', 'mode':'20'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/tv-channels/bbc-arabic/', 'title':'BBC Arabic', 'desc':'', 'icon':'', 'mode':'20'})

    def showmenu18(self,cItem):#1
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/animals-categories/', 'title':'الحيوانات و الحياة البريّة', 'desc':'', 'icon':'', 'mode':'20'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/history/', 'title':'تاريخ', 'desc':'', 'icon':'', 'mode':'20'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/space/', 'title':'الفضاء', 'desc':'', 'icon':'', 'mode':'20'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/technology/', 'title':'علوم وتكنولوجيا', 'desc':'', 'icon':'', 'mode':'20'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/mystery/', 'title':'غموض و ألغاز', 'desc':'', 'icon':'', 'mode':'20'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/adventure/', 'title':'مغامرات', 'desc':'', 'icon':'', 'mode':'20'})
        self.addDir({'import':cItem['import'],'category' :'host2', 'url':self.MAIN_URL+'/category/weapons-fight/', 'title':'أسلحة و فنون قتال', 'desc':'', 'icon':'', 'mode':'20'})
    
    def showsearch(self,cItem):
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن فيلم','icon':'https://i.ibb.co/RSgNt5N/cimanow-aflam.png','mode':'51','section':'فيلم'})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن مسلسل','icon':'https://i.ibb.co/QrB4PQ3/cimanow-mousalsalat.png','mode':'51','section':'مسلسل'})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث في الموقع','icon':'https://i.ibb.co/9wyG5xk/cimanow-search.png','mode':'51','section':''})
    
    def getTag(self,url):
        printDBG('getTaggetTaggetTaggetTaggetTaggetTaggetTaggetTaggetTaggetTaggetTag')
        if 'الافلام-' in url: tag = 'MOVIE'
        elif 'مسلسلات-انيميشن' in url: tag = 'ANIM'        
        elif 'مسلسلات' in url: tag = 'TVSHOW'
        else: tag = 'MOVIE'
        return tag
    
    def get_data_films(self,data):
        printDBG('get_data_filmsget_data_filmsget_data_filmsget_data_filmsget_data_filmsget_data_films')
        
        data = data.encode('latin-1').decode('utf-8')
        if 'adilbo' in data:
            t_script = re.findall('<script.*?;.*?\'(.*?);', data, re.S)
            t_int = re.findall('/g.....(.*?)\)', data, re.S)
            if t_script and t_int:
                script = t_script[0].replace("'",'')
                script = script.replace("+",'')
                script = script.replace("\n",'')
                sc = script.split('.')
                page = ''
                for elm in sc:
                    c_elm = base64.b64decode(elm+'==').decode()
                    t_ch = re.findall('\d+', c_elm, re.S)
                    if t_ch:
                        nb = int(t_ch[0])+int(t_int[0])
                        page = page + chr(nb)
                if isPY2(): return page
                else: return page.encode('latin-1').decode('utf-8')
        else:return ''
    def _callback(self,matches):
        id = matches.group(1)
        try:
            return unichr(int(id))
        except:
            return id
    def decode_unicode_references(self,data):
        Extrn = re.sub("&#(\d+)(;|(?=\s))", self._callback, data)
        Extrn = Extrn.replace('</p><p>',' ').replace('</p><h2>',' ').replace('</h2><p>',' ').replace('&ndash;','')
        return Extrn
    def showitms(self,cItem):
        URL=cItem['url']
        if not URL.startswith('http'): URL = self.MAIN_URL + URL
        titre = cItem['title']
        page = cItem.get('page',1)
        print('titre='+titre)        
        if page == 1:
            URL0 = URL 
        else:
            if cItem['title']=='الحيوانات و الحياة البريّة' and page>70:URL0 = URL + '/page/1/'
            else:URL0 = URL + '/page/'+str(page)+'/'
        sts, data = self.getPage(URL0)
        pat = '''<a aria-label="([^<]+)" href="([^<]+)" class=.+?src=.+?data-breeze="([^<]+)".+?<div class="post-meta clearfix"><span class="date meta-item tie-icon">([^<]+)</span>.+?</span>([^<]+)</span>.+?</h2><p class="post-excerpt">([^<]+)</p> <a class="'''
        if sts:
            data = self.decode_unicode_references(data)
            data_list = re.findall(pat,data,re.M|re.I|re.DOTALL)
            for (titre,url,image,date,vue,discrpt) in data_list:            
                year = str(date)
                desc = ''
                desc = str(discrpt.replace('&hellip;',' ').replace('&hellip;',' ').replace('&rsquo;',' ').replace('&lsquo;',' '))+'\n'+'عدد المشاهدات :'+str(vue)
                titre = str(titre)
                image = image.split('" width=')[0]
                self.addDir({'import':cItem['import'],'category' : 'host2','url': url,'title':titre,'year':year,'qual':'','desc':desc,'icon':image,'hst':'tshost','good_for_fav':True,'mode':'21','tag':'','selary':'0'})
            if 'link rel="next"' not in data:
                self.addDir({'import':cItem['import'],'category' : 'host2','url': URL,'page':1,'title':T('Last Page'),'desc':cItem.get('desc',''),'icon':cItem['icon'],'mode':'20','hst':'tshost','good_for_fav':True})
            else:
                self.addDir({'import':cItem['import'],'category' : 'host2','url': URL,'page':page+1,'title':T('Next /'+str(page+1)),'desc':cItem.get('desc',''),'icon':cItem['icon'],'mode':'20','hst':'tshost','good_for_fav':True})
    def showelms(self,cItem):
        saison = cItem.get('saison')
        URL    = cItem['url']
        page = cItem.get('page',1)
        title  = cItem.get('name',cItem['title']).strip() 
        tag    = cItem['tag']
        img    = cItem['icon']        
        sts, data = self.getPage(URL) 
        if sts:
            data = self.decode_unicode_references(data)
            regx = '''"allowfullscreen"></iframe>(.+?)</p><div id="inline-related-post" class='''
            regx_1= '''<title>(.+?)</title>'''
            regx_2= '''content="(.+?)" /><link'''
            regx_3= '''<div class="single-post-meta post-meta clearfix"><span class="date meta-item tie-icon">(.+?)</span><div class="tie-alignright">'''
            regx_4 = '''<figure class="single-featured-image"><img class=.+?data-breeze="(.+?)"'''
            regx_5 = '''<iframe loading="lazy".+?src="(.+?)"'''
            try:
                Discpt_1 = re.findall(regx,data,re.M|re.I|re.DOTALL)
            except:Discpt_1=''
            if Discpt_1:
                Discpt_1 = Discpt_1[0]
            try:
                B = re.findall('<(.+?)>',Discpt_1,re.M|re.I|re.DOTALL)
            except:B=''
            if B:
                for x in B:
                    Discpt_1 = Discpt_1.replace(x,' ').replace('<','').replace('>','').replace('</a>','')
            try:
                Title = re.findall(regx_1,data,re.M|re.I|re.DOTALL)
            except:Title=''
            if Title:
                Title = Title[0]
            try:
                SouTitle = re.findall(regx_2,data,re.M|re.I|re.DOTALL)
            except:SouTitle=''
            if SouTitle:
                SouTitle = SouTitle[0]
            try:
                Datime = re.findall(regx_3,data,re.M|re.I|re.DOTALL)
            except:Datime=''
            if Datime:
                Datime = Datime[0]
            try:
                Imag = re.findall(regx_4,data,re.M|re.I|re.DOTALL)
            except:Imag=''
            if Imag:
                Imag = Imag[0]
            MyDiscrpt = str(SouTitle)+'\n'+str(Discpt_1)+'\n'+str(Datime)
            self.addVideo({'import':cItem['import'],'category' : 'host2','url': URL,'title':str(Title),'desc':MyDiscrpt,'icon':Imag,'hst':'tshost','good_for_fav':True,'tag':tag})
            
    def showelms333(self,cItem):
        saison = cItem.get('saison')
        URL    = cItem['url']
        page = cItem.get('page',1)
        title  = cItem.get('name',cItem['title']).strip() 
        tag    = cItem['tag']
        img    = cItem['icon']        
        sts, data = self.getPage(URL) 
        if sts:
            data = self.get_data_films(data)     
            if cItem.get('selary','0') == '0':
                Liste_els = re.findall('iframe.src="(https://www.youtube.*?)"', data, re.S)
                if Liste_els:
                    self.addVideo({'category':'host2','good_for_fav':True, 'title': cItem['title']+' - Trailer','url':Liste_els[0], 'desc':cItem.get('desc',''),'import':cItem['import'],'icon':cItem['icon'],'hst':'none'})
                self.addVideo({'category':'host2','good_for_fav':True, 'title': cItem['title'],'url':cItem['url'], 'desc':cItem.get('desc',''),'import':cItem['import'],'icon':cItem['icon'],'hst':'tshost'})						
            else:
                if not saison:
                    tag = 'TVSHOW'
                    printDBG('title='+title)
                    Liste_els = re.findall('label="seasons">(.*?)</section>', data, re.S)
                    if Liste_els:
                        Liste_els = re.findall('<li.*?href="(.*?)".*?>(.*?)<', Liste_els[0], re.S)
                        for (url,saison) in Liste_els:
                            saison = saison.replace('الموسم','').strip()
                            printDBG('S'+saison+' '+title)
                            self.addDir({'import':cItem['import'],'category' : 'host2','url': url,'title':title+' S'+saison,'desc':cItem['desc'],'icon':img,'mode':'21','hst':'tshost','good_for_fav':True,'tag':tag,'saison':saison,'selary':'1'})                  
                else:
                    tag = 'EPISODE'
                    Liste_els = re.findall('<ul class.{,30}?id="eps">(.*?)</ul>', data, re.S)
                    if Liste_els:
                        Liste_els = re.findall('<li.*?href="(.*?)".*?(?:alt="logo"|</h3>).*?src="(.*?)".*?alt="(.*?)".*?<em>(.*?)</em>', Liste_els[0], re.S)
                        for (url,image,titre,ep) in Liste_els:
                            image = self.std_url(image)
                            self.addVideo({'import':cItem['import'],'category' : 'host2','url': url,'title':title+ 'E'+ep,'desc':cItem['desc'],'icon':image,'hst':'tshost','good_for_fav':True,'tag':tag})
    
    def get_links(self,cItem):
        urlTab = []
        url = cItem['url']
        referer = url
        printDBG('get_linksget_linksget_links'+url)
        sts, data = self.getPage(url)
        if sts:
            data = self.decode_unicode_references(data)
            regx_5 = '''<iframe loading="lazy".+?src="(https://www.youtube.*?)"'''
            try:
                Video = re.findall(regx_5,data,re.M|re.I|re.DOTALL)
            except:Video=''
            if Video:
                Video = Video[0]
            printDBG('get_linksget_linksget_links___________Video'+Video)
            if 'youtube' in Video:                
                label   = gethostname(url)
                urlTab.append({'name':'|Watch|'+label, 'url':Video, 'need_resolve':1})
            else:urlTab.append({'name':Tag+self.cleanHtmlStr(titre), 'url':Video, 'need_resolve':1,'type':'local'})		       
        return urlTab
    
    def getVideos_direct(self,videoUrl):
        urlTab = []
        tabs = self.getVideos(videoUrl)
        for (url,type_) in tabs:
            if   type_ == '1':
                resolve = 1
                label   = gethostname(url)
            elif type_ == '4':
                label,url = url.split('|',1)
                resolve = 0
            urlTab.append({'name':'|Watch|'+label, 'url':url, 'need_resolve':resolve})	
        return urlTab
    def getVideos(self,videoUrl):
        urlTab = []
        sts, data = self.getPage(videoUrl)
        printDBG('getVideos___________Video'+videoUrl)
        if sts:
            data = self.decode_unicode_references(data)
            regx_5 = '''<iframe loading="lazy".+?src="(.*?)"'''
            try:
                Video = re.findall(regx_5,data,re.M|re.I|re.DOTALL)
            except:Video=''
            if Video:
                Video = Video[0]
                printDBG('getVideos___________Video'+Video)
                label   = gethostname(Video)
                urlTab.append({'name':'|Watch|'+label, 'url':Video, 'need_resolve':1})
            else:
                urlTab.append({'name':'|Watch|'+'No_Link', 'url':Video, 'need_resolve':1})
        return urlTab
    def getVideos9999999(self,videoUrl):
        urlTab = []	
        code,id_ = videoUrl.split('|',1)
        if id_ == 'DOWN':
            sts, data = self.getPage(code,self.defaultParams)
            Liste_els = re.findall('id="downloadbtn".*?href="(.*?)"', data, re.S|re.IGNORECASE)			
            if Liste_els:
                url_ = Liste_els[0]
                if url_.endswith('mp4'):
                    host = url_.split('.net/',1)[0]+'.net'
                    URL_= strwithmeta('MP4|'+url_, {'Referer':host})
                    urlTab.append((URL_,'4'))	
                else:
                    urlTab.append((url_,'1'))
        else:	
            url = self.MAIN_URL+'/wp-content/themes/Cima%20Now%20New/core.php?action=switch&index='+code+'&id='+id_
            addParams = dict(self.defaultParams)
            header = dict(addParams['header'])
            header['Referer'] = self.MAIN_URL
            addParams.update({'header':header})            
            sts, data = self.getPage(url,addParams)
            if sts:
                Liste_els_3 = re.findall('src="(.+?)"', data, re.S|re.IGNORECASE)	
                if Liste_els_3:
                    URL = Liste_els_3[0]
                    if URL.startswith('//'): URL='http:'+URL
                    if 'cimanow.net' not in URL:
                        urlTab.append((URL,'1'))
                    else:
                        host = 'https://' + URL.split('/')[2]                       
                        sts, data = self.getPage(URL,addParams)
                        if sts:
                            Liste_els = re.findall('source.*?src="(.*?)".*?size="(.*?)"', data, re.S|re.IGNORECASE)
                            for elm in Liste_els:
                                url_ = elm[0]
                                if not(url_.startswith('http')): url_ = host + Quote(url_)
                                URL_= strwithmeta(elm[1]+'|'+url_, {'Referer':host})
                                urlTab.append((URL_,'4'))       
        return urlTab
    
    def searchResult(self,cItem):
        str_ch  = cItem.get('str_ch','')
        if str_ch =='': 
            ret = self.sessionEx.waitForFinishOpen(GetVirtualKeyboard(), title=('Search Text:'), text='')
            str_ch = ret[0]
        if not str_ch: return []
        page    = cItem.get('page',1)
        section = cItem.get('section','')
        extra   = cItem.get('import','')
        elms = self.SearchAll(str_ch,page,extra,section)       
        for elm in elms:
           self.addDir(elm)
        return elms
    
    def SearchAll(self,str_ch,page=1,extra='',type_='',icon=''):
        elms = []
        if type_ != '':
            URL = self.MAIN_URL+'/page/'+str(page)+'/?s='+str_ch+'+'+type_
        else:
            URL = self.MAIN_URL+'/page/'+str(page)+'/?s='+str_ch
        sts, data = self.getPage(URL)
        if sts:
            data_list0 = re.findall('<article .*?href="(.*?)"(.*?)title">(.*?)(<em>.*?)</li>.*?data-src="(.*?)"', data, re.S)
            if data_list0:
                for (url,desc1,titre,desc2,image) in data_list0:
                    year = ''
                    desc = ''
                    data_desc = desc1 + desc2
                    titre = titre.replace('&#8217;',"'").replace('&#8216;',"'")
                    inf_list = re.findall('Ribbon">(.*?)</li>', data_desc, re.S)
                    if inf_list: desc = desc + 'Info: '+inf_list[0]+'\n'
                    inf_list = re.findall('year">(.*?)</li>', data_desc, re.S)
                    if inf_list:
                        desc = desc + 'Year: '+inf_list[0]+'\n'
                        year = inf_list[0].strip()
                    episode = ''
                    inf_list = re.findall('label="episode">(.*?)</li>', data_desc, re.S)
                    if inf_list:
                        episode = self.cleanHtmlStr(inf_list[0]).replace('الحلقة','E')                        
                    inf_list = re.findall('الموسم(.*?)</li>', data_desc, re.S)
                    if inf_list:
                        saison = 'S'+self.cleanHtmlStr(inf_list[-1])
                        episode = saison + episode
                    if episode != '':
                        desc = desc + 'Episode: '+episode+'\n'
                    inf_list = re.findall('<em>(.*?)</em>', data_desc, re.S)
                    if inf_list: desc = desc + 'Genre: '+inf_list[-1]+'\n'
                    inf_list = re.findall('aria-label="ribbon">(.*?)<', data_desc, re.S)
                    TAG = ''
                    for elm in inf_list:
                        if TAG=='': TAG = elm
                        else: TAG = TAG +'|'+elm
                    if TAG != '': desc = desc + 'TAG: '+TAG+'\n'
                    if '1080' in TAG: qual = '1080p'
                    elif '720' in TAG: qual = '720p'
                    else: qual = ''
                    image = self.std_url(image)
                    titre = titre.strip()
                    if ('/فيلم-' in url) or ('/%d9%81%d9%8a%d9%84%d9%85-' in url):
                        tag = 'MOVIE'
                        elms.append({'import':extra,'category' : 'host2','url': url,'title':titre,'year':year,'qual':qual,'desc':desc,'icon':image,'mode':'21','hst':'tshost','good_for_fav':True,'tag':tag,'selary':'0'})	
                    #elif '/مسلسل-' in url:
                    else:
                        tag = 'TVSHOW'
                        name = titre
                        titre = titre + ' ' + episode
                        elms.append({'import':extra,'category' : 'host2','url': url,'title':titre.strip(),'year':year,'qual':qual,'desc':desc,'icon':image,'hst':'tshost','good_for_fav':True,'mode':'21','tag':tag,'selary':'1','name':name})	                  
                if re.findall('<li class="active">.*?</li>.{0,5}<li><a href="(.*?)"', data, re.S):
                    elms.append({'import':extra,'category' : 'host2','title':T('Next'),'mode':'51','section':type_,'page':page+1,'str_ch':str_ch})        
        return(elms)
    
    def SearchMovies(self,str_ch,page=1,extra=''):
        elms = self.SearchAll(str_ch,page,extra=extra,type_='فيلم')
        return elms
    
    def SearchSeries(self,str_ch,page=1,extra=''):
        elms = self.SearchAll(str_ch,page,extra=extra,type_='مسلسل')
        return elms
    
    def SearchResult(self,str_ch,page,extra):
        URL = self.MAIN_URL+'/page/'+str(page)+'/?s='+str_ch
        sts, data = self.getPage(URL)
        if sts:
            data_list0 = re.findall('<article .*?href="(.*?)"(.*?)title">(.*?)(<em>.*?)</li>.*?data-src="(.*?)"', data, re.S)
            if data_list0:
                for (url,desc1,titre,desc2,image) in data_list0:
                    year = ''
                    desc = ''
                    data_desc = desc1 + desc2
                    titre = titre.replace('&#8217;',"'").replace('&#8216;',"'")
                    inf_list = re.findall('Ribbon">(.*?)</li>', data_desc, re.S)
                    if inf_list: desc = desc + 'Info: '+inf_list[0]+'\n'
                    inf_list = re.findall('year">(.*?)</li>', data_desc, re.S)
                    if inf_list:
                        desc = desc + 'Year: '+inf_list[0]+'\n'
                        year = inf_list[0].strip()
                    inf_list = re.findall('<em>(.*?)</em>', data_desc, re.S)
                    if inf_list: desc = desc + 'Genre: '+inf_list[0]+'\n'
                    inf_list = re.findall('aria-label="ribbon">(.*?)<', data_desc, re.S)
                    TAG = ''
                    for elm in inf_list:
                        if TAG=='': TAG = elm
                        else: TAG = TAG +'|'+elm
                    if TAG != '': desc = desc + 'TAG: '+TAG+'\n'
                    if '1080' in TAG: qual = '1080p'
                    elif '720' in TAG: qual = '720p'
                    else: qual = ''
                    printDBG("titttttr"+url)
                    if ('/فيلم-' in url) or ('/%d9%81%d9%8a%d9%84%d9%85-' in url):
                        tag = 'MOVIE'
                        self.addVideo({'import':extra,'category' : 'host2','url': url,'title':titre,'year':year,'qual':qual,'desc':desc,'icon':image,'hst':'tshost','good_for_fav':True,'tag':tag})                    
                    else:
                        tag = 'TVSHOW'
                        self.addDir({'import':extra,'category' : 'host2','url': url,'title':titre,'year':year,'qual':qual,'desc':desc,'icon':image,'hst':'tshost','good_for_fav':True,'mode':'21','tag':tag})
    
    def getArticle(self,cItem):
        Desc = [('Quality','fa-play"></i>الجودة.*?<a>(.*?)</a>','',''),('Time','fa-clock">.*?<a>(.*?)</a>','',''),
                ('Story','fa-info-circle">(.*?)</li>','\n','')]
        desc = self.add_menu(cItem,'','','','desc',Desc=Desc)	
        if desc =='': desc = cItem.get('desc','')
        return [{'title':cItem['title'], 'text': desc, 'images':[{'title':'', 'url':cItem.get('icon','')}], 'other_info':{}}]
