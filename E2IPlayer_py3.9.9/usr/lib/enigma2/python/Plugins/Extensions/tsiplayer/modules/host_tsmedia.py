# -*- coding: utf-8 -*-
###################################################
from Plugins.Extensions.IPTVPlayer.tools.iptvtools             import printDBG,GetTmpDir
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools      import TSCBaseHostClass,tscolor
from Plugins.Extensions.IPTVPlayer.components.e2ivkselector import GetVirtualKeyboard
###################################################
from os import remove as os_remove, path as os_path, system as os_system
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Components.config import config
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.urlparser    import urlparser as ts_urlparser
from Plugins.Extensions.IPTVPlayer.libs.urlparser              import urlparser
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads
import json
###################################################
import re,sys,inspect,os
###################################################

def getinfo():
    version_f='/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/libs/tsmedia/version'
    if not os.path.exists(version_f): version_f='/usr/lib/enigma2/python/Plugins/Extensions/TSmedia/version'
    if os.path.exists(version_f):
        with open(version_f) as f:
            lines = f.readlines()
        version = lines[0].split(':')[1].strip()		
        info_={}
        info_['name']='TSMedia'
        info_['version']='2.0 20/10/2020'+' | '+tscolor('\c0000????')+version+ ' (TSMedia)'
        info_['dev']='mfaraj57 + TSmedia Team'
        info_['cat_id']='903'
        info_['desc']='TSMedia Enigma2 Addon'
        info_['icon']='https://i.ibb.co/tH06msx/img1.png'
    else:
        info_={}
        info_['name']='TSMedia'
        info_['version']='Not Installed'
        info_['dev']='mfaraj57 + TSmedia Team'
        info_['cat_id']='99'
        info_['desc']='TSMedia Enigma2 Addon'
        info_['icon']='https://i.ibb.co/tH06msx/img1.png'        
    return info_

    
    
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'tsiplayer.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
        self.MAIN_URL = 'https://gitlab.com'
        self.HTTP_HEADER = {'User-Agent': self.USER_AGENT}
        self.defaultParams = {'header':self.HTTP_HEADER}
        self.getPage = self.cm.getPage
        if config.plugins.iptvplayer.tsi_resolver.value=='tsiplayer':
            self.ts_up = ts_urlparser()
        else:
            self.ts_up = urlparser()
        path0='/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/libs/tsmedia/'
        if not os.path.exists(path0): path0='/usr/lib/enigma2/python/Plugins/Extensions/TSmedia/scripts/'		
        paths = ['main/lib','main/lib/libs']	
        for path in paths:
            printDBG('path added:'+path0+path)
            if path0+path not in sys.path: sys.path.append(path0+path) 


    def PrintExTs(self,e):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        inf_ = str(fname)+' ('+ str(exc_tb.tb_lineno)+')\n'+str(type(e).__name__)+' ('+str(e)+')\n'
        frm = inspect.trace()[-1]
        mod = inspect.getmodule(frm[0])
        (filename, line_number,function_name, lines, index) = inspect.getframeinfo(frm[0])			
        filename = filename.replace('/usr/lib/enigma2/python/Plugins/Extensions/','>> ')
        inf_ = inf_+'FileName: '+str(filename)+' ('+str(line_number)+')\n'
        inf_ = inf_+'Function: '+str(function_name)+'\n'
        try:
            inf_ = inf_+'Line: '+str(lines[index]).strip()
        except:
            pass
        self.addMarker({'title':tscolor('\c00????00')+'----> Erreur <----','icon':'','desc':inf_})

                                 
    def showmenu0(self,cItem):
        img=cItem['icon']
        #folder='/usr/lib/enigma2/python/Plugins/Extensions/TSmedia/addons'
        folders=['/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/libs/tsmedia/addons','/usr/lib/enigma2/python/Plugins/Extensions/TSmedia/addons']
        for folder in folders:
            lst=[]
            if os.path.exists(folder):
                if '/tsiplayer/' in folder:
                    self.addMarker({'category' :'marker','title':tscolor('\c00????00')+' -----●★| Local Hosts |★●-----','desc':''})	
                else: self.addMarker({'category' :'marker','title':tscolor('\c00????00')+' -----●★| TSMedia Hosts |★●-----','desc':''})	
                lst=os.listdir(folder)
                for (dir_) in lst:
                    if ('.py' not in dir_)and('youtube' not in dir_)and('programs' not in dir_):
                        folder2=folder+'/'+dir_
                        lst2=[]
                        lst2=os.listdir(folder2)
                        if (len(lst2)>1):			
                            self.addDir({'import':cItem['import'],'category' :'host2','title':dir_.upper(),'desc':cItem['desc'],'icon':img,'folder':folder2,'section':dir_,'mode':'10'})			

    def showmenu1(self,cItem):
        folder=cItem['folder']
        img=cItem['icon']
        lst=[]
        lst=os.listdir(folder)
        for (dir_) in lst:
            if ('.py' not in dir_):
                folder2=folder+'/'+dir_	
                img1='file://'+folder2+'/icon.png'
                version=folder2+'/addon.xml'
                version1=folder2+'/params'
                desc=''
                titre=dir_.upper()
                if os.path.exists(version1):
                    f = open(version1, 'r')
                    Lines = f.readlines() 						
                    for line in Lines: 
                        if ('plugin_title' in line) and ('==' in line): titre = line.split('==',1)[1].strip()
                        if ('version' in line) and ('==' in line): desc=desc+tscolor('\c00????00')+'Version:'+tscolor('\c00??????')+' '+line.split('==',1)[1].strip()+'\\n'
                        if ('plugin_id' in line) and ('==' in line): desc+tscolor('\c00????00')+'ID:'+tscolor('\c00??????')+' '+line.split('==',1)[1].strip()+'\\n'
                        if ('provider' in line) and ('==' in line): desc+tscolor('\c00????00')+'Provider Name:'+tscolor('\c00??????')+' '+line.split('==',1)[1].strip()+'\\n'
                        if ('source' in line) and ('==' in line): desc+tscolor('\c00????00')+'Source:'+tscolor('\c00??????')+' '+line.split('==',1)[1].strip()+'\\n'
                        if ('description' in line) and ('==' in line): desc+tscolor('\c00????00')+'Description:'+tscolor('\c00??????')+' '+line.split('==',1)[1].strip()+'\\n'
                else:
                    if os.path.exists(version):	
                        with open(version) as f:
                            content = f.read()	
                        inf_list = re.findall('id.*?"(.*?)".*?version.*?"(.*?)".*?name.*?"(.*?)".*?name.*?"(.*?)".*?<description>(.*?)</description>', content, re.S)
                        if inf_list: 
                            desc=tscolor('\c00????00')+'Version:'+tscolor('\c00??????')+' '+inf_list[0][1]+'\\n'
                            desc=desc+tscolor('\c00????00')+'ID:'+tscolor('\c00??????')+' '+inf_list[0][0]+'\\n'
                            desc=desc+tscolor('\c00????00')+'Provider Name:'+tscolor('\c00??????')+' '+inf_list[0][3]+'\\n'
                            desc=desc+tscolor('\c00????00')+'Description:'+tscolor('\c00??????')+' '+inf_list[0][4].strip()+'\\n'
                            titre=inf_list[0][2].strip()
                self.addDir({'import':cItem['import'],'category' :'host2','title':titre,'desc':desc,'icon':img1,'py_file':folder2+'/default.py','section':cItem['section'],'plugin_id':dir_,'mode':'20'})	

    def getitems(self,cItem):
        printDBG('Start Get items from:'+str(cItem))
        section_   = cItem['section']
        plugin_id_ = cItem['plugin_id']					
        py_file    = cItem['py_file']
        argv2      = cItem.get('argv2','{}')
        argv       = cItem.get('argv',{})
        type_      = cItem.get('type_','')
        lst        = []	
        sys.argv   = [py_file,'1',argv2,'']
        if type_=='search':
            printDBG('11111')
            ret = self.sessionEx.waitForFinishOpen(GetVirtualKeyboard(), title=_('Set file name'))
            printDBG('22222')
            input_txt = ret[0]
            if not isinstance(input_txt, basestring): input_txt =''
            if not os.path.exists('/tmp/TSmedia'): os.makedirs('/tmp/TSmedia')
            file = open('/tmp/TSmedia/searchSTR', 'w')
            file.write(input_txt)
            file.close()
            file = open('/tmp/TSmedia/searchSTR.txt', 'w')
            file.write(input_txt)
            file.close()		
        try:
            if '/tsiplayer/' in py_file:
                import_    = 'from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tsmedia.addons.' + section_ + '.' + plugin_id_ + '.default import start'			
            else:
                import_    = 'from Plugins.Extensions.TSmedia.addons.' + section_ + '.' + plugin_id_ + '.default import start'
            exec (import_)
            printDBG('argv:'+str(argv)+'#')
            lst=start(argv)
            printDBG(str(lst))
        except Exception as e:
            lst=None
            self.PrintExTs(e)
        if lst:
            self.tsmedia_getlist(lst,cItem)

    def tsmedia_getlist(self,lst,cItem):
        img=cItem['icon']
        for elm in lst:  
            titre=elm.get('title','')
            if titre=='':
                titre=elm.get('name','')
            img_=elm['image']
            if img_.startswith('/usr/'):
                img_ = img_.replace('/IPTVPlayer/tsiplayer/libs/tsmedia/main/lib/iTools.py','/TSmedia')
                printDBG('img_='+img_)
                if os.path.exists(img_):
                    img_='file://'+img_
                else:
                    img_=cItem['icon']
            img_=img_.replace('TSmedia//interface','TSmedia/interface')
            img_=img_.replace('TSmedia//','TSmedia/addons/')
            desc_=elm['desc']
            url_=elm['url']
            mode_=elm['mode']
            printDBG('elm'+str(elm))
            type_ =''
            if str(mode_)=='103' or str(mode_)=='603' or str(mode_)=='703' or str(mode_)=='803':
                type_='search'
            
                #URL=cItem['section']+'|'+cItem['plugin_id']+'|'+cItem['py_file']+'|'+str(elm)
                #self.addDir({'category':'search'  ,'title': _('Search'),'search_item':True,'page':-1,'hst':'tsmedia','url':URL,'icon':img})				
            if ('plugin.video.youtube' in url_) and  ('&videoid=' in url_):
                self.addVideo({'good_for_fav':True,'category' : 'video','hst':'none','title':titre,'url':'https://www.youtube.com/watch?v='+url_.split('&videoid=',1)[1],'desc':desc_,'icon':cItem['icon']})
            elif mode_==0:
                if 'youtube' in url_:
                    self.addVideo({'import':cItem['import'],'category' : 'video','good_for_fav':True,'hst':'none','title':titre,'url':url_,'desc':desc_,'icon':cItem['icon']})				
                else:
                    self.addVideo({'import':cItem['import'],'category' : 'video','good_for_fav':True,'hst':'direct','title':titre,'url':url_,'desc':desc_,'icon':cItem['icon']})	
            elif (self.ts_up.checkHostSupport(url_) == 1) and config.plugins.iptvplayer.ts_resolver.value=='tsiplayer':
                URL=url_
                img_ = self.std_url(img_)
                self.addVideo({'import':cItem['import'],'category' : 'video','good_for_fav':True,'hst':'none','title':titre.title().replace('\C0','\c0'),'url':URL,'desc':desc_,'icon':cItem['icon'],'py_file':cItem['py_file'],'section':cItem['section'],'plugin_id':cItem['plugin_id'],'argv2':str(elm),'gnr':'menu2',})					
            else:
                img_ = self.std_url(img_)
                self.addDir({'import':cItem['import'],'category' :'host2','good_for_fav':True,'argv2':str(elm),'argv':elm,'title':titre.title().replace('\C0','\c0'),'desc':desc_,'icon':img_,'py_file':cItem['py_file'],'section':cItem['section'],'plugin_id':cItem['plugin_id'],'type_':type_,'mode':'20',})		



    def start(self,cItem):      
        mode=cItem.get('mode', None)
        if mode=='00':
            self.showmenu0(cItem)
        if mode=='10':
            self.showmenu1(cItem)	
        if mode=='20':
            self.getitems(cItem)
            
