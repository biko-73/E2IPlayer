# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools                                 import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools                          import TSCBaseHostClass,tscolor,URLResolver
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.youtubedl_data.youtubeparser   import YouTubeParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.utils                            import QuotePlus
from Components.config                                                             import config
import json,os,re

def getinfo():	
    info_={}
    info_['name']='Youtube'
    info_['version']='1.0 23/06/2021'
    info_['dev']='RGYSOFT'
    info_['cat_id']='902'
    info_['desc']='Youtube'
    info_['icon']='https://i.ibb.co/cgRTW3r/youtube.png'
    return info_
    
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':''})
        self.MAIN_URL = ''
        self.ytp = YouTubeParser()

    def showmenu(self,cItem):
        self.addDir({'import':cItem['import'],'category' : 'host2','url': '','title':'Video','desc':'','icon':cItem['icon'],'mode':'10','type_':'video'})	
        self.addDir({'import':cItem['import'],'category' : 'host2','url': '','title':'Live','desc':'','icon':cItem['icon'],'mode':'10','type_':'live'})	
        self.addDir({'import':cItem['import'],'category' : 'host2','url': '','title':'Playlist','desc':'','icon':cItem['icon'],'mode':'10','type_':'playlist'})	
        self.addDir({'import':cItem['import'],'category' : 'host2','url': '','title':'Channel','desc':'','icon':cItem['icon'],'mode':'10','type_':'channel'})	
 
    def showmenu1(self,cItem):
        type_ = cItem['type_']
        self.addDir({'import':cItem['import'],'category' :'search','title':tscolor('\c00????30') + _('Search'),'search_item':True,'page':type_,'hst':'tshost','icon':cItem['icon']})  
                
    def SearchResult(self,str_ch,page,extra):
        type_ = page
        printDBG('------------->type_ =' + type_)        
        page=0
        tmpList = self.ytp.getSearchResult(QuotePlus(str_ch), type_, page, 'search', config.plugins.iptvplayer.ytSortBy.value)
        printDBG('result ='+str(tmpList))
        self.SetResult(tmpList,extra,type_)
     
    def showitms(self,cItem):
        page    = cItem.get("page", '1')
        url     = cItem.get("url", "")
        str_ch  = cItem.get("str_ch", "")
        type_   = cItem.get("type_", "video")
        tmpList = self.ytp.getSearchResult(QuotePlus(str_ch), type_, page, 'search', config.plugins.iptvplayer.ytSortBy.value,url)
        printDBG('result ='+str(tmpList))
        self.SetResult(tmpList,cItem['import'],type_)

    def showelms(self,cItem):
        printDBG("----------> showelms")
        category = cItem['cat']
        url = cItem.get("url", '')
        page = cItem.get("page", '1')     
        if (category=='channel'):
            if not ('browse' in url) and (not 'ctoken' in url):
                if url.endswith('/videos'):
                    url = url + '?flow=list&view=0&sort=dd'
                else:
                    url = url + '/videos?flow=list&view=0&sort=dd'
            tmpList = self.ytp.getVideosFromChannelList(url, category, page, cItem)
        else:
            tmpList = self.ytp.getVideosFromPlaylist(url, category, page, cItem)
        self.SetResult(tmpList,cItem['import'],'')



    def SetResult(self,tmpList,extra,type_):
        for item in tmpList:
            category = item['category']
            printDBG('item ='+str(item))
            if (category =='search_next_page'):
                item.update({'name': 'category','hst':'tshost','str_ch':'str_ch','category' :'host2','import':extra,'mode':'20','type_':type_})
            elif (category =='playlist') or (category =='channel'):
                item.update({'name': 'category','hst':'tshost','str_ch':'str_ch','category' :'host2','import':extra,'mode':'21','type_':type_,'good_for_fav':True,'cat':category})            
            else:
                item.update({'name': 'category','hst':'none','good_for_fav':True})
            if 'video' == item['type']:
                #self.addVideo(item)
                if ((type_=='live') and (os.path.isfile('/etc/enigma2/ipaudio.json'))):
                    item.update({'name': 'category','category' :'host2','hst':'tshost','good_for_fav':True,'mode':'19','import':extra})
                    self.addDir(item)
                else:
                    self.addVideo(item)
            else:
                self.addDir(item)
                
    def showfilter(self,cItem):
        elm = {'name': 'category','category' :'video','hst':'none','good_for_fav':True,'url':cItem['url'],'title':cItem['title'],'icon':cItem['icon']}
        self.addVideo(elm)
        elm2 = {'name': 'category','category' :'host2','hst':'tshost','url':cItem['url'],'title':'Add To IPAUDIO','titre':cItem['title'],'import':cItem['import'],'mode':'11','icon':cItem['icon']}
        self.addDir(elm2)
        
    def showmenu2(self,cItem):
        videoUrl = cItem['url']
        urlTab = URLResolver(videoUrl).getLinks()
        printDBG('urlTab='+str(urlTab))
        links = []
        i=100
        for elm in urlTab:
            if (elm.get('name','none').startswith('M3U8 ')):
                inf_data = re.findall(' (.*?)P',elm['name'], re.S)
                if inf_data:
                    links.append((int(inf_data[0]),elm['url']))
                else:
                    links.append((i,elm['url']))
                    i=i-1
            else:
                links.append((int(elm['format'].replace('x','')),elm['url']))

        if (links != []):
            links = sorted(links, key=lambda x: x[0])
        try:
            elm01 = {"channel":cItem['titre'],"url":links[0][1]}
            with open('/etc/enigma2/ipaudio.json', 'r') as f:
                playlist = json.loads(f.read())
            playlist['playlist'].append(elm01)
            with open('/etc/enigma2/ipaudio.json', 'w') as f:
                json.dump(playlist, f, indent=4) 
            self.addMarker({'title':tscolor('\c00????00')+'#'+cItem['titre']+'# Successfully added','icon':cItem['icon'],'desc':str(links[0][0])})	
        except Exception as e:
            self.addMarker({'title':tscolor('\c00??0000')+'#'+cItem['titre']+'# Not added (Error)','icon':cItem['icon'],'desc':str(e)})	   

        #self.addMarker({'category':'Marker','title': tscolor('\c00????30') + 'Added OK','desc':str(links[0][0])})
