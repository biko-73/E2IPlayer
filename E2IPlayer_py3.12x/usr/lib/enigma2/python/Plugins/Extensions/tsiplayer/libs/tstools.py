# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit    import TranslateTXT as _, GetIPTVNotify
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes              import strwithmeta
from Plugins.Extensions.IPTVPlayer.components.asynccall         import MainSessionWrapper
from Plugins.Extensions.IPTVPlayer.components.e2ivkselector import GetVirtualKeyboard

#from Plugins.Extensions.IPTVPlayer.libs.pCommon                import common, CParsingHelper 
from Plugins.Extensions.IPTVPlayer.libs.urlparser               import urlparser
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.urlparser     import urlparser as ts_urlparser
from Plugins.Extensions.IPTVPlayer.tools.iptvtools              import CSearchHistoryHelper, GetCookieDir, printDBG, printExc, GetCacheSubDir
from Plugins.Extensions.IPTVPlayer.libs.e2ijson                 import loads as json_loads, dumps as json_dumps
from Plugins.Extensions.IPTVPlayer.libs.crypto.cipher.aes_cbc   import AES_CBC
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.utils         import string_escape
from Components.config import config
import os
import re
import base64
import hashlib
import time

from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.utils import IsPython3    

if IsPython3():
    from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.pCommon3       import common, CParsingHelper
    import urllib.parse as urllib
else:
    from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.pCommon2       import common, CParsingHelper
    import urllib2
    import urllib

import threading
import sys

black,white,gray='\c00000000','\c00??????','\c00808080'
blue,green,red,yellow,cyan,magenta='\c000000??','\c0000??00','\c00??0000','\c00????00','\c0000????','\c00??00??'

tunisia_gouv = [("", "None"),("Tunis","Tunis"),("Ariana","Ariana"),("Béja","Béja"),("Ben Arous","Ben Arous"),("Bizerte","Bizerte"),\
                ("Gab%E8s","Gabès"),("Gafsa","Gafsa"),("Jendouba","Jendouba"),("Kairouan","Kairouan"),("Kasserine","Kasserine"),\
                ("Kébili","Kébili"),("Kef","Kef"),("Mahdia","Mahdia"),("Manouba","Manouba"),("Médnine","Médnine"),\
                ("Monastir","Monastir"),("Nabeul","Nabeul"),("Sfax","Sfax"),("Sidi Bouzid","Sidi Bouzid"),("Siliana","Siliana"),\
                ("Sousse","Sousse"),("Tataouine","Tataouine"),("Tozeur","Tozeur"),("Zaghouane","Zaghouane")]


class URLResolver():
    def __init__(self,sHosterUrl):
        sHosterUrl = sHosterUrl.replace('\r','').replace('\n','')
        self.sHosterUrl = sHosterUrl
    
    def getLinks(self):
        urlTab=[]
        if config.plugins.iptvplayer.tsi_resolver.value=='tsiplayer':
            ts_parse = ts_urlparser()
            e2_parse = urlparser()
        else:
            ts_parse = urlparser()
            e2_parse = ts_urlparser()

        # Youtube exception
        if (self.sHosterUrl.startswith('https://www.youtube.') or self.sHosterUrl.startswith('http://www.youtube.')):
            if (config.plugins.iptvplayer.tsi_resolver.value=='tsiplayer') and (os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/youtubedl_data/youtube_dl')):
                urlTab = ts_parse.getVideoLinkExt(self.sHosterUrl)
            elif (config.plugins.iptvplayer.tsi_resolver.value=='tsiplayer'):
                urlTab = e2_parse.getVideoLinkExt(self.sHosterUrl)
            else:
                urlTab = ts_parse.getVideoLinkExt(self.sHosterUrl)                  
        else:        
            if ts_parse.checkHostSupport(self.sHosterUrl)==1:
                urlTab = ts_parse.getVideoLinkExt(self.sHosterUrl)
            elif e2_parse.checkHostSupport(self.sHosterUrl)==1:
                urlTab = e2_parse.getVideoLinkExt(self.sHosterUrl)
            else:
                printDBG('------------> Pas de parse Trouver <-------------')            
                urlTab = ts_parse.getVideoLinkExt(self.sHosterUrl)
        return urlTab

        
def printD(x1,x2=''):
    printDBG(x1)
    return ''

def T(txt):
    if txt == 'Next': return (tscolor('\c00????20')+'>> Next')
    if txt == 'Search': return (tscolor('\c00????20')+'>> البحث <<')
    else: return  txt


def parseInt(sin):
  m = re.search(r'^(\d+)[.,]?\d*?', str(sin))
  return int(m.groups()[-1]) if m and not callable(sin) else 0

def aes(txt):
    import pyaes, base64
    from binascii import unhexlify
    key = unhexlify('0123456789abcdef0123456789abcdef')
    iv = unhexlify('abcdef9876543210abcdef9876543210')
    aes = pyaes.Encrypter(pyaes.AESModeOfOperationCBC(key, iv))
    return base64.b64encode(aes.feed(txt) + aes.feed()).decode()
  
def atob(elm):
    try:
        ret = base64.b64decode(elm)
    except:
        try:
            ret = base64.b64decode(elm+'=')
        except:
            try:
                ret = base64.b64decode(elm+'==')
            except:
                ret = 'ERR:base64 decode error'
    return ret.decode()
    
def a0d(main_tab,step2,a):
    a = a - step2
    if a<0:
        c = 'undefined'
    else:
        c = main_tab[a]
    return c

def x(main_tab,step2,a):
    return(a0d(main_tab,step2,a))

def decal(tab,step,step2,decal_fnc):
    decal_fnc = decal_fnc.replace('var ','global d; ') 
    decal_fnc = decal_fnc.replace('x(','x(tab,step2,') 
    exec(decal_fnc)
    aa=0
    while True:
        aa=aa+1
        tab.append(tab[0])
        del tab[0]
        #print([i for i in tab[0:10]])
        exec(decal_fnc) 
        #print(str(aa)+':'+str(c))
        if ((d == step) or (aa>10000)): break
      
def VidStream(script):
    tmp = re.findall('var.*?=(.{2,4})\(\)', script, re.S)
    if not tmp: return 'ERR:Varconst Not Found'
    varconst = tmp[0].strip()
    print('Varconst     = %s' % varconst)
    tmp = re.findall('}\('+varconst+'?,(0x[0-9a-f]{1,10})\)\);', script)
    if not tmp: return 'ERR:Step1 Not Found'
    step = eval(tmp[0])
    print('Step1        = 0x%s' % '{:02X}'.format(step).lower())
    tmp = re.findall('d=d-(0x[0-9a-f]{1,10});', script)
    if not tmp: return 'ERR:Step2 Not Found'
    step2 = eval(tmp[0])
    print('Step2        = 0x%s' % '{:02X}'.format(step2).lower())    
    tmp = re.findall("try{(var.*?);", script)
    if not tmp: return 'ERR:decal_fnc Not Found'
    decal_fnc = tmp[0]
    print('Decal func   = " %s..."' % decal_fnc[0:135])
    tmp = re.findall("'data':{'(_[0-9a-zA-Z]{10,20})':'ok'", script)
    if not tmp: return 'ERR:PostKey Not Found'
    PostKey = tmp[0]
    print('PostKey      = %s' % PostKey)
    tmp = re.findall("function "+varconst+".*?var.*?=(\[.*?])", script)
    if not tmp: return 'ERR:TabList Not Found'	
    TabList = tmp[0]
    TabList = varconst + "=" + TabList
    exec(TabList) in globals(), locals()
    main_tab = locals()[varconst]
    print(varconst+'          = %.90s...'%str(main_tab))
    decal(main_tab,step,step2,decal_fnc)
    print(varconst+'          = %.90s...'%str(main_tab))
    tmp = re.findall("\(\);(var .*?)\$\('\*'\)", script, re.S)
    if not tmp:
        tmp = re.findall("a0a\(\);(.*?)\$\('\*'\)", script, re.S)
        if not tmp:
            return 'ERR:List_Var Not Found'	
    List_Var = tmp[0]
    List_Var = re.sub("(function .*?}.*?})", "", List_Var)
    print('List_Var     = %.90s...' % List_Var)
    tmp = re.findall("(_[a-zA-z0-9]{4,8})=\[\]" , List_Var)
    if not tmp: return 'ERR:3Vars Not Found'
    _3Vars = tmp
    print('3Vars        = %s'%str(_3Vars))
    big_str_var = _3Vars[1]
    print('big_str_var  = %s'%big_str_var)    
    List_Var = List_Var.replace(',',';').split(';')
    for elm in List_Var:
        elm = elm.strip()
        if 'ismob' in elm: elm=''
        if '=[]'   in elm: elm = elm.replace('=[]','={}')
        elm = re.sub("(a0.\()", "a0d(main_tab,step2,", elm)
        #if 'a0G('  in elm: elm = elm.replace('a0G(','a0G(main_tab,step2,') 
        if elm!='':
            #print('elm = %s' % elm)
            elm = elm.replace('!![]','True');
            elm = elm.replace('![]','False');
            elm = elm.replace('var ','');
            #print('elm = %s' % elm)
            try:
                exec(elm)
            except:
                print('elm = %s' % elm)
                print('v = "%s" exec problem!' % elm, sys.exc_info()[0])            
    bigString = ''
    for i in range(0,len(locals()[_3Vars[2]])):
        if locals()[_3Vars[2]][i] in locals()[_3Vars[1]]:
            bigString = bigString + locals()[_3Vars[1]][locals()[_3Vars[2]][i]]	
    print('bigString    = %.90s...'%bigString) 
    tmp = re.findall('var b=\'/\'\+(.*?)(?:,|;)', script, re.S)
    if not tmp: return 'ERR:GetUrl Not Found'
    GetUrl = str(tmp[0])
    print('GetUrl       = %s' % GetUrl)    
    tmp = re.findall('(_.*?)\[', GetUrl, re.S)
    if not tmp: return 'ERR:GetVar Not Found'
    GetVar = tmp[0]
    print('GetVar       = %s' % GetVar)
    GetVal = locals()[GetVar][0]
    GetVal = atob(GetVal)
    print('GetVal       = %s' % GetVal)
    tmp = re.findall('}var (f=.*?);', script, re.S)        
    if not tmp: return 'ERR:PostUrl Not Found'
    PostUrl = str(tmp[0])
    print('PostUrl      = %s' % PostUrl)
    PostUrl = re.sub("(window\[.*?\])", "atob", PostUrl)        
    PostUrl = re.sub("([A-Z]{1,2}\()", "a0d(main_tab,step2,", PostUrl)    
    PostUrl = 'global f; '+PostUrl
    exec(PostUrl)
    return(['/'+GetVal,f+bigString,{ PostKey : 'ok'}])

    
def cryptoJS_AES_decrypt(encrypted, password, salt):
    def derive_key_and_iv(password, salt, key_length, iv_length):
        d = d_i = ''
        while len(d) < key_length + iv_length:
            d_i = hashlib.md5(d_i + password + salt).digest()
            d += d_i
        return d[:key_length], d[key_length:key_length+iv_length]
    bs = 16
    key, iv = derive_key_and_iv(password, salt, 32, 16)
    cipher = AES_CBC(key=key, keySize=32)
    return cipher.decrypt(encrypted, iv)

def tscolor(color):
    if config.plugins.iptvplayer.use_colors.value=='yes':
        return color
    elif config.plugins.iptvplayer.use_colors.value=='no':
        return ''
    else:
        if os.path.isfile('/etc/image-version'):
            with open('/etc/image-version') as file:  
                data = file.read() 
                if 'opendreambox'   in data.lower(): return ''
                #elif 'openatv'      in data.lower(): return ''
                else: return color
        else: return color	

def tshost(hst):
    url_ = config.plugins.iptvplayer.ts_hosts_online.value
    if url_ !='':        
        hosts_path = '/tmp/tsiplayer_hosts.txt'
        if os.path.exists(hosts_path):
            with open(hosts_path) as fp:
                Lines = fp.readlines()
                for line in Lines:
                    printDBG (line)
                    if '"::"' in line:
                        name,url = line.strip().split('"::"',1)
                        name = name.replace('"','')
                        url  = url.replace('"','')
                        printDBG (name)
                        printDBG (hst)
                        if ( name.lower().replace('-','').replace('_','').replace(' ','') == hst.lower().replace('-','').replace('_','').replace(' ','')):
                            printDBG (name)
                            return url
    return ''

def GetHostsFromFiles():
    return True

    
def gethostname(url):
    url=url.replace('http://','').replace('https://','').replace('www.','')
    if url.startswith('embed.'): url=url.replace('embed.','')
    if '/' in url:
        url=url.split('/',1)[0]
    return url
        
def resolve_liveFlash(link,referer):
    URL=''
    cm = common()
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
    HEADER = {'User-Agent': USER_AGENT, 'Connection': 'keep-alive', 'Accept-Encoding':'gzip', 'Content-Type':'application/x-www-form-urlencoded','Referer':''}
    defaultParams = {'header':HEADER, 'use_cookie': False, 'load_cookie':  False, 'save_cookie': False}

    urlo = link.replace('embedplayer','membedplayer')
    params = dict(defaultParams)
    params['header']['Referer'] = referer	
    sts, data2 = cm.getPage(urlo,params)
    sts, data3 = cm.getPage(urlo,params)
    Liste_films_data2 = re.findall('var hlsUrl =.*?\+.*?"(.*?)".*?enableVideo.*?"(.*?)"', data2, re.S)
    Liste_films_data3 = re.findall('var hlsUrl =.*?\+.*?"(.*?)".*?enableVideo.*?"(.*?)"', data3, re.S)
    if Liste_films_data2 and Liste_films_data3:
        tmp2=Liste_films_data2[0][1]
        tmp3=Liste_films_data3[0][1]
        i=0
        pk=tmp2
        printDBG('tmp2='+tmp2)
        printDBG('tmp3='+tmp3)
        while True:
            if (tmp2[i] != tmp3[i]):
                pk = tmp2[:i] + tmp2[i+1:]
                break
            i=i+1
            if i>len(tmp3)-1:
                break
        url = Liste_films_data3[0][0]+pk	
        ajax_data = re.findall('ajax\({url:.*?"(.*?)"', data3, re.S)
        if ajax_data:
            ajax_url = ajax_data[0] 
            sts, data4 = cm.getPage(ajax_url,params)											
            Liste_films_data = re.findall('=(.*)', data4, re.S)
            if Liste_films_data:
                URL = 'https://'+Liste_films_data[0]+url
                meta = {'direct':True}
                meta.update({'Referer':urlo})
                URL=strwithmeta(URL, meta)
    return URL

def resolve_zony(link,referer):
    URL=''
    cm = common()
    USER_AGENT = 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0'
    HEADER = {'User-Agent': USER_AGENT, 'Connection': 'keep-alive', 'Accept-Encoding':'gzip', 'Content-Type':'application/x-www-form-urlencoded','Referer':''}
    defaultParams = {'header':HEADER, 'use_cookie': False, 'load_cookie':  False, 'save_cookie': False}
    urlo = link.replace('embedplayer','membedplayer')
    params = dict(defaultParams)
    params['header']['Referer'] = referer	
    sts, data2 = cm.getPage(urlo,params)
    
    Liste_films_data = re.findall('source.setAttribute.*?ea.*?"(.*?)"', data2, re.S)
    if Liste_films_data:
        url = Liste_films_data[0]		
        ajax_data = re.findall('ajax\({url:.*?"(.*?)"', data2, re.S)
        if ajax_data:
            ajax_url = ajax_data[0] 
            sts, data3 = cm.getPage(ajax_url,params)											
            Liste_films_data = re.findall('=(.*)', data3, re.S)
            if Liste_films_data:
                URL = 'http://'+Liste_films_data[0]+url
                meta = {'direct':True}
                meta.update({'Referer':urlo})
                URL=strwithmeta(URL, meta)
    return URL

def unifurl(url):
    if url.startswith('//'):
        url='http:'+url
    if url.startswith('www'):
        url='http://'+url
    return url	
def xtream_get_conf():
    multi_tab=[]
    xuser = config.plugins.iptvplayer.ts_xtream_user.value
    xpass = config.plugins.iptvplayer.ts_xtream_pass.value	
    xhost = config.plugins.iptvplayer.ts_xtream_host.value	
    xua = config.plugins.iptvplayer.ts_xtream_ua.value
    if ((xuser!='') and (xpass!='') and (xhost!='')):
        name_=xhost+' ('+xuser+')'
        if not xhost.startswith('http'): xhost='http://'+xhost
        multi_tab.append((name_,xhost,xuser,xpass,xua))
    
    xtream_conf_path='/etc/tsiplayer_xtream.conf'
    if os.path.isfile(xtream_conf_path):
        with open(xtream_conf_path) as f: 
            for line in f:
                line=line.strip()
                name_,ua_,host_,user_,pass_= '','','','',''
                _data = re.findall('(.*?//.*?)/.*?username=(.*?)&.*?password=(.*?)&',line, re.S)			
                if _data: name_,host_,user_,pass_= _data[0][0]+' ('+_data[0][1]+')',_data[0][0],_data[0][1],_data[0][2]
                else:
                    _data = re.findall('(.*?)#(.*?)#(.*?)#(.*?)#(.*)',line, re.S) 
                    if _data: name_,host_,user_,pass_,ua_= _data[0][0],_data[0][1],_data[0][2],_data[0][3],_data[0][4]
                    else:
                        _data = re.findall('(.*?)#(.*?)#(.*?)#(.*)',line, re.S) 
                        if _data: name_,host_,user_,pass_= _data[0][0],_data[0][1],_data[0][2],_data[0][3]															
                if ((user_!='') and (pass_!='') and (host_!='')):
                    if not host_.startswith('http'): host_='http://'+host_
                    multi_tab.append((name_,host_,user_,pass_,ua_))
    return 	multi_tab




class TsThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
        
    def run(self):
        self._target(*self._args)
        
class TSCBaseHostClass:
    def __init__(self, params={}):
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        self.HEADER = {'User-Agent': self.USER_AGENT, 'Connection': 'keep-alive'}
        if '' != params.get('cookie', ''):
            self.COOKIE_FILE = GetCookieDir(params['cookie'])
            self.defaultParams = {'header':self.HEADER,'with_metadata':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        else:
            self.defaultParams = {'header':self.HEADER}
        self.sessionEx = MainSessionWrapper() 
        self.up = urlparser()
        self.ts_urlpars = ts_urlparser()
        proxyURL = params.get('proxyURL', '')
        useProxy = params.get('useProxy', False)
        self.cm = common(proxyURL, useProxy)
        self.currList = []
        self.currItem = {}
        if '' != params.get('history', ''):
            self.history = CSearchHistoryHelper(params['history'], params.get('history_store_type', False))
        self.moreMode = False
        self.TrySetMainUrl = True
        self.MyPath = GetCacheSubDir('Tsiplayer')
        
    def set_MAIN_URL(self):
        if self.TrySetMainUrl:
            sts, data = self.getPage(self.MAIN_URL)
            url = data.meta['url']
            if url.endswith('/'): url = url[:-1]
            printDBG('NEw URL = '+url)
            self.MAIN_URL = url
            self.TrySetMainUrl = False
            
    def getPage(self, baseUrl, addParams = {}, post_data = None):
        baseUrl=self.std_url(baseUrl)
        if addParams == {}: addParams = dict(self.defaultParams)
        return self.cm.getPage(baseUrl, addParams, post_data)

    def getPage_(self, baseUrl, addParams = {}, post_data = None):
        if not IsPython3():
            baseUrl=self.std_url(baseUrl)
            if addParams == {}: addParams = dict(self.defaultParams)
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
        else:
            return self.getPage(baseUrl, addParams, post_data)
        return sts, data

    def get_url_page(self,url,page,type_=1):
        if page > 1:
            if type_==1:
                url=url+'/page/'+str(page)
                url = url.replace('//page','/page')
        return url

    def searchResult(self,cItem):
        str_ch  = cItem.get('str_ch','')
        if str_ch =='':
            txt_def = '' 
            if os.path.isfile(self.MyPath +'searchSTR'):
                with open(self.MyPath + 'searchSTR','r') as f:
                    txt_def = f.read().strip()            
            ret = self.sessionEx.waitForFinishOpen(GetVirtualKeyboard(), title=('Search Text:'), text=txt_def)
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
        extra   = cItem.get('import','')
        elms = self.SearchAll(str_ch,page,extra,section)          
        for elm in elms:
            if elm.get('type','') == 'video':
                self.addVideo(elm)
            elif elm.get('type','') == 'marker':
                self.addMarker(elm)            
            else:
                self.addDir(elm)
        return elms
        
    def start(self,cItem):
        mode=cItem.get('mode', None)
        if mode=='00':
            self.showmenu(cItem)
        elif mode=='10':
            self.showmenu1(cItem)	
        elif mode=='11':
            self.showmenu2(cItem)
        elif mode=='19':
            self.showfilter(cItem)                    
        elif mode=='20':
            self.showitms(cItem)
        elif mode=='21':
            self.showelms(cItem)		
        elif mode=='50':
            self.showsearch(cItem)
        elif mode=='51':
            self.searchResult(cItem)	        
        return True
        
    def add_menu(self, cItem, pat1, pat2, data, mode_,s_mode=[], del_=[], TAB=[], search=False, Titre='',ord=[0,1],Desc=[],Next=[0,0],u_titre=False,ind_0=0,local=[],resolve='0',EPG=False,corr_=True,pref_='',post_data='',pat3='',ord3=[0,1],LINK='',hst='tshost',add_vid=True,image_cook=[False,{}],year_op=0,del_titre='',addParams={},bypass=False):
        if isinstance(mode_, str):
            mode = mode_
        else:
            mode = ''
        printDBG('start_add_menu, URL = '+cItem.get('url',self.MAIN_URL) )
        page=cItem.get('page',1)
        data_out  = ''
        found = False
        TAB0  = []
        elms_   = []
        if TAB!=[]:
            if Titre!='':
                self.addMarker({'category':'Marker','title': tscolor('\c00????30') + Titre,'icon':cItem['icon']})
            for (titre,url,mode,sub_mode) in TAB:
                if url.startswith('/'): url = self.MAIN_URL+url
                self.addDir({'category':'host2', 'title': titre,'mode':mode,'sub_mode':sub_mode,'url':url,'import':cItem['import'],'icon':cItem['icon']})
        else:
            if data=='':
                if LINK == '': LINK = cItem.get('url',self.MAIN_URL) 
                if LINK == '': LINK = self.MAIN_URL
                if LINK.startswith('//'): LINK = 'https:'+LINK
                if LINK.startswith('/'): LINK = self.MAIN_URL+LINK				
                if ((Next[0]==1) and (page>1)):
                    LINK=LINK+'/page/'+str(page)+'/'
                    LINK=LINK.replace('//page','/page')
                printDBG('link4:'+LINK)
                
                if post_data !='':
                    sts, data = self.getPage(LINK,addParams,post_data=post_data)
                else:
                    sts, data = self.getPage(LINK,addParams)
                if not sts: data=''
            #printDBG('DATA:'+data)
            if pat1 !='':
                data0=re.findall(pat1, data, re.S)
            else:
                data0 = [data,]
            if ((not data0) and bypass):
                data0 = [data,]
            if data0:
                if (len(data0)>ind_0) or (ind_0 == -1):
                    if pat2 !='':
                        #printDBG('pat2:'+pat2)
                        data1=re.findall(pat2, data0[ind_0], re.S)
                        #printDBG('data1:'+str(data1))
                        if ((not data1) and (pat3!='')):
                            ord = ord3
                            data1=re.findall(pat3, data0[ind_0], re.S)	
                    else:
                        data1 = [data0[ind_0],]	                                                      
                    
                        
                    if data1 and (Titre!=''):
                        self.addMarker({'title': tscolor('\c00????30') + Titre,'icon':cItem['icon']})
                    if mode=='desc': 
                        desc = ''
                        for (tag,pat,frst,Del_0) in Desc:
                            if desc == '': frst = ''
                            elif frst == '': frst = ' | '
                            if data1:
                                desc_=re.findall(pat, data1[0], re.S)	
                                if desc_:
                                    if ((Del_0=='') or ((Del_0!='') and (Del_0.lower() not in desc_[0].lower()))):
                                        if self.cleanHtmlStr(desc_[0]).strip()!='':
                                            desc = desc + frst + tscolor('\c00????00') + tag + ': ' + tscolor('\c00??????') + self.cleanHtmlStr(desc_[0])
                        return desc
                    elif mode=='param_servers':
                        for elm in data1:
                            titre = elm[ord[0]]
                            x = range(1, len(ord))
                            params = ''
                            for i in x:
                                params = params + elm[ord[i]]+'%%'                       
                            TAB0.append({'name':self.cleanHtmlStr(titre), 'url':'hst#tshost#'+params, 'need_resolve':1})
                        return (data,TAB0)
                    for elm in data1:
                        if len(ord)==2:
                            if mode.startswith('data_out0'):
                                url   = ''
                                titre = elm[ord[0]]
                                image = cItem.get('icon','')
                                desc  = cItem.get('desc','')
                                data_out  = elm[ord[1]]
                                #printDBG('data_out0='+data_out)
                            elif mode.startswith('data_out'):
                                url   = elm[ord[0]]
                                titre = elm[ord[1]]
                                image = cItem.get('icon','')
                                desc  = cItem.get('desc','')
                                data_out  = elm[2]
                                #printDBG('data_out1='+data_out)
                            else:
                                url   = elm[ord[0]]
                                titre = elm[ord[1]]
                                image = cItem.get('icon','')
                                desc  = cItem.get('desc','')
                        elif len(ord)==3:
                            url   = elm[ord[0]]
                            titre = elm[ord[1]]
                            if elm[ord[2]] !=-1: image = self.std_url(elm[ord[2]])
                            else: image = cItem.get('icon','')
                            desc  = cItem.get('desc','')
                        elif len(ord)>3:
                            url   = elm[ord[0]]
                            titre = elm[ord[1]]
                            if elm[ord[2]] !=-1: image = self.std_url(elm[ord[2]])
                            else: image = cItem.get('icon','')
                            x = range(3, len(ord))
                            desc0 = ''
                            for i in x:
                                desc0  = desc0 + elm[ord[i]]					
                            desc = ''
                            for (tag,pat,frst,Del_0) in Desc:
                                if desc == '': frst = ''
                                elif frst == '': frst = ' | '
                                desc_=re.findall(pat, desc0, re.S)	
                                if desc_:
                                    if ((Del_0=='') or ((Del_0!='') and (Del_0.lower() not in desc_[0].lower()))):
                                        if self.cleanHtmlStr(desc_[0]).strip()!='':
                                            desc = desc + frst + tscolor('\c00????00') + tag + ': ' + tscolor('\c00??????') + self.cleanHtmlStr(desc_[0])
                        sub_mode=0
                        if del_titre!='': titre = re.sub(del_titre,'',titre)
                        for (elm_0,elm_1) in s_mode:
                            if elm_0 in url: sub_mode=elm_1
                        if corr_:
                            if pref_!='': url = pref_+url
                            else:
                                if   url.startswith('http'): url = url
                                elif url.startswith('//'): url = 'https:'+url
                                elif url.startswith('/'): url = self.MAIN_URL+url
                                else: url = self.MAIN_URL+'/'+url
                        if mode.startswith('serv'): 
                            Local = ''
                            need_resolve = 1							
                            if mode == 'serv_url':
                                if url.startswith('http'):
                                    titre = self.up.getDomain(url, onlyDomain=True)
                                else:
                                    titre=''                            
                            if resolve == '1': URL = 'hst#tshost#'+url
                            else: URL = url 
                            for elm__ in local:
                                if elm__[0] in url:
                                    Local = 'local'
                                    if 'TRAILER' in elm__[1]: titre = '|Trailer| '+elm__[1].replace('TRAILER','').strip()
                                    elif '#0#' in elm__[1]:
                                        titre = elm__[1].replace('#0#','').strip()
                                        Local = ''
                                    else:
                                        if titre!='': titre = '|Local| '+elm__[1]+' - '+titre
                                        else: titre = '|Local| '+elm__[1]
                                    if elm__[2] == '1':
                                        URL = 'hst#tshost#'+url
                                    elif elm__[2] == '2':
                                        URL = url
                                        need_resolve = 0
                                    else:
                                        URL = url
                            if '!!DELETE!!' not in titre:
                                TAB0.append({'name':self.cleanHtmlStr(titre), 'url':URL, 'need_resolve':need_resolve,'type':Local})
                        elif mode.startswith('link'):
                            url = url.replace('\\/','/')
                            url = url.replace('\\','')
                            if mode=='link4':
                                TAB0.append((titre+'|'+url,'4'))
                            elif mode=='link1':
                                TAB0.append((url,'1'))
                        else:
                            if image.startswith('/'): image = self.MAIN_URL+image
                            if image_cook[0]: image = strwithmeta(image,image_cook[1])
                            #printDBG('------------------->'+titre)
                            if ('u06' in titre) and ('\\u0' not in titre) :
                                titre = titre.replace('u0','\\u0')
                            #printDBG('------------------->'+titre)
                            if '\\u0' in titre:
                            #    titre = titre.decode('unicode_escape',errors='ignore')
                                titre = string_escape(titre)
                            #printDBG('------------------->'+titre)                           
                            titre = self.cleanHtmlStr(str(titre))
                            cntrl = titre
                            if del_ != []:
                                if del_[0].startswith('url:'):
                                    del_[0] = del_[0].replace('url:','')
                                    cntrl = url
                            if not any(word in cntrl for word in del_):
                                if u_titre:
                                    desc1,titre = self.uniform_titre(titre,year_op)
                                    desc = desc1 + desc                             
                                if (titre!='') and (url!=''):
                                    if isinstance(mode_, str):
                                        mode = mode_
                                    else:
                                        for (tag,md,tp) in mode_:
                                            if tp == 'URL': str_cnt = url
                                            else: str_cnt = titre
                                            if tag=='': mode = md
                                            elif tag in str_cnt: mode = md 
                                    printDBG('link0000:'+mode+'|'+url)
                                    if mode=='video':
                                        found = True
                                        eelm = {'category':'host2','good_for_fav':True, 'title': titre,'sub_mode':sub_mode,'url':url, 'desc':desc,'import':cItem['import'],'icon':image,'hst':hst,'EPG':EPG}
                                        self.addVideo(eelm)	
                                        elms_.append(eelm)
                                    elif mode=='picture':
                                        found = True
                                        self.addPicture({'category':'host2','good_for_fav':True, 'title': titre,'sub_mode':sub_mode,'url':url, 'desc':desc,'import':cItem['import'],'icon':image,'hst':hst,'EPG':EPG})	
                                    else:	
                                        #printDBG('link0000:'+url)
                                        eelm = {'category':'host2','good_for_fav':True, 'title': titre,'sub_mode':sub_mode,'mode':mode.replace('data_out:','').replace('data_out0:',''),'url':url, 'desc':desc,'import':cItem['import'],'icon':image,'hst':'tshost','EPG':EPG,'data_out':data_out}
                                        self.addDir(eelm)
                                        elms_.append(eelm)
                    if ((Next[0]==1) or (Next[0]==2)) and (Next[1]!='none'):
                        if (len(elms_)>5):
                            self.addDir({'import':cItem['import'],'name':'categories', 'category':'host2', 'url':cItem['url'], 'title':'Page Suivante', 'page':page+1, 'desc':'Page Suivante', 'icon':cItem['icon'], 'mode':Next[1]})	
                    elif (Next[0]!=0) and (Next[1]!='none'):
                        next_=re.findall(Next[0], data, re.S)	
                        if next_:
                            URL_=next_[0]
                            if corr_:
                                if pref_!='': URL_ = pref_+URL_
                                else:
                                    if   URL_.startswith('http'): URL_ = URL_
                                    elif URL_.startswith('/'): URL_ = self.MAIN_URL+URL_
                                    else: URL_ = self.MAIN_URL+'/'+URL_
                            self.addDir({'import':cItem['import'],'name':'categories', 'category':'host2', 'url':URL_, 'title':'Page Suivante', 'page':1, 'desc':'Page Suivante', 'icon':cItem['icon'], 'mode':Next[1]})	
            if (mode=='video') and (not found) and (add_vid):
                desc=''
                for (tag,pat,frst,Del_0) in Desc:
                    if desc == '': frst = ''
                    elif frst == '': frst = ' | '
                    desc_=re.findall(pat, data, re.S)	
                    if desc_:
                        if ((Del_0=='') or ((Del_0!='') and (Del_0.lower() not in desc_[0].lower()))):
                            if self.cleanHtmlStr(desc_[0]).strip()!='':
                                desc = desc + frst + tscolor('\c00????00') + tag + ': ' + tscolor('\c00??????') + self.cleanHtmlStr(desc_[0])
                desc = cItem.get('desc','') + '\n'+ desc            
                self.addVideo({'category':'host2','good_for_fav':True, 'title': cItem['title'],'url':cItem['url'], 'desc':desc,'import':cItem['import'],'icon':cItem['icon'],'hst':'tshost','EPG':EPG})						
        if search:
            self.addDir({'category':'search'  ,'title':tscolor('\c00????30') + _('Search'),'search_item':True,'page':1,'hst':'tshost','import':cItem['import'],'icon':cItem['icon']})
        printDBG('elms_='+str(elms_))
        return (data,TAB0,elms_)	




    def std_host_name(self,name_, direct=False):
        if '|' in name_:
            n1 = name_.split('|')[-1]
            n2 = name_.replace(name_.split('|')[-1],'')
            if direct=='direct': name_=n2+tscolor('\c0090??20')+n1.replace('embed.','').title()
            elif self.ts_urlpars.checkHostSupportbyname(n1):
                name_=n2+tscolor('\c0090??20')+n1.replace('embed.','').title()	
            elif self.ts_urlpars.checkHostNotSupportbyname(n1):
                name_=n2+tscolor('\c00??1020')+n1.replace('embed.','').title()
            else:
                name_=n2+tscolor('\c00999999')+n1.replace('embed.','').title()                	
        else: 
            if direct=='direct': name_=tscolor('\c0090??20')+name_.replace('embed.','').title()
            elif self.ts_urlpars.checkHostSupportbyname(name_):
                name_=tscolor('\c0090??20')+name_.replace('embed.','').title()
            elif self.ts_urlpars.checkHostNotSupportbyname(name_):
                name_=tscolor('\c00??5050')+name_.replace('embed.','').title()	
              
                                
        return name_ 
        
    def std_url(self,url):
        url1=url
        printDBG('url0='+url1)
        if r'\u0' in url1:
            url1 = url1.encode()
            url1 = str(url1.decode('unicode_escape',errors='ignore'))
        if '%' not in url1: 
            url1=url1.replace('\\/','/')     
            url1=url1.replace('://','rgy11soft')
            url1=url1.replace('?','rgy22soft')        
            url1=url1.replace('&','rgy33soft') 
            url1=url1.replace('=','rgy44soft')
            url1=url1.replace(':','rgy55soft')
            url1=url1.replace('~','rgy66soft')
            url1=url1.replace(',','rgy77soft')
            
            #url1=urllib.unquote(url1)
            #printDBG(url1)
            url1=urllib.quote(url1)
            url1=url1.replace('rgy11soft','://')
            url1=url1.replace('rgy22soft','?')        
            url1=url1.replace('rgy33soft','&') 	
            url1=url1.replace('rgy44soft','=') 	
            url1=url1.replace('rgy55soft',':')
            url1=url1.replace('rgy66soft','~')  
            url1=url1.replace('rgy77soft',',')              
            printDBG('url1='+url1)
        return url1
        
    def std_url1(self,url):
        return url.encode('utf-8')       


    def std_title(self,titre,with_type=False,desc='',with_ep=False):
        #print(titre)
        info = {}
        info.clear()
        if desc=='':
            desc = {}
            desc.clear()
        titre=titre.replace('مشاهدة وتحميل مباشر','').replace('مشاهدة','').replace('اون لاين','').replace('  ',' ').replace('  ',' ').replace('  ',' ')
        tag_film  = [('مسلسل الكرتون','CARTOON'),('مسلسل الانمي','ANIM'),('مسلسل انمي','ANIM'),('مسلسل كرتون','CARTOON'),
                    ('فيلم الكرتون','CARTOON FILM'),('فلم الكرتون','CARTOON FILM'),('فيلم الانمي','ANIM FILM'),('فيلم كرتون','CARTOON FILM'),
                    ('فيلم الانيميشن','ANIM FILM'),('كرتون','CARTOON'),('فيلم','FILM'),('فلم','FILM'),('مسلسل','SERIE'),('عرض','TV SHOW'),('انمي','ANIM'),
                    ('برنامج','TV SHOW')]    
        tag_type  = [('مدبلج للعربية','مدبلج'),('مترجمة للعربية','مترجم'),('مترجم للعربية','مترجم'), ('مدبلجة','مدبلج'), ('مترجمة','مترجم') , ('مترجم','مترجم') , ('مدبلج','مدبلج'),
                     ('باللغة العربية - كامل','Arabic Full'),('باللغة العربية','Arabic')]

        for elm in tag_film: tag_type.append(elm)
        tag_qual   = ['1080p','720p','WEB-DL','BluRay','DVDRip','HDCAM','HDTC','HDRip', 'HD', '1080P','720P','DVBRip','TVRip','DVD','SD']    
        tag_saison = [('الموسم الثاني','2'),('الموسم الاول','1'),('الموسم الأول','1'),('الموسم الثالث','3'),('الموسم الرابع','4'),('الموسم الخامس','5'),('الموسم السادس','6'),('الموسم السابع','7'),('الموسم الثامن','8'),('الموسم التاسع','9'),('الموسم العاشر','10'),
                      ('الموسم 1','1'),('الموسم 2','2'),('الموسم 3','3'),('الموسم 4','4'),('الموسم 5','5'),('الموسم 6','6'),('الموسم 7','7'),('الموسم 8','8'),('الموسم 9','9'),('الموسم 10','10'),]
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
            if elm[0] in titre:
                titre = titre.replace(elm[0],'').strip()
                for elm_ in tag_film:
                    if elm[0] == elm_[0]:
                        type_ = elm_[1]
                tags_.append(elm[1])

        for elm in tags_special:
            if elm[0] in titre:
                titre = titre.replace(elm[0],elm[1]).strip()
                tags_.append(elm[0])

        info['type'] = type_
        info['tags'] = tags_

        for tg in desc.get('tags',[]):
            info['tags'].append(tg)   

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
        if year == '': year = desc.get('year','') 
        info['year'] = year
        
        #extract episode:
        episode = ''
        titre = titre.replace('الحلقة','_EP_')
        data_list = re.findall('EP_([ 0-9]{1,5})', titre.replace('الحلقة','_EP_'), re.S)
        if data_list:
            episode = data_list[0]
            titre = titre.replace(episode,'').replace('_EP_','').strip()
        if episode.strip() != '': desc['episode'] = episode.strip()
        #print(titre)
        #Titre en
        titre_en = ''
        titre_ =''
        data_list = re.findall("[a-zA-Z0-9 :_\-\.&,!'’]+", titre, re.S)
        if data_list:
            #print(data_list)
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
        #print('titre_en=' + titre_en)

        if titre_en.endswith('-') or titre_en.endswith(':'): titre_en = titre_en[:-2].strip()
        #Titre ar
        titre_ar = ''
        titre_ =''    
        titre_ = titre.replace(titre_en,'').replace('  ',' ').replace('  ',' ').strip()  
        if len(titre_.strip())>2:
            titre_ar = titre_
        #print('titre_ar=' + titre_ar)
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
            
        rating  = desc.get('rating','')
        quality = desc.get('quality','')
        plot    = desc.get('plot','')
        episode = desc.get('episode','') 
        info_   = desc.get('info','')                   

        tag = ''
        if with_type and type_!='':
            tag = tag + tscolor('\c0030??30')+type_+' - '
        if saison != '':
            tag =  tag + tscolor('\c00????30')+'Saison '+saison + ' - '
        elif part != '':
            tag =  tag + tscolor('\c00????30')+'Part '+part + ' - ' 
        if (with_ep) and (episode!=''): 
            tag =  tag + tscolor('\c00????30')+'E'+episode + ' - '        
        if year != '':
            tag =  tag + tscolor('\c0000????')+year +' - '
        if tag.endswith(' - '): tag = tag[:-3]
        if tag!='': tag = tscolor('\c00??????') +'['+ tag + tscolor('\c00??????') + '] '
        info['title_display'] = tag  + titre.strip()
        #print(str(info))

        tags = ''
        for tg in info['tags']:
            tags= tags + tg + ' | '

        desc = ''
        if episode: desc = desc + tscolor('\c0000????')+'Episode: '+tscolor('\c00??????')+episode+' | '
        if (rating and rating!='0'):  desc = desc + tscolor('\c0000????')+'Rating: '+tscolor('\c00??????')+rating+' | '
        if quality: desc = desc + tscolor('\c0000????')+'Quality: '+tscolor('\c00??????')+quality+' | '
        if info_: desc = desc + tscolor('\c0000????')+'Info: '+tscolor('\c00??????')+info_+' | '        
        if plot: desc = desc +'\n' +  tscolor('\c0000????')+'Plot: '+tscolor('\c00??????')+plot
        if tags: desc = desc +'\n' +  tscolor('\c0000????')+'Tags: '+tscolor('\c00??????')+tags
        info['desc'] = desc.strip()
        return info   

    def std_episode(self,titre,cItem):
        sTitle = cItem.get('sTitle',cItem.get('info',{}).get('title',''))
        saison = cItem.get('saison',cItem.get('info',{}).get('saison',''))
        part   = cItem.get('part','')
        print(saison)
        tag = ''
        
        if 'اعلان' in titre:
            if saison != '':
                tag =  tag + tscolor('\c00????30')+'S'+saison + tscolor('\c00??????')+' | ' +tscolor('\c0000????')+'Trailer'+tscolor('\c00??????')
            elif part != '':
                tag =  tag + tscolor('\c00????30')+'Part'+part + tscolor('\c00??????')+' | ' +tscolor('\c0000????')+'Trailer'+tscolor('\c00??????')                    
            else:                        
                tag = tscolor('\c0000????')+'Trailer'+tscolor('\c00??????')
        elif 'حلقة' in titre:
            episode = titre.replace('الحلقة','').replace('والأخيرة','').replace('والاخيرة','').replace('الاخيرة','').replace('الأخيرة','').replace('حلقة','').strip()
            #if episode.endswith('-'): episode = episode[:-2]
            if len(episode)<4:
                if len(episode)<2:
                    episode = '0'+episode
                if saison != '':
                    tag = 'S'+saison+'E'+episode
                elif part != '':
                    tag = 'S'+part+'E'+episode                       
                else:
                    tag = 'E'+episode
            else:
                if (saison != '') :
                    tag = 'S'+saison+' | '+episode
                elif part != '':
                    tag = 'S'+part+' | '+episode                
        elif ('مشاهدة' in titre) and ('تحميل' in titre): 
            tag = ''
        else:
            tag = titre
        if tag!='': tag = tscolor('\c00??????') +'['+ tag + tscolor('\c00??????') + '] '
        return (tag  + sTitle)  

    def extract_desc(self,data,Desc):
        info = {}
        for (tag,pat) in Desc:
            desc_=re.findall(pat, data, re.S)	
            if desc_:
                if self.cleanHtmlStr(desc_[0]).strip()!='':
                    info[tag] = self.cleanHtmlStr(desc_[0])
        return info
    
    def uniform_titre(self,titre,year_op=0):
        titre=titre.replace('مشاهدة وتحميل مباشر','').replace('مشاهدة','').replace('اون لاين','')
        tag_type   = ['مدبلج للعربية','مترجمة للعربية','مترجم للعربية', 'مدبلجة', 'مترجمة' , 'مترجم' , 'مدبلج', 'مسلسل', 'عرض', 'انمي', 'فيلم']
        tag_qual   = ['1080p','720p','WEB-DL','BluRay','DVDRip','HDCAM','HDTC','HDRip', 'HD', '1080P','720P','DVBRip','TVRip','DVD','SD']
        tag_saison = [('الموسم الثاني','02'),('الموسم الاول','01'),('الموسم الثالث','03'),('الموسم الرابع','04'),('الموسم الخامس','05'),('الموسم السادس','06'),('الموسم السابع','07'),('الموسم الثامن','08'),('الموسم التاسع','09'),('الموسم العاشر','10')]
        type_ = tscolor('\c00????00')+ 'Type: '+tscolor('\c00??????')
        qual = tscolor('\c00????00')+ 'Quality: '+tscolor('\c00??????')
        sais = tscolor('\c00????00')+ 'Saison: '+tscolor('\c00??????')
        desc=''
        saison=''
        
        for elm in tag_saison:
            if elm[0] in titre:
                sais=sais+elm[1]
                titre = titre.replace(elm[0],'')
                break
                
        for elm in tag_type:
            if elm in titre:
                titre = titre.replace(elm,'')
                type_ = type_+elm+' | '
        for elm in tag_qual:
            if elm in titre:
                #re_st = re.compile(re.escape(elm.lower()), re.IGNORECASE)
                #titre=re_st.sub('', titre)
                titre = titre.replace(elm,'')
                qual = qual+elm+' | '
                
        data = re.findall('((?:19|20)\d{2})', titre, re.S)
        if data:
            year_ = data[-1]
            year_out = tscolor('\c0000????')+data[-1]+tscolor('\c00??????')
            if year_op==0:
                titre = year_out+'  '+titre.replace(year_, '')
                desc = 	tscolor('\c00????00')+ 'Year: '+tscolor('\c00??????')+year_+'\n'
            elif year_op==-1:
                titre = year_out+'  '+titre.replace(year_, '')
                desc = 	''			
            elif year_op==1:
                titre = titre.replace(year_, '')
                desc = 	tscolor('\c00????00')+ 'Year: '+tscolor('\c00??????')+year_+'\n'
            elif year_op==2:	
                titre = titre.replace(year_, '')
                desc = 	year_
                    
        if year_op<2:
            if sais != tscolor('\c00????00')+ 'Saison: '+tscolor('\c00??????'):
                desc = desc+sais+'\n'				
            if type_!=tscolor('\c00????00')+ 'Type: '+tscolor('\c00??????'):
                desc = desc+type_[:-3]+'\n'
            if qual != tscolor('\c00????00')+ 'Quality: '+tscolor('\c00??????'):
                desc = desc+qual[:-3]+'\n'

        pat = 'موسم.*?([0-9]{1,2}).*?حلقة.*?([0-9]{1,2})'
         
        data = re.findall(pat, titre, re.S)
        if data:
            sa = data[0][0]
            ep = data[0][1]
            if len(sa)==1: sa='0'+sa
            if len(ep)==1: ep='0'+ep			
            ep_out = tscolor('\c0000????')+'S'+sa+tscolor('\c0000????')+'E'+ep+tscolor('\c00??????')
            titre = ep_out+' '+re.sub(pat,'',titre)
            titre = titre.replace('ال ','')
            
            
        return desc,self.cleanHtmlStr(titre).replace('()','').strip()

    def MediaBoxResult(self,str_ch,year_,extra):
        urltab=[]
        str_ch_o = str_ch
        str_ch = urllib.quote(str_ch_o+' '+year_)
        result = self.SearchResult(str_ch,1,'')
        if result ==[]:
            str_ch = urllib.quote(str_ch_o)
            result = self.SearchResult(str_ch,1,'')
        for elm in result:
            titre     = elm['title']
            url       = elm['url']
            desc      = elm.get('desc','')
            image     = elm.get('icon','')
            mode      = elm.get('mode','') 
            type_     = elm.get('type','')
            sub_mode  = elm.get('sub_mode','') 
            if str_ch_o.lower().replace(' ','') == titre.replace('-',' ').replace(':',' ').lower().replace(' ',''):
                trouver = True
            else:
                trouver = False
            name_eng='|'+tscolor('\c0060??60')+self.SiteName+tscolor('\c00??????')+'| '+titre				
            if type_=='video':
                cat= 'video'
            else:
                cat = 'host2'
            element = {'titre':titre,'import':extra,'good_for_fav':True,'EPG':True, 'hst':'tshost', 'category':cat, 'url':url, 'title':name_eng, 'desc':desc, 'icon':image,'sub_mode':sub_mode, 'mode':mode}
            if trouver:
                urltab.insert(0, element)					
            else:
                urltab.append(element)	
        return urltab
        
    def informAboutGeoBlockingIfNeeded(self, country, onlyOnce=True):
        try: 
            if onlyOnce and self.isGeoBlockingChecked: return
        except Exception: 
            self.isGeoBlockingChecked = False
        sts, data = self.cm.getPage('https://dcinfos.abtasty.com/geolocAndWeather.php')
        if not sts: return
        try:
            data = json_loads(data.strip()[1:-1], '', True)
            if data['country'] != country:
                message = _('%s uses "geo-blocking" measures to prevent you from accessing the services from outside the %s Territory.') 
                GetIPTVNotify().push(message % (self.getMainUrl(), country), 'info', 5)
            self.isGeoBlockingChecked = True
        except Exception: printExc()
    
    def listsTab(self, tab, cItem, type='dir'):
        defaultType = type
        for item in tab:
            params = dict(cItem)
            params.update(item)
            params['name']  = 'category'
            type = item.get('type', defaultType)
            if type == 'dir': self.addDir(params)
            elif type == 'marker': self.addMarker(params)
            else: self.addVideo(params)

    def listSubItems(self, cItem):
        printDBG("TSCBaseHostClass.listSubItems")
        self.currList = cItem['sub_items']

    def listToDir(self, cList, idx):
        return self.cm.ph.listToDir(cList, idx)
    
    def getMainUrl(self):
        return self.MAIN_URL
    
    def setMainUrl(self, url):
        if self.cm.isValidUrl(url):
            self.MAIN_URL = self.cm.getBaseUrl(url)
            return True
        return False
    
    def getFullUrl(self, url, currUrl=None):
        if currUrl == None or not self.cm.isValidUrl(currUrl):
            try:
                currUrl = self.getMainUrl()
            except Exception:
                currUrl = None
            if currUrl == None or not self.cm.isValidUrl(currUrl):
                currUrl = 'http://fake/'
        return self.cm.getFullUrl(url, currUrl)

    def getFullIconUrl(self, url, currUrl=None):
        if currUrl != None: return self.getFullUrl(url, currUrl)
        else: return self.getFullUrl(url)
        
    def getDefaulIcon(self, cItem=None):
        try:
            return self.DEFAULT_ICON_URL
        except Exception:
            pass
        return ''

    @staticmethod 
    def cleanHtmlStr(str):
        return CParsingHelper.cleanHtmlStr(str)

    @staticmethod 
    def getStr(v, default=''):
        if type(v) == type(u''): return v.encode('utf-8')
        elif type(v) == type(''):  return v
        return default

    def getCurrList(self):
        return self.currList

    def setCurrList(self, list):
        self.currList = list
        
    def getCurrItem(self):
        return self.currItem

    def setCurrItem(self, item):
        self.currItem = item

    def addDir(self, params):
        params['type'] = 'category'
        self.currList.append(params)
        return

    def addMore(self, params):
        params['type'] = 'more'
        self.currList.append(params)
        return

    def addVideo(self, params):
        params['type'] = 'video'
        self.currList.append(params)
        return

    def addAudio(self, params):
        params['type'] = 'audio'
        self.currList.append(params)
        return

    def addPicture(self, params):
        params['type'] = 'picture'
        self.currList.append(params)
        return

    def addData(self, params):
        params['type'] = 'data'
        self.currList.append(params)
        return

    def addArticle(self, params):
        params['type'] = 'article'
        self.currList.append(params)
        return

    def addMarker(self, params):
        params['type'] = 'marker'
        self.currList.append(params)
        return

    def listsHistory(self, baseItem={'name': 'history', 'category': 'Wyszukaj'}, desc_key='plot', desc_base=(_("Type: ")) ):
        list = self.history.getHistoryList()
        for histItem in list:
            plot = ''
            try:
                if type(histItem) == type({}):
                    pattern     = histItem.get('pattern', '')
                    search_type = histItem.get('type', '')
                    if '' != search_type: plot = desc_base + _(search_type)
                else:
                    pattern     = histItem
                    search_type = None
                params = dict(baseItem)
                params.update({'title': pattern, 'search_type': search_type,  desc_key: plot})
                self.addDir(params)
            except Exception: printExc()

    def getFavouriteData(self, cItem):
        try:
            return json_dumps(cItem)
        except Exception: 
            printExc()
        return ''

    def getLinksForFavourite(self, fav_data):
        try:
            if self.MAIN_URL == None:
                self.selectDomain()
        except Exception: 
            printExc()
        links = []
        try:
            cItem = json_loads(fav_data)
            links = self.getLinksForItem(cItem)
        except Exception: printExc()
        return links

    def setInitListFromFavouriteItem(self, fav_data):
        try:
            if self.MAIN_URL == None:
                self.selectDomain()
        except Exception: 
            printExc()
        try:
            params = json_loads(fav_data)
        except Exception: 
            params = {}
            printExc()
            return False
        self.currList.append(params)
        return True

    def getLinksForItem(self, cItem):
        # for backward compatibility
        return self.getLinksForVideo(cItem)

    def markSelectedLink(self, cacheLinks, linkId, keyId='url', marker="*"):
        # mark requested link as used one
        if len(cacheLinks.keys()):
            for key in cacheLinks:
                for idx in range(len(cacheLinks[key])):
                    if linkId in cacheLinks[key][idx][keyId]:
                        if not cacheLinks[key][idx]['name'].startswith(marker):
                            cacheLinks[key][idx]['name'] = marker + cacheLinks[key][idx]['name'] + marker
                        break

    def handleService(self, index, refresh=0, searchPattern='', searchType=''):
        self.moreMode = False
        if 0 == refresh:
            if len(self.currList) <= index:
                return
            if -1 == index:
                self.currItem = { "name": None }
            else:
                self.currItem = self.currList[index]
        if 2 == refresh: # refresh for more items
            printDBG(">> endHandleService index[%s]" % index)
            # remove item more and store items before and after item more
            self.beforeMoreItemList = self.currList[0:index]
            self.afterMoreItemList = self.currList[index+1:]
            self.moreMode = True
            if -1 == index:
                self.currItem = { "name": None }
            else:
                self.currItem = self.currList[index]

    def endHandleService(self, index, refresh):
        if 2 == refresh: # refresh for more items
            currList = self.currList
            self.currList = self.beforeMoreItemList
            for item in currList:
                if 'more' == item['type'] or (item not in self.beforeMoreItemList and item not in self.afterMoreItemList):
                    self.currList.append(item)
            self.currList.extend(self.afterMoreItemList)
            self.beforeMoreItemList = []
            self.afterMoreItemList  = []
        self.moreMode = False
    
