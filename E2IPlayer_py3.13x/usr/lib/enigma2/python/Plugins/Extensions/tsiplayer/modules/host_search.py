# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, GetCacheSubDir
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,TsThread,T
from Plugins.Extensions.IPTVPlayer.components.e2ivkselector import GetVirtualKeyboard
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import GetIPTVSleep
from Components.config import config
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.utils import IsPython3
try:
    import _thread
except:
    pass

from threading import Thread

try:
    from utils.emu_tools import change_code
    from tsIplayer_emu import my_exec
    
except:
    pass
    
import re,os,time

def getinfo():
    info_={}
    info_['name']=tscolor('\c0030??30')+'>> Search ALL <<' + tscolor('\c00??????')
    info_['version']='2.0 26/02/2023'
    info_['dev']='RGYSoft'
    info_['cat_id']='904'
    info_['desc']='Search in ALL Hosts'
    info_['icon']='https://i.ibb.co/rfPB0v5/database-icon-4.png'	
    return info_

class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'tsiplayer.cookie'})
        self.host_folder  = '/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer'
        self.import_      = 'Plugins.Extensions.IPTVPlayer.tsiplayer.'
        self.elms         = []
        self.MyPath       = GetCacheSubDir('Tsiplayer')

    
    def showmenu0(self,cItem):
        self.addDir({'category' : 'host2','title':'ALL','desc':'','icon':cItem['icon'],'mode':'01','import':cItem['import'],'section':''})			
        self.addDir({'category' : 'host2','title':'Films','desc':'','icon':cItem['icon'],'mode':'01','import':cItem['import'],'section':'movie'})			
        self.addDir({'category' : 'host2','title':'Series','desc':'','icon':cItem['icon'],'mode':'01','import':cItem['import'],'section':'serie'})			
        self.addDir({'category' : 'host2','title':'Anims','desc':'','icon':cItem['icon'],'mode':'01','import':cItem['import'],'section':'anime'})			

    def searchResult(self,cItem):
        str_ch  = cItem.get('str_ch','')
        if str_ch == '': 
            txt_def = ''
            if os.path.isfile(self.MyPath +'searchSTR'):
                with open(self.MyPath + 'searchSTR','r') as f:
                    txt_def = f.read().strip()           
            ret = self.sessionEx.waitForFinishOpen(GetVirtualKeyboard(), title=('Search Text:'), text = txt_def)
            str_ch = ret[0]
            if not str_ch: return []
            try:
                basestring
            except NameError:
                basestring = str
            if isinstance(str_ch, basestring):
                file = open(self.MyPath + 'searchSTR', 'w')
                file.write(str_ch)
                file.close() 
        page    = cItem.get('page',1)
        section = cItem.get('section','')
        import_ = cItem.get('import','')
        self.SearchAll(str_ch,page,section,import_)       
        self.addMarker({'title':tscolor('\c00????00')+'Results for: '+tscolor('\c0030??30')+str_ch+tscolor('\c00????00')+' (page:'+str(page)+')','desc':'','icon':''})
        count = 1
        nb_total = 0
        for (elm0,titre) in self.elms:
            #print(elm)
            elm = []
            if elm0 != []:
                for i in elm0:
                    if i.get('title','') != T('Next'):
                        elm.append(i)
                nb = len(elm)
                if nb>1:
                    title = tscolor('\c00????00')+str(count)+'. '+tscolor('\c00??30??')+ titre + tscolor('\c00??????')+  ' ('+ tscolor('\c00??2020')+str(nb)+tscolor('\c00??????')+' items found)'
                    count = count + 1
                    self.addMarker({'title':title,'desc':'','icon':''})
                    for itm in elm:
                        nb_total = nb_total +1 
                        #printDBG('itm='+str(itm))
                        if itm.get('type','') == 'video':
                            self.addVideo(itm)
                        else: self.addDir(itm)
        printDBG ('nbnbnbnbnb= ' + str(nb_total))
        if count>1:
            self.addDir({'category' : 'host2','title':T('Next'),'desc':'','icon':cItem['icon'],'mode':'01','import':cItem['import'],'section':cItem['section'],'str_ch':str_ch,'page':page+1})			            
        else:
            self.addMarker({'title':tscolor('\c00??5050')+'no items found','desc':'','icon':''})
        self.elms = []

    def SearchAll(self,str_ch,page=1,section='',import_=''):
        elms = []
        if   section == '':       fnc = 'SearchAll'
        elif section == 'movie':  fnc = 'SearchMovies'
        elif section == 'serie':  fnc = 'SearchSeries'
        elif section == 'anime':  fnc = 'SearchAnims'
        self.elms = []
        lst     = os.listdir(self.host_folder)
        lst.sort()
        threads = []
        for (file_) in lst:
            if (file_.endswith('.py'))and(file_.startswith('host_')and ('host_search' not in file_)):
                file_       = file_.replace('.py','')
                import_str  = self.import_ + file_
                emu = False
                if import_str.startswith('hosts'): emu = True
                threading = True
                if threading:
                    t = Thread(target=self.get_host_result, args=(import_str,file_,fnc,str_ch,page,emu,))
                    t.start()
                    threads.append(t)
                else:
                    self.get_host_result(import_str,file_,fnc,str_ch,page,emu) 
                    threads = []

        for t in threads:
            t.join(timeout=3) 

        #time.sleep(10)
                #self.get_host_result(import_str,file_,fnc,str_ch,page,emu)      

    def get_host_result(self,import_str,file_,fnc,str_ch,page = 1,emu=False):
        #printDBG ('file_: ' + file_)
        elm   = []
        name = file_        
        if emu:
            file_path = 'hosts/'+file_+'.py'
            with open(file_path,'r',encoding='utf-8') as f:
                contents = f.read()
                mycode   = change_code(contents) 
            try:
                exec(mycode, globals(),None)
                hst   = TSIPHost()
                name  = getinfo()['name']
            except:
                hst = None
                printDBG ('Host Problem 0: ' + file_)
        else:
            _temp       = __import__(import_str, globals(), locals(), ['getinfo'], 0)  
            name        = _temp.getinfo()['name']
            hst         = _temp.TSIPHost()
        if hst:
            try:
                fnc_        = getattr(hst, fnc)
                import_str  = 'from '+import_str+' import '        
                elm         = fnc_(str_ch,page,import_str) 
                if not elm: elm = []         
            except AttributeError:
                elm   = []
            except Exception as err:  
                elm   = []
                printDBG ('Host Problem 1: ' + file_ + ' ER:'+str(err))
        self.elms.append((elm,name))       
              
            
    def start(self,cItem):
        list_=[]
        mode=cItem.get('mode', None)
        if mode=='00':
            list_ = self.showmenu0(cItem)	
        if mode=='01':
            list_ = self.searchResult(cItem)	
        return True
    










    
    def showmenu1(self,cItem):
        try:
            basestring
        except NameError:
            basestring = str
        type_  = cItem.get('gnr','')
        cat_id_filtre=[]
        if type_=='ar': cat_id_filtre=['21']
        if type_=='fr': cat_id_filtre=['31']
        if type_=='en': cat_id_filtre=['41']
        self.list=[]
        if config.plugins.iptvplayer.xtream_active.value=='Yes': cat_id_filtre.append('101')
        str_ch = cItem.get('str_ch','NoneNone')
        page   = cItem.get('page',1)
        if str_ch=='NoneNone':
            ret = self.sessionEx.waitForFinishOpen(GetVirtualKeyboard(), title=_('Set file name'))
            if isinstance(ret[0], basestring): str_ch=ret[0]
            else:
                self.addMarker({'title':'String Search Not Valid !!'})
                return
        folder  = '/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer'
        import_ = 'Plugins.Extensions.IPTVPlayer.tsiplayer.'
        lst     = []
        lst     = os.listdir(folder)
        lst.sort()
        threads = []
        for (file_) in lst:
            if (file_.endswith('.py'))and(file_.startswith('host_')):
                #try:
                path_       = folder+'/'+file_
                file_ = file_.replace('.py','')
                import_str  = import_+file_
                _temp       = __import__(import_str, globals(), locals(), ['getinfo'], 0)
                info        = _temp.getinfo()
                search      = info.get('recherche_all', '0')	
                cat_id      = info.get('cat_id', '0')
                name        = info['name']
                if 	(cat_id in cat_id_filtre)and(search!='0'):	
                    printDBG('--------------> Recherche '+name+'<----------------')
                    if IsPython3():
                        _thread.start_new_thread( self.get_results, (import_str,str_ch,page,name,file_,) )
                    else:
                        threads.append(TsThread(self.get_results,import_str,str_ch,page,name,file_))
                    
                #except:
                #printDBG('--------------> Error '+file_+'<----------------')
        if IsPython3():
            GetIPTVSleep().Sleep(11)
        else:
            for i in threads:
                i.start()
                i.join(timeout=2)
      
        #GetIPTVSleep().Sleep(3)    
        #[i.start() for i in threads]
        #[i.join(timeout=2)  for i in threads]	
        for elm in self.list:
            if elm.get('category' ,'')=='video':
                self.addVideo(elm)
            elif elm.get('category' ,'')=='mark':
                self.addMarker(elm)
            else:
                self.addDir(elm)
        self.addDir({'category' : 'host2','title':tscolor('\c0000??00')+'Next','str_ch':str_ch,'desc':'','icon':cItem['icon'],'mode':'00','import':cItem['import'],'gnr':type_})			
        
    def get_results(self,import_str,str_ch,page,name,file_):
        printDBG('--------------> start '+name+'<----------------')
        _temp = __import__(import_str, globals(), locals(), ['TSIPHost'], 0)
        host_ = _temp.TSIPHost()
        host_.currList=[]
        host_.SearchResult(str_ch,page,extra='')
        lst = host_.currList
        import_str = 'from '+import_str+' import '
        lst.insert(0,{'title':tscolor('\c00????00')+' ----> '+name+' <----','category' : 'mark'})
        for elm in lst:
            elm['import']=import_str
            #elm['title']=name+'|'+elm['title']
            self.list.append(elm)

