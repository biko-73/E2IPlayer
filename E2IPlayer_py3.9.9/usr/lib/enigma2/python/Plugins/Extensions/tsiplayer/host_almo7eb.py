# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,gethostname,T
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta

import re,urllib,json
import base64
import sys



def getinfo():
    info_={}
    name = 'Almo7eb'
    hst = 'https://www.almo7eb.com'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='1.0 18/07/2022'    
    info_['dev']='RGYSoft'
    info_['cat_id']='21'
    info_['desc']='Almo7eb Films'
    info_['icon']='https://i.ibb.co/wQ0FX88/almo7eb.png'
    info_['recherche_all']='1'
    info_['update']='New Site'
    return info_

def uniform_titre5(titre,with_type=False):
    #print(titre)
    info = {}
    titre=titre.replace('مشاهدة وتحميل مباشر','').replace('مشاهدة','').replace('اون لاين','')
    tag_film  = [('فيلم','FILM'),('فلم','FILM'),('مسلسل','SERIE'),('عرض','TV SHOW'),('انمي','ANIM')]    
    tag_type  = ['مدبلج للعربية','مترجمة للعربية','مترجم للعربية', 'مدبلجة', 'مترجمة' , 'مترجم' , 'مدبلج']
    for elm in tag_film: tag_type.append(elm[0])
    tag_qual   = ['1080p','720p','WEB-DL','BluRay','DVDRip','HDCAM','HDTC','HDRip', 'HD', '1080P','720P','DVBRip','TVRip','DVD','SD']    
    tag_saison = [('الموسم الثاني','2'),('الموسم الاول','1'),('الموسم الثالث','3'),('الموسم الرابع','4'),('الموسم الخامس','5'),('الموسم السادس','6'),('الموسم السابع','7'),('الموسم الثامن','8'),('الموسم التاسع','9'),('الموسم العاشر','10')]
    tags_special = [('رمضان 2023','2023'),('رمضان 2022','2023'),('رمضان 2021','2023'),('رمضان 2020','2023'),('رمضان 2019','2023'),('رمضان 2018','2023'),('رمضان 2017','2023'),('رمضان 2016','2023'),]
    cars = [':','-','_','|']
    tag_part=[]
    for elm in tag_saison:
        tag_part.append(elm)
        tag_part.append((elm[0].replace('الموسم','الجزء'),elm[1]))
    tag_saison = tag_saison + [('S01','1'),]

    #Tags
    tags_ = []
    type_ = ''
    for elm in tag_type:
        if elm in titre:
            titre = titre.replace(elm,'').strip()
            for elm_ in tag_film:
                if elm == elm_[0]:
                    type_ = elm_[1]
            tags_.append(elm)

    for elm in tags_special:
        if elm[0] in titre:
            titre = titre.replace(elm[0],elm[1]).strip()
            tags_.append(elm[0])

    info['type'] = type_
    info['tags'] = tags_

    #Quality
    qual_ = []
    for elm in tag_qual:
        if elm in titre:
            titre = titre.replace(elm,'').strip()
            qual_.append(elm)
    info['qual'] = qual_

    #Saison
    saison = ''
    for elm in tag_saison:
        if elm[0] in titre:
            saison = elm[1]
            titre = titre.replace(elm[0],'').strip()
            break
    info['saison'] = saison

    #Part
    part = ''
    for elm in tag_part:
        if elm[0] in titre:
            part = elm[1]
            titre = titre.replace(elm[0],'').strip()
            break
    info['part'] = part


    #Year
    year = ''
    data = re.findall('(20[0-2][0-9])', titre, re.S)
    if data:
        year = data[0].strip()
        titre = titre.replace(year,'').strip()
    else:
        data = re.findall('(19[0-9]{2})', titre, re.S)
        if data:
            year = data[0].strip()
            titre = titre.replace(year,'').strip()
    info['year'] = year

    #Titre en
    titre_en = ''
    titre_ =''
    data_list = re.findall('[a-zA-Z0-9 :_\-\.]+', titre, re.S)
    if data_list:
        for elm in data_list:
            if elm.strip() != '':
                if len(elm.strip())>len(titre_):
                    titre_ = elm.strip()                           
    if len(titre_)>2:
        titre_en = titre_

    for car in cars+cars:
        if titre_en.startswith(car): titre_en = titre_en[1:].strip()
        if titre_en.endswith(car): titre_en = titre_en[:-2].strip()
    info['title_en'] = titre_en

    if titre_en.endswith('-') or titre_en.endswith(':'): titre_en = titre_en[:-2].strip()
    #Titre ar
    titre_ar = ''
    titre_ =''    
    titre_ = titre.replace(titre_en,'').replace('  ',' ').replace('  ',' ').strip()  
    if len(titre_.strip())>2:
        titre_ar = titre_
    
    # Host Almo7eb
    artists = ''
    if 'بطولة'  in titre_ar: 
        titre_ar,artists = titre_ar.replace('- بطولة','بطولة').split('بطولة')
    titre_ar = titre_ar.strip()
    artists  = artists.strip()
    info['artists']  = artists
    #############

    for car in cars+cars:
        if titre_ar.startswith(car): titre_ar = titre_ar[1:].strip()
        if titre_ar.endswith(car): titre_ar = titre_ar[:-2].strip()
    info['title_ar'] = titre_ar
    
    #Titre
    if len(titre_en)<3:
        titre = titre_ar
    else:
        titre = titre_en
    info['title'] = titre
    
    #if 'بطولة' in titre: titre = titre.split('بطولة',1)[0]
    #display titre
    tag = ''
    if with_type and type_!='':
        tag = tscolor('\c0030??30')+type_+' - '
    if saison != '':
        tag =  tag + tscolor('\c00????30')+'Saison '+saison + ' - '
    elif part != '':
        tag =  tag + tscolor('\c00????30')+'Part '+part + ' - '   
    if year != '':
        tag =  tag + tscolor('\c0000????')+year +' - '
    if tag.endswith(' - '): tag = tag[:-3]
    if tag!='': tag = tscolor('\c00??????') +'['+ tag + tscolor('\c00??????') + '] '
    info['title_display'] = tag  + titre
    #print(str(info))
    return info   

class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'aflamfree.cookie'})
        self.MAIN_URL = getinfo()['host']

    def showmenu(self,cItem):
        TAB = [('الافلام','/ar/m7b-273','10',0),('المسلسلات','/ar/m7b-525','10',1),]
        self.add_menu(cItem,'','','','','',TAB=TAB,search=False)
        self.addDir({'import':cItem['import'],'category' :'host2','title':T('Search'),'icon':'https://i.ibb.co/dQg0hSG/search.png','mode':'51'})	

    def showmenu100(self,cItem):
        gnr = cItem.get('sub_mode',0)
        sts, data = self.getPage(cItem['url'])
        data_list = re.findall('id=\'blocktitle\'>(.*?)</h3>(.*?)(?:<h3|id=\'pagination)', data, re.S)
        for (titre,data_) in data_list:
            self.addDir({'import':cItem['import'],'category' : 'host2','url': cItem['url'],'title':self.cleanHtmlStr(titre),'desc':'','icon':cItem['icon'],'mode':'20','data':data_})

    def showmenu1(self,cItem):
        gnr = cItem.get('sub_mode',0)
        if gnr == 0:
            self.addDir({'import':cItem['import'],'category' :'host2', 'url':'273', 'title':'جميع الأفلام', 'desc':'', 'icon':'https://i.ibb.co/RSgNt5N/cimanow-aflam.png', 'mode':'20'})
            self.addDir({'import':cItem['import'],'category' :'host2', 'url':'50', 'title':tscolor('\c00????30')+'حسب النوع', 'desc':'', 'icon':'https://i.ibb.co/RSgNt5N/cimanow-aflam.png', 'mode':'10', 'sub_mode':2})            					
            self.addDir({'import':cItem['import'],'category' :'host2', 'url':'51', 'title':tscolor('\c00????30')+'حسب السنة', 'desc':'', 'icon':'https://i.ibb.co/RSgNt5N/cimanow-aflam.png', 'mode':'10', 'sub_mode':2})
        elif gnr == 1:
            self.addDir({'import':cItem['import'],'category' :'host2', 'url':'525', 'title':'جميع المسلسلات', 'desc':'', 'icon':'https://i.ibb.co/RSgNt5N/cimanow-aflam.png', 'mode':'20'})
            self.addDir({'import':cItem['import'],'category' :'host2', 'url':'52', 'title':tscolor('\c00????30')+'حسب النوع', 'desc':'', 'icon':'https://i.ibb.co/RSgNt5N/cimanow-aflam.png', 'mode':'10', 'sub_mode':2})            					
            self.addDir({'import':cItem['import'],'category' :'host2', 'url':'61', 'title':tscolor('\c00????30')+'مسلسلات رمضان', 'desc':'', 'icon':'https://i.ibb.co/RSgNt5N/cimanow-aflam.png', 'mode':'10', 'sub_mode':2})
        else:
            menue_id  = cItem['url']
            m7b       = "273"
            pages     = "218"
            post_data = {'menue_id':menue_id,'m7b':m7b,'pages':pages}
            post_url   = self.MAIN_URL +  '/ar/fetch_menu.php'
            sts, data = self.getPage(post_url,post_data=post_data)
            if sts:
                data_list = re.findall('<option value=\'(.*?)\'.*?>(.*?)</option>', data, re.S)
                for (value,titre) in data_list:
                    self.addDir({'import':cItem['import'],'category' :'host2', 'url':value, 'title':titre.strip(), 'desc':'','mode':'20', 'sub_mode':0})            					

    def showitms(self,cItem):
        page = cItem.get('page',1)
        if page == 1:
            post_data = {'submenue_id':cItem['url'],'catstyle':'carton-movies-01'}
            post_url   = self.MAIN_URL +  '/ar/fetch_menu.php'
            sts, data = self.getPage(post_url,post_data=post_data)            
        else:
            url0 = self.MAIN_URL+'/ar/m7b-'+cItem['url']+'&page='+str(page)+'.html'
            sts, data = self.getPage(url0)
        count = 0
        if sts:
            data_list = re.findall('<a href=\'(.*?)\'.*?src=\'(.*?)\'.*?title=\'(.*?)\'', data, re.S)
            for (url,image,titre) in data_list:
                if not (url.endswith('/ar') or url.endswith('.com')):
                    printDBG('titre='+titre)
                    info   = self.std_title(titre)
                    saison = info.get('saison')
                    part = info.get('part')
                    image = self.MAIN_URL + '/ar/' + image
                    image = self.std_url(image)
                    if '?url=' in url: x1,url = url.split('?url=',1)
                    count = count+1
                    self.addDir({'import':cItem['import'],'category' : 'host2','url': url,'title':info.get('title_display'),'sTitle':info.get('title'),'desc':'','icon':image,'mode':'21','good_for_fav':True,'hst':'tshost','saison':saison,'part':part})            
        if count>19:
            self.addDir({'import':cItem['import'],'category' : 'host2','url': cItem['url'],'title':T('Next'),'desc':'','icon':'','hst':'tshost','mode':'20','page':page+1})  
    
    def showelms(self,cItem):
        sts, data = self.getPage(cItem['url']) 
        if sts:
            data_list = re.findall('<a data-id=\'(.*?)\'.*?data-idp=\'(.*?)\'.*?data-name=\'(.*?)\'.*?data-post=\'(.*?)\'', data, re.S)
            if data_list:
                for (id_,idp,titre,post_) in data_list:
                    url_post = self.MAIN_URL + '/ar/serv.php'
                    titre = self.std_episode(titre,cItem)
                    self.addVideo({'import':cItem['import'],'good_for_fav':True,'category':'host2', 'url':url_post,'id_':id_,'idp':idp,'titre':titre,'post_':post_, 'desc':cItem['desc'],'title':titre, 'icon':cItem['icon'],'EPG':True,'hst':'tshost'} )
            else:
                data_list = re.findall('class="button-stream".*?href="(.*?)".*?>(.*?)<', data, re.S)
                for (url,titre) in data_list:
                    titre = self.std_episode(titre,cItem)
                    self.addVideo({'import':cItem['import'],'good_for_fav':True,'category':'host2', 'url':url, 'desc':cItem['desc'],'title':titre, 'icon':cItem['icon'],'EPG':True,'hst':'tshost'} )

    def get_links(self,cItem): 	
        printDBG("User Current Version:-"+ str( sys.version))        
        urlTab = []	
        URL    = cItem['url']				
        printDBG('URL1===='+str(URL))
        id_ = cItem.get('id_','')
        if id_ != '':
            url_post = URL
            idp = cItem.get('idp','')
            titre = cItem.get('titre','')
            post_ = cItem.get('post_','')
            printDBG('Params===='+str((id_,idp,titre,post_)))
            post_data = {'vid':id_,'idp':idp,'referdomain':'','name':titre,'post':post_}
            sts, data = self.getPage(url_post,post_data=post_data)
            if sts:
                #printDBG('dataelmo7eb='+data)
                # elms_data = re.findall('id=\'(?:playserver|playphoto|playyoutube|playdrive|playlinkbox)\'.*?data-code=\'(.*?)\'.*?data-thefile=\'(.*?)\'', data, re.S)
                # i=1
                # for (code,url1) in elms_data:
                    # MainURL = self.MAIN_URL + '/ar/'
                    # url0 = 'hst#tshost#'+code+'|||'+url1+'|||'+MainURL
                    # urlTab.append({'name':'Server '+str(i), 'url':url0, 'need_resolve':1})
                    # i=i+1 
                elms_data = re.findall("id='playerdetails' >(.*?)onClick", data, re.S)
                if elms_data:
                    elms_data = elms_data[0]
                elms_data = re.findall("<a id='(?:.*?)'.*?data-type='(.*?)'.*?data-servername='(.*?)'.*?data-medianame='(.*?)'.*?data-servercode='(.*?)'.*?class='butt.*?>(.*?)<", data, re.S)
                i= 0
                for (type_,servername,medianame,servercode,label) in elms_data:
                    if type_ =='download':
                        MainURL = self.MAIN_URL + '/ar/'
                        url0 = 'hst#tshost#'+type_+'|||'+servername+'|||'+medianame+'|||'+servercode+'|||'+MainURL
                        urlTab.append({'name':'Server '+str(i+1)+' |'+label, 'url':url0, 'need_resolve':1})
                        i=i+1 
                elms_data = re.findall("<a id='(?:playyoutube)'.*?data-code='(.*?)'", data, re.S)
                if elms_data:
                    youtube_id = elms_data[0]
                    URL = 'https://www.youtube.com/embed/'+youtube_id+'?modestbranding=0&cc_load_policy=1&rel=0&showinfo=0'
                    urlTab.append({'name':'Youtube ', 'url':URL, 'need_resolve':1})      
        else:
            sts, data = self.getPage(URL)
            if sts:
                elms_data = re.findall('playerbuttn\'.*?href=\'(.*?)\'', data, re.S)
                i=1
                for (url) in elms_data:
                    url0 = 'hst#tshost#'+URL+url
                    urlTab.append({'name':'Server '+str(i), 'url':url0, 'need_resolve':1})
                    i=i+1 
        return urlTab
        
    def getVideos(self,videoUrl):
        urlTab = []
        if '|||' in videoUrl:
            type_,servername,medianame,servercode,MainURL = videoUrl.split('|||')
            post_data = {'type':type_,'servername':servername,'medianame':medianame,'servercode':servercode}
            printDBG('Post Data ='+str(post_data))
            if servername == 'linkbox':
                url = 'https://www.sharezweb.com/api/file/detail?itemId='+servercode+'&needUser=1&needTpInfo=1&token='
                sts, data = self.getPage(url)
                if sts:
                    data = json.loads(data)
                    url = data.get('data',{}).get('itemInfo',{}).get('url','')
                    url = strwithmeta(url,{'User-Agent': self.USER_AGENT,'Referer':'https://www.sharezweb.com/'})
                    urlTab.append((url,'0'))                
                    return(urlTab)                                   
            elif servername == 'codeserver':
                url = strwithmeta(servercode,{'User-Agent': self.USER_AGENT,'Referer':'https://www.hawarycairo.com'})
                urlTab.append((url,'0'))            
                return(urlTab)
            elif servername == 'getgoogle':
                url = strwithmeta(servercode,{'User-Agent': self.USER_AGENT})
                urlTab.append((url,'0'))                
                return(urlTab)            
            elif servername == 'googledrive':
                cnt = '?alt=media&key=AIzaSyBXV3qGJ2rwDaxvUmAzaVpZMmn1t6PyU0E&fref=gc&h=ATOAOfKrTqeRe2-ljwMLFtWsz0CEUuWFtqWoS9qYUoKcPDDXnk6ec2GlpzTB7MDfFEnoXqqjHE1-g-rHJI6dfZzvLnowH0gBzh-nDpikmSPvFVkkbdie0YD0EALS6kbdwZHVUzfRrzjDsw'
                url = strwithmeta('https://www.googleapis.com/drive/v3/files/'+servercode+cnt,{'User-Agent': self.USER_AGENT})
                urlTab.append((url,'0'))                
                return(urlTab)              
            else:
                return(urlTab)
        else:
            sts, data = self.getPage(videoUrl)
        if sts:
            elms_data = re.findall('<source src=\'(.*?)\'.*?label=\'(.*?)\'', data, re.S)        
            if elms_data:
                for (url,label) in elms_data:
                    if 'googlevideo' in url:
                        url = strwithmeta(label+'|'+url.strip(),{'User-Agent': self.USER_AGENT})
                    else:
                        url = strwithmeta(label+'|'+url.strip(),{'Referer':'https://shahed.life/','User-Agent': self.USER_AGENT})
                    urlTab.append((url,'4'))
            else:
                elms_data = re.findall('<iframe.*?src=[\'"](.*?)[\'"]', data, re.S)        
                if elms_data:
                    url = elms_data[0]
                    if url.startswith('//'): url = 'https:'+url
                    url = strwithmeta(url,{'User-Agent': self.USER_AGENT})
                    urlTab.append((url,'1'))
                else:
                    print('dfgdgdfgdfg')
        return urlTab

    def showsearch(self,cItem):
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن فيلم','icon':'https://i.ibb.co/k56BbCm/aflam.png','mode':'51','section':'FILM'})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث عن مسلسل','icon':'https://i.ibb.co/3M38qkV/mousalsalat.png','mode':'51','section':'SERIE'})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'البحث في الموقع','icon':'https://i.ibb.co/2nztSQz/all.png','mode':'51','section':''})        

    def SearchResult(self,str_ch,page,extra):
        elms = []
        url0 = self.MAIN_URL+'/ar/search.php?q='+str_ch+'&sitesearch=almo7eb&page='+str(page)
        sts, data = self.getPage(url0)
        if sts:
            data_list = re.findall('class=\'article\'>.*?image: url\((.*?)\).*?<a href=\'(.*?)\'.*?>(.*?)<', data, re.S)
            for (image,url,titre) in data_list:
                if '?url=' in url: x1,url = url.split('?url=',1)
                #printDBG('url====='+url)
                self.addDir({'import':extra,'category' : 'host2','url': url,'title':titre,'desc':'','icon':image,'mode':'21','good_for_fav':True})            

    def SearchAll(self,str_ch,page=1,extra='',type_=''):
        elms = []
        url0 = self.MAIN_URL+'/ar/search.php?q='+str_ch+'&sitesearch=almo7eb&page='+str(page)
        nb=0
        sts, data = self.getPage(url0)
        if sts:
            data_list = re.findall('class=\'article\'>.*?image: url\((.*?)\).*?<a href=\'(.*?)\'.*?>(.*?)<', data, re.S)
            for (image,url,titre) in data_list:
                if '?url=' in url: url = url.split('?url=',1)[1]
                info   = self.std_title(titre,with_type=True)
                saison = info.get('saison')
                part = info.get('part')
                image = self.std_url(image)
                type_elm = info.get('type','')
                add = False
                if (type_==''):
                    add = True
                elif (type_=='FILM'): 
                    if type_ == type_elm:
                        add = True
                elif (type_=='SERIE'): 
                    if (type_ == type_elm) or ('TV SHOW' == type_elm):
                        add = True                    
                if add:
                    elms.append({'import':extra,'category' : 'host2','url': url,'title':info.get('title_display'),'sTitle':info.get('title'),'desc':'','icon':image,'mode':'21','good_for_fav':True,'saison':saison,'part':part,'info':info})            
                    nb = nb +1
            if nb>13:
                elm = {'import':extra,'category' : 'host2','title':T('Next'),'url':url,'desc':'next','icon':'','mode':'51','good_for_fav':True,'EPG':True,'hst':'tshost','page':page+1,'str_ch':str_ch,'section':type_}
                elms.append(elm)
        return elms

    def SearchMovies(self,str_ch,page=1,extra=''):
        print('-------------------------ALMO7EB-----------------------')
        elms = self.SearchAll(str_ch,page,extra,'FILM')
        return (elms)

    def SearchSeries(self,str_ch,page=1,extra=''):
        elms = self.SearchAll(str_ch,page,extra,'SERIE')
        return (elms)        

