# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, GetTmpDir
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,xtream_get_conf,tscolor
import base64
import re
import os
import os.path
import json

def getinfo():
    info_={}
    info_['name']='Xtream IPTV (LIVE)'
    info_['version']='2.0 22/08/2021'
    info_['dev']='RGYSoft'
    info_['cat_id']='10'
    info_['desc']='مشاهدة القنوات مباشر من اشتراكات xtream'
    info_['icon']='https://i.ibb.co/nPHsSDp/xtream-code-iptv.jpg'
    info_['filtre']='xtream_active'
    info_['recherche_all']='0'
    return info_

class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'xtream.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Linux; Android 4.4.2; SAMSUNG-SM-N900A Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36'
        self.MAIN_URL = ''
        self.HEADER = {'User-Agent': self.USER_AGENT, 'X-Requested-With': 'com.sportstv20.app','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
        self.defaultParams = {'header':self.HEADER, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        
        
    def showmenu0(self,cItem):
        multi_tab=xtream_get_conf()
        if len(multi_tab)==0:
            self.addMarker({'title':'Please configure xstream first','icon':cItem['icon'],'desc':'Please configure xstream first, (add user,pass &host in tsiplayer params or add your config file in /etc/tsiplayer_xtream.conf)'})	
        elif len(multi_tab)==1:
            self.showmenu1({'import':cItem['import'],'icon':cItem['icon'],'xuser':multi_tab[0][2],'xpass':multi_tab[0][3],'xhost':multi_tab[0][1],'xua':multi_tab[0][4]})
        else:	
            for elm in multi_tab:
                self.addDir({'import':cItem['import'],'category' : 'host2','title': elm[0],'icon':cItem['icon'],'xuser':elm[2],'xpass':elm[3],'xhost':elm[1],'xua':elm[4],'mode':'20'})	

    def showmenu1(self,cItem):
        Url=cItem['xhost']+'/player_api.php?username='+cItem['xuser']+'&password='+cItem['xpass']+'&action=get_live_categories'
        printDBG('url='+Url)
        sts, data = self.cm.getPage(Url)
        if sts:
            data = json_loads(data)
            self.addDir({'import':cItem['import'],'category' : 'host2','title':'All','icon':cItem['icon'],'category_id':'','xuser':cItem['xuser'],'xpass':cItem['xpass'],'xhost':cItem['xhost'],'xua':cItem['xua'],'mode':'21'} )
            for elm in data:
                self.addDir({'import':cItem['import'],'category' : 'host2','title':elm['category_name'].strip(),'icon':cItem['icon'],'category_id':elm['category_id'],'xuser':cItem['xuser'],'xpass':cItem['xpass'],'xhost':cItem['xhost'],'xua':cItem['xua'],'mode':'21'} )
        else:
            self.addMarker({'title':'Please verif your config.','icon':cItem['icon'],'desc':'Please verif your config.'})	

    def showchannels(self,cItem):		
        
        Url=cItem['xhost']+'/player_api.php?username='+cItem['xuser']+'&password='+cItem['xpass']+'&action=get_live_streams&category_id='+str(cItem['category_id'])
        sts, data = self.cm.getPage(Url)
        data = json_loads(data)
        for elm in data:
            Url=cItem['xhost']+'/live/'+cItem['xuser']+'/'+cItem['xpass']+'/'+str(elm['stream_id'])+'.ts'
            if cItem['xua']!='': Url  = strwithmeta(Url,{'User-Agent' : cItem['xua']})
            if elm['stream_icon']: stream_icon =elm['stream_icon']
            else: stream_icon = ''
            if '---'in elm['name']:
                self.addMarker({'title':tscolor('\c0000??00')+elm['name'],'icon':cItem['icon']})	
            elif '***'in elm['name']:
                self.addMarker({'title':tscolor('\c00????00')+elm['name'],'icon':cItem['icon']})	
            else:
                opt = False
                if os.path.isfile('/etc/enigma2/ipaudio.json'):
                    opt = True
                if os.path.exists('/etc/enigma2/iptosat.json'):
                    opt = True
                for file in os.listdir("/etc/enigma2"):
                    if ((file.endswith(".tv")) and ('tsiplayer' in file.lower())):
                        opt = True
                        break
                if (opt):
                    self.addDir({'import':cItem['import'],'category' : 'host2','url': Url,'title':elm['name'],'icon':stream_icon,'mode':'22','xuser':cItem['xuser'],'xpass':cItem['xpass'],'xhost':cItem['xhost'],'stream_id':elm['stream_id']})                
                else:
                    self.addVideo({'import':cItem['import'],'category' : 'host2','url': Url,'title':elm['name'],'icon':stream_icon,'hst':'direct','xuser':cItem['xuser'],'xpass':cItem['xpass'],'xhost':cItem['xhost'],'stream_id':elm['stream_id'],'EPG':True,'good_for_fav':True})


    def showoptions(self,cItem):
        self.addVideo({'import':cItem['import'],'category' : 'host2','url': cItem['url'],'title':cItem['title'],'icon':cItem['icon'],'hst':'direct','xuser':cItem['xuser'],'xpass':cItem['xpass'],'xhost':cItem['xhost'],'stream_id':cItem['stream_id'],'EPG':True,'good_for_fav':True})
        if os.path.isfile('/etc/enigma2/ipaudio.json'):
            self.addDir({'import':cItem['import'],'category' : 'host2','url': cItem['url'],'title':'Add to IPAUDIO','titre':cItem['title'],'icon':cItem['icon'],'mode':'23'})                
        if os.path.isfile('/etc/enigma2/iptosat.json'):
            filePath = GetTmpDir('.tsiplayer_channel_name.txt')
            if os.path.exists(filePath):   
                channel_name = ''
                with open(filePath) as f:
                    channel_name = f.read()
                if channel_name.strip() != '':
                    self.addDir({'import':cItem['import'],'category' : 'host2','url': cItem['url'],'channel':channel_name.strip(),'title':'Add to IPTOSAT','titre':cItem['title'],'icon':cItem['icon'],'mode':'25'})                
        for file in os.listdir("/etc/enigma2"):
            if ((file.endswith(".tv")) and ('tsiplayer' in file.lower())):
                self.addDir({'import':cItem['import'],'category' : 'host2','url': cItem['url'],'title':'Add to Enigma2 Fav','titre':cItem['title'],'icon':cItem['icon'],'mode':'24','file':os.path.join("/etc/enigma2", file)})                
                break       
        
    def addtoipaudio(self,cItem):
        try:
            elm = {"channel":cItem['titre'],"url":cItem['url']}
            with open('/etc/enigma2/ipaudio.json', 'r')as f:
                playlist = json.loads(f.read())
            playlist['playlist'].append(elm)
            with open('/etc/enigma2/ipaudio.json', 'w') as f:
                json.dump(playlist, f, indent=4) 
            self.addMarker({'title':tscolor('\c00????00')+'#'+cItem['titre']+'# Successfully added','icon':cItem['icon']})	
        except Exception as e:
            self.addMarker({'title':tscolor('\c00??0000')+'#'+cItem['titre']+'# Not added (Error)','icon':cItem['icon'],'desc':str(e)})	   
        
    def addtoiptosat(self,cItem):
        try:
            elm = {"channel":cItem['channel'],"url":cItem['url']}
            with open('/etc/enigma2/iptosat.json', 'r')as f:
                playlist = json.loads(f.read())
            playlist['playlist'].append(elm)
            with open('/etc/enigma2/iptosat.json', 'w') as f:
                json.dump(playlist, f, indent=4) 
            self.addMarker({'title':tscolor('\c00????00')+'#'+cItem['titre']+'# Successfully added','icon':cItem['icon']})	
        except Exception as e:
            self.addMarker({'title':tscolor('\c00??0000')+'#'+cItem['titre']+'# Not added (Error)','icon':cItem['icon'],'desc':str(e)})	   
        
        
    def addtoenigma2(self,cItem):
        try:
            lines = '#SERVICE 4097:0:19:22CC:434:1:C00000:0:0:0:'+cItem['url'].replace(':','%3a')+':'+cItem['titre']+'\n'
            lines = lines + '#DESCRIPTION '+cItem['titre']+'\n'
            with open(cItem['file'], 'a') as f:
                f.write(lines)    
            Url = 'http://localhost/web/servicelistreload?mode=2'
            sts, data = self.cm.getPage(Url)
            if sts:
                self.addMarker({'title':tscolor('\c00????00')+'#'+cItem['titre']+'# Successfully added','icon':cItem['icon']})	
            else:
                self.addMarker({'title':tscolor('\c00????00')+'#'+cItem['titre']+'# Successfully added (Restart Your Enigma)','icon':cItem['icon']})	
        except Exception as e:
            self.addMarker({'title':tscolor('\c00??0000')+'#'+cItem['titre']+'# Not added (Error)','icon':cItem['icon'],'desc':str(e)})	   
            
        
    def getArticle(self,cItem):
        otherInfo = {}
        desc=''
        title1 = cItem['title']
        icon = cItem.get('icon', '')
        Url=cItem['xhost']+'/player_api.php?username='+cItem['xuser']+'&password='+cItem['xpass']+'&action=get_short_epg&stream_id='+str(cItem['stream_id'])
        sts, data = self.cm.getPage(Url)
        data = json_loads(data)
        for elm in data['epg_listings']:
            time_star=elm['start'].split(' ')[1]
            time_end=elm['end'].split(' ')[1]
            time1,time2,x1=time_star.split(':')
            time_1,time_2,x1=time_end.split(':')
            start_=tscolor('\c0000??00')+'['+time1+':'+time2+' - '+time_1+':'+time_2+']'+tscolor('\c00??????')
            title = tscolor('\c00????00')+base64.b64decode(elm['title'])+tscolor('\c00??????')
            descr = base64.b64decode(elm['description'])
            desc=desc+start_+' | '+title+' | '+descr+'\\n'
        
        printDBG(str(data))
        #desc=str(data)
        #

        return [{'title':title1 , 'text': desc , 'images':[{'title':'', 'url':icon}], 'other_info':otherInfo}]







    def start(self,cItem):
        mode=cItem.get('mode', None)
        if mode=='00':
            self.showmenu0(cItem)	
        if mode=='20':
            self.showmenu1(cItem)			
        elif mode=='21':
            self.showchannels(cItem)
        elif mode=='22':
            self.showoptions(cItem) 
        elif mode=='23':
            self.addtoipaudio(cItem) 
        elif mode=='24':
            self.addtoenigma2(cItem) 
        elif mode=='25':
            self.addtoiptosat(cItem)            
        return True
