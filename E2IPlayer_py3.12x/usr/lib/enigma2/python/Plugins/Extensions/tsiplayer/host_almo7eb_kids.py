# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,gethostname,T
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta

import re,urllib
import base64,json


def getinfo():
    info_={}
    name = 'Almo7eb - KIDS'
    hst = 'https://www.kids.almo7eb.com'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='1.0 18/07/2022'    
    info_['dev']='RGYSoft'
    info_['cat_id']='22'
    info_['desc']='Almo7eb Kids'
    info_['icon']='https://i.ibb.co/wQ0FX88/almo7eb.png'
    info_['update']='New Site'
    return info_
    
    
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'aflamfree.cookie'})
        self.MAIN_URL = getinfo()['host']
        self.Fetch    =  self.MAIN_URL +  '/fetch_menu.php'

    def showmenu(self,cItem):
        #del_ = ['مجلة المحب الاطفال']
        TAB = [('أفلام كرتون',self.MAIN_URL+'/m7b-6','10',0),('مسلسلات كرتون',self.MAIN_URL+'/m7b-4','10',1),]
        self.add_menu(cItem,'','','','','',TAB=TAB,search=False)
        self.addDir({'import':cItem['import'],'category' :'host2','title':T('Search'),'icon':'https://i.ibb.co/dQg0hSG/search.png','mode':'51'})	
        

    # def showmenu(self,cItem):
        # TAB = [('Main','/ar/','10',0),('الافلام','/ar/m7b-273','20',1),('المسلسلات','/ar/m7b-525','20',2),]
        # self.add_menu(cItem,'','','','','',TAB=TAB,search=True)

    def showmenu100(self,cItem):
        gnr = cItem.get('sub_mode',0)
        sts, data = self.getPage(cItem['url'])
        data_list = re.findall('id=\'blocktitle\'>(.*?)</h3>(.*?)(?:<h3|id=\'pagination)', data, re.S)
        for (titre,data_) in data_list:
            self.addDir({'import':cItem['import'],'category' : 'host2','url': cItem['url'],'title':self.cleanHtmlStr(titre),'desc':'','icon':cItem['icon'],'mode':'20','data':data_})

    def showmenu1(self,cItem):
        gnr = cItem.get('sub_mode',0)
        if gnr == 0:
            self.addDir({'import':cItem['import'],'category' :'host2', 'url':'6', 'title':'جميع أفلام الكرتون و الانمي', 'desc':'', 'icon':'https://i.ibb.co/RSgNt5N/cimanow-aflam.png', 'mode':'20'})
            self.addDir({'import':cItem['import'],'category' :'host2', 'url':'62', 'title':'افلام كرتون', 'desc':'', 'icon':'https://i.ibb.co/RSgNt5N/cimanow-aflam.png', 'mode':'10', 'sub_mode':2})            					
            self.addDir({'import':cItem['import'],'category' :'host2', 'url':'89', 'title':'افلام انمي', 'desc':'', 'icon':'https://i.ibb.co/RSgNt5N/cimanow-aflam.png', 'mode':'10', 'sub_mode':2})
            self.addDir({'import':cItem['import'],'category' :'host2', 'url':'63', 'title':'حلقات و فيديو', 'desc':'', 'icon':'https://i.ibb.co/RSgNt5N/cimanow-aflam.png', 'mode':'10', 'sub_mode':2})
        elif gnr == 1:
            self.addDir({'import':cItem['import'],'category' :'host2', 'url':'4', 'title':'جميع مسلسلات الكرتون و الانمي', 'desc':'', 'icon':'https://i.ibb.co/RSgNt5N/cimanow-aflam.png', 'mode':'20'})
            self.addDir({'import':cItem['import'],'category' :'host2', 'url':'92', 'title':'مسلسلات انمي', 'desc':'', 'icon':'https://i.ibb.co/RSgNt5N/cimanow-aflam.png', 'mode':'10', 'sub_mode':2})            					
            self.addDir({'import':cItem['import'],'category' :'host2', 'url':'93', 'title':'مسلسلات كرتون', 'desc':'', 'icon':'https://i.ibb.co/RSgNt5N/cimanow-aflam.png', 'mode':'10', 'sub_mode':2})
        else:
            menue_id  = cItem['url']
            m7b       = "4"
            pages     = "77"
            post_data = {'menue_id':menue_id,'m7b':m7b,'pages':pages}
            post_url   = self.Fetch
            sts, data = self.getPage(post_url,post_data=post_data)
            if sts:
                data_list = re.findall('<option value=\'(.*?)\'.*?>(.*?)</option>', data, re.S)
                for (value,titre) in data_list:
                    self.addDir({'import':cItem['import'],'category' :'host2', 'url':value, 'title':titre.strip(), 'desc':'','mode':'20', 'sub_mode':0})            					

    def showitms(self,cItem):
        page = cItem.get('page',1)
        if page == 1:
            post_data = {'submenue_id':cItem['url'],'catstyle':'carton-movies-01'}
            post_url   = self.Fetch
            sts, data = self.getPage(post_url,post_data=post_data)            
        else:
            url0 = self.MAIN_URL+'/m7b-'+cItem['url']+'&page='+str(page)+'.html'
            sts, data = self.getPage(url0)
        count = 0
        if sts:
            data_list = re.findall('class=\'article\'>.*?<a href=\'(.*?)\'.*?src=\'(.*?)\'.*?title=\'(.*?)\'', data, re.S)
            for (url,image,titre) in data_list:
                printDBG('titre='+titre)
                info   = self.std_title(titre)
                saison = info.get('saison')
                part = info.get('part')
                image = self.MAIN_URL  + image
                image = self.std_url(image)
                if '?url=' in url: x1,url = url.split('?url=',1)
                count = count+1
                self.addDir({'import':cItem['import'],'category' : 'host2','url': url,'title':info.get('title_display'),'sTitle':info.get('title'),'desc':'','icon':image,'mode':'21','good_for_fav':True,'hst':'tshost','saison':saison,'part':part})            
        if count>19:
            self.addDir({'import':cItem['import'],'category' : 'host2','url': cItem['url'],'title':T('Next'),'desc':'','icon':'','hst':'tshost','mode':'20','page':page+1})  
    

    def showitms1(self,cItem):
        data  = cItem.get('data','')
        sts   = True
        next_ = False
        if data=='':
            page = cItem.get('page',1)
            url0 = cItem['url']+ '&page='+str(page)+'.html'
            next_ = True
            sts, data = self.getPage(url0)
        if sts:
            data_list = re.findall('<a href=\'(.*?)\'.*?src=\'(.*?)\'.*?title=\'(.*?)\'', data, re.S)
            for (url,image,titre) in data_list:
                if not (url.endswith('/ar') or url.endswith('.com') or ('مجلة المحب الاطفال' in titre) ):
                    image = self.MAIN_URL + '/ar/' + image
                    if '?url=' in url: x1,url = url.split('?url=',1)
                    printDBG('url====='+url)
                    self.addDir({'import':cItem['import'],'category' : 'host2','url': url,'title':titre,'desc':'','icon':image,'mode':'21','good_for_fav':True})            
        if next_:
            self.addDir({'import':cItem['import'],'category' : 'host2','url': cItem['url'],'title':'Next Page','desc':'','icon':cItem['icon'],'mode':'20','page':page+1})  
    
    def showelms(self,cItem):
        sts, data = self.getPage(cItem['url']) 
        if sts:
            data_list = re.findall('<a data-id=\'(.*?)\'.*?data-idp=\'(.*?)\'.*?data-name=\'(.*?)\'.*?data-post=\'(.*?)\'', data, re.S)
            if data_list:
                for (id_,idp,titre,post_) in data_list:
                    url_post = self.MAIN_URL + '/serv.php'
                    titre = self.std_episode(titre,cItem)
                    self.addVideo({'import':cItem['import'],'good_for_fav':True,'category':'host2', 'url':url_post,'id_':id_,'idp':idp,'titre':titre,'post_':post_, 'desc':cItem['desc'],'title':titre, 'icon':cItem['icon'],'EPG':True,'hst':'tshost'} )
            else:
                data_list = re.findall('class="button-stream".*?href="(.*?)".*?>(.*?)<', data, re.S)
                for (url,titre) in data_list:
                    titre = self.std_episode(titre,cItem)
                    self.addVideo({'import':cItem['import'],'good_for_fav':True,'category':'host2', 'url':url, 'desc':cItem['desc'],'title':titre, 'icon':cItem['icon'],'EPG':True,'hst':'tshost'} )


    def showelms1(self,cItem):
        sts, data = self.getPage(cItem['url']) 
        if sts:
            data_list = re.findall('<a data-id=\'(.*?)\'.*?data-name=\'(.*?)\'.*?data-post=\'(.*?)\'', data, re.S)
            if data_list:
                for (id_,titre,post_) in data_list:
                    url_post = self.MAIN_URL + '/serv.php'
                    url = url_post+'%%%'+id_+'%%%'+titre+'%%%'+post_
                    self.addVideo({'import':cItem['import'],'good_for_fav':True,'category':'host2', 'url':url, 'desc':cItem['desc'],'title':titre, 'icon':cItem['icon'],'EPG':True,'hst':'tshost'} )
            else:
                data_list = re.findall('class="button-stream".*?href="(.*?)".*?>(.*?)<', data, re.S)
                for (url,titre) in data_list:
                    self.addVideo({'import':cItem['import'],'good_for_fav':True,'category':'host2', 'url':url, 'desc':cItem['desc'],'title':titre, 'icon':cItem['icon'],'EPG':True,'hst':'tshost'} )

    def SearchResult(self,str_ch,page,extra):
        elms = []
        url0 = self.MAIN_URL+'/search.php?q='+str_ch+'&page='+str(page)
        sts, data = self.getPage(url0)
        if sts:
            data_list = re.findall('class=\'article\'>.*?image: url\((.*?)\).*?<a href=\'(.*?)\'.*?>(.*?)<', data, re.S)
            for (image,url,titre) in data_list:
                if '?url=' in url: x1,url = url.split('?url=',1)
                printDBG('url====='+url)
                self.addDir({'import':extra,'category' : 'host2','url': url,'title':titre,'desc':'','icon':image,'mode':'21','good_for_fav':True})            

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
                        MainURL = self.MAIN_URL + '/'
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
        return urlTab
    
    def SearchAll(self,str_ch,page=1,extra='',type_='',icon=''):
        elms = []
        url0 = self.MAIN_URL+'/search.php?q='+str_ch+'&page='+str(page)
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
                elms.append({'import':extra,'category' : 'host2','url': url,'title':info.get('title_display'),'sTitle':info.get('title'),'desc':'','icon':image,'mode':'21','good_for_fav':True,'saison':saison,'part':part})            
                nb = nb +1
            if nb>13:
                elm = {'import':extra,'category' : 'host2','title':T('Next'),'url':url,'desc':'next','icon':icon,'mode':'51','good_for_fav':True,'EPG':True,'hst':'tshost','page':page+1,'str_ch':str_ch}
                elms.append(elm)
        return elms               

    def SearchAnims(self,str_ch,page=1,extra='',type_='',icon=''):
        return self.SearchAll(str_ch,page,extra,type_,icon)
