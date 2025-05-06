#coding: utf-8

###################################################
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.urlparser    import urlparser as ts_urlparser
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools      import TSCBaseHostClass,tscolor
from Plugins.Extensions.IPTVPlayer.libs.urlparser              import urlparser
from Plugins.Extensions.IPTVPlayer.libs.urlparserhelper        import getDirectM3U8Playlist
from Plugins.Extensions.IPTVPlayer.libs.e2ijson                import loads as json_loads
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes             import strwithmeta
from Plugins.Extensions.IPTVPlayer.tools.iptvtools             import printDBG,printExc, GetCacheSubDir
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit   import GetIPTVSleep
from Plugins.Extensions.IPTVPlayer.components.e2ivkselector    import GetVirtualKeyboard
from Components.config import config
import time,os
import glob
import datetime
import re,sys

from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.vstream.resources.lib.gui.hoster import cHosterGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.vstream.resources.lib.tmdb import cTMDb
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.vstream.resources.lib.home import cHome
MAIN_URL0   = '/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/vstream/resources/sites'
fncs_search = ['showsearch','myshowsearchmovie','myshowsearchserie','showmoviessearch','showsearchtext']

try:
  basestring
except NameError:
  basestring = str

def whatisthis(s,tag=''):
    if isinstance(s, str):
        printDBG(tag+": ordinary string")
    elif isinstance(s, unicode):
        printDBG(tag + ": unicode string")
    else:
        printDBG(tag+ ": not a string")


def getinfo():	
    info_={}
    info_['name']='Vstream'
    info_['version']='2.0 19/02/2023'
    info_['dev']='RGYSOFT'
    info_['cat_id']='902'
    info_['desc']='Matrix (KODI Addon)'
    info_['icon']='https://i.ibb.co/wJ5k47d/icon.png'
    return info_

def timeTostr(time_):	
    return str(datetime.timedelta(seconds=time_))
   
def get_url_meta(URL):
    printDBG('get_url_meta='+URL)
    tags =''
    meta_={}
    if '|' in URL:
        URL,tags = URL.split('|')
        if tags!='':
            if '&' in tags:
                tags = tags.split('&')
                for tag in tags:
                    id_,val_ = tag.split('=',1)
                    meta_[id_]=val_.replace('+',' ')							
            else:	
                id_,val_ = tags.split('=')
                meta_[id_]=val_
            #URL = strwithmeta(URL,meta_)
    return (URL,meta_)

def getHosts():	
    Hosts=[]
    Hosts.append(('21','','aflamfree'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','alarab'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','alfajertv'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','arbcinema'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','aracinema_co'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','awaan'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','cdrama'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','egyclub'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','ehna'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','familymoviz'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','fnteam'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','halacima'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','pakistani'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','panet'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','replay'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','rotana'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','shooflive'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','shoofvod'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','themoviedb_org'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','topimdb'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','tvfun'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('21','','watanflix'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('27','','alarabiya'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('27','','aljazeera'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('27','','arabsciences'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('27','','docarabic'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('27','','geoarabic'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('22','','animeblkom'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('22','','animeslayer'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('23','','animezid'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('23','','cartoonrbi'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('22','','detectiveconanar'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('23','','eyoon'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('22','','fansubs'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('22','','gateanime'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('23','','katkoute'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('23','','nightosphere'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('22','','spacepowerfan'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('23','','stardima'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('22','','xsanime'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('22','','animeup'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('25','','ahdaf'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('26','','asgoal'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('26','','beinmatch'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('25','','beinsports_net'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('25','','btolat'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('26','','kingfoot'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('26','','tvnine'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('26','','yallalive'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('25','','yallashoot'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('24','','aicpmadih'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))
    Hosts.append(('24','','hidaya'         ,'1.0 18/01/2021','VOD ARAB'  ,'New Host',''))  
    
    Hosts_=[]
    Hosts_00=[]
    for (id_,titre,hst_,version_,desc_,up_,image) in Hosts:
        if image=='': image = 'file:///usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/matrix/resources/art/sites/'+hst_+'.png'
        if titre=='': titre = hst_.replace('_','.').title()
        imp0  = 'from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.sites.'
        imp1  = 'from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.host_matrix import '
        desc  = tscolor('\c00????00')+' Info: '+tscolor('\c00??????')+desc_+'\\n '+tscolor('\c00????00')+'Version: '+tscolor('\c00??????')+version_+'\\n '
        desc  = desc+tscolor('\c00????00')+'Adaptation: '+tscolor('\c00??????')+'RGYSOFT'+'\\n'+tscolor('\c00????00')+' Last Update: '+tscolor('\c00??????')+up_+'\\n '
        desc  = desc+tscolor('\c00????00')+'Origine: '+tscolor('\c00??????')+'matrix (KODI Addon)'+'\\n '
        desc  = desc+tscolor('\c00????00')+'Source: '+tscolor('\c00??????')+'https://github.com/zombiB/zombi-addons'+'\\n '
        elm_ = {'category': 'host2', 'params': {}, 'import_': imp0+hst_+' import ', 'title': titre,'desc':desc, 'import': imp1, 'mode': '10', 'icon':image, 'type': 'category', 'sSiteName':hst_}
        Hosts_.append((id_,elm_))
    return Hosts_00
    

def replaceColors(titre):
    titre         = str(titre)
    color_replace = [('%5BCOLOR+coral%5D','\c00??7950'),('%5B%2FCOLOR%5D','\c00??????'),('%5BCOLOR+COLOR+gold%5D','\c00??9900'),
                     ('%5BCOLOR+COLOR+violet%5D','\c00??0099'), ('%5BCOLOR+COLOR+orange%5D','\c00??6600'),('%5BCOLOR+COLOR+dodgerblue%5D','\c00??90??')]

    color_replace = [('[COLOR violet]','\c00??90??'),('[COLOR dodgerblue]','\c007070??'),('[COLOR lightcoral]','\c00?08080'),('[/COLOR]','\c00??????'),
                     ('[COLOR gold]','\c00????00'),('[COLOR orange]','\c00???020'),('[COLOR red]','\c00??5555'),('[COLOR skyblue]','\c0000????'),
                     ('[COLOR teal]','\c00009999'),('[COLOR coral]','\c00??7950'),('[COLOR khaki]','\c00997050'),('[COLOR 0]','\c00??????'),
                     ('[COLOR crimson]','\c00??5555'),('[COLOR grey]','\c00999999'),('[COLOR olive]','\c00808000'),('[COLOR fuchsia]','\c00??40??'),
                     ('[COLOR yellow]','\c00????33'),('[COLOR aqua]','\c000030??'),('[COLOR cyan]','\c0030????'),]



    for cl0,cl1 in color_replace:
        titre = titre.replace(cl0,tscolor(cl1))
        titre = titre.replace(cl0,tscolor(cl1))        
    return titre

def convert_desc(SITE_DESC):
    desc  = tscolor('\c00????00')+' Info: '+tscolor('\c00??????')+SITE_DESC+'\\n '
    desc  = desc+tscolor('\c00????00')+'Adaptation: '+tscolor('\c00??????')+'RGYSOFT'+'\\n'
    desc  = desc+tscolor('\c00????00')+'Origine: '+tscolor('\c00??????')+'matrix (KODI Addon)'+'\\n '
    desc  = desc+tscolor('\c00????00')+'Source: '+tscolor('\c00??????')+'https://github.com/zombiB/zombi-addons'+'\\n '
    return desc


def getDesc(Items):
    desc0 = ''
    genre        = str(Items.get('genre',''))
    sDescription = Items.get('plot','') 
    year         = str(Items.get('year',''))
    rating       = Items.get('rating',0)
    duration     = Items.get('duration',0)
    genre        = str(Items.get('genre',''))
    sDescription = replaceColors(sDescription)
    try:
        rating   = "{:.1f}".format(rating)
    except:
        rating   = str(rating)
    try:
        duration = timeTostr(duration)
    except:
        duration = str(duration)   
    
    if rating.strip()   == '0.0': rating = ''
    if year.strip()     == '0': year = ''
    if duration.strip() == '0:00:00': duration = ''
    if rating           == '0': rating = ''
    if duration         == '0': duration = ''
    if genre            == '0': genre = ''
    if sDescription     == '0': sDescription = ''
    if (rating     != '') and (rating != '0'): desc0 = desc0+tscolor('\c00????00')+'TMDB: '+tscolor('\c00??????')+ rating+' | '   
    if year       != '': desc0 = desc0+tscolor('\c00????00')+'Year: '+tscolor('\c00??????')+year+' | '	
    if duration   != '': desc0 = desc0+tscolor('\c00????00')+'Duration: '+tscolor('\c00??????')+duration+' | '	
    if genre      != '': desc0 = desc0+'\n'+tscolor('\c00????00')+'Genre: '+tscolor('\c00??????')+genre
    if desc0.strip()         != '': desc0 = desc0+'\n'+sDescription
    else: desc0 = sDescription
    return desc0 


def get_desc(inf):
        desc0=''
        elm = inf[0]['other_info']
        if elm.get('tmdb_rating','')    != '': desc0 = desc0+tscolor('\c00????00')+'TMDB: '+tscolor('\c00??????')+elm['tmdb_rating']+' | '
        if elm.get('year','')           != '': desc0 = desc0+tscolor('\c00????00')+'Year: '+tscolor('\c00??????')+elm['year']+' | '	
        if elm.get('duration','')       != '': desc0 = desc0+tscolor('\c00????00')+'Duration: '+tscolor('\c00??????')+elm['duration']+' | '	
        if elm.get('genres','')         != '': desc0 = desc0+'\n'+tscolor('\c00????00')+'Genre: '+tscolor('\c00??????')+elm['genres']
        if inf[0].get('text','')        != '':
            if desc0.strip()!='': desc0 = desc0+'\n'+inf[0]['text']
            else: desc0 = inf[0]['text']
        desc0 = desc0.strip()
        return desc0

def _pluginSearch(plugin, sSearchText):
    try:  
        plugins = __import__('Plugins.Extensions.IPTVPlayer.tsiplayer.addons.vstream.resources.sites.%s' % plugin['identifier'], fromlist=[plugin['identifier']])
        function = getattr(plugins, plugin['search'][1])
        sUrl = plugin['search'][0] + str(sSearchText)
        function(sUrl)    
        printDBG('Load Search: ' + str(plugin['identifier']))
    except:
        printDBG(plugin['identifier'] + ': search failed')

   
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'tsiplayer.cookie'})
        self.USER_AGENT    = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
        self.MAIN_URL      = '/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/vstream'
        self.MAIN_URL0     = MAIN_URL0
        self.fncs_search   = fncs_search
        self.MAIN_IMP      = 'from '+self.MAIN_URL0.replace('/usr/lib/enigma2/python/','').replace('/','.')
        self.HTTP_HEADER   = {'User-Agent': self.USER_AGENT}
        self.defaultParams = {'header':self.HTTP_HEADER}
        self.getPage       = self.cm.getPage
        self.MyPath        = GetCacheSubDir('Tsiplayer')
        printDBG('------------ MyPath= '+self.MyPath)
        self.path_listing  = self.MyPath + 'VStream_listing'
        self.workflag      = self.MyPath + 'addon_working.txt'
        self.DB_path       = self.MyPath + 'matrix_DB'
        if config.plugins.iptvplayer.tsi_resolver.value=='tsiplayer':
            self.ts_up = ts_urlparser()
        else:
            self.ts_up = urlparser()
        
        if not os.path.exists(self.MyPath + 'tmdb'):
            os.makedirs(self.MyPath + 'tmdb')
        files = glob.glob(self.MyPath + 'tmdb/*')
        for f in files:
            os.remove(f)   
 
    def showmenu(self,cItem):
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'Sites','icon':cItem['icon'],'mode':'01'})
        printDBG(str({'import':cItem['import'],'category' : 'host2','title':'Main','icon':cItem['icon'],'mode':'03'}))
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'Main','icon':cItem['icon'],'mode':'03'})

    def showmenuHome(self,cItem):
        sys.argv = ''
        oHome = cHome()
        oHome.load()
        self.showResult(cItem)        
        
    def showmenu0(self,cItem):
        folder = self.MAIN_URL0 #self.MAIN_URL+'/matrix/sites'
        lst    = os.listdir(folder)
        lst.sort()
        params={}
        for (dir_) in lst:
            if (dir_.endswith('.py')) and ('init' not in dir_) and ('globalSources' not in dir_)and ('globalSearch' not in dir_):
                if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer_local/'):
                    file_   = dir_.replace('.py','')   
                    elm = ['plugin://plugin.video.vstream/', '13', 'site='+file_+'&siteUrl=&sTitleWatched=']
                    sys.argv = elm                
                    image   = 'file:///usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/vstream/resources/art/sites/'+file_+'.png'
                    import_ = self.MAIN_IMP+'.' + file_+' import '
                    printDBG('import_+SITE_DESC='+import_+'SITE_DESC')
                    exec (import_+'SITE_DESC',globals())
                    desc = convert_desc(SITE_DESC) 
                    elm={'import':cItem['import'],'category' : 'host2','argv':elm,'sSiteName':file_,'params':params,'import_':import_,'title':file_.replace('_','.').title(),'desc':desc,'icon':image,'mode':'10'}
                    self.addDir(elm)
                else:
                    try:
                        file_   = dir_.replace('.py','')   
                        elm = ['plugin://plugin.video.vstream/', '13', 'site='+file_+'&siteUrl=&sTitleWatched=']
                        sys.argv = elm                
                        image   = 'file:///usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/vstream/resources/art/sites/'+file_+'.png'
                        import_ = self.MAIN_IMP+'.' + file_+' import '
                        printDBG('import_+SITE_DESC='+import_+'SITE_DESC')
                        exec (import_+'SITE_DESC',globals())
                        desc = convert_desc(SITE_DESC) 
                        elm={'import':cItem['import'],'category' : 'host2','argv':elm,'sSiteName':file_,'params':params,'import_':import_,'title':file_.replace('_','.').title(),'desc':desc,'icon':image,'mode':'10'}
                        self.addDir(elm)
                    except:
                        pass	
        if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer_local/'):
            folder = self.MAIN_URL0.replace('/sites','/hosters') #self.MAIN_URL+'/matrix/sites'
            lst    = os.listdir(folder)
            lst.sort()
            cHoster = cHosterGui()
            for (dir_) in lst:
                if (dir_.endswith('.py')) and ('init' not in dir_) and ('hoster.py' not in dir_):
                    printDBG(' ------> import_ '+dir_)
                    file_   = dir_.replace('.py','') 
                    oHoster = cHoster.getHoster(file_)
                    self.addMarker({'title':file_,'desc':'','icon':''} )	

    def showmenu1(self,cItem):
        printDBG('showmenu1')
        sFunction   = cItem.get('sFunction','load')
        sSiteName   = cItem.get('sSiteName','')
        siteurl     = cItem.get('sSiteUrl','')
        sys.argv    = cItem.get('argv',['plugin://plugin.video.vstream/', '13', '?'])   
        import_     = self.MAIN_IMP+'.' + sSiteName+' import '
        if sFunction.lower() in self.fncs_search:
            if sSiteName != 'globalSearch':
                if self.write_search():
                    pass
                else:
                    return False
        
        if (sSiteName=='globalSearch'):
            sFunction = 'showSearch'
            f = open(self.workflag, "w")
            f.write('OK')
            f.close()
            
        if (sSiteName=='cHome'):         
            oHome = cHome()
            printDBG('exec='+'oHome.'+sFunction+'()')
            exec ('oHome.'+sFunction+'()')
        else:
            exec (import_+sFunction)
            exec (sFunction+'()')           
        
        if os.path.exists(self.workflag):	
            os.remove(self.workflag)

        self.showResult(cItem)   

    def showResult(self,cItem):
        import_   = cItem.get('import_','')
        path_listing = GetCacheSubDir('Tsiplayer') + 'Matrix_listing.json'
        with open(path_listing) as f:
            listing = f.read()
        #printDBG('listing='+listing)
        listing = json_loads(listing)
        nb_list = len(listing)
        for Items in listing:           
            printDBG('Item'+str(Items))   
            icon           = str(Items.get('icon',''))
            thumb          = str(Items.get('thumb',''))
            if thumb != '': icon = thumb
            
            icon           = icon.replace('plugin.video.xxxx','plugin.video.vstream')
            icon           = icon.replace('special://home/addons/plugin.video.vstream/resources/','file:///usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/vstream/resources/')
            sTitle         = Items.get('title','')
            sTitle         = sTitle.replace('\xc3\xa9','é').replace('\xe9','é').replace('\xe8','è').replace('\xe0','à')
            sTitle         = replaceColors(sTitle)
            sDescription   = getDesc(Items)
            if sDescription == '': sDescription = cItem.get('desc','')
            sSiteUrl       = Items.get('siteUrl','')
            sSiteName      = Items.get('sId','')
            sFunction      = Items.get('sFav','')
            sFileName      = Items.get('sFileName','')
            sParams        = Items.get('sParams','')
            sMeta          = Items.get('sMeta','')
            argv           = ['plugin://plugin.video.vstream/', '13','?'+sParams]            
            Year           = ''
            sHosterIdentifier    = Items.get('sHosterIdentifier','')
            sMediaUrl    = Items.get('sMediaUrl','')
            
            sMeta = str(sMeta).replace('1', 'movie').replace('2', 'tvshow').replace('3', 'collection').replace('4', 'anime').replace('7', 'person').replace('8', 'network')
            
            if sMeta in ['tvshow','movie','collection','anime','person','network']:
                EPG = True
            else:
                EPG = False 
            if ('Tools' != sTitle.strip()) and ('My accounts' != sTitle.strip()) and ('Continue watching' != sTitle.strip()) and ('Search history' != sTitle.strip()) and ('Bookmarks' != sTitle.strip()) and ('Mes contenus' != sTitle.strip()):
                if sFunction=='DoNothing':
                    if (nb_list==1) and (sTitle.strip()==''):
                        sTitle = tscolor('\c00??8888')+ 'No informations'
                    self.addMarker({'title':sTitle,'desc':'','icon':icon} )	
                elif ((sFunction=='play') or (sFunction=='play__') or ((sSiteName=='radio') and (sFunction==''))) or (sHosterIdentifier =='lien_direct'): 
                    if (sMediaUrl!='') and (sMediaUrl!=False):
                        url = sMediaUrl
                    else:
                        url = sSiteUrl
                    if (sHosterIdentifier == False):
                        sHosterIdentifier ='lien_direct'

                    if (sHosterIdentifier =='lien_direct') :
                        host = 'direct'
                    else:
                        host = 'none' 

                    host = 'tshost'
                    color = ''
                    printDBG(' ----- > Items='+str(Items))
                    printDBG(' ----- > url='+str(url))
                    host_ = urlparser.getDomain(url).replace('www.','')
                    if sHosterIdentifier=='lien_direct':
                        color = tscolor('\c0060??60')  
                    elif ts_urlparser().checkHostSupportbyname(host_):
                        color = tscolor('\c0090??20')
                    elif ts_urlparser().checkHostNotSupportbyname(host_):
                        color = tscolor('\c00??3030')
                    elif ts_urlparser().checkHostSupportbyname_e2iplayer(host_):
                        color = tscolor('\c00????60')
                    regexp = re.compile(r'[ء-ي]')
                    if (regexp.search(sTitle)) and (not sTitle.startswith('I-')):
                        sTitle       = 'I- '+sTitle                    
                    sTitle = '| '+sTitle +' | '+color+urlparser.getDomain(url).replace('www.','').title()
                    sDescription  = tscolor('\c00????00')+'Host: '+tscolor('\c00??????')+sHosterIdentifier.title()+'\n'+sDescription
                    vid = {'import':cItem['import'],'EPG':EPG,'sMeta':sMeta,'good_for_fav':True,'category' : 'video','url': url,'sHosterIdentifier':sHosterIdentifier,'title':sTitle,'desc':sDescription,'icon':icon,'hst':host,'gnr':1}
                    printDBG('VID='+str(vid))
                    self.addVideo(vid)						                 
                elif sTitle!='None':
                    dir = {'good_for_fav':True,'EPG':EPG,'sMeta':sMeta,'import':cItem['import'],'sFileName':sFileName,'Year':Year,'category' : 'host2','title':sTitle,'sFunction':sFunction,'sSiteUrl':sSiteUrl,'desc':sDescription,'sSiteName':sSiteName,'argv':argv,'icon':icon,'mode':'10','import_':import_,'hst':'tshost'}
                    printDBG('DIR='+str(dir))
                    self.addDir(dir)			

    def get_links(self,cItem): 	
        urlTab = []
        gnr    = cItem.get('gnr',0)
        sHosterIdentifier = cItem['sHosterIdentifier']
        sMediaUrl         = cItem['url']
        printDBG('get_links URL='+str(sMediaUrl))
        printDBG('sys.argv='+str(sys.argv))
        if (sHosterIdentifier == 'lien_direct') or (sHosterIdentifier ==''): gnr=0
        if gnr ==0:
            URL,meta_ = get_url_meta(sMediaUrl)
            if 'm3u8' in URL:
                URL = strwithmeta(URL,meta_)	
                urlTab = getDirectM3U8Playlist(URL, False, checkContent=True, sortWithMaxBitrate=999999999)
            else:
                URL=strwithmeta(URL,meta_)
                urlTab.append({'name':'Direct', 'url':URL, 'need_resolve':0})
        elif gnr==1:
            try_tsiplayer = False
            try:
                from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.vstream.resources.lib.gui.hoster import cHosterGui
                cHoster = cHosterGui()
                oHoster = cHoster.getHoster(sHosterIdentifier)
                oHoster.setUrl(sMediaUrl)				
                aLink = oHoster.getMediaLink()
                printDBG('aLink='+str(aLink))
            except Exception as e:
                aLink = [False,'']
                printExc()
            if aLink:
                if (aLink[0] == True):
                    URL = aLink[1]
                    if'||'in URL: urls = URL.split('||')
                    else: urls = [URL]
                    for URL in urls:
                        if URL.strip()!='':
                            label=''
                            if '|tag:' in URL: URL,label = URL.split('|tag:',1)
                            printDBG('URL='+URL)
                            if URL.startswith('//'): URL = 'http:'+URL                            
                            URL,meta = get_url_meta(URL)
                            URL = strwithmeta(URL, meta)

                            printDBG('URL='+URL)
                            urlTab.append({'url':URL , 'name': sHosterIdentifier+' '+label})
                else:
                    try_tsiplayer = True
            else:
                try_tsiplayer = True
            if try_tsiplayer:
                printDBG('Try with TSIPLAYER Parser')
                if (ts_urlparser().checkHostSupport(str(sMediaUrl))==1) or (urlparser().checkHostSupport(str(sMediaUrl))==1):
                    url_ = str(sMediaUrl).replace('://www.youtube.com/embed/','://www.youtube.com/watch?v=')
                    printDBG('TSIPLAYER Parser Found :'+url_+ '('+str(sMediaUrl)+')')
                    urlTab.append({'name':'Tsiplayer', 'url':url_, 'need_resolve':1})  
        return urlTab	


    def getArticle(self,cItem):
        otherInfo = {}
        icon       = cItem.get('icon','')
        titre      = cItem.get('title','')
        desc       = cItem.get('desc','')        
        sFileName  = cItem.get('sFileName','')
        Year       = cItem.get('Year','')
        sMeta      = cItem.get('sMeta','')
        if sFileName.strip() == '': sFileName = titre        
        printDBG('elm_0='+str((sMeta, sFileName,str(Year))))
        grab       = cTMDb()
        elm        = grab.get_meta(sMeta, sFileName, year=str(Year))
        printDBG('elm_1='+str(elm))
        duration = elm.get('duration',0)
        if (duration!='') and (duration!=0):
            try:
                duration = time.strftime('%-Hh %Mmn', time.gmtime(int(duration)))
            except:
                pass        
        if (duration != 0) and (duration != ''): 
            otherInfo['duration'] = str(duration)
        if elm.get('rating',0)          != 0 : otherInfo['tmdb_rating'] = str(elm['rating'])
        if elm.get('year',0)            != 0 : otherInfo['year']        = str(elm['year'])
        if elm.get('writer','')         != '': otherInfo['writers']     = str(elm['writer'])
        if elm.get('genre','')          != '': otherInfo['genres']      = str(elm['genre'])
        if elm.get('studio','')         != '': otherInfo['station']     = str(elm['studio'])
        if elm.get('director','')       != '': otherInfo['directors']   = str(elm['director'])
        if elm.get('plot','')           != '':
            desc = tscolor('\c00????00')+'Plot: '+tscolor('\c0000????')+str(elm['plot'])
        if elm.get('poster_path','') != '':
            poster_path = str(elm['poster_path'])#.replace('/0/','/w342/')
            printDBG('poster_path = '+str(poster_path))
            
            #if poster_path !='https://image.tmdb.org/t/p/0None':
            icon = poster_path             
        return [{'title':titre, 'text': desc, 'images':[{'title':'', 'url':icon}], 'other_info':otherInfo}]        


    def start(self,cItem):      
        if os.path.exists(self.workflag):	
            os.remove(self.workflag)
            GetIPTVSleep().Sleep(5)
        files = glob.glob(self.MyPath + 'tmdb/*')
        for f in files:
            os.remove(f)
        self.currList = []
        mode=cItem.get('mode', None)
        printDBG('Start:'+str(cItem))
        if mode=='00':
            self.showmenu(cItem)
            #self.showmenuHome(cItem)
        if mode=='01':
            self.showmenu0(cItem)	
        if mode=='02':
            self.searchGlobal(cItem)
        if mode=='03':
            self.showmenuHome(cItem)	            
        if mode=='10':
            self.showmenu1(cItem)
        

    def write_search(self,txt='',txt_def=''):
        if txt_def == '':
            if os.path.isfile(self.MyPath +'searchSTR'):
                with open(self.MyPath + 'searchSTR','r') as f:
                    txt_def = f.read().strip() 
        if txt == '':
            ret = self.sessionEx.waitForFinishOpen(GetVirtualKeyboard(), title=_('Set file name'), text=txt_def)
            input_txt = ret[0]
            printDBG ('retttttttttt='+str(ret))
        else: input_txt = txt 
        try:
            basestring
        except NameError:
            basestring = str
        if isinstance(input_txt, basestring):
            file = open(self.MyPath + 'searchSTR', 'w')
            file.write(input_txt)
            file.close() 
            return True
        else:
            printDBG ('keybord_exit')
            return False
 
