# -*- coding: utf-8 -*-
###################################################
from Plugins.Extensions.IPTVPlayer.tools.iptvtools             import printDBG,GetTmpDir
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools      import TSCBaseHostClass,tscolor
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.utils        import download_url
###################################################
from os import remove as os_remove, path as os_path, system as os_system
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
###################################################
import re
###################################################

def getinfo():
    info_={}
    info_['name']='TSIPlayer INFO'
    info_['name2']='-----●★| NEW UPDATE |★●-----'
    info_['version']='1.0 11/11/2019'
    info_['dev']='RGYSoft'
    info_['cat_id']='901'
    info_['desc']='Info & Update'
    info_['icon']='https://i.ibb.co/Q8ZRP0X/yaq9y3ab.png'
    info_['icon2']='https://i.ibb.co/fVR0HL6/tsiplayer-update.png'
    return info_

    
    
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'tsiplayer.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
        self.MAIN_URL = 'https://gitlab.com'
        self.HTTP_HEADER = {'User-Agent': self.USER_AGENT}
        self.defaultParams = {'header':self.HTTP_HEADER}
        self.getPage = self.cm.getPage
        self.tsiplayerversion = 'xxxx.xx.xx.x'
        self.tsiplayerremote = 'xxxx.xx.xx.x'

    def GetVersions(self):
        printDBG( 'GetVersions begin' )
        #get tsiplayerversion
        _file = '/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/version.py'
        try:
            with open(_file) as f:
                data = f.read()
            vers_data = re.findall('="(.*?)"', data, re.S)
            if vers_data:
                printDBG( 'tsiplayerversion = '+vers_data[0] )
                self.tsiplayerversion=vers_data[0]			
        except:
            pass
        
        #get tsiplayerremote
        _url = 'https://gitlab.com/Rgysoft/iptv-host-e2iplayer/raw/master/IPTVPlayer/tsiplayer/version.py'
        try:
            sts,data = self.getPage(_url)
            if sts:
                vers_data = re.findall('="(.*?)"', data, re.S)
                if vers_data:
                    printDBG( 'tsiplayerremote = '+vers_data[0] )
                    self.tsiplayerremote=vers_data[0]
        except:
            pass	
                                 
    def showmenu0(self,cItem):
        self.GetVersions()
        params = {'title':'Local version: '+str(self.tsiplayerversion)+'  |  '+'Remote version: '+str(self.tsiplayerremote),'desc':'Version'} 
        self.addMarker(params)		
        if (self.tsiplayerversion != self.tsiplayerremote) and (self.tsiplayerremote!='xxxx.xx.xx.x'):
            self.addDir({'import':cItem['import'],'category' : 'host2','fnc' : 'update_now_tar','title':tscolor('\c0000????')+' +++++++ UPDATE & RESTART ( '+tscolor('\c00????00')+'TAR Method'+tscolor('\c0000????')+' ) +++++++ ','restart':True,'mode':'10'})	
            self.addDir({'import':cItem['import'],'category' : 'host2','fnc' : 'update_now_zip','title':tscolor('\c0000????')+' +++++++ UPDATE & RESTART ( '+tscolor('\c00????00')+'ZIP Method'+tscolor('\c0000????')+' ) +++++++ ','restart':True,'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','fnc' : 'GetCommits','title':"What's New",'name':'update','mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','fnc' : 'contact','title':'Contact Us','name':'contact','mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','fnc' : 'thx','title':'Thanks','name':'thx','mode':'10'}) 		 


    def GetCommits(self,cItem):
        printDBG( 'GetCommits begin' )
        try:
            data = self.cm.getURLRequestData({ 'url': 'https://gitlab.com/Rgysoft/iptv-host-e2iplayer/commits/master.atom', 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True })
        except:
            printDBG( 'Host listsItems query error' )
        printDBG( 'Host listsItems data: '+data )
        phCats = re.findall("<entry>.*?<title>(.*?)</title>.*?<updated>(.*?)</updated>.*?<name>(.*?)</name>", data, re.S)
        if phCats:
            for (phTitle, phUpdated, phName ) in phCats:
                phUpdated = phUpdated.replace('T', '   ')
                phUpdated = phUpdated.replace('Z', '   ')
                phUpdated = phUpdated.replace('+01:00', '   ')
                phUpdated = phUpdated.replace('+02:00', '   ')
                printDBG( 'Host listsItems phTitle: '+phTitle )
                printDBG( 'Host listsItems phUpdated: '+phUpdated )
                printDBG( 'Host listsItems phName: '+phName )
                params = {'category' : 'none','title':phUpdated+'|  '+phTitle,'desc':phUpdated+' '+phName+'  >>  '+phTitle,'name':'update'} 
                self.addMarker(params)	
                
    def contact(self,cItem):
        desc = 'For all requests (new hosts, correction & improvement)'
        self.addMarker({'title':tscolor('\c0000??00')+' eMail: '+tscolor('\c00??????')+' rgysoft@mail.ru','desc':desc})	
        self.addMarker({'title':tscolor('\c0000??00')+' Tunisia Sat: '+tscolor('\c00??????')+' https://www.tunisia-sat.com/forums/threads/3951696/','desc':desc})	
        self.addMarker({'title':tscolor('\c0000??00')+' Facebook: '+tscolor('\c00??????')+' https://www.facebook.com/E2TSIPlayer/','desc':desc})	

    def thx(self,cItem):
        self.addMarker({'title':'Special thank to '+tscolor('\c0000??00')+' samsamsam '+tscolor('\c00??????')+' the Main developer & all Developer Team','desc':''})	
        self.addMarker({'title':'Special thank to '+tscolor('\c0000????')+' mamrot '+tscolor('\c00??????')+' & '+tscolor('\c0000????')+' mosz_nowy '+tscolor('\c00??????')+' (update script)','desc':''})	
    
    def update_now_tar(self,cItem):
        restart=cItem.get('retstart',True)
        printDBG('TSIplayer: Start Update' )
        
        
        
        
        #crc=''
        #_url = 'https://gitlab.com/Rgysoft/iptv-host-e2iplayer'
        #try:
        #	crc_data = re.findall('/Rgysoft/iptv-host-e2iplayer/commit/([^"^\']+?)[\'"]',self.cm.getPage(_url)[1], re.S)
        #	if crc_data:
        #		crc=crc_data[0]
        #		printDBG('TSIplayer: crc = '+crc)
        #	else: printDBG('TSIplayer: crc not found') 
        #except:
        #	printDBG('TSIplayer: Get Main URL Error')		
        #	return ''		
        
        
        #crc=''
        #_url = 'https://gitlab.com/Rgysoft/iptv-host-e2iplayer/-/refs/master/logs_tree/?format=json&o'
        #try:
        #    crc_data = re.findall('commit.*?id":"(.*?)"',self.cm.getPage(_url)[1], re.S)
        #    if crc_data:
        #        crc=crc_data[0]
        #        printDBG('TSIplayer: crc = '+crc)
        #    else: printDBG('TSIplayer: crc not found')  
        #except:
        #    printDBG('TSIplayer: Get Main URL Error')		
        #    return ''		
        
        
        
        
        
        
        
        tmpDir = GetTmpDir() 
        source = os_path.join(tmpDir, 'iptv-host-e2iplayer.tar.gz') 
        dest = os_path.join(tmpDir , '') 
        #_url = 'https://gitlab.com/Rgysoft/iptv-host-e2iplayer/repository/archive.tar.gz?ref=master' 
        _url = 'https://gitlab.com/Rgysoft/iptv-host-e2iplayer/-/archive/master/iptv-host-e2iplayer-master.tar.gz'
        try:
            download_url(_url,source)
            #output = open(source,'wb')
            #output.write(self.getPage(_url)[1])
            #output.close() 
            os_system ('sync')
            printDBG('TSIplayer: Download iptv-host-e2iplayer.tar.gz OK' )
        except:
            if os_path.exists(source): os_remove(source)
            printDBG('TSIplayer: Download Error iptv-host-e2iplayer.tar.gz' )	
            return ''
        
        cmd = 'tar -xzf "%s" -C "%s" 2>&1' % ( source, dest )  
        try: 
            os_system (cmd)
            os_system ('sync')
            printDBG('TSIplayer: Unpacking OK' )
        except:
            printDBG( 'TSIplayer: Unpacking Error' )
            os_system ('rm -f %s' % source)
            os_system ('rm -rf %siptv-host-e2iplayer' % (dest))
            return ''

        try:
            od = '%siptv-host-e2iplayer-master/'% (dest)
            do = resolveFilename(SCOPE_PLUGINS, 'Extensions/') 
            cmd = 'cp -rf "%s"/* "%s"/ 2>&1' % (os_path.join(od, 'IPTVPlayer'), os_path.join(do, 'IPTVPlayer'))
            printDBG('<<<<<<<<<<<<<<<<<<<<<<<<<<cmd='+cmd)
            os_system (cmd)
            os_system ('sync')
            printDBG('TSIplayer: Copy OK')		
        except:
            printDBG('TSIplayer: Copy Error')
            os_system ('rm -f %s' % source)
            os_system ('rm -rf %siptv-host-e2iplayer-master' % (dest))
            return ''

        #printDBG( 'TSIplayer: Deleting temporary files' )
        #os_system ('rm -f %s' % source)
        #os_system ('rm -rf %siptv-host-e2iplayer-master-%s' % (dest, crc))

         
        if restart:
            try:			
                from enigma import quitMainloop
                quitMainloop(3)
            except Exception as e:
                printDBG( 'TSIplayer: Erreur='+str(e) )				
                pass			
             
        params = {'category' : 'none','title':'Update End. Please manual restart enigma2','name':'update'} 
        self.addDir(params)				  
        return ''
        
    def update_now_zip(self,cItem):
        restart=cItem.get('retstart',True)
        printDBG('TSIplayer: Start Update' )

        tmpDir = GetTmpDir() 
        source = os_path.join(tmpDir, 'archive.zip') 
        dest = os_path.join(tmpDir , '') 
        #_url = 'https://gitlab.com/Rgysoft/iptv-host-e2iplayer/repository/archive.zip' 
        _url = 'https://gitlab.com/Rgysoft/iptv-host-e2iplayer/-/archive/master/iptv-host-e2iplayer-master.zip' 
        try:
        
            download_url(_url,source)
            #output = open(source,'w')
            #output.write(self.cm.getPage(_url)[1])
            #output.close() 
            os_system ('sync')
            printDBG('TSIplayer: Download archive.zip OK' )
        except:
            if os_path.exists(source): os_remove(source)
            printDBG('TSIplayer: Download Error archive.zip' )	
            return ''
        
        cmd = 'unzip -o "%s" -d "%s"'  % ( source, dest )
        try: 
            os_system (cmd)
            os_system ('sync')
            printDBG('TSIplayer(zip): Unpacking OK' )
        except:
            printDBG( 'TSIplayer(zip): Unpacking Error' )
            os_system ('rm -f %s' % source)
            os_system ('rm -rf /tmp/iptv-host-e2iplayer*/IPTVPlayer')
            return ''
            
        try:
            os_system ('cp -rf /tmp/iptv-host-e2iplayer*/IPTVPlayer /usr/lib/enigma2/python/Plugins/Extensions')
            os_system ('sync')
            printDBG('TSIplayer(Zip): Copy OK')			
        except:
            printDBG('TSIplayer(Zip): Copy Error')
            os_system ('rm -f %s' % source)
            os_system ('rm -rf /tmp/iptv-host-e2iplayer*/IPTVPlayer')
            return ''

        printDBG( 'TSIplayer: Deleting temporary files' )
        os_system ('rm -f %s' % source)
        os_system ('rm -rf /tmp/iptv-host-e2iplayer*/IPTVPlayer')

         
        if restart:
            try:			
                from enigma import quitMainloop
                quitMainloop(3)
            except Exception as e:
                printDBG( 'TSIplayer: Erreur='+str(e) )				
                pass			
             
             
        params = {'category' : 'none','title':'Update End. Please manual restart enigma2','name':'update'} 
        self.addDir(params)				  
        return ''


    def start(self,cItem):      
        mode=cItem.get('mode', None)
        if mode=='00':
            self.showmenu0(cItem)
        if mode=='10':
            exec('self.'+cItem['fnc']+'(cItem)')	
