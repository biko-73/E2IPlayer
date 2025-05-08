# -*- coding: utf-8 -*-

###################################################
# LOCAL import
###################################################
#from Plugins.Extensions.IPTVPlayer.libs.pCommon                    import common

from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit       import SetIPTVPlayerLastHostError, GetIPTVSleep
from Plugins.Extensions.IPTVPlayer.components.recaptcha_v2helper   import CaptchaHelper
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes                 import strwithmeta
from Plugins.Extensions.IPTVPlayer.tools.iptvtools                 import printDBG, printExc, GetCookieDir, formatBytes, rm
from Plugins.Extensions.IPTVPlayer.tools.iptvtools                 import MergeDicts,GetJSScriptFile,CSelOneLink
from Plugins.Extensions.IPTVPlayer.libs.youtube_dl.utils           import unescapeHTML, clean_html
from Plugins.Extensions.IPTVPlayer.libs.urlparserhelper            import captchaParser, getDirectM3U8Playlist, getMPDLinksWithMeta, decorateUrl, unicode_escape
from Plugins.Extensions.IPTVPlayer.iptvdm.iptvdh                   import DMHelper
from Plugins.Extensions.IPTVPlayer.tools.e2ijs                     import js_execute, js_execute_ext
from Plugins.Extensions.IPTVPlayer.libs.e2ijson                    import loads as json_loads, dumps as json_dumps
from Plugins.Extensions.IPTVPlayer.libs                            import ph
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.packer           import cPacker
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.util     import AADecoder,decodeAA,JJDecoder,cParser,JSUnfuck
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.utils            import IsPython3,Unquote,Quote,QuotePlus
if IsPython3():
    from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.pCommon3       import common, CParsingHelper
    from urllib.parse import urlparse, parse_qs
else:
    from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.pCommon2       import common, CParsingHelper
    from urlparse import urlparse, parse_qs


###################################################
# FOREIGN import
###################################################
import re
import base64
import json
import random
import string
import time


from Components.config import config
###################################################

from binascii import unhexlify
from hashlib import md5
from Plugins.Extensions.IPTVPlayer.libs.crypto.cipher.aes_cbc import AES_CBC
import os,json,io
try:
    from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.youtubedl_data.youtube_dl.extractor import (YoutubePlaylistIE,YoutubeIE,)
    from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.youtubedl_data.youtube_dl import YoutubeDL
    class YDL(YoutubeDL):
        def __init__(self, override=None):
            # Different instances of the downloader can't share the same dictionary
            # some test set the "sublang" parameter, which would break the md5 checks.
            params = get_params(override=override)
            super(YDL, self).__init__(params, auto_init=False)
            self.result = []

        def to_screen(self, s, skip_eol=None):
            print(s)

        def trouble(self, s, tb=None):
            raise Exception(s)

        def download(self, x):
            self.result.append(x)

        def expect_warning(self, regex):
            # Silence an expected warning matching a regex
            old_report_warning = self.report_warning

            def report_warning(self, message):
                if re.match(regex, message):
                    return
                old_report_warning(message)
            self.report_warning = types.MethodType(report_warning, self)	
except:
    pass

def get_params(override=None):
    parameters=''
    PARAMETERS_FILE = "/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/youtubedl_data/parameters.json"
    with io.open(PARAMETERS_FILE, encoding='utf-8') as pf:
        parameters = json.load(pf)
    return parameters
    



def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)


def cryptoJS_AES_decrypt(encrypted, password, salt):
    def derive_key_and_iv(password, salt, key_length, iv_length):
        d = d_i = ''
        while len(d) < key_length + iv_length:
            d_i = md5(d_i + password + salt).digest()
            d += d_i
        return d[:key_length], d[key_length:key_length+iv_length]
    bs = 16
    key, iv = derive_key_and_iv(password, salt, 32, 16)
    cipher = AES_CBC(key=key, keySize=32)
    return cipher.decrypt(encrypted, iv)
    
    
def DecodeAllThePage(html):
    Maxloop = 10
    while (Maxloop > 0):
        Maxloop = Maxloop - 1
        r = re.search(r'unescape\("([^"]+)"\)', html, re.DOTALL | re.UNICODE)
        if not r:
            break
        tmp = cUtil().unescape(r.group(1))
        html = html[:r.start()] + tmp + html[r.end():]
    while (Maxloop > 0):
        Maxloop = Maxloop - 1
        r = re.search(r'(;eval\(function\(w,i,s,e\){.+?\)\);)\s*<', html, re.DOTALL | re.UNICODE)
        if not r:
            break
        tmp = data = unwise.unwise_process(r.group(1))
        html = html[:r.start()] + tmp + html[r.end():]
    return html


def Cdecode(sHtmlContent,encodedC):
    oParser = cParser()
    sPattern =  '<([0-9a-zA-Z]+)><script>([^<]+)<\/script>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    z = []
    y = []
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            z.append(JJDecoder(aEntry[1]).decode())
        #VSlog(z)
        printDBG('z='+str(z))
        for x in z:
            r1 = re.search("atob\(\'([^']+)\'\)", x, re.DOTALL | re.UNICODE)
            if r1:
                y.append(base64.b64decode(r1.group(1)))
        printDBG('y='+str(y))		
        for w in y:
            r2 = re.search(encodedC + "='([^']+)'", w)
            if r2:
                return r2.group(1)
            else:
                if '|' in w:
                    return w.split('|')[1]			
def decode(urlcoded,a,b,c):
    TableauTest = {}
    key = ''

    l = a
    n = "0123456789"
    h = b
    j = 0

    while j < len(l) :
        k = 0
        while k < len(n):
            TableauTest[l[j] + n[k]] = h[int(j + k)]

            k+=1

        j+=1

    hash = c
    i = 0
    while i < len(hash):
        key = key + TableauTest[hash[i] + hash[i + 1]]
        i+= 2


    chain = base64.b64decode(urlcoded)

    secretKey = {}
    y = 0
    temp = ''
    url = ""

    x = 0
    while x < 256:
        secretKey[x] = x
        x += 1

    x = 0
    while x < 256:
        y = (y + secretKey[x] + ord(key[x % len(key)])) % 256
        temp = secretKey[x]
        secretKey[x] = secretKey[y]
        secretKey[y] = temp
        x += 1

    x = 0
    y = 0
    i = 0
    while i < len(chain):
        x += 1 % 256
        y = (y + secretKey[x]) % 256
        temp = secretKey[x]
        secretKey[x] = secretKey[y]
        secretKey[y] = temp

        url = url + (chr(ord(chain[i]) ^ secretKey[(secretKey[x] + secretKey[y]) % 256]))

        i += 1
        
    return url


class urlparser:
    def __init__(self):
        self.cm = common()
        self.pp = pageParser()
        self.setHostsMap()
        
    @staticmethod
    def getDomain(url, onlyDomain=True):
        parsed_uri = urlparse( url )
        if onlyDomain:
            domain = '{uri.netloc}'.format(uri=parsed_uri)
        else:
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return domain
    
    @staticmethod
    def decorateUrl(url, metaParams={}):
        return decorateUrl(url, metaParams)
        
    @staticmethod
    def decorateParamsFromUrl(baseUrl, overwrite=False):
        printDBG("urlparser.decorateParamsFromUrl ---> %s" % baseUrl)
        tmp        = baseUrl.split('|')
        baseUrl    = strwithmeta(tmp[0].strip(), strwithmeta(baseUrl).meta)
        KEYS_TAB = list(DMHelper.HANDLED_HTTP_HEADER_PARAMS)
        KEYS_TAB.extend(["iptv_audio_url", "iptv_proto", "Host", "Accept", "MPEGTS-Live", "PROGRAM-ID"])
        if 2 == len(tmp):
            baseParams = tmp[1].strip()
            try:
                params  = parse_qs(baseParams)
                printDBG("PARAMS FROM URL [%s]" % params)
                for key in params.keys():
                    if key not in KEYS_TAB: continue
                    if not overwrite and key in baseUrl.meta: continue
                    try: baseUrl.meta[key] = params[key][0]
                    except Exception: printExc()
            except Exception: printExc()
        baseUrl= urlparser.decorateUrl(baseUrl)
        return baseUrl

    def preparHostForSelect(self, v, resolveLink = False):
        valTab = []
        i = 0
        if len(v) > 0:
            for url in (v.values() if type(v) is dict else v):
                if 1 == self.checkHostSupport(url):
                    hostName = self.getHostName(url, True)
                    i=i+1
                    if resolveLink:
                        url = self.getVideoLink( url )
                    if isinstance(url, basestring) and url.startswith('http'):
                        valTab.append({'name': (str(i) + '. ' + hostName), 'url': url})
        return valTab

    def getItemTitles(self, table):
        out = []
        for i in range(len(table)):
            value = table[i]
            out.append(value[0])
        return out

        
    def setHostsMap(self):
        self.hostMap = {'youdbox.com'     : self.pp.parserUNI01,
                        'youdbox.net'     : self.pp.parserUNI01,
                        'youdbox.org'     : self.pp.parserUNI01,
                        #'youdbox.com'     : self.pp.parserYOUDBOX,
                        #'youdbox.net'     : self.pp.parserYOUDBOX,
                        #'youdbox.org'     : self.pp.parserYOUDBOX,
                        'userload.co'     : self.pp.parserVSTREAM,#self.pp.parserUSERLOAD,
                        'embed.mystream.to':self.pp.parserVSTREAM,
                        'uptostream.com'  : self.pp.parserVSTREAM,
                        'uptobox.com'     : self.pp.parserVSTREAM,                        
                        'streamtape.com'  : self.pp.parserVSTREAM,
                        'streamtape.site' : self.pp.parserVSTREAM,                     
                        'evoload.io'      : self.pp.parserVSTREAM, 
                        'dood.so'         : self.pp.parserVSTREAM,
                        'doodstream.co'   : self.pp.parserVSTREAM,
                        'doodstream.so'   : self.pp.parserDOOD,
                        'protonvideo.to'  : self.pp.parserPROTONVIDEO,
                        'linkbox.to'      : self.pp.parserLINKBOX,                        
                        'thevideobee.to'  : self.pp.parserUNI01,
                        'uqload.com'      : self.pp.parserUNI01,
                        'vidia.tv'        : self.pp.parserUNI01,
                        'vidfast.co'      : self.pp.parserUNI01,
                        'vidoza.net'      : self.pp.parserUNI01,
                        'upstream.to'     : self.pp.parserUNI01,
                        'samaup.co'       : self.pp.parserUNI01,
                        'clipwatching.com': self.pp.parserUNI01,	
                        'vidhd.net'       : self.pp.parserUNI01,
                        'vidlox.tv'       : self.pp.parserUNI01, 
                        'vidlox.me'       : self.pp.parserUNI01,   
                        'gounlimited.to'  : self.pp.parserUNI01,
                        'filerio.in'      : self.pp.parserUNI01,
                        'cloudvideo.tv'   : self.pp.parserUNI01,
                        'vup.to'          : self.pp.parserUNI01,
                        'video.sibnet.ru' : self.pp.parserUNI01,
                        'watchvideo.us'   : self.pp.parserUNI01,
                        'letsupload.co'   : self.pp.parserUNI01, 
                        'vidsat.net'      : self.pp.parserUNI01,
                        'hdvid.tv'        : self.pp.parserUNI01,	
                        'mp4upload.com'   : self.pp.parserUNI01,
                        'supervideo.tv'   : self.pp.parserUNI01,
                        'vudeo.net'	      : self.pp.parserUNI01,	
                        'streamwire.net'  : self.pp.parserUNI01,
                        'vidshare.tv'     : self.pp.parserUNI01,
                        'vidshaar.com'    : self.pp.parserUNI01,                        
                        'vidshar.tv'      : self.pp.parserUNI01,
                        'vidshar.net'     : self.pp.parserUNI01,						
                        'videobin.co'     : self.pp.parserUNI01,
                        'youflix.me'      : self.pp.parserUNI01,
                        'imdb.com'        : self.pp.parserUNI01,
                        'hdup.net'        : self.pp.parserUNI01,
                        'govid.co'        : self.pp.parserUNI01,
                        'vidbm.com'       : self.pp.parserUNI01,
                        'vidbem.com'      : self.pp.parserUNI01,
                        'vidbom.com'      : self.pp.parserUNI01,
                        'vidbeem.com'     : self.pp.parserUNI01,
                        'vedbom.com'      : self.pp.parserUNI01,
                        'vedpom.com'      : self.pp.parserUNI01, 
                        'vedsharr.com'    : self.pp.parserUNI01,                         
                        'vedshar.com'     : self.pp.parserUNI01,                        
                        'asia2tv.cc'      : self.pp.parserUNI01,
                        'asiatv.online'   : self.pp.parserUNI01,						
                        'allvid.co'       : self.pp.parserUNI01,
                        'moshahda.online' : self.pp.parserUNI01,
                        'moshahda.net'    : self.pp.parserUNI01,
                        'anavids.com'     : self.pp.parserUNI01,
                        'sendvid.com'     : self.pp.parserUNI01,
                        'arabseed.me'     : self.pp.parserUNI01,
                        'arabveturk.com'  : self.pp.parserUNI01,
                        'okgaming.org'    : self.pp.parserUNI01,
                        'okanime.com'     : self.pp.parserUNI01, 
                        'filesload.xyz'   : self.pp.parserUNI01,
                        'mightyupload.com': self.pp.parserUNI01,
                        'vidlo.us'        : self.pp.parserUNI01,
                        'aparat.cam'      : self.pp.parserUNI01,
                        'playtube.ws'     : self.pp.parserUNI01,
                        'extremenow.net'  : self.pp.parserUNI01,
                        'streamsb.net'    : self.pp.parserUNI01,
                        'sbembed1.com'    : self.pp.parserUNI01,
                        'kobatube.xyz'    : self.pp.parserUNI01, 
                        'oktube.co'       : self.pp.parserUNI01,
                        'rumble.com'      : self.pp.parserRUMBLE,                
                        'movcloud.net'    : self.pp.parserMOVCLOUD,                        
                        'ninjastream.to'  : self.pp.parserNINJASTREAMTO,                        
                        'movs4u.club'     : self.pp.parserMOVS4U,
                        'dustreaming.fr'  : self.pp.parserDUSTREAMING,
                        'fcdn.stream'     : self.pp.parserDUSTREAMING,                        
                        'vid4up.com'      : self.pp.parserZIMABDKO,						
                        'gofile.io'       : self.pp.parserGOFILE,
                        'okstream.cc'     : self.pp.parserOKSTREAM,
                        'saruch.co'       : self.pp.parserSARUCH,
                        'zimabdko.com'    : self.pp.parserZIMABDKO,
                        'abcvideo.cc'     : self.pp.parserABCVIDEO,
                        'fembed.net'	  : self.pp.parserFEURL, 						
                        'feurl.com'	      : self.pp.parserFEURL, 
                        'playvid.pw'	  : self.pp.parserFEURL, 
                        'fsimg.info'	  : self.pp.parserFEURL,
                        'mg-play.info'	  : self.pp.parserFEURL,										
                        'easyload.io'     : self.pp.parserEASYLOAD,	
                        'dood.to'         : self.pp.parserDOOD,	
                        'dood.watch'      : self.pp.parserDOOD,	
                        'deepmic.com'     : self.pp.parserDEEPMIC,#self.pp.parserVIDOZANET,							
                        'mixdrop.to'      : self.pp.parserMIXDROP,	
                        'mixdrop.co'      : self.pp.parserMIXDROP,								
                        'jawcloud.co'     : self.pp.parserJAWCLOUDCO,						
                        'vidtodo.com'     : self.pp.parserVIDTODOCOM,						
                        'tune.pk'         : self.pp.parseTUNEPLUS,
                        'tuneplus.co'     : self.pp.parseTUNEPLUS,                        
                        #'dailymotion.com' : self.pp.parserDAILYMOTION,
                        'youtube.com'     : self.pp.parserYOUTUBE1, 
                        #'youtu.be'        : self.pp.parserYOUTUBE,
                        'ok.ru'           : self.pp.parserOKRU,						
                        'flashx.tv'       : self.pp.parserFLASHXTV, 
                        'flashx.pw'       : self.pp.parserFLASHXTV, 
                        'flashx.co'       : self.pp.parserFLASHXTV,
                        #'uptobox.com'     : self.pp.parserUPTOSTREAMCOM,	
                        'google.com'      : self.pp.parserGOOGLE, 
                        'fembed.com'      : self.pp.parserXSTREAMCDNCOM, 
                        'uppom.live'      :	self.pp.downUPPOM, 	
                        'sandup.co'       : self.pp.downSANDUP,
                        't7meel.co'       : self.pp.downTA7MEEL,
                        't7meel.site'     : self.pp.downTA7MEEL,                         
                        #					
                        #'hqq.tv'          : self.pp.parserHQQ,
                        'verystream.com'  : self.pp.parserVERYSTREAM,
                        'woof.tube'       : self.pp.parserVERYSTREAM,	
                        'thevid.live'     : self.pp.parserTHEVIDLIVE, 
                        'thevid.net'      : self.pp.parserTHEVIDLIVE, 
                        'onlystream.tv'   : self.pp.parserSTD03,
                        'vcstream.to'     : self.pp.parserVCSTREAMTO,
                        'vidcloud.co'     : self.pp.parserVCSTREAMTO,
                        'rapidvideo.com'  : self.pp.parserRAPIDVIDEO,
                        'rapidvideo.is'   : self.pp.parserRAPIDVIDEO,
                        'rapidvid.to'     : self.pp.parserRAPIDVIDEO,
                        'streamcherry.com': self.pp.parserSTREAMANGOCOM,
                        'govid.me'        : self.pp.parserGOVIDME, 		
                        'vidspeed.net'    : self.pp.parserSTD05,					
                        #'streamango.com'  : self.pp.parserSTREAMANGOCOM,
                        #'openload.co'     : self.pp.parserOPENLOADCO, 
                        #'openload.pw'     : self.pp.parserOPENLOADCO, 
                        #'oload.tv'        : self.pp.parserOPENLOADCO, 
                        #'oload.stream'    : self.pp.parserOPENLOADCO, 
                        #'oload.site'      : self.pp.parserOPENLOADCO, 
                        #'oload.download'  : self.pp.parserOPENLOADCO, 
                        #'oload.life'      : self.pp.parserOPENLOADCO,
                        #'oload.biz'       : self.pp.parserOPENLOADCO,
                        #'vev.io'          : self.pp.parserTHEVIDEOME, 						
                        #'vev.red'         : self.pp.parserTHEVIDEOME,
                        #'thevideo.me'     : self.pp.parserTHEVIDEOME,
                        #'deepmic.com'      : self.pp.parserSTD04,
                        #'vidstream.in'    : self.pp.parserVIDSTREAM,
                        #'vidstream.to'    : self.pp.parserVIDSTREAM,
                        #'faststream.in'   : self.pp.parserVIDSTREAM,   						 
                        'waaw.tv'         : self.pp.parserHQQ,
                                                }
        #self.hostMap('youtube.com') = self.pp.parserYOUTUBE1 
        return

    def checkHostNotSupportbyname(self, name):
        nothostMap_404 = ['upvid','streamango.com','videoz.me','yourupload.com','openload.co','openload.pw','oload.tv','oload.stream','oload.site','oload.download','oload.life','oload.biz']
        nothostMap_not_found = ['file-up.org',]
        nothostMap_not_work = ['playhydrax.com','jetload.net','hqq.tv','waaw.tv','videomega.co','vidshare.tv','vev.red','hqq.watch','hqq.tv','netu','videoz.me','file-up.org','deepmic.com',
        'uptostream.com','uptobox.com']
        nothostMap = nothostMap_404 + nothostMap_not_found + nothostMap_not_work
        if '|' in name: name=name.split('|')[-1].strip() 
        name=name.lower().replace('embed.','').replace('www.','').replace(' ','')
        found = False
        for key in nothostMap:
            if name in key:
                found=True
                break
            elif name in key.replace('.',''):	
                found=True
                break				
        return found


    def getHostName(self, url, nameOnly = False):
        hostName = strwithmeta(url).meta.get('host_name', '')
        if not hostName:
            match = re.search('https?://(?:www.)?(.+?)/', url)
            if match:
                hostName = match.group(1)
                if (nameOnly):
                    n = hostName.split('.')
                    try: hostName = n[-2]
                    except Exception: printExc()
            hostName = hostName.lower()
        printDBG("_________________getHostName: [%s] -> [%s]" % (url, hostName))
        return hostName
        
    def getParser(self, url, host=None):
        if None == host:
            host = self.getHostName(url.replace('orno.com','.com'))
        parser = self.hostMap.get(host, None)
        if None == parser:
            host2 = host[host.find('.')+1:]
            printDBG('urlparser.getParser II try host[%s]->host2[%s]' % (host, host2))
            parser = self.hostMap.get(host2, None)
            if None == parser:
                printDBG('------------> Tester avec le Standard Parse <-------------')
                parser = self.pp.parserUNI001
        return parser

    def checkHostSupport(self, url):
        # -1 - not supported
        #  0 - unknown
        #  1 - supported
        url = url.replace('orno.com','.com')
        host  = self.getHostName(url)
        
        # quick fix
        if host == 'facebook.com' and 'likebox.php' in url or 'like.php' in url or '/groups/' in url:
            return 0
        
        ret = 0
        parser = self.getParser(url, host)
        if None != parser:
            if parser != self.pp.parserUNI001:
                return 1
        elif self.isHostsNotSupported(host):
            return -1
        return ret

    def checkHostSupportbyname(self, name):
        if '|' in name: name=name.split('|')[-1].strip()
        name=name.lower().replace('www.','').replace(' ','')
        if name.startswith('embed.'): name=name.replace('embed.','')
        found = False
        for key in self.hostMap:
            if name in key:
                found=True
                break
            elif name in key.replace('.',''):	
                found=True
                break				
        
        return found

    def checkHostSupportbyname_e2iplayer(self, name):
        if '|' in name: name=name.split('|')[-1].strip()
        if name.lower() in ['embed.mystream.to','mystream.to']:
            return True
        return False
         
    def isHostsNotSupported(self, host): 
        return host in ['rapidgator.net', 'oboom.com']

    def getVideoLinkExt(self, url):
        printDBG('>>>>>>>>> Start TS Urlparser <<<<<<')
        videoTab = []
        try:
            ret = self.getVideoLink(url, True)
            
            if isinstance(ret, str):
                if 0 < len(ret):
                    host = self.getHostName(url)
                    videoTab.append({'name': host, 'url': ret})
            elif isinstance(ret, list) or isinstance(ret, tuple):
                videoTab = ret
                
            for idx in range(len(videoTab)):
                if not self.cm.isValidUrl(url): continue
                url = strwithmeta(videoTab[idx]['url'])
                if 'User-Agent' not in url.meta:
                    #url.meta['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:21.0) Gecko/20100101 Firefox/21.0'
                    url.meta['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
                    
                    videoTab[idx]['url'] = url
        except Exception:
            printExc()
            
        return videoTab
        
    def getVideoLink(self, url, acceptsList = False):
        try:
            url = self.decorateParamsFromUrl(url)
            nUrl=''
            parser = self.getParser(url)
            if None != parser:
                nUrl = parser(url)
            else:
                host = self.getHostName(url)
                if self.isHostsNotSupported(host):
                    SetIPTVPlayerLastHostError(_('Hosting "%s" not supported.') % host)
                else:
                    SetIPTVPlayerLastHostError(_('Hosting "%s" unknown.') % host)

            if isinstance(nUrl, list) or isinstance(nUrl, tuple):
                if True == acceptsList:
                    return nUrl
                else:
                    if len(nUrl) > 0:
                        return nUrl[0]['url']
                    else:
                        return False
            return nUrl
        except Exception:
            printExc()
        return False

class pageParser(CaptchaHelper):
    HTTP_HEADER= {  'User-Agent'  : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                    'Accept'      : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Content-type': 'application/x-www-form-urlencoded' }
    FICHIER_DOWNLOAD_NUM = 0
    def __init__(self):
        self.cm = common()
        self.captcha = captchaParser()
        self.ytParser = None
        self.moonwalkParser = None
        self.vevoIE = None
        self.bbcIE = None
        self.sportStream365ServIP = None
        
        #config
        self.COOKIE_PATH = GetCookieDir('')
        self.jscode = {}
        self.jscode['jwplayer'] = 'window=this; function stub() {}; function jwplayer() {return {setup:function(){print(JSON.stringify(arguments[0]))}, onTime:stub, onPlay:stub, onComplete:stub, onReady:stub, addButton:stub}}; window.jwplayer=jwplayer;'


    def getPageCF(self, baseUrl, addParams = {}, post_data = None):
        addParams['cloudflare_params'] = {'cookie_file':addParams['cookiefile'], 'User-Agent':addParams['header']['User-Agent']}
        sts, data = self.cm.getPageCFProtection(baseUrl, addParams, post_data)
        return sts, data

    def getHostName(self, url, nameOnly = False):
        hostName = strwithmeta(url).meta.get('host_name', '')
        if not hostName:
            match = re.search('https?://(?:www.)?(.+?)/', url)
            if match:
                hostName = match.group(1)
                if (nameOnly):
                    n = hostName.split('.')
                    try: hostName = n[-2]
                    except Exception: printExc()
            hostName = hostName.lower()
        return hostName

    def parserMOVCLOUD(self, baseUrl):
        printDBG("parserMOVCLOUD baseUrl[%s]" % baseUrl)
        #example: https://movcloud.net/embed/ei-RkZ9lI_Bg
        #api url format: https://api.movcloud.net/stream/ei-RkZ9lI_Bg
        hlsTab = []
        mp4Tab = []        
        urlTabs=[]
        m = re.search("embed/(?P<id>[^/]+)($|/)",baseUrl)
        
        if m:
            video_id = m.groupdict().get('id','')
            if video_id:
                url = "https://api.movcloud.net/stream/" + video_id
                
                sts, data = self.cm.getPage(url)
                if sts:
                    response = json_loads(data)
                    printDBG(str(response))
                    
                    if response.get('success', False):
                        for s in response['data']['sources']:
                            link_url = s.get('file','')
                            label = s.get('label','Link')
                            if  self.cm.isValidUrl(link_url):
                                link_url = urlparser.decorateUrl(link_url, {'Referer': baseUrl})
                                mp4Tab.append({'name':label, 'url':link_url})                             
        urlTabs.extend(mp4Tab)
        urlTabs.extend(hlsTab)
        return urlTabs
        
    def parserVSTREAM(self, baseUrl):
        printDBG("parserVSTREAM baseUrl[%r]" % baseUrl)
        UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'
        videoTab = []
        if 'uptobox.com/' in baseUrl:
            baseUrl = baseUrl.replace('uptobox.com/', 'uptostream.com/')
        if 'doodstream.co/' in baseUrl:
            baseUrl = baseUrl.replace('doodstream.co/', 'dood.sh/')        
        
        hst_name = self.getHostName(baseUrl, True)
        printDBG("Host Name="+hst_name)
        #exec ("from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.hosters." + hst_name + " import cHoster")
        exec ("from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources.hosters." + hst_name + " import cHoster",globals())
        oHoster = cHoster()
        referer = strwithmeta(baseUrl).meta.get('Referer','')
        if 'userload' in baseUrl:
            if '|Referer=' not in baseUrl: baseUrl = baseUrl+'|Referer='+referer
        oHoster.setUrl(baseUrl)
        aLink = oHoster.getMediaLink()
        printDBG('aLink='+str(aLink))
        if (aLink[0] == True):
            URL = aLink[1]
            if'||'in URL: urls = URL.split('||')
            else: urls = [URL]
            for URL in urls:
                if URL.strip()!='':
                    label=''
                    if '|tag:' in URL: URL,label = URL.split('|tag:',1)
                    if '|User-Agent=' in URL:
                        URL,UA=URL.split('|User-Agent=',1)
                    URL = strwithmeta(URL, {'User-Agent':UA})
                    printDBG('URL='+URL)
                    videoTab.append({'url':URL , 'name': hst_name+' '+label})		
        return videoTab

    def parserXFILESHARE(self, baseUrl):
        printDBG("parserVIDSHARETV baseUrl[%s]" % baseUrl)
        
        baseUrl = strwithmeta(baseUrl)
        HTTP_HEADER= { 'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:21.0) Gecko/20100101 Firefox/21.0',
                       'Referer':baseUrl.meta.get('Referer', baseUrl),
                     }
        COOKIE_FILE = GetCookieDir("xfileshare.cookie")
        rm (COOKIE_FILE)
        params = {'header':HTTP_HEADER, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': COOKIE_FILE}
        data_player = ''
        sts, data = self.cm.getPage(baseUrl, params)
        if not sts: return
        lst_data = re.findall('jwplayer\("[^"]+"\)\.setup\(({.+?})\);', data, re.S)
        if lst_data:   
            data_player = lst_data[0]	
        lst_data = re.findall('(ﾟ.+)', data)
        if lst_data:
            jscode = 'function jwplayer() {return {load:function(){print(JSON.stringify(arguments[0]))}}}; \n%s' % lst_data[0]
            ret = js_execute( jscode )
            if ret['sts'] and 0 == ret['code']:
                data_player=data_player+ret['data']	
        cookieHeader = self.cm.getCookieHeader(COOKIE_FILE)
        dashTab = []
        hlsTab = []
        mp4Tab = []
        lst_data = re.findall('sources.*?(\[.*?\])', data_player, re.S)
        if lst_data:
            printDBG(str(lst_data[0])+'#')
            data = str(lst_data[0]).strip()
            data = data.replace('file:','"file":').replace('label:','"label":')
            items = json.loads(data)
            for item in items:
                url = item['file']
                type = item.get('type', url.split('?', 1)[0].split('.')[-1]).lower()
                label = item.get('label', type)
                
                if url.startswith('//'): url = 'http:' + url
                if not self.cm.isValidUrl(url): continue
                url = strwithmeta(url, {'Cookie':cookieHeader, 'Referer':HTTP_HEADER['Referer'], 'User-Agent':HTTP_HEADER['User-Agent']})
                #if 'dash' in url:
                    #dashTab.extend(getMPDLinksWithMeta(url, False, sortWithMaxBandwidth=999999999))
                if 'hls' in type or 'm3u8' in type:
                    hlsTab.extend(getDirectM3U8Playlist(url, checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
                elif 'mp4' in type or 'mpegurl' in type:
                    try: sortKey = int(self.cm.ph.getSearchGroups(label, '''([0-9]+)''')[0])
                    except Exception: sortKey = -1
                    mp4Tab.append({'name':'[%s] %s' % (type, label), 'url':url, 'sort_key':sortKey})
        
        videoTab = []
        mp4Tab.sort(key=lambda item: item['sort_key'], reverse=True)
        videoTab.extend(mp4Tab)
        videoTab.extend(hlsTab)
        videoTab.extend(dashTab)
        printDBG('videoTab:'+str(videoTab))
        return videoTab

    def parserVERYSTREAM(self, baseUrl):
        printDBG("parserVERYSTREAM baseUrl[%r]" % baseUrl )
        HTTP_HEADER = MergeDicts(self.cm.getDefaultHeader('firefox'), {'Referer':baseUrl})
        sts, data = self.cm.getPage(baseUrl, {'header':HTTP_HEADER})
        if not sts: return False
        #printDBG("parserVERYSTREAM data: [%s]" % data )
        id = ph.search(data, """id="videolink">([^>]+?)<""")[0]
        videoUrl = 'https://verystream.com/gettoken/{0}?mime=true'.format(id)
        sts, data = self.cm.getPage(videoUrl, {'max_data_size':0})
        if not sts: return False
        return self.cm.meta['url']		

    def parserNINJASTREAM(self, baseUrl):
        printDBG("parserNINJASTREAM baseUrl[%r]" % baseUrl )
        linksTab = []
        HTTP_HEADER = MergeDicts(self.cm.getDefaultHeader('firefox'), {'Referer':baseUrl})
        sts, data = self.cm.getPage(baseUrl, {'header':HTTP_HEADER})
        if not sts: return False
        r = re.search(r'v-bind:stream="([^"]+)', data)
        if r:
            data = json.loads(r.group(1).replace('&quot;', '"'))
            murl = self.decodeNinja(data.get('host')) + data.get('hash') + '/index.m3u8'
            murl ='https://databasegdriveplayer.co/files2.php?id=OG92KzdteWNQY0tjNC9ZUkMzVjNkUnhxZy9RMnV6QW1tK2VuVXdmUTdMNjFwUm1VNEN4RVdtU0wwZVBVZ0VNWQ==.m3u8'
            linksTab.extend(getDirectM3U8Playlist(murl, checkExt=False, checkContent=True))
        return linksTab

    def decodeNinja(self, host):
        s = ''
        for n in range(len(host)):
            s += chr(ord(host[n]) ^ ord('2'))
        return s
 

    def parserNINJASTREAMTO(self, baseUrl):
        printDBG("parserNINJASTREAMTO baseUrl [%s]" % baseUrl)

        COOKIE_FILE = GetCookieDir('ninjastream.cookie')
        httpParams = {
            'header': {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip',
                'Referer': baseUrl.meta.get('Referer', baseUrl)
            },
            'use_cookie': True,
            'load_cookie': True,
            'save_cookie': True,
            'cookiefile': COOKIE_FILE
        }

        urlsTab = []

        sts, data = self.cm.getPage(baseUrl, httpParams)
        if sts:
            r = self.cm.ph.getSearchGroups(data, r'v-bind:[n|s]*stream="([^"]+?)"')[0].replace('&quot;', '"')
            if not r:
                r = self.cm.ph.getSearchGroups(data, r'v-bind:[n|s]*file="([^"]+?)"')[0].replace('&quot;', '"')
            printDBG("parserNINJASTREAMTO r [%s]" % r)
            httpParams['header']['X-Requested-With'] = 'XMLHttpRequest'
            httpParams['header']['x-csrf-token'] = self.cm.ph.getSearchGroups(data, '''<[^>]+?csrf-token[^>]+?content=['"]([^'^"]+?)['"]''')[0]
            httpParams['header']['x-xsrf-token'] = self.cm.getCookieItem(COOKIE_FILE, 'XSRF-TOKEN')
            if r:
                data = json_loads(r)
                sts, data = self.cm.getPage('https://ninjastream.to/api/video/get', httpParams, {'id': data.get('hashid')})
                if sts:
                    data = json_loads(data)
                    url = data['result']['playlist']
                    urlsTab.extend(getDirectM3U8Playlist(url, checkContent=True, sortWithMaxBitrate=999999999))

        return urlsTab

 
    def parserJAWCLOUDCO(self, baseUrl):
        printDBG("parserJAWCLOUDCO baseUrl[%r]" % baseUrl)
        if 'embed' not in baseUrl:
            baseUrl = baseUrl.replace('jawcloud.co/','jawcloud.co/embed-')
        baseUrl = strwithmeta(baseUrl)
        HTTP_HEADER= self.cm.getDefaultHeader(browser='chrome')
        HTTP_HEADER['Referer'] = baseUrl.meta.get('Referer', baseUrl)
        urlParams = {'with_metadata':True, 'header':HTTP_HEADER}
        
        sts, data = self.cm.getPage(baseUrl, urlParams)
        if not sts: return False
        cUrl = self.cm.meta['url']
        domain = urlparser.getDomain(cUrl)
        
        linksTab = []
        data = self.cm.ph.getDataBeetwenMarkers(data, '<video', '</video>')[1]
        data = self.cm.ph.getAllItemsBeetwenMarkers(data, '<source', '>', False)
        for item in data:
            url = self.cm.getFullUrl(self.cm.ph.getSearchGroups(item, '''src=['"]([^'^"]+?)['"]''')[0], domain)
            type = self.cm.ph.getSearchGroups(item, '''type=['"]([^'^"]+?)['"]''')[0].lower()
            if 'video' not in type and 'x-mpeg' not in type: continue
            if url == '': continue
            if 'video' in type:
                linksTab.append({'name':'[%s]' % type, 'url':url})
            elif 'x-mpeg' in type:
                linksTab.extend(getDirectM3U8Playlist(url, checkContent=True, sortWithMaxBitrate=999999999))
        return linksTab

    def parserSTREAMANGOCOM(self, baseUrl):
        printDBG("parserSTREAMANGOCOM url[%s]\n" % baseUrl)
        baseUrl = strwithmeta(baseUrl)
        HTTP_HEADER = dict(pageParser.HTTP_HEADER) 
        
        videoTab = []
        if '/embed/' not in baseUrl:
            sts, data = self.cm.getPage(baseUrl)
            if not sts: return videoTab
            url = self.cm.ph.getSearchGroups(data, '''<iframe[^>]+?src=["'](http[^"^']+?/embed/[^"^']+?)["']''', 1, True)[0]
            if url == '':
                data = self.cm.ph.getDataBeetwenMarkers(data, 'embedbox', '</textarea>')[1]
                data = clean_html(self.cm.ph.getDataBeetwenMarkers(data, '<textarea', '</textarea>')[1])
                url = self.cm.ph.getSearchGroups(data, '''<iframe[^>]+?src=["'](http[^"^']+?/embed/[^"^']+?)["']''', 1, True)[0]
                HTTP_HEADER['Referer'] = baseUrl.meta.get('Referer', baseUrl)
        else:
            url = baseUrl
        
        sts, data = self.cm.getPage(url, {'header' : HTTP_HEADER})
        if not sts: return videoTab
        cUrl = self.cm.meta['url']

        timestamp = time.time()

        errMsg = self.cm.ph.getDataBeetwenNodes(data, ('<', '>', 'important'), ('<', '>', 'div'))[1]
        SetIPTVPlayerLastHostError(clean_html(errMsg))
        
        # select valid section
        data = self.cm.ph.getAllItemsBeetwenMarkers(data, '<script', '</script>')
        for item in data:
            if 'srces.push' in item:
                data = item
                break
                
        #jscode = 'var document = {};\nvar window = this;\n' + self.cm.ph.getDataBeetwenReMarkers(data, re.compile('<script[^>]*?>'), re.compile('var\s*srces\s*=\s*\[\];'), False)[1]
        #data = self.cm.ph.getAllItemsBeetwenMarkers(data, 'srces.push(', ');')
        #jscode += '\nvar srces=[];\n' + '\n'.join(data) + '\nprint(JSON.stringify(srces));'
        #ret = js_execute( jscode )
        
        jscode = 'var document = {};\nvar window = this;\n' + self.cm.ph.getDataBeetwenReMarkers(data, re.compile('<script[^>]*?>'), re.compile('var\s*srces\s*=\s*\[\];'), False)[1]
        js_params = [{'name':'streamgo', 'code':jscode}]
        data = self.cm.ph.getAllItemsBeetwenMarkers(data, 'srces.push(', ');')
        jscode = '\nvar srces=[];\n' + '\n'.join(data) + '\nprint(JSON.stringify(srces));'
        js_params.append({'code':jscode})
        ret = js_execute_ext( js_params )
        data = ret['data'].strip()
        data = json_loads(data)
        
        dashTab = []
        hlsTab = []
        mp4Tab = []
        printDBG(data)
        for tmp in data:
            tmp = str(tmp).split('}')
            for item in tmp:
                item += ','
                url = self.cm.ph.getSearchGroups(item, r'''['"]?src['"]?\s*:\s*['"]([^"^']+)['"]''')[0]
                if url.startswith('//'): url = cUrl.split('//', 1)[0] + url
                type = self.cm.ph.getSearchGroups(item, r'''['"]?type['"]?\s*:\s*['"]([^"^']+)['"]''')[0]
                if not self.cm.isValidUrl(url): continue
            
                url = strwithmeta(url, {'User-Agent':HTTP_HEADER['User-Agent'], 'Referer':self.cm.meta['url'], 'Range':'bytes=0-'})
                if 'dash' in type:
                    dashTab.extend(getMPDLinksWithMeta(url, False))
                elif 'hls' in type:
                    hlsTab.extend(getDirectM3U8Playlist(url, checkExt=False, checkContent=True))
                elif 'mp4' in type or 'mpegurl' in type:
                    name = self.cm.ph.getSearchGroups(item, '''['"]?height['"]?\s*\:\s*([^\,]+?)[\,]''')[0]
                    mp4Tab.append({'name':'[%s] %sp' % (type, name), 'url':url})

        videoTab.extend(mp4Tab)
        videoTab.extend(hlsTab)
        videoTab.extend(dashTab)
        if len(videoTab):
            wait = time.time() - timestamp
            if wait < 4:
                printDBG(" time [%s]" % wait)
                GetIPTVSleep().Sleep(3 - int(wait))
        return videoTab

    def parserOKRU(self, baseUrl):
        printDBG("parserOKRU baseUrl[%r]" % baseUrl)
        HTTP_HEADER= { 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                       'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Referer':baseUrl,
                       'Cookie':'_flashVersion=18',
                       'X-Requested-With':'XMLHttpRequest'}
        
        metadataUrl = ''
        if 'videoPlayerMetadata' not in baseUrl:
            sts, data = self.cm.getPage(baseUrl, {'header':HTTP_HEADER})
            if not sts: return False
            error = clean_html(self.cm.ph.getDataBeetwenNodes(data, ('<div', '>', 'vp_video_stub_txt'), ('</div', '>'), False)[1])
            if error == '': error = clean_html(self.cm.ph.getDataBeetwenNodes(data, ('<', '>', 'page-not-found'), ('</', '>'), False)[1])
            if error != '': SetIPTVPlayerLastHostError(error)
        
            tmpTab = re.compile('''data-options=['"]([^'^"]+?)['"]''').findall(data)
            for tmp in tmpTab:
                tmp = clean_html(tmp)
                tmp = json_loads(tmp)
                printDBG("====")
                printDBG(tmp)
                printDBG("====")
                
                tmp = tmp['flashvars']
                if 'metadata' in tmp:
                    data = json_loads(tmp['metadata'])
                    metadataUrl = ''
                    break
                else:
                    metadataUrl = Unquote(tmp['metadataUrl'])
        else:
            metadataUrl = baseUrl
        
        if metadataUrl != '':
            url = metadataUrl
            sts, data = self.cm.getPage(url, {'header':HTTP_HEADER})
            if not sts: return False
            data = json_loads(data)
        
        urlsTab = []
        for item in data['videos']:
            url = item['url'] #.replace('&ct=4&', '&ct=0&') #+ '&bytes'#=0-7078'
            url = strwithmeta(url, {'Referer':baseUrl, 'User-Agent':HTTP_HEADER['User-Agent']})
            urlsTab.append({'name':item['name'], 'url':url})
        urlsTab = urlsTab[::-1]
        
        if 1: #0 == len(urlsTab):
            url = urlparser.decorateUrl(data['hlsManifestUrl'], {'iptv_proto':'m3u8', 'Referer':baseUrl, 'User-Agent':HTTP_HEADER['User-Agent']})
            linksTab = getDirectM3U8Playlist(url, checkExt=False, checkContent=True)
            
            for idx in range(len(linksTab)):
                meta = dict(linksTab[idx]['url'].meta)
                meta['iptv_proto'] = 'm3u8'
                url = linksTab[idx]['url']
                if url.endswith('/'):
                    linksTab[idx]['url'] = strwithmeta(url+'playlist.m3u8', meta)
                    
            try:
                tmpUrlTab = sorted(linksTab, key=lambda item: -1 * int(item.get('bitrate', 0)))
                tmpUrlTab.extend(urlsTab)
                urlsTab = tmpUrlTab
            except Exception:  printExc()
        return urlsTab

    def parserOPENLOADCO(self, baseUrl):
        printDBG('parserOPENLOADIO baseUrl[%r]' % baseUrl)
        HTTP_HEADER = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'Accept': 'text/html', 
            #'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 
            'Accept-Encoding': 'gzip', 
            'Accept-Language': 'en-US,en;q=0.8'
        }
        #referer = strwithmeta(baseUrl).meta.get('Referer', '')
        #if referer:
        #    HTTP_HEADER['Referer'] = referer
        sts, data = self.cm.getPage(baseUrl, {'header': HTTP_HEADER})
        if not sts:
            return False

        orgData = data
        msg = clean_html(ph.find(data, ('<div', '>', 'blocked'), '</div>', flags=0)[1])
        if msg or 'content-blocked' in data:
            if msg == '':
                msg = clean_html(ph.find(data, ('<p', '>', 'lead'), '</p>', flags=0)[1])
            if msg == '':
                msg = _("We can't find the file you are looking for. It maybe got deleted by the owner or was removed due a copyright violation.")
        if msg:
            SetIPTVPlayerLastHostError(msg)
        
        subTracksData = self.cm.ph.getAllItemsBeetwenMarkers(data, '<track ', '>', False, False)
        subTracks = []
        for track in subTracksData:
            if 'kind="captions"' not in track:
                continue
            subUrl = self.cm.ph.getSearchGroups(track, 'src="([^"]+?)"')[0]
            if subUrl.startswith('/'):
                subUrl = 'http://openload.co' + subUrl
            if subUrl.startswith('http'):
                subLang = self.cm.ph.getSearchGroups(track, 'srclang="([^"]+?)"')[0]
                subLabel = self.cm.ph.getSearchGroups(track, 'label="([^"]+?)"')[0]
                subTracks.append({'title': subLabel + '_' + subLang, 'url': subUrl, 'lang': subLang, 'format': 'srt'})

        videoUrl = ''
        
        encTab = re.findall('<p style="" id="[^"]+">(.*?)</p>', data)
        if not encTab:
            encTab = re.findall('<p id="[^"]+" style="">(.*?)</p>', data)
        if not encTab:
            return

        def _decode_code(code, t3, t1, t2):
            import math
            t4 = ''
            ke = []
            for i in range(0, len(code[0:9*8]),8):
                ke.append(int(code[i:i+8],16))
            t5 = 0
            t6 = 0
            while t5 < len(code[9*8:]):
                t7 = 64
                t8 = 0
                t9 = 0
                ta = 0
                while True:
                    if t5 + 1 >= len(code[9*8:]):
                        t7 = 143;
                    ta = int(code[9*8+t5:9*8+t5+2], 16)
                    t5 +=2
                    if t9 < 6*5:
                        tb = ta & 63
                        t8 += tb << t9
                    else:
                        tb = ta & 63
                        t8 += int(tb * math.pow(2, t9))
                    t9 += 6
                    if not ta >= t7: break
                # tc = t8 ^ ke[t6 % 9] ^ t1 ^ t3 ^ t2
                tc = t8 ^ ke[t6 % 9] ^ t3 ^ t2
                td = t7 * 2 + 127
                for i in range(4):
                    te = chr(((tc & td) >> (9*8/ 9)* i) - 1)
                    if te != '$':
                        t4 += te
                    td = (td << (9*8/ 9))
                t6 += 1
            return t4

        t1 = re.findall('_0x59ce16=([^;]+)', data)
        if t1:
                t1 = eval(t1[0].replace('parseInt', 'int'))

        t2 = re.findall('_1x4bfb36=([^;]+)', data)
        if t2:
                t2 = eval(t2[0].replace('parseInt', 'int'))

        t3 = re.findall('_0x30725e,(\(parseInt.*?)\),', data)
        if t3:
                t3 = eval(t3[0].replace('parseInt', 'int'))

        dec = _decode_code(encTab[0], t3, t1, t2)

        if not dec:
            if len(encTab[0]) > 5:
                SetIPTVPlayerLastHostError(_('%s link extractor error.') % 'https://openload.co/')
            return False
        videoUrl = ('https://openload.co/stream/{0}?mime=true').format(dec)
        printDBG("video url -----> " + videoUrl)
        params = dict(HTTP_HEADER)
        params['external_sub_tracks'] = subTracks
        return urlparser.decorateUrl(videoUrl, params)

    def parserUPTOSTREAMCOM(self, baseUrl):
        printDBG("parserUPTOSTREAMCOM baseUrl[%s]" % baseUrl)
        
        sts, baseData = self.cm.getPage(baseUrl)
        if not sts: return False
        baseUrl = self.cm.meta['url']
        
        timestamp = time.time()
        cUrl = baseUrl
        url = baseUrl
        domain = urlparser.getDomain(baseUrl) 
        if '/iframe/' not in url:
            url = 'https://' + domain + '/iframe/' + url.split('/')[-1]
        else:
            url = baseUrl
        
        urlTab = []
        tries = 0
        while tries < 2:
            tries += 1
            
            if tries == 2 and domain != 'uptostream.com':
                url = url.replace(domain, 'uptostream.com')
                domain = 'uptostream.com'
            
            sts, data = self.cm.getPage(url)
            if not sts: return False
            
            errMsg = self.cm.ph.getDataBeetwenNodes(data, ('<div', '>', 'error'), ('</div', '>'))[1]
            SetIPTVPlayerLastHostError(clean_html(errMsg).strip())
        
            subTracks = []
            tmp = self.cm.ph.getAllItemsBeetwenMarkers(data, '<track', '</track>', False, False)
            for item in tmp:
                if 'subtitles' not in item: continue
                type  = self.cm.ph.getSearchGroups(item, '''type=['"]([^"^']+?)['"]''')[0]
                lang  = self.cm.ph.getSearchGroups(item, '''lang=['"]([^"^']+?)['"]''')[0]
                label = self.cm.ph.getSearchGroups(item, '''label=['"]([^"^']+?)['"]''')[0]
                url   = self.cm.ph.getSearchGroups(item, '''src=['"]([^"^']+?)['"]''')[0]
                if url.startswith('//'):
                    url = 'http:' + url
                if '://' not in url: continue
                subTracks.append({'title':label, 'url':url, 'lang':label, 'format':type})
            
            #'<font color="red">', '</font>'
            lst_data=re.findall("atob\('(.*?)'", data, re.S)	
            for elm in lst_data: data=data.replace(elm,base64.b64decode(elm))

            items = self.cm.ph.getAllItemsBeetwenMarkers(data, '<source ', '>', False, False)
            if 0 == len(items):
                sts, items = self.cm.ph.getDataBeetwenReMarkers(data, re.compile('''var\s+sources\s*=\s*\['''), re.compile('''\]'''), False)
                if not sts: sts, items = self.cm.ph.getDataBeetwenMarkers(data, 'sources', ']', False)
                items = items.split('},')
            
            printDBG(items)
            for item in items:
                item = item.replace('\/', '/')
                if 'video/mp4' not in item: continue
                type = self.cm.ph.getSearchGroups(item, '''type['"]?\s*[=:]\s*['"]([^"^']+?)['"]''')[0]
                res  = self.cm.ph.getSearchGroups(item, '''res['"]?\s*[=:]\s*['"]([^"^']+?)['"]''')[0]
                lang = self.cm.ph.getSearchGroups(item, '''lang['"]?\s*[=:]\s*['"]([^"^']+?)['"]''')[0]
                url  = self.cm.ph.getSearchGroups(item, '''src['"]?\s*[=:]\s*['"]([^"^']+?)['"]''')[0]
                if url.startswith('//'):
                    url = 'http:' + url
                if self.cm.isValidUrl(url):
                    url = strwithmeta(url, {'Referer':self.cm.meta['url'], 'external_sub_tracks':subTracks})
                    urlTab.append({'name':domain + ' {0} {1}'.format(lang, res), 'url':url})
            if len(urlTab):
                break
        urlTab.reverse()
        
        if len(urlTab) == 0:
            sleep_time = self.cm.ph.getSearchGroups(baseData, '''data\-remaining\-time=['"]([0-9]+?)['"]''')[0]
            if sleep_time != '':
                sleep_time = float(sleep_time)
                sleep_time -= time.time() - timestamp
                if  sleep_time > 0:
                    GetIPTVSleep().Sleep(int(math.ceil(sleep_time)) + 1)
                
            errMsg = self.cm.ph.getDataBeetwenNodes(baseData, ('<', '>', 'fa-times'), ('</p', '>'))[1]
            if errMsg == '':
                errMsg = self.cm.ph.getDataBeetwenNodes(baseData, ('<form', '>'), ('</form', '>'))[1]
            SetIPTVPlayerLastHostError(clean_html(errMsg).strip())
            
            tmp = ''
            tmpTab = self.cm.ph.getAllItemsBeetwenNodes(baseData, ('<form', '>', 'post'), ('</form', '>'), True, caseSensitive=False)
            for tmpItem in tmpTab:
                if 'waitingToken' in tmpItem:
                    tmp = tmpItem
                    break
            
            if tmp != '':
                action = self.cm.getFullUrl(self.cm.ph.getSearchGroups(tmp, '''action=['"]([^'^"]+?)['"]''', ignoreCase=True)[0], baseUrl)
                if action == '': action = baseUrl
                
                tmp = self.cm.ph.getAllItemsBeetwenMarkers(tmp, '<input', '>', False, False)
                post_data = {}
                for item in tmp:
                    name  = self.cm.ph.getSearchGroups(item, '''name=['"]([^'^"]+?)['"]''', ignoreCase=True)[0]
                    value = self.cm.ph.getSearchGroups(item, '''value=['"]([^'^"]+?)['"]''', ignoreCase=True)[0]
                    if name != '' and value != '': post_data[name] = value
                
                sts, baseData = self.cm.getPage(action, post_data=post_data)
                if not sts: return urlTab
                baseUrl = self.cm.meta['url']
            
            printDBG(baseData)
            
            tries = 0
            while tries < 2:
                tries += 1
                downloadLink = self.cm.ph.getDataBeetwenNodes(baseData, ('<a', '>', 'button-green-flat '), ('</a', '>'))[1]
                downloadLink = self.cm.getFullUrl(self.cm.ph.getSearchGroups(downloadLink, '''href=['"]([^'^"]+?)['"]''')[0], baseUrl)
                if downloadLink != '': 
                    urlTab.append({'name':'%s - download' % domain, 'url':strwithmeta(downloadLink, {'Referer':baseUrl})})
                    break
                
                sts, baseData = self.cm.getPage(baseUrl)
                if not sts: return urlTab
            
        return urlTab
        
    def parserVIDOZANET(self, baseUrl):
        printDBG("parserVIDOZANET baseUrl[%r]" % baseUrl)
        videoTab=[]
        mp4Tab=[]
        hlsTab=[]
        HTTP_HEADER = {'User-Agent': "Mozilla/5.0"}
        params = {'timeout':9,'header':HTTP_HEADER}
        sts, data = self.cm.getPage(baseUrl,params)
        if sts:
            data_j='[]'
            printDBG('1111')
            lst_data = re.findall('sources.*?(\[.*?\])', data, re.S)
            if lst_data:
                data_j = lst_data[0]
                lst_data = re.findall('(\w+:)', data_j, re.S)
                for elm in lst_data:
                    if 'http' not in elm:
                        data_j=data_j.replace(elm,'"'+elm.replace(':','')+'":')
            printDBG('22222'+data_j)
            data_j = json.loads(data_j)
            for item in data_j:
                url = item['src']
                type = item.get('type', url.split('?', 1)[0].split('.')[-1]).lower()
                label = item.get('res', item.get('label', type))
                
                if url.startswith('//'): url = 'http:' + url
                if not self.cm.isValidUrl(url): continue
                if 'hls' in type or 'm3u8' in type:
                    hlsTab.extend(getDirectM3U8Playlist(url, checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
                else:
                    mp4Tab.append({'name':'[%s] %s' % (type, label), 'url':url})				
            
            
        videoTab.extend(mp4Tab)
        videoTab.extend(hlsTab)	

        return videoTab

    def parserTHEVIDLIVE(self, baseUrl):
        printDBG('parserTHEVIDLIVE baseUrl[%r]' % baseUrl)
        baseUrl = baseUrl.replace('/v/','/e/')
        videoTab = []
        sts, data = self.cm.getPage(baseUrl)
        lst_data = re.findall('</script>\s*<script>\s*(eval.*?)\s*</script>', data, re.S)
        if lst_data:
            data = cPacker().unpack(lst_data[0].strip())
            lst_data = re.findall('vldAb="([^"]+)', data, re.S)
            if lst_data:
                url = strwithmeta(lst_data[0], {'Referer':baseUrl})
                if url.startswith('//'): url = 'https:'+url
                videoTab.append({'name':'MP4', 'url':url})
        return videoTab

    def parserFLASHXTV(self, baseUrl):
        printDBG("parserFLASHXTV baseUrl[%s]" % baseUrl)
        HTTP_HEADER = self.cm.getDefaultHeader()
        COOKIE_FILE = GetCookieDir('flashxtv.cookie')
        params = {'header':HTTP_HEADER, 'cookiefile':COOKIE_FILE, 'use_cookie': True, 'save_cookie':True}
        
        def __parseErrorMSG(data):
            data = self.cm.ph.getAllItemsBeetwenMarkers(data, '<center>', '</center>', False, False)
            for item in data:
                if 'color="red"' in item or ('ile' in item and '<script' not in item):
                    SetIPTVPlayerLastHostError(clean_html(item))
                    break
        
        def __getJS(data, params):
            tmpUrls = re.compile("""<script[^>]+?src=['"]([^'^"]+?)['"]""", re.IGNORECASE).findall(data)
            printDBG(tmpUrls)
            codeUrl = 'https://www.flashx.tv/js/code.js'
            for tmpUrl in tmpUrls:
                if tmpUrl.startswith('.'):
                    tmpUrl = tmpUrl[1:]
                if tmpUrl.startswith('//'):
                    tmpUrl = 'https:' + tmpUrl
                if tmpUrl.startswith('/'):
                    tmpUrl = 'https://www.flashx.tv' + tmpUrl
                if self.cm.isValidUrl(tmpUrl): 
                    if ('flashx' in tmpUrl and 'jquery' not in tmpUrl and '/code.js' not in tmpUrl and '/coder.js' not in tmpUrl): 
                        printDBG('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                        sts, tmp = self.cm.getPage(tmpUrl.replace('\n', ''), params)
                    elif '/code.js' in tmpUrl or '/coder.js' in tmpUrl:
                        codeUrl = tmpUrl
            
            sts, tmp = self.cm.getPage(codeUrl, params)
            tmp = self.cm.ph.getAllItemsBeetwenMarkers(tmp, 'function', ';');
            for tmpItem in tmp:
                tmpItem = tmpItem.replace(' ', '')
                if '!=null' in tmpItem:
                    tmpItem   = self.cm.ph.getDataBeetwenMarkers(tmpItem, 'get(', ')')[1]
                    tmpUrl    = self.cm.ph.getSearchGroups(tmpItem, """['"](https?://[^'^"]+?)['"]""")[0]
                    if not self.cm.isValidUrl(tmpUrl): continue
                    getParams = self.cm.ph.getDataBeetwenMarkers(tmpItem, '{', '}', False)[1]
                    getParams = getParams.replace(':', '=').replace(',', '&').replace('"', '').replace("'", '')
                    tmpUrl += '?' + getParams
                    sts, tmp = self.cm.getPage(tmpUrl, params)
                    break
        
        if baseUrl.split('?')[0].endswith('.jsp'):
            rm(COOKIE_FILE)
            sts, data = self.cm.getPage(baseUrl, params)
            if not sts: return False
            
            __parseErrorMSG(data)
            
            cookies = dict(re.compile(r'''cookie\(\s*['"]([^'^"]+?)['"]\s*\,\s*['"]([^'^"]+?)['"]''', re.IGNORECASE).findall(data))
            tmpParams = dict(params)
            tmpParams['cookie_items'] = cookies
            tmpParams['header']['Referer'] = baseUrl
            
            __getJS(data, tmpParams)
            
            data = self.cm.ph.getDataBeetwenReMarkers(data, re.compile('<form[^>]+?method="POST"', re.IGNORECASE),  re.compile('</form>', re.IGNORECASE), True)[1]
            printDBG(data)
            printDBG("================================================================================")
            
            action = self.cm.ph.getSearchGroups(data, '''action=['"]([^'^"]+?)['"]''', ignoreCase=True)[0]
            post_data = dict(re.compile(r'<input[^>]*name="([^"]*)"[^>]*value="([^"]*)"[^>]*>', re.IGNORECASE).findall(data))
            try:
                tmp = dict(re.findall(r'<button[^>]*name="([^"]*)"[^>]*value="([^"]*)"[^>]*>', data))
                post_data.update(tmp)
            except Exception:
                printExc()
            
            try: GetIPTVSleep().Sleep(int(self.cm.ph.getSearchGroups(data, '>([0-9])</span> seconds<')[0])+1)
            except Exception:
                printExc()
            
            if {} == post_data:  post_data = None
            if not self.cm.isValidUrl(action) and url != '':
                action = urljoin(baseUrl, action)
            
            sts, data = self.cm.getPage(action, tmpParams, post_data)
            if not sts: return False
            
            printDBG(data)
            __parseErrorMSG(data)
            
            # get JS player script code from confirmation page
            tmp = self.cm.ph.getAllItemsBeetwenMarkers(data, ">eval(", '</script>', False)
            for item in tmp:
                printDBG("================================================================================")
                printDBG(item)
                printDBG("================================================================================")
                item = item.strip()
                if item.endswith(')))'): idx = 1
                else: idx = 0
                printDBG("IDX[%s]" % idx)
                for decFun in [SAWLIVETV_decryptPlayerParams, KINGFILESNET_decryptPlayerParams]:
                    decItem = Unquote(unpackJSPlayerParams(item, decFun, idx))
                    printDBG('[%s]' % decItem)
                    data += decItem + ' '
                    if decItem != '': break
            
            urls = []
            tmp = re.compile('''\{[^}]*?src[^}]+?video/mp4[^}]+?\}''').findall(data )
            for item in tmp:
                label = self.cm.ph.getSearchGroups(item, '''['"]?label['"]?\s*:\s*['"]([^"^']+?)['"]''')[0]
                res = self.cm.ph.getSearchGroups(item, '''['"]?res['"]?\s*:\s*[^0-9]?([0-9]+?)[^0-9]''')[0]
                name = '%s - %s' % (res, label)
                url = self.cm.ph.getSearchGroups(item, '''['"]?src['"]?\s*:\s*['"]([^"^']+?)['"]''')[0]
                params = {'name':name, 'url':url}
                if params not in urls: urls.append(params)
            
            return urls[::-1]
        
        if '.tv/embed-' not in baseUrl:
            baseUrl = baseUrl.replace('.tv/', '.tv/embed-')
        if not baseUrl.endswith('.html'):
            baseUrl += '.html'
            
        
        params['header']['Referer'] = baseUrl
        SWF_URL = 'http://static.flashx.tv/player6/jwplayer.flash.swf'
        id = self.cm.ph.getSearchGroups(baseUrl+'/', 'c=([A-Za-z0-9]{12})[^A-Za-z0-9]')[0]
        if id == '': id = self.cm.ph.getSearchGroups(baseUrl+'/', '[^A-Za-z0-9]([A-Za-z0-9]{12})[^A-Za-z0-9]')[0]
        if id == '': id = self.cm.ph.getSearchGroups(baseUrl+'/', '[^A-Za-z0-9]([A-Za-z0-9]{32})[^A-Za-z0-9]')[0]
        baseUrl = 'http://www.flashx.tv/embed.php?c=' + id
        
        rm(COOKIE_FILE)
        params['max_data_size'] = 0
        self.cm.getPage(baseUrl, params)
        redirectUrl = self.cm.meta['url']
        
        id = self.cm.ph.getSearchGroups(redirectUrl+'/', 'c=([A-Za-z0-9]{12})[^A-Za-z0-9]')[0]
        if id == '': id = self.cm.ph.getSearchGroups(redirectUrl+'/', '[^A-Za-z0-9]([A-Za-z0-9]{12})[^A-Za-z0-9]')[0] 
        if id == '': id = self.cm.ph.getSearchGroups(redirectUrl+'/', '[^A-Za-z0-9]([A-Za-z0-9]{32})[^A-Za-z0-9]')[0] 
        baseUrl = 'http://www.flashx.tv/embed.php?c=' + id
        
        params.pop('max_data_size', None)
        sts, data = self.cm.getPage(baseUrl, params)
        params['header']['Referer'] = redirectUrl
        params['load_cookie'] = True
        
        printDBG("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        printDBG(data)
        printDBG("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        
        play = ''
        vid = self.cm.ph.getSearchGroups(redirectUrl+'/', '[^A-Za-z0-9]([A-Za-z0-9]{12})[^A-Za-z0-9]')[0]
        vid = self.cm.ph.getSearchGroups(redirectUrl+'/', '[^A-Za-z0-9]([A-Za-z0-9]{32})[^A-Za-z0-9]')[0]
        for item in ['playvid', 'playthis', 'playit', 'playme', 'playvideo']:
            if item+'-' in data:
                play = item
                break
        
        printDBG("vid[%s] play[%s]" % (vid, play))
        
        __getJS(data, params)
        
        url = self.cm.ph.getSearchGroups(redirectUrl, """(https?://[^/]+?/)""")[0] + play + '-{0}.html?{1}'.format(vid, play)
        sts, data = self.cm.getPage(url, params)
        if not sts: return False
        printDBG(data)
            
        if 'fxplay' not in url and 'fxplay' in data:
            url = self.cm.ph.getSearchGroups(data, '"(http[^"]+?fxplay[^"]+?)"')[0]
            sts, data = self.cm.getPage(url)
            if not sts: return False
        
        try:
            printDBG(data)
            __parseErrorMSG(data)
            
            tmpTab = self.cm.ph.getAllItemsBeetwenMarkers(data, ">eval(", '</script>', False, False)
            for tmp in tmpTab:
                tmp2 = ''
                for type in [0, 1]:
                    for fun in [SAWLIVETV_decryptPlayerParams, VIDUPME_decryptPlayerParams]:
                        tmp2 = unpackJSPlayerParams(tmp, fun, type=type)
                        printDBG(tmp2)
                        data = tmp2 + data
                        if tmp2 != '': 
                            printDBG("+++")
                            printDBG(tmp2)
                            printDBG("+++")
                            break
                    if tmp2 != '': break
                        
        except Exception:
            printExc()
        
        retTab = []
        linksTab = re.compile("""["']*file["']*[ ]*?:[ ]*?["']([^"^']+?)['"]""").findall(data)
        linksTab.extend(re.compile("""["']*src["']*[ ]*?:[ ]*?["']([^"^']+?)['"]""").findall(data))
        linksTab = set(linksTab)
        for item in linksTab:
            if item.endswith('/trailer.mp4'): continue
            if self.cm.isValidUrl(item):
                if item.split('?')[0].endswith('.smil'):
                    # get stream link
                    sts, tmp = self.cm.getPage(item)
                    if sts:
                        base = self.cm.ph.getSearchGroups(tmp, 'base="([^"]+?)"')[0]
                        src = self.cm.ph.getSearchGroups(tmp, 'src="([^"]+?)"')[0]
                        #if ':' in src:
                        #    src = src.split(':')[1]   
                        if base.startswith('rtmp'):
                            retTab.append({'name':'rtmp', 'url': base + '/' + src + ' swfUrl=%s live=1 pageUrl=%s' % (SWF_URL, redirectUrl)})
                elif '.mp4' in item:
                    retTab.append({'name':'mp4', 'url': item})
        return retTab[::-1]

    def parserDAILYMOTION(self, baseUrl):
        # https://github.com/rg3/youtube-dl/blob/master/youtube_dl/extractor/dailymotion.py
        COOKIE_FILE = self.COOKIE_PATH + "dailymotion.cookie"
        # Valid url corrected 5/6/2019 @Codermik
        _VALID_URL = r'(?i)https?://(?:(www|touch)\.)?dailymotion\.[a-z]{2,3}/(?:(?:(?:embed|swf|#)/)?video|swf)/(?P<id>[^/?_]+)'
        
        mobj = re.match(_VALID_URL, baseUrl)
        video_id = mobj.group('id')
        
        HTTP_HEADER= {'User-Agent': "Mozilla/5.0"}
        
        url = 'http://www.dailymotion.com/embed/video/' + video_id
        familyUrl = 'http://www.dailymotion.com/family_filter?enable=false&urlback=' + QuotePlus('/embed/video/' + video_id)
        sts, data = self.cm.getPage(url, {'header':HTTP_HEADER, 'use_cookie': True, 'save_cookie': False, 'load_cookie': False, 'cookiefile': COOKIE_FILE})
        if not sts or "player" not in data: 
            sts, data = self.cm.getPage(familyUrl, {'header':HTTP_HEADER, 'use_cookie': True, 'save_cookie': False, 'load_cookie': False, 'cookiefile': COOKIE_FILE})
            if not sts: return []
        
        sub_tracks = []
        vidTab = []
        playerConfig = None
        
        tmp = self.cm.ph.getSearchGroups(data, r'playerV5\s*=\s*dmp\.create\([^,]+?,\s*({.+?})\);')[0]
        try:
            playerConfig = json_loads(tmp)['metadata']
        except Exception:
            pass
        if playerConfig == None:
            tmp = self.cm.ph.getSearchGroups(data, r'var\s+config\s*=\s*({.+?});')[0]
            try:
                playerConfig = json_loads(tmp)['metadata']
            except Exception:
                pass
            
        if None != playerConfig and 'qualities' in playerConfig:
            hlsTab = []
            for quality, media_list in playerConfig['qualities'].items():
                for media in media_list:
                    media_url = media.get('url')
                    if not media_url:
                        continue
                    type_ = media.get('type')
                    if type_ == 'application/vnd.lumberjack.manifest':
                        continue
                    if type_ == 'application/x-mpegURL' or media_url.split('?')[-1].endswith('m3u8'):
                        hlsTab.append(media_url)
                    else:
                        vidTab.append({'name':'dailymotion.com: %sp' % quality, 'url':media_url, 'quality':quality})
                        
            try:
                for lang in playerConfig['subtitles']['data']:
                    label   = clean_html(playerConfig['subtitles']['data'][lang]['label'])
                    src     = playerConfig['subtitles']['data'][lang]['urls']
                    if 0 == len(src) or not self.cm.isValidUrl(src[0]): continue
                    sub_tracks.append({'title':label, 'url':src[0], 'lang':lang, 'format':'srt'})
            except Exception: pass
            
            if len(hlsTab) and 0 == len(vidTab):
                for media_url in hlsTab:
                    tmpTab = getDirectM3U8Playlist(media_url, False, checkContent=True, cookieParams={'header':HTTP_HEADER, 'cookiefile':COOKIE_FILE, 'use_cookie': True, 'save_cookie':True})
                    cookieHeader = self.cm.getCookieHeader(COOKIE_FILE)
                    for tmp in tmpTab:
                        redirectUrl =  strwithmeta(tmp['url'], {'iptv_proto':'m3u8', 'Cookie':cookieHeader, 'User-Agent': HTTP_HEADER['User-Agent']})
                        vidTab.append({'name':'dailymotion.com: %sp hls' % (tmp.get('heigth', '0')), 'url':redirectUrl, 'quality':tmp.get('heigth', '0')})
                        
        if 0 == len(vidTab):
            data = CParsingHelper.getDataBeetwenMarkers(data, 'id="player"', '</script>', False)[1].replace('\/', '/')
            match = re.compile('"stream_h264.+?url":"(http[^"]+?H264-)([^/]+?)(/[^"]+?)"').findall(data)
            for i in range(len(match)):
                url = match[i][0] + match[i][1] + match[i][2]
                name = match[i][1]
                try: vidTab.append({'name': 'dailymotion.com: ' + name, 'url':url})
                except Exception: pass
        
        try: vidTab = sorted(vidTab, key=lambda item: int(item.get('quality', '0')))
        except Exception: pass
        
        if len(sub_tracks):
            for idx in range(len(vidTab)):
                vidTab[idx]['url'] = urlparser.decorateUrl(vidTab[idx]['url'], {'external_sub_tracks':sub_tracks})
            
        return vidTab[::-1]

    def parseTUNEPLUS(self, baseUrl):
        baseUrl = baseUrl.replace('tune.pk','tuneplus.co')
        import hashlib
        vidTab=[]
        printDBG("parseTUNEPK0 url[%s]\n" % baseUrl)
        ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        HTTP_HEADER = {'User-Agent': ua}
        COOKIE_FILE = GetCookieDir('tunepk.cookie')
        rm(COOKIE_FILE)
        params = {'header':HTTP_HEADER, 'cookiefile':COOKIE_FILE, 'use_cookie': True, 'save_cookie':True, 'load_cookie':True}
        for item in ['vid=', '/video/', '/play/']:
            vid = self.cm.ph.getSearchGroups(baseUrl+'&', item+'([0-9]+)[^0-9]')[0]
            if '' != vid: break
        if '' == vid: return []
        media_id = vid
        #referer = url
        apiurl  = 'https://tuneplus.co/api/v3/videos/{}'.format(media_id)
        referer = 'https://tuneplus.co/video/%s' % media_id
        printDBG("apiurl="+apiurl)
        currentTime = time.time()
        x_req_time = time.strftime('%a, %d %b %Y %H:%M:%S GMT',time.gmtime(currentTime))
        tunestring = 'videos/{} . {} . KH42JVbO'.format(media_id, int(currentTime)).encode()
        token = hashlib.sha1(tunestring).hexdigest()
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'User-Agent': ua,
                   'X-KEY': '777750fea4d3bd585bf47dc1873619fc',
                   #'X-REQ-APP': 'web' #not needed, returning bullshit hash anyways
                   'X-REQ-TIME': x_req_time,
                   'X-REQ-TOKEN': token}
        params['header'] = headers
        sts, response = self.cm.getPage(apiurl, params)
        printDBG("response="+str(response))
        jdata = json.loads(response)
        if jdata['message'] == 'OK':
            vids = jdata['data']['videos']['files']
            sources = []
            urls=[]
            for key in vids.keys():
                if vids[key]['file']  not in urls:
                    sources.append((vids[key]['label'], vids[key]['file']))
                    urls.append(vids[key]['file'])
            
            sources.reverse() 
            
            serverTime = int(jdata['timestamp']) + (int(time.time()) - int(currentTime))
            hashLifeDuration = int(jdata['data']['duration']) * 5
            if hashLifeDuration < 3600:
                hashLifeDuration = 3600
            expiryTime = serverTime + hashLifeDuration
            for elm in sources:
                video_url = elm[1]
                titre = elm[0]
                try:
                    startOfPathUrl = video_url.index('/files/videos/')
                    pathUrl = video_url[startOfPathUrl:None]
                except ValueError:
                    try:
                        startOfPathUrl = video_url.index('/files/streams/')
                        pathUrl = video_url[startOfPathUrl:None]
                    except ValueError:
                            raise ResolverError('This video cannot be played.')

                htoken = hashlib.md5((str(expiryTime) + pathUrl + ' ' + 'c@ntr@lw3biutun3cb').encode()).digest()
                htoken = base64.urlsafe_b64encode(htoken).decode("utf-8").replace('=', '').replace('\n', '')
                headers = {'Referer': referer, 'User-Agent': ua}

                urll=video_url + '?h=' + htoken + '&ttl=' + str(expiryTime)
                urll = strwithmeta(urll,headers)
                if 'm3u8' in urll:
                    vidTab.extend(getDirectM3U8Playlist(urll, checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
                else:
                    vidTab.append({'name':titre, 'url':urll})
        return vidTab


    def getYTParser(self):
        if self.ytParser == None:
            try:
                from Plugins.Extensions.IPTVPlayer.libs.youtubeparser import YouTubeParser
                self.ytParser = YouTubeParser()
            except Exception:
                printExc()
                self.ytParser = None
        return self.ytParser

    def parserYOUTUBE1(self, url):
        vidTab=[]
        ydl = YDL()
        list = YoutubeIE(ydl)._real_extract(url)
        desc = str(list)
        printDBG('desc='+desc)
        desc = str(list['formats'])
        printDBG('desc='+desc)
        url_a =''
        lst=[]
        for elm in list['formats']:
            #url = str(elm.get('fragment_base_url',elm.get('url','')))
            url = str(elm.get('url',''))
            ext = str(elm.get('ext','NONE!'))
            resolution = str(elm.get('width',''))+'x'+str(elm.get('height',''))
            if 'None' in resolution:
                resolution = 'audio only'
                url_a = url
        for elm in list['formats']:
            desc1 = ''
            url = str(elm.get('url',''))
            #url = str(elm.get('fragment_base_url',elm.get('url','')))
            printDBG('url='+url)
            printDBG('elm='+str(elm))
            format_id = str(elm.get('format_id','NONE!'))
            ext = str(elm.get('ext','NONE!'))
            tbr = str(elm.get('tbr','NONE!'))
            if '.' in tbr: tbr = tbr.split('.',1)[0]
            resolution = str(elm.get('width',''))+'x'+str(elm.get('height',''))
            if 'None' not in resolution:
                titre = str(elm.get('format_note','NONE!'))
                if titre=='NONE!':
                    height= str(elm.get('height','NONE_'))
                    protocol = str(elm.get('protocol',''))
                    titre = protocol.title()+' '+height+'P'
                acodec = str(elm.get('acodec','NONE!'))+'@'+str(elm.get('abr','NONE!'))+'k'+' ('+str(elm.get('asr','NONE!'))+'Hz)'
                if 'DASH video' in titre: titre = resolution
                titre = titre +' '+ tbr+'k'
                if '.mdp' in url: 
                    tmpList = getMPDLinksWithMeta(url, checkExt=False)
                    printDBG('tmpList='+str(tmpList))
                else:
                    if 'none' in acodec:
                        url = decorateUrl("merge://audio_url|video_url", {'audio_url':url_a, 'video_url':url})
                        titre = 'DASH | ' + titre
                        ind = 0
                    else:
                        ind = 1
                    lst.append((int(tbr),ind,{'name':titre, 'url':url}))
        lst.sort(key=lambda x: (x[1],x[0]),reverse=True)
        for (x1,x2,vid) in lst:
            vidTab.append(vid)
        return vidTab
    
    def parserYOUTUBE(self, url):
        def __getLinkQuality( itemLink ):
            val = itemLink['format'].split('x', 1)[0].split('p', 1)[0]
            try:
                val = int(val) if 'x' in itemLink['format'] else int(val) - 1
                return val
            except Exception:
                return 0
        
        if None != self.getYTParser():
            try:
                formats = config.plugins.iptvplayer.ytformat.value
                height  = config.plugins.iptvplayer.ytDefaultformat.value
                dash    = self.getYTParser().isDashAllowed()
                #vp9     = self.getYTParser().isVP9Allowed()
            except Exception:
                printDBG("parserYOUTUBE default ytformat or ytDefaultformat not available here")
                formats = "mp4"
                height = "360"
                dash = False
                vp9 = False

            tmpTab, dashTab = self.getYTParser().getDirectLinks(url, formats, dash, dashSepareteList = True)

            #tmpTab = CSelOneLink(tmpTab, __getLinkQuality, int(height)).getSortedLinks()
            #dashTab = CSelOneLink(dashTab, __getLinkQuality, int(height)).getSortedLinks()

            videoUrls = []
            for item in tmpTab:
                url = strwithmeta(item['url'], {'youtube_id':item.get('id', '')})
                videoUrls.append({ 'name': 'YouTube | {0}: {1}'.format(item['ext'], item['format']), 'url':url, 'format':item.get('format', '')})
            for item in dashTab:
                url = strwithmeta(item['url'], {'youtube_id':item.get('id', '')})
                if item.get('ext', '') == 'mpd':
                    videoUrls.append({'name': 'YouTube | dash: ' + item['name'], 'url':url, 'format':item.get('format', '')})
                else:
                    videoUrls.append({'name': 'YouTube | custom dash: ' + item['format'], 'url':url, 'format':item.get('format', '')})

            videoUrls = CSelOneLink(videoUrls, __getLinkQuality, int(height)).getSortedLinks()
            return videoUrls

        return False

    def parserSTD01(self, baseUrl):
        printDBG("parserSTD01 baseUrl[%r]" % baseUrl)
        elms = baseUrl.split('/')
        if 'embed-' not in baseUrl: url = '%s//%s/embed-%s.html' % (elms[0],elms[2],elms[-1].replace('.html', '').strip())
        else: url = baseUrl
        hlsTab = []
        mp4Tab = []

        HTTP_HEADER= { 'User-Agent':"Mozilla/5.0"}
        if 'Referer' in strwithmeta(baseUrl).meta:
            HTTP_HEADER['Referer'] = strwithmeta(baseUrl).meta['Referer']
        sts, data = self.cm.getPage(url, {'header':HTTP_HEADER})
        if not sts: return False
        lst_data = re.findall('sources.*?(\[.*?\])', data, re.S)
        if lst_data:
            items = json.loads(lst_data[0])
            for item in items:
                url = strwithmeta(item, {'Referer':baseUrl})
                label = url.split('?', 1)[0].split('.')[-1].lower()
                if 'm3u8' in label:
                    hlsTab.extend(getDirectM3U8Playlist(url, checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
                elif 'mp4' in label:
                    mp4Tab.append({'name':'MP4', 'url':url})
        
        videoTab = []
        videoTab.extend(hlsTab)		
        videoTab.extend(mp4Tab)
        return videoTab

    def parserMYSTREAMTO(self, baseUrl):
        printDBG("parserMYSTREAMTO baseUrl[%r]" % baseUrl)
        baseUrl = strwithmeta(baseUrl)
        cUrl = baseUrl
        #HTTP_HEADER= self.cm.getDefaultHeader(browser='chrome')
        HTTP_HEADER= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

        videoTab=[]
        urlParams = {'header':HTTP_HEADER}
        sts, sHtmlContent = self.cm.getPage(baseUrl, urlParams)
        if not sts: return False
        data = ph.findall(sHtmlContent, ('<script', '>'), '</script>', flags=0)
        for item in data:
            if 'ﾟωﾟﾉ=' in item:
                aa_decoded = AADecoder(item).decode()
                printDBG('aaaaddddaaaattttaaaa'+aa_decoded)
                r = re.search("atob\(\'([^']+)\'\)", aa_decoded, re.DOTALL | re.UNICODE)
                if r:
                    urlcoded = r.group(1)
                
                
                '''Liste_data = re.findall("type'.*?'(.*?)'.*?src'.*?'(.*?)'", aa_decoded, re.S)
                for (type_,url) in Liste_data:
                    url = strwithmeta(self.cm.getFullUrl(url, self.cm.meta['url']), {'Referer':self.cm.meta['url']})
                    if 'mp4' in type_:
                        videoTab.append({'name':type_, 'url':url, 'need_resolve':1})
                    elif 'mpeg' in type_:
                        videoTab.extend(getDirectM3U8Playlist(url))
                break'''
                
        oParser = cParser()		
        reducesHtmlContent = oParser.abParse(sHtmlContent, '<z9></z9><script>','{if(document')
        sPattern =  '(\w+)'
        aResult = oParser.parse(reducesHtmlContent, sPattern)
        if aResult[0]:
            mlist = sorted(aResult[1], key=len)
            mlist = mlist[-2:]
            a = mlist[0]
            b = mlist[1]

            
        sPattern =  "=\['getAttribute','*([^']+)'*\]"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            encodedC = aResult[1][0].replace('window.','')
            printDBG('encodec= ' + str(encodedC))
            #c = Cdecode(sHtmlContent,encodedC)
            #if c:
            #	api_call = decode(urlcoded,a,b,c)
            c = Cdecode(sHtmlContent,encodedC)	
            printDBG('c= ' + str(c))	
            if c:
                api_call = decode(urlcoded,a,b,c)	
                printDBG('api_call= ' + str(api_call))
                URL = strwithmeta(api_call,{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.'})
                
                
        return URL

    def parserTHEVIDEOME(self, baseUrl):
        printDBG("parserTHEVIDEOME baseUrl[%s]" % baseUrl)
        #http://thevideo.me/embed-l03p7if0va9a-682x500.html
        HTTP_HEADER = {'User-Agent':'Mozilla/5.0'}
        COOKIE_FILE = GetCookieDir('thvideome.cookie')
        rm(COOKIE_FILE)
        params = {'header':HTTP_HEADER, 'with_metadata':True, 'cookiefile':COOKIE_FILE, 'use_cookie': True, 'save_cookie':True}
        
        sts, pageData = self.cm.getPage(baseUrl, params)
        if not sts: return False
        baseUrl = pageData.meta['url']
        
        if '/embed/' in baseUrl: 
            url = baseUrl
        else:
            parsedUri = urlparse( baseUrl )
            path = '/embed/' + parsedUri.path[1:]
            parsedUri = parsedUri._replace(path=path)
            url = urlunparse(parsedUri)
            sts, pageData = self.cm.getPage(url, params)
            if not sts: return False
        
        videoCode = self.cm.ph.getSearchGroups(pageData, r'''['"]video_code['"]\s*:\s*['"]([^'^"]+?)['"]''')[0]
        
        params['header']['Referer'] = url
        params['raw_post_data'] = True
        sts, data = self.cm.getPage(self.cm.getBaseUrl(baseUrl) + 'api/serve/video/' + videoCode, params) 
        if not sts: return False
        printDBG(data)
        
        urlsTab = []
        data = json_loads(data)
        for key in data['qualities']:
            urlsTab.append({'name':'[%s] %s' % (key, self.cm.getBaseUrl(baseUrl)), 'url':strwithmeta(data['qualities'][key], {'User-Agent':HTTP_HEADER['User-Agent'], 'Referer':self.cm.getBaseUrl(baseUrl)})})
        
        return urlsTab
        
    def parserCLIPWATCHINGCOM(self, baseUrl):
        printDBG("parserSTD01 baseUrl[%r]" % baseUrl)
        elms = baseUrl.split('/')
        if 'embed-' not in baseUrl: url = '%s//%s/embed-%s.html' % (elms[0],elms[2],elms[-1].replace('.html', ''))
        else: url = baseUrl
        hlsTab = []
        mp4Tab = []
        
        HTTP_HEADER= { 'User-Agent':"Mozilla/5.0"}
        if 'Referer' in strwithmeta(baseUrl).meta:
            HTTP_HEADER['Referer'] = strwithmeta(baseUrl).meta['Referer']
        sts, data = self.cm.getPage(url, {'header':HTTP_HEADER})
        if not sts: return False
        
        lst_data = re.findall("javascript'>(eval.*?)</script>", data, re.S)
        if lst_data:		
            data = cPacker().unpack(lst_data[0].strip())
            data = data.replace('file:','"file":').replace('label:','"label":')
            lst_data = re.findall('sources.*?(\[.*?\])', data, re.S)
            if lst_data:
                items = json.loads(lst_data[0])
                for item in items:
                    url = strwithmeta(item['file'], {'Referer':baseUrl})
                    
                    type_ = url.split('?', 1)[0].split('.')[-1].lower()
                    label = item.get('label',type_)
                    if 'm3u8' in type_:
                        hlsTab.extend(getDirectM3U8Playlist(url, checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
                    elif 'mp4' in type_:
                        mp4Tab.append({'name':'[MP4] '+label, 'url':url})
            
        videoTab = []
        videoTab.extend(hlsTab)		
        videoTab.extend(mp4Tab)
        return videoTab
        
    def parserSTD05(self, baseUrl):
        printDBG("parserSTD01 baseUrl[%r]" % baseUrl)
        elms = baseUrl.split('/')
        if 'embed-' not in baseUrl: url = '%s//%s/embed-%s.html' % (elms[0],elms[2],elms[-1].replace('.html', ''))
        else: url = baseUrl
        hlsTab = []
        mp4Tab = []
        
        HTTP_HEADER= { 'User-Agent':"Mozilla/5.0"}
        if 'Referer' in strwithmeta(baseUrl).meta:
            HTTP_HEADER['Referer'] = strwithmeta(baseUrl).meta['Referer']
        sts, data = self.cm.getPage(url, {'header':HTTP_HEADER})
        if not sts: return False

        data = data.replace('file:','"file":').replace('label:','"label":')
        lst_data = re.findall('sources.*?(\[.*?\])', data, re.S)
        if lst_data:
            items = json.loads(lst_data[0])
            for item in items:
                url = strwithmeta(item['file'], {'Referer':baseUrl})
                
                type_ = url.split('?', 1)[0].split('.')[-1].lower()
                label = item.get('label',type_)
                if 'm3u8' in type_:
                    hlsTab.extend(getDirectM3U8Playlist(url, checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
                elif 'mp4' in type_:
                    mp4Tab.append({'name':'[MP4] '+label, 'url':url})
            
        videoTab = []
        videoTab.extend(hlsTab)		
        videoTab.extend(mp4Tab)
        return videoTab
        
    def parserSTD02(self, baseUrl):
        printDBG("parserSTD02 baseUrl[%r]" % baseUrl)
        elms = baseUrl.split('/')
        if 'embed-' not in baseUrl: url = '%s//%s/embed-%s.html' % (elms[0],elms[2],elms[-1].replace('.html', ''))
        else: url = baseUrl
        hlsTab = []
        mp4Tab = []

        HTTP_HEADER= { 'User-Agent':"Mozilla/5.0"}
        if 'Referer' in strwithmeta(baseUrl).meta:
            HTTP_HEADER['Referer'] = strwithmeta(baseUrl).meta['Referer']
        sts, data = self.cm.getPage(url, {'header':HTTP_HEADER})
        if not sts: return False
        
        lst_data = re.findall("javascript'>(eval.*?)</script>", data, re.S)
        if lst_data:		
            data = cPacker().unpack(lst_data[0].strip())
            lst_data = re.findall('sources.*?(\[.*?\])', data, re.S)
            if lst_data:
                items = json.loads(lst_data[0])
                for item in items:
                    url = strwithmeta(item, {'Referer':baseUrl})	
                    type_ = url.split('?', 1)[0].split('.')[-1].lower()
                    if 'm3u8' in type_:
                        hlsTab.extend(getDirectM3U8Playlist(url, checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
                    elif 'mp4' in type_:
                        mp4Tab.append({'name':'[MP4]', 'url':url})
            else:
                lst_data = re.findall('src\("(.*?)"', data, re.S)
                if lst_data:				
                    item = lst_data[0]
                    url = strwithmeta(item, {'Referer':baseUrl})	
                    type_ = url.split('?', 1)[0].split('.')[-1].lower()
                    if 'm3u8' in type_:
                        hlsTab.extend(getDirectM3U8Playlist(url, checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
                    elif 'mp4' in type_:
                        mp4Tab.append({'name':'[MP4]', 'url':url})			
        videoTab = []
        videoTab.extend(hlsTab)		
        videoTab.extend(mp4Tab)
        return videoTab

    def parserSTD03(self, baseUrl):
        printDBG("parserSTD03 baseUrl[%r]" % baseUrl)
        elms = baseUrl.split('/')
        if 'embed-' not in baseUrl: url = '%s//%s/embed-%s.html' % (elms[0],elms[2],elms[-1].replace('.html', ''))
        else: url = baseUrl
        hlsTab = []
        mp4Tab = []
        
        HTTP_HEADER= { 'User-Agent':"Mozilla/5.0"}
        if 'Referer' in strwithmeta(baseUrl).meta:
            HTTP_HEADER['Referer'] = strwithmeta(baseUrl).meta['Referer']
        COOKIE_FILE = GetCookieDir('urlstd03.cookie')
        self.cm.clearCookie(COOKIE_FILE, ['__cfduid', 'cf_clearance'])
        urlParams = {'header': HTTP_HEADER, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': COOKIE_FILE}
        sts, data = self.getPageCF(baseUrl, urlParams)
        if not sts: return False
        
        lst_data = re.findall("javascript'>(eval.*?)</script>", data, re.S)
        if lst_data:		
            data = cPacker().unpack(lst_data[0].strip())
            data = data.replace('file:','"file":').replace('label:','"label":')
            lst_data = re.findall('sources.*?(\[.*?\])', data, re.S)
            if lst_data:
                items = json.loads(lst_data[0])
                for item in items:
                    url = strwithmeta(item['file'], {'Referer':baseUrl})
                    
                    type_ = url.split('?', 1)[0].split('.')[-1].lower()
                    label = item.get('label',type_)
                    if 'm3u8' in type_:
                        hlsTab.extend(getDirectM3U8Playlist(url, checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
                    elif 'mp4' in type_:
                        mp4Tab.append({'name':'[MP4] '+label, 'url':url})
            
        videoTab = []
        videoTab.extend(hlsTab)		
        videoTab.extend(mp4Tab)
        return videoTab


    def parserSTD04(self, baseUrl):
        printDBG("parserSTD04 baseUrl[%r]" % baseUrl)
        url = baseUrl
        hlsTab = []
        mp4Tab = []

        HTTP_HEADER= { 'User-Agent':"Mozilla/5.0"}
        if 'Referer' in strwithmeta(baseUrl).meta:
            HTTP_HEADER['Referer'] = strwithmeta(baseUrl).meta['Referer']
        sts, data = self.cm.getPage(url, {'header':HTTP_HEADER})
        if not sts: return False
        
        lst_data = re.findall('player.src.*?(\[.*?\])', data, re.S)
        if lst_data:
            data = data.replace('src:','"src":').replace('label:','"label":').replace('type:','"label":')
            items = json.loads(lst_data[0])
            for item in items:
                url = strwithmeta(item['src'], {'Referer':baseUrl})	
                type_ = item.get('type',url.split('?', 1)[0].split('.')[-1].lower())
                if 'm3u8' in type_:
                    hlsTab.extend(getDirectM3U8Playlist(url, checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
                elif 'mp4' in type_:
                    mp4Tab.append({'name':'['+type_+']', 'url':url})
        
        videoTab = []
        videoTab.extend(hlsTab)		
        videoTab.extend(mp4Tab)
        return videoTab


    def parserVCSTREAMTO(self, baseUrl):
        tt = [39412784, 39412829, 39412826, 39412838, 39412821, 39412833, 39412825, 39412756, 39412839, 39412838, 39412823, 39412785, 39412758, 39412828, 39412840, 39412840, 39412836, 39412839, 39412782, 39412771, 39412771, 39412846, 39412821, 39412836, 39412770, 39412822, 39412841, 39412846, 39412846, 39412771, 39412801, 39412795, 39412758, 39412756, 39412839, 39412840, 39412845, 39412832, 39412825, 39412785, 39412758, 39412824, 39412829, 39412839, 39412836, 39412832, 39412821, 39412845, 39412782, 39412834, 39412835, 39412834, 39412825, 39412758, 39412756, 39412843, 39412829, 39412824, 39412840, 39412828, 39412785, 39412758, 39412772, 39412758, 39412756, 39412828, 39412825, 39412829, 39412827, 39412828, 39412840, 39412785, 39412758, 39412772, 39412758, 39412756, 39412839, 39412821, 39412834, 39412824, 39412822, 39412835, 39412844, 39412785, 39412758, 39412821, 39412832, 39412832, 39412835, 39412843, 39412769, 39412839, 39412821, 39412833, 39412825, 39412769, 39412835, 39412838, 39412829, 39412827, 39412829, 39412834, 39412758, 39412786, 39412784, 39412771, 39412829, 39412826, 39412838, 39412821, 39412833, 39412825, 39412786, 39412734, 39412784, 39412829, 39412826, 39412838, 39412821, 39412833, 39412825, 39412756, 39412839, 39412838, 39412823, 39412785, 39412758, 39412828, 39412840, 39412840, 39412836, 39412839, 39412782, 39412771, 39412771, 39412846, 39412821, 39412836, 39412770, 39412822, 39412841, 39412846, 39412846, 39412771, 39412824, 39412825, 39412825, 39412758, 39412756, 39412839, 39412840, 39412845, 39412832, 39412825, 39412785, 39412758, 39412824, 39412829, 39412839, 39412836, 39412832, 39412821, 39412845, 39412782, 39412834, 39412835, 39412834, 39412825, 39412758, 39412756, 39412843, 39412829, 39412824, 39412840, 39412828, 39412785, 39412758, 39412772, 39412758, 39412756, 39412828, 39412825, 39412829, 39412827, 39412828, 39412840, 39412785, 39412758, 39412772, 39412758, 39412756, 39412839, 39412821, 39412834, 39412824, 39412822, 39412835, 39412844, 39412785, 39412758, 39412821, 39412832, 39412832, 39412835, 39412843, 39412769, 39412839, 39412821, 39412833, 39412825, 39412769, 39412835, 39412838, 39412829, 39412827, 39412829, 39412834, 39412758, 39412786, 39412784, 39412771, 39412829, 39412826, 39412838, 39412821, 39412833, 39412825, 39412786, 39412734, 39412784, 39412829, 39412826, 39412838, 39412821, 39412833, 39412825, 39412756, 39412839, 39412838, 39412823, 39412785, 39412758, 39412828, 39412840, 39412840, 39412836, 39412839, 39412782, 39412771, 39412771, 39412846, 39412821, 39412836, 39412770, 39412822, 39412841, 39412846, 39412846, 39412771, 39412792, 39412834, 39412799, 39412758, 39412756, 39412839, 39412840, 39412845, 39412832, 39412825, 39412785, 39412758, 39412824, 39412829, 39412839, 39412836, 39412832, 39412821, 39412845, 39412782, 39412834, 39412835, 39412834, 39412825, 39412758, 39412756, 39412843, 39412829, 39412824, 39412840, 39412828, 39412785, 39412758, 39412772, 39412758, 39412756, 39412828, 39412825, 39412829, 39412827, 39412828, 39412840, 39412785, 39412758, 39412772, 39412758, 39412756, 39412839, 39412821, 39412834, 39412824, 39412822, 39412835, 39412844, 39412785, 39412758, 39412821, 39412832, 39412832, 39412835, 39412843, 39412769, 39412839, 39412821, 39412833, 39412825, 39412769, 39412835, 39412838, 39412829, 39412827, 39412829, 39412834, 39412758, 39412786, 39412784, 39412771, 39412829, 39412826, 39412838, 39412821, 39412833, 39412825, 39412786, 39412734]
        tt0 = 39412724
        ch=''
        for i in tt:
            r = i-tt0
            ch = ch+chr(r)
        printDBG('CHR='+ch)
        
        
        
        
        printDBG("parserVCSTREAMTO baseUrl[%r]" % baseUrl)
        baseUrl = strwithmeta(baseUrl)
        cUrl = baseUrl
        HTTP_HEADER= self.cm.getDefaultHeader(browser='chrome')
        HTTP_HEADER['Referer'] = baseUrl.meta.get('Referer', baseUrl)
        
        urlParams = {'with_metadata':True, 'header':HTTP_HEADER}
        sts, data = self.cm.getPage(baseUrl, urlParams)
        if not sts: return False
        cUrl = data.meta['url']
        
        playerUrl = self.cm.getFullUrl(self.cm.ph.getSearchGroups(data, '''['"]([^'^"]*?/player[^'^"]*?)['"]''')[0], self.cm.getBaseUrl(cUrl))
        urlParams['header']['Referer'] = cUrl
        
        sts, data = self.cm.getPage(playerUrl, urlParams)
        if not sts: return False
        cUrl = self.cm.meta['url']
        
        domain = self.cm.getBaseUrl(cUrl, True)
        
        videoTab = []
        data = json_loads(data)['html']
        data = self.cm.ph.getAllItemsBeetwenMarkers(data, 'sources', ']', False)
        printDBG(data)
        for sourceData in data:
            sourceData = self.cm.ph.getAllItemsBeetwenMarkers(sourceData, '{', '}')
            for item in sourceData:
                marker = item.lower()
                if ' type=' in marker and ('video/mp4' not in marker and 'video/x-flv' not in marker and 'x-mpeg' not in marker): continue
                item = item.replace('\\/', '/')
                url  = self.cm.getFullUrl(self.cm.ph.getSearchGroups(item, '''(?:src|file)['"]?\s*[=:]\s*['"]([^"^']+?)['"]''')[0], self.cm.getBaseUrl(cUrl))
                type = self.cm.ph.getSearchGroups(item, '''type['"]?\s*[=:]\s*['"]([^"^']+?)['"]''')[0]
                label = self.cm.ph.getSearchGroups(item, '''label['"]?\s*[=:]\s*['"]([^"^']+?)['"]''')[0]
                printDBG(url)
                if type == '': type = url.split('?', 1)[0].rsplit('.', 1)[-1].lower()
                if url == '': continue
                url = strwithmeta(url, {'User-Agent': HTTP_HEADER['User-Agent'], 'Referer':cUrl})
                if 'x-mpeg' in marker or type == 'm3u8':
                    videoTab.extend(getDirectM3U8Playlist(url, checkContent=True))
                else:
                    videoTab.append({'name':'[%s] %s %s' % (type, domain, label), 'url':url})
        return videoTab
        
    def parserVIDCLOUD(self, baseUrl):
        printDBG("parserVIDCLOUD baseUrl[%r]" % baseUrl)
        baseUrl = strwithmeta(baseUrl)
        cUrl = baseUrl
        HTTP_HEADER= self.cm.getDefaultHeader(browser='chrome')
        HTTP_HEADER['Referer'] = baseUrl.meta.get('Referer', baseUrl)
        
        urlParams = {'with_metadata':True, 'header':HTTP_HEADER}
        sts, data = self.cm.getPage(baseUrl, urlParams)
        if not sts: return False
        cUrl = data.meta['url']
        
        urlsTab = []
        data = self.cm.ph.getAllItemsBeetwenMarkers(data, 'sources', ']', False)
        if not data:
            videoId = re.findall("embed/([0-9a-z]*?)(/.*|)$", baseUrl)
            if videoId:
                videoId=videoId[0][0]
                url = "https://vidcloud.co/player?fid={0}&page=embed".format(videoId)
                sts, data = self.cm.getPage(url, urlParams)
                if sts: 
                    data = json_loads(data)
                    ret= data["html"]
                    printDBG(ret)
                    data = self.cm.ph.getAllItemsBeetwenMarkers(ret, 'sources', ']', False)
                else:
                    data = ''
        if data:
            printDBG(str(data))
            for sourceData in data:
                sourceData = self.cm.ph.getAllItemsBeetwenMarkers(sourceData, '{', '}')
                for item in sourceData:
                    #printDBG(item)
                    item_data = json_loads(item)
                    printDBG(str(item_data))
                    if 'file' in item_data:
                        video_url = item_data['file']
                    elif 'src' in item_data: 
                        video_url = item_data['src']
                    else:
                        video_url = ''
                    if video_url:
                        if 'type' in item_data:
                            video_type = item_data['type']
                        else:
                            video_type = ''

                        if 'name' in item_data:
                            video_name = item_data['name']
                        else:
                            video_name = urlparser.getDomain(url)
                        
                        video_name = video_name + ' ' + video_type

                        video_url = strwithmeta(video_url, {'Referer':cUrl})
                        urlsTab.append({'name':video_name, 'url': video_url})
        
        return urlsTab

    def parserXSTREAMCDNCOM(self, baseUrl):
        printDBG('parserXSTREAMCDNCOM baseUrl[%r]' % baseUrl)
        baseUrl = strwithmeta(baseUrl)
        urlsTab=''
        mp4Tab = []
        hlsTab = []
        HTTP_HEADER = self.cm.getDefaultHeader(browser='chrome')
        referer = baseUrl.meta.get('Referer')
        if referer:
            HTTP_HEADER['Referer'] = referer
        COOKIE_FILE = GetCookieDir('xstreamcdn.com.cookie')
        rm(COOKIE_FILE)
        urlParams = {'header': HTTP_HEADER, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': COOKIE_FILE}
        sts, data = self.cm.getPage(baseUrl, urlParams)
        if not sts:
            return False
        cUrl = self.cm.meta['url']
        printDBG('curl='+cUrl)
        if cUrl.endswith('/'): cUrl=cUrl[:-1]
        printDBG('curl='+cUrl)
        urlParams['header'].update({'Referer': cUrl, 'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest'})
        url = self.cm.getFullUrl('/api/source/%s' % cUrl.rsplit('/', 1)[(-1)], cUrl)
        sts, data = self.cm.getPage(url, urlParams, {'r': '', 'd': self.cm.getBaseUrl(cUrl, True)})
        if not sts:
            return False
        data = json_loads(data)
        printDBG('data='+str(data))
        for item in data['data']:
            url = item['file']
            type = item.get('type', url.split('?', 1)[0].split('.')[-1]).lower()
            label = item.get('label', type)
            if url.startswith('//'): url = 'http:' + url
            if not self.cm.isValidUrl(url): continue
            url = strwithmeta(url, {'Referer':HTTP_HEADER['Referer'], 'User-Agent':HTTP_HEADER['User-Agent']})
            if 'hls' in type or 'm3u8' in type:
                hlsTab.extend(getDirectM3U8Playlist(url, checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
            elif 'mp4' in type or 'mpegurl' in type:
                mp4Tab.append({'name':'[%s] %s' % (type, label), 'url':url})
        
        videoTab = []
        videoTab.extend(mp4Tab)
        videoTab.extend(hlsTab)
        printDBG('videoTab:'+str(videoTab))			
        return videoTab

    def parserRAPIDVIDEO(self, baseUrl, getQualityLink=False):
        retTab = []
        baseUrl = baseUrl.replace('rapidvideo.com','rapidvideo.is')
        baseUrl = baseUrl.replace('rapidvid.to','rapidvideo.is')
        if not getQualityLink:
            if '/e/' not in baseUrl:
                video_id = self.cm.ph.getSearchGroups(baseUrl+'/', '(?:embed|e|view|v)[/-]([A-Za-z0-9]+)[^A-Za-z0-9]')[0]
                url = 'http://www.rapidvideo.is/e/'+video_id
            else:
                url = baseUrl
        else:
            url = baseUrl
            
        baseUrl = strwithmeta(baseUrl)
        referer = baseUrl.meta.get('Referer', '')
        
        HTTP_HEADER = self.cm.getDefaultHeader(browser='chrome')
        if referer != '': HTTP_HEADER['Referer'] = referer
        paramsUrl = {'header':HTTP_HEADER}
        
        sts, data = self.cm.getPage(url, paramsUrl)
        if not sts: return False
        
        if not getQualityLink:
            tmp = self.cm.ph.getDataBeetwenMarkers(data, 'Quality:', '<script')[1]
            tmp = self.cm.ph.getAllItemsBeetwenMarkers(tmp, '<a', '</a>')
            for item in tmp:
                url = self.cm.ph.getSearchGroups(item, '''href=['"]([^'^"]+?)['"]''')[0]
                title = clean_html(item).strip()
                if self.cm.isValidUrl(url):
                    try:
                        tmpTab = self.parserRAPIDVIDEO(url, True)
                        for vidItem in tmpTab:
                            vidItem['name'] = '%s - %s' % (title, vidItem['name'])
                            retTab.append(vidItem)
                    except Exception:
                        pass
            if len(retTab): return retTab[::-1]
        
        try:
            tmp = self.cm.ph.getDataBeetwenMarkers(data, '.setup(', ');', False)[1].strip()
            tmp = self.cm.ph.getDataBeetwenMarkers(data, '"sources":', ']', False)[1].strip()
            if tmp != '': tmp = json_loads(data+']')
        except Exception:
            printExc()
        
        for item in tmp:
            try: retTab.append({'name':'rapidvideo ' + item.get('label', item.get('res', '')), 'url':item['file']})
            except Exception: pass
        
        tmp = self.cm.ph.getDataBeetwenMarkers(data, '<video', '</video>')[1]
        tmp = self.cm.ph.getAllItemsBeetwenMarkers(tmp, '<source', '>', False)
        for item in tmp:
            url = self.cm.ph.getSearchGroups(item, '''src=['"]([^'^"]+?)['"]''')[0]
            type = self.cm.ph.getSearchGroups(item, '''type=['"]([^'^"]+?)['"]''')[0] 
            if 'video' not in type and 'x-mpeg' not in type: continue
            if url.startswith('/'):
                url = domain + url[1:]
            if self.cm.isValidUrl(url):
                if 'video' in type:
                    retTab.append({'name':'[%s]' % type, 'url':url})
                elif 'x-mpeg' in type:
                    retTab.extend(getDirectM3U8Playlist(url, checkContent=True))
        return retTab

    def parserSTREAMANGOCOM(self, baseUrl):
        printDBG("parserSTREAMANGOCOM url[%s]\n" % baseUrl)
        baseUrl = strwithmeta(baseUrl)
        HTTP_HEADER = dict(pageParser.HTTP_HEADER) 
        
        videoTab = []
        if '/embed/' not in baseUrl:
            sts, data = self.cm.getPage(baseUrl)
            if not sts: return videoTab
            url = self.cm.ph.getSearchGroups(data, '''<iframe[^>]+?src=["'](http[^"^']+?/embed/[^"^']+?)["']''', 1, True)[0]
            if url == '':
                data = self.cm.ph.getDataBeetwenMarkers(data, 'embedbox', '</textarea>')[1]
                data = clean_html(self.cm.ph.getDataBeetwenMarkers(data, '<textarea', '</textarea>')[1])
                url = self.cm.ph.getSearchGroups(data, '''<iframe[^>]+?src=["'](http[^"^']+?/embed/[^"^']+?)["']''', 1, True)[0]
                HTTP_HEADER['Referer'] = baseUrl.meta.get('Referer', baseUrl)
        else:
            url = baseUrl
        
        sts, data = self.cm.getPage(url, {'header' : HTTP_HEADER})
        if not sts: return videoTab
        cUrl = self.cm.meta['url']

        timestamp = time.time()

        errMsg = self.cm.ph.getDataBeetwenNodes(data, ('<', '>', 'important'), ('<', '>', 'div'))[1]
        SetIPTVPlayerLastHostError(clean_html(errMsg))
        
        # select valid section
        data = self.cm.ph.getAllItemsBeetwenMarkers(data, '<script', '</script>')
        for item in data:
            if 'srces.push' in item:
                data = item
                break
                
        #jscode = 'var document = {};\nvar window = this;\n' + self.cm.ph.getDataBeetwenReMarkers(data, re.compile('<script[^>]*?>'), re.compile('var\s*srces\s*=\s*\[\];'), False)[1]
        #data = self.cm.ph.getAllItemsBeetwenMarkers(data, 'srces.push(', ');')
        #jscode += '\nvar srces=[];\n' + '\n'.join(data) + '\nprint(JSON.stringify(srces));'
        #ret = js_execute( jscode )
        
        jscode = 'var document = {};\nvar window = this;\n' + self.cm.ph.getDataBeetwenReMarkers(data, re.compile('<script[^>]*?>'), re.compile('var\s*srces\s*=\s*\[\];'), False)[1]
        js_params = [{'name':'streamgo', 'code':jscode}]
        data = self.cm.ph.getAllItemsBeetwenMarkers(data, 'srces.push(', ');')
        jscode = '\nvar srces=[];\n' + '\n'.join(data) + '\nprint(JSON.stringify(srces));'
        js_params.append({'code':jscode})
        ret = js_execute_ext( js_params )
        data = ret['data'].strip()
        data = json_loads(data)
        
        dashTab = []
        hlsTab = []
        mp4Tab = []
        printDBG(data)
        for tmp in data:
            tmp = str(tmp).split('}')
            for item in tmp:
                item += ','
                url = self.cm.ph.getSearchGroups(item, r'''['"]?src['"]?\s*:\s*['"]([^"^']+)['"]''')[0]
                if url.startswith('//'): url = cUrl.split('//', 1)[0] + url
                type = self.cm.ph.getSearchGroups(item, r'''['"]?type['"]?\s*:\s*['"]([^"^']+)['"]''')[0]
                if not self.cm.isValidUrl(url): continue
            
                url = strwithmeta(url, {'User-Agent':HTTP_HEADER['User-Agent'], 'Referer':self.cm.meta['url'], 'Range':'bytes=0-'})
                if 'dash' in type:
                    dashTab.extend(getMPDLinksWithMeta(url, False))
                elif 'hls' in type:
                    hlsTab.extend(getDirectM3U8Playlist(url, checkExt=False, checkContent=True))
                elif 'mp4' in type or 'mpegurl' in type:
                    name = self.cm.ph.getSearchGroups(item, '''['"]?height['"]?\s*\:\s*([^\,]+?)[\,]''')[0]
                    mp4Tab.append({'name':'[%s] %sp' % (type, name), 'url':url})

        videoTab.extend(mp4Tab)
        videoTab.extend(hlsTab)
        videoTab.extend(dashTab)
        if len(videoTab):
            wait = time.time() - timestamp
            if wait < 4:
                printDBG(" time [%s]" % wait)
                GetIPTVSleep().Sleep(3 - int(wait))
        return videoTab

    def parserCLOUDVIDEOTV(self, baseUrl):
        printDBG("parserCLOUDVIDEOTV baseUrl[%r]" % baseUrl)
        # example video: https://cloudvideo.tv/embed-1d3w4w97woun.html
        baseUrl = strwithmeta(baseUrl)
        HTTP_HEADER= self.cm.getDefaultHeader(browser='chrome')
        HTTP_HEADER['Referer'] = baseUrl.meta.get('Referer', baseUrl)
        urlParams = {'header':HTTP_HEADER}

        sts, data = self.cm.getPage(baseUrl, urlParams)
        if not sts: return False
        cUrl = self.cm.meta['url']
        domain = urlparser.getDomain(cUrl)

        retTab = []
        tmp = ph.find(data, '<video', '</video>', flags=ph.IGNORECASE)[1]
        tmp = ph.findall(tmp, '<source', '>', flags=ph.IGNORECASE)
        for item in tmp:
            url = ph.getattr(item, 'src')
            type = ph.getattr(item, 'type') 
            if 'video' not in type and 'x-mpeg' not in type: continue
            if url:
                url = self.cm.getFullUrl(url, cUrl)
                if 'video' in type:
                    retTab.append({'name':'[%s]' % type, 'url':url})
                elif 'x-mpeg' in type:
                    retTab.extend(getDirectM3U8Playlist(url, checkContent=True, sortWithMaxBitrate=999999999))
        return retTab
        
    def parserGOOGLE(self, baseUrl):
        printDBG("parserGOOGLE baseUrl[%s]" % baseUrl)

        videoTab = []
        _VALID_URL = r'https?://(?:(?:docs|drive)\.google\.com/(?:uc\?.*?id=|file/d/)|video\.google\.com/get_player\?.*?docid=)(?P<id>[a-zA-Z0-9_-]{28,})'
        mobj = re.match(_VALID_URL, baseUrl)
        try:
            video_id = mobj.group('id')
            linkUrl = 'http://docs.google.com/file/d/' + video_id
        except Exception:
            linkUrl = baseUrl

        _FORMATS_EXT = {
            '5': 'flv', '6': 'flv',
            '13': '3gp', '17': '3gp',
            '18': 'mp4', '22': 'mp4',
            '34': 'flv', '35': 'flv',
            '36': '3gp', '37': 'mp4',
            '38': 'mp4', '43': 'webm',
            '44': 'webm', '45': 'webm',
            '46': 'webm', '59': 'mp4',
        }

        HTTP_HEADER = self.cm.getDefaultHeader(browser='chrome')
        HTTP_HEADER['Referer'] = linkUrl

        COOKIE_FILE = GetCookieDir('google.cookie')
        defaultParams = {'header': HTTP_HEADER, 'use_cookie': True, 'load_cookie': False, 'save_cookie': True, 'cookiefile': COOKIE_FILE}

        sts, data = self.cm.getPage(linkUrl, defaultParams)
        if not sts:
            return False

        cookieHeader = self.cm.getCookieHeader(COOKIE_FILE)
        fmtDict = {}
        fmtList = self.cm.ph.getSearchGroups(data, '"fmt_list"[:,]"([^"]+?)"')[0]
        fmtList = fmtList.split(',')
        printDBG('fmtList='+str(fmtList))
        for item in fmtList:
            item = self.cm.ph.getSearchGroups(item, '([0-9]+?)/([0-9]+?x[0-9]+?)/', 2)
            if item[0] != '' and item[1] != '':
                fmtDict[item[0]] = item[1]
        data = self.cm.ph.getSearchGroups(data, '"fmt_stream_map"[:,]"([^"]+?)"')[0]
        data = data.split(',')
        for item in data:
            item = item.split('|')
            printDBG(">> type[%s]" % item[0])
            if 'mp4' in _FORMATS_EXT.get(item[0], ''):
                try:
                    quality = int(fmtDict.get(item[0], '').split('x', 1)[-1])
                except Exception:
                    quality = 0
                videoTab.append({'name': 'drive.google.com: %s' % fmtDict.get(item[0], '').split('x', 1)[-1] + 'p', 'quality': quality, 'url': strwithmeta(unicode_escape(item[1]), {'Cookie': cookieHeader, 'Referer': 'https://youtube.googleapis.com/', 'User-Agent': HTTP_HEADER['User-Agent']})})
        videoTab.sort(key=lambda item: item['quality'], reverse=True)
        return videoTab

        
    def parserGOOGLE1(self, baseUrl):
        printDBG("parserGOOGLE baseUrl[%s]" % baseUrl)
        
        videoTab = []
        _VALID_URL = r'https?://(?:(?:docs|drive)\.google\.com/(?:uc\?.*?id=|file/d/)|video\.google\.com/get_player\?.*?docid=)(?P<id>[a-zA-Z0-9_-]{28,})'
        mobj = re.match(_VALID_URL, baseUrl)
        try:
            video_id = mobj.group('id')
            linkUrl = 'http://docs.google.com/file/d/' + video_id 
        except Exception:
            linkUrl = baseUrl
            
        _FORMATS_EXT = {
            '5': 'flv', '6': 'flv',
            '13': '3gp', '17': '3gp',
            '18': 'mp4', '22': 'mp4',
            '34': 'flv', '35': 'flv',
            '36': '3gp', '37': 'mp4',
            '38': 'mp4', '43': 'webm',
            '44': 'webm', '45': 'webm',
            '46': 'webm', '59': 'mp4',
        }
        
        HTTP_HEADER= self.cm.getDefaultHeader(browser='chrome')
        HTTP_HEADER['Referer'] = linkUrl
        
        COOKIE_FILE = GetCookieDir('google.cookie')
        defaultParams = {'header': HTTP_HEADER, 'use_cookie': True, 'load_cookie': False, 'save_cookie': True, 'cookiefile': COOKIE_FILE}
        
        sts, data = self.cm.getPage(linkUrl, defaultParams)
        if not sts: return False 
        
        cookieHeader = self.cm.getCookieHeader(COOKIE_FILE)
        fmtDict = {} 
        fmtList = self.cm.ph.getSearchGroups(data, '"fmt_list"[:,]"([^"]+?)"')[0]
        fmtList = fmtList.split(',')
        for item in fmtList:
            item = self.cm.ph.getSearchGroups(item, '([0-9]+?)/([0-9]+?x[0-9]+?)/', 2)
            if item[0] != '' and item[1] != '':
                fmtDict[item[0]] = item[1]
        data = self.cm.ph.getSearchGroups(data, '"fmt_stream_map"[:,]"([^"]+?)"')[0]
        data = data.split(',')
        for item in data:
            item = item.split('|')
            printDBG(">> type[%s]" % item[0])
            if 'mp4' in _FORMATS_EXT.get(item[0], ''):
                try: quality = int(fmtDict.get(item[0], '').split('x', 1)[-1])
                except Exception: quality = 0
                videoTab.append({'name':'drive.google.com: %s' % fmtDict.get(item[0], '').split('x', 1)[-1] + 'p', 'quality':quality, 'url':strwithmeta(unicode_escape(item[1]), {'Cookie':cookieHeader, 'Referer':'https://youtube.googleapis.com/', 'User-Agent':HTTP_HEADER['User-Agent']})})
        videoTab.sort(key=lambda item: item['quality'], reverse=True)
        return videoTab


    def _getSources(self, data):
        printDBG('>>>>>>>>>> _getSources')
        urlTab = []
        tmp = self.cm.ph.getDataBeetwenMarkers(data, 'sources', ']')[1]
        if tmp != '':
            tmp = tmp.replace('\\', '')
            tmp = tmp.split('}')
            urlAttrName = 'file'
            sp = ':'
        else:
            tmp = self.cm.ph.getAllItemsBeetwenMarkers(data, '<source', '>', withMarkers=True)
            urlAttrName = 'src'
            sp = '='
        printDBG(tmp)
        for item in tmp:
            url  = self.cm.ph.getSearchGroups(item, r'''['"]?{0}['"]?\s*{1}\s*['"](https?://[^"^']+)['"]'''.format(urlAttrName, sp))[0]
            if not self.cm.isValidUrl(url): continue
            name = self.cm.ph.getSearchGroups(item, r'''['"]?label['"]?\s*''' + sp + r'''\s*['"]?([^"^'^\,^\{]+)['"\,\{]''')[0]
            
            printDBG('---------------------------')
            printDBG('url:  ' + url)
            printDBG('name: ' + name)
            printDBG('+++++++++++++++++++++++++++')
            printDBG(item)
            
            if 'flv' in item:
                if name == '': name = '[FLV]'
                urlTab.insert(0, {'name':name, 'url':url})
            elif 'mp4' in item:
                if name == '': name = '[MP4]'
                urlTab.append({'name':name, 'url':url})
            
        return urlTab


        
    def _findLinks(self, data, serverName='', linkMarker=r'''['"]?file['"]?[ ]*:[ ]*['"](http[^"^']+)['"][,}]''', m1='sources', m2=']', contain='', meta={}):
        linksTab = []
        
        def _isSmil(data):
            return data.split('?')[0].endswith('.smil')
        
        def _getSmilUrl(url):
            if _isSmil(url):
                SWF_URL=''
                # get stream link
                sts, data = self.cm.getPage(url)
                if sts:
                    base = self.cm.ph.getSearchGroups(data, 'base="([^"]+?)"')[0]
                    src = self.cm.ph.getSearchGroups(data, 'src="([^"]+?)"')[0]
                    #if ':' in src:
                    #    src = src.split(':')[1]   
                    if base.startswith('rtmp'):
                        return base + '/' + src + ' swfUrl=%s pageUrl=%s' % (SWF_URL, url)
            return ''
        
        subTracks = []
        subData = self.cm.ph.getDataBeetwenReMarkers(data, re.compile('''['"]?tracks['"]?\s*?:'''), re.compile(']'), False)[1].split('}')
        for item in subData:
            kind = self.cm.ph.getSearchGroups(item, r'''['"]?kind['"]?\s*?:\s*?['"]([^"^']+?)['"]''')[0].lower()
            if kind != 'captions': continue
            src = self.cm.ph.getSearchGroups(item, r'''['"]?file['"]?\s*?:\s*?['"](https?://[^"^']+?)['"]''')[0]
            if src == '': continue
            label = self.cm.ph.getSearchGroups(item, r'''label['"]?\s*?:\s*?['"]([^"^']+?)['"]''')[0]
            format = src.split('?', 1)[0].split('.')[-1].lower()
            if format not in ['srt', 'vtt']: continue
            if 'empty' in src.lower(): continue
            subTracks.append({'title':label, 'url':src, 'lang':'unk', 'format':'srt'})
        
        srcData = self.cm.ph.getDataBeetwenMarkers(data, m1, m2, False)[1].split('},')
        for item in srcData:
            item += '},'
            if contain != '' and contain not in item: continue
            link = self.cm.ph.getSearchGroups(item, linkMarker)[0].replace('\/', '/')
            if '%3A%2F%2F' in link and '://' not in link:
                link = Unquote(link)
            link = strwithmeta(link, meta)
            label = self.cm.ph.getSearchGroups(item, r'''['"]?label['"]?[ ]*:[ ]*['"]([^"^']+)['"]''')[0]
            if _isSmil(link):
                link = _getSmilUrl(link)
            if '://' in link:
                proto = 'mp4'
                if link.startswith('rtmp'):
                    proto = 'rtmp'
                if link.split('?')[0].endswith('m3u8'):
                    tmp = getDirectM3U8Playlist(link)
                    linksTab.extend(tmp)
                else:
                    linksTab.append({'name': '%s %s' % (proto + ' ' +serverName, label), 'url':link})
                printDBG('_findLinks A')
        
        if 0 == len(linksTab):
            printDBG('_findLinks B')
            link = self.cm.ph.getSearchGroups(data, linkMarker)[0].replace('\/', '/')
            link = strwithmeta(link, meta)
            if _isSmil(link):
                link = _getSmilUrl(link)
            if '://' in link:
                proto = 'mp4'
                if link.startswith('rtmp'):
                    proto = 'rtmp'
                linksTab.append({'name':proto + ' ' +serverName, 'url':link})
        
        if len(subTracks):
            for idx in range(len(linksTab)):
                linksTab[idx]['url'] = urlparser.decorateUrl(linksTab[idx]['url'], {'external_sub_tracks':subTracks})
        
        return linksTab

    def parserGOVIDME(self, baseUrl):
        printDBG("parserGOVIDME baseUrl[%s]" % baseUrl)
        retTab = []
        sts, data = self.cm.getPage(baseUrl)
        if not sts: return False		
        lst_data = re.findall('sources.*?[\'"](.*?)[\'"]',data, re.S)
        if lst_data:
            link = lst_data[0]
            if 'm3u8' in link:
                retTab.extend(getDirectM3U8Playlist(link, checkExt=False, checkContent=True))
            else:
                retTab.append({'name':'MP4', 'url':link})
        return retTab
        
    def parserHQQ(self, baseUrl):
        #From Vstream
        baseUrl = baseUrl.replace('//waaw.tv/','//hqq.tv/').replace('/watch_video.php?vid','/player/embed_player.php?vid')
        printDBG("parserHQQ baseUrl[%s]" % baseUrl)
        retTab = []
        sts, data = self.cm.getPage(baseUrl)
        if sts:
            vid = re.search('videokeyorig *= *[\'"](.+?)[\'"]', data, re.DOTALL).group(1)
            url = "time=1&ver=0&secure=0&adb=0%2F&v={}&token=&gt=&embed_from=0&wasmcheck=1".format(vid)
            url = 'https://hqq.tv/player/get_md5.php?' + url
            UA  = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/66.0'
            headers = {'User-Agent': UA, 'Accept': '*/*', 'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3', 'x-requested-with': 'XMLHttpRequest', 'Referer': baseUrl}
            defaultParams = {'header': headers}
            sts, data = self.cm.getPage(url,defaultParams)
            if sts:
                printDBG('data='+str(data))
        return retTab		
        
    def parserMIXDROP(self, baseUrl):
        printDBG("parserMIXDROP baseUrl[%r]" % baseUrl)
        vidTab = []
        HTTP_HEADER= { 'User-Agent':"Mozilla/5.0"}
        if 'Referer' in strwithmeta(baseUrl).meta:
            HTTP_HEADER['Referer'] = strwithmeta(baseUrl).meta['Referer']
        urlParams = {'header': HTTP_HEADER}
        sts, data = self.cm.getPage(baseUrl, urlParams)
        if not sts: return False
        lst_data = re.findall("(eval\(function.*?)</script>", data, re.S)
        if lst_data:		
            data0 = cPacker().unpack(lst_data[0].strip())
            lst_data = re.findall('MDCore.wurl.*?"(.*?)"', data0, re.S)
            if lst_data:
                url_ = lst_data[0]
                if url_.startswith('//'): url_ = 'http:'+url_
                vidTab.append({'name':'[MP4]', 'url':url_})
                return vidTab
        if 'Video will be converted and ready to play' in data: SetIPTVPlayerLastHostError('Video will be converted and ready to play soon')
        return []	
    def parserSAMAUP(self, baseUrl):
        printDBG("parserSAMAUP baseUrl[%r]" % baseUrl)
        vidTab = []
        HTTP_HEADER= { 'User-Agent':"Mozilla/5.0"}
        if 'Referer' in strwithmeta(baseUrl).meta:
            HTTP_HEADER['Referer'] = strwithmeta(baseUrl).meta['Referer']
        urlParams = {'header': HTTP_HEADER}
        sts, data = self.cm.getPage(baseUrl, urlParams)
        if not sts: return False
        
        lst_data = re.findall("(eval\(function.*?)</script>", data, re.S)
        if lst_data:		
            data = cPacker().unpack(lst_data[0].strip())
            lst_data = re.findall('file.*?"(.*?)"', data, re.S)
            if lst_data:
                url_ = lst_data[0]
                if url_.startswith('//'): url_ = 'http:'+url_
                vidTab.append({'name':'[MP4]', 'url':url_})

        return vidTab
        
    def parserYOUDBOX(self, baseUrl):
        printDBG("parserYOUDBOX baseUrl[%r]" % baseUrl)
        vidTab = []
        HTTP_HEADER= { 'User-Agent':"Mozilla/5.0"}
        if 'Referer' in strwithmeta(baseUrl).meta:
            HTTP_HEADER['Referer'] = strwithmeta(baseUrl).meta['Referer']
        urlParams = {'header': HTTP_HEADER}
        sts, data = self.cm.getPage(baseUrl, urlParams)
        if not sts: return False
        lst_data = re.findall('function\(\) {var.*?\[(.*?)\]', data, re.S)
        if lst_data:		
            html_ = ''
            elms = lst_data[0].split(',')
            for elm in elms:
                elm=elm.replace('"','').replace('\\x','')
                elm=chr(int(elm,16))
                html_=elm+html_
            printDBG('html_100 ='+html_)
            lst_data = re.findall('src="(.*?)"', html_, re.S)
            if lst_data:
                url_=lst_data[0]
                if url_.startswith('//'): url_ = 'http:'+url_
                vidTab.append({'name':'[MP4]', 'url':url_})
 
        return vidTab

    def parserSTD06(self, baseUrl):
        printDBG("parserSTD06 baseUrl[%r]" % baseUrl)
        url = baseUrl
        hlsTab = []
        mp4Tab = []
        
        HTTP_HEADER= { 'User-Agent':"Mozilla/5.0"}
        if 'Referer' in strwithmeta(baseUrl).meta:
            HTTP_HEADER['Referer'] = strwithmeta(baseUrl).meta['Referer']
        COOKIE_FILE = GetCookieDir('urlstd03.cookie')
        self.cm.clearCookie(COOKIE_FILE, ['__cfduid', 'cf_clearance'])
        urlParams = {'header': HTTP_HEADER, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': COOKIE_FILE}
        sts, data = self.getPageCF(baseUrl, urlParams)
        if not sts: return False
        
        lst_data = re.findall("javascript'>(eval.*?)</script>", data, re.S)
        if lst_data:		
            data = cPacker().unpack(lst_data[0].strip())
            data = data.replace('file:','"file":').replace('label:','"label":')
            lst_data = re.findall('sources.*?(\[.*?\])', data, re.S)
            if lst_data:
                items = json.loads(lst_data[0])
                for item in items:
                    url = strwithmeta(item['file'], {'Referer':baseUrl})
                    type_ = url.split('?', 1)[0].split('.')[-1].lower()
                    label = item.get('label',type_)
                    if 'm3u8' in url:
                        hlsTab.extend(getDirectM3U8Playlist(url, checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
                    elif 'mp4' in url:
                        mp4Tab.append({'name':'[MP4] '+label, 'url':url})
                        
    def parserMOVS4U(self, baseUrl):
        printDBG("parserMOVS4U baseUrl[%r]" % baseUrl)
        printDBG("parserUNI01"+str(strwithmeta(baseUrl).meta))
        videoTab = []
        url = baseUrl
        HTTP_HEADER= {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0','Referer':''}
        COOKIE_FILE = GetCookieDir('UNI01.cookie')	
        self.cm.clearCookie(COOKIE_FILE, ['__cfduid', 'cf_clearance'])
        urlParams = {'header': HTTP_HEADER, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': COOKIE_FILE}
        sts, data = self.getPageCF(url, urlParams)
        if not sts: return False
        lst_data = re.findall('<source src="(.*?)".*?label="(.*?)"', data, re.S)
        for (url,label) in lst_data:
            videoTab.append({'name':label, 'url':url})	
        return videoTab	

    def parserUNI001(self, baseUrl):
        return self.parserUNI01(baseUrl)

    def parserUNI01(self, baseUrl):
        printDBG("parserUNI01 baseUrl[%r]" % baseUrl)
        printDBG("parserUNI01"+str(strwithmeta(baseUrl).meta))
        videoTab = []
        url = baseUrl
        HTTP_HEADER= {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}
        if 'Referer' in strwithmeta(baseUrl).meta:
            referer = strwithmeta(baseUrl).meta['Referer']
            if IsPython3():
                referer = referer.encode("utf-8").decode("latin1")
            printDBG('---------referer = '+referer)
            HTTP_HEADER['Referer'] = referer
        if 'arabveturk'  in baseUrl: HTTP_HEADER['Referer'] = ''
        if 'gounlimited' in baseUrl: HTTP_HEADER['Referer'] = ''
        if 'movs4u'      in baseUrl: HTTP_HEADER['Referer'] = ''
        if 'uqload'  in baseUrl: HTTP_HEADER['Referer'] = ''       
        if 'asia2tv'  in baseUrl: HTTP_HEADER['Referer'] = 'https://asiatv.online'
        if '/sbembed1.com/e/' in baseUrl: url = baseUrl.replace('/e/','/play/') 
        #printDBG("parserUNI01"+str(HTTP_HEADER))
        COOKIE_FILE = GetCookieDir('UNI01.cookie')	
        self.cm.clearCookie(COOKIE_FILE, ['__cfduid', 'cf_clearance'])
        urlParams = {'header': HTTP_HEADER, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': COOKIE_FILE}
        sts, data = self.getPageCF(url, urlParams)
        #sts, data = self.cm.getPage(url)
        if not sts: return False
        #printDBG('data='+'#'+str(data)+'#')
        if 'ﾟωﾟ' in data:
            lst_pk = re.findall("(ﾟωﾟ.*?)<", data, re.S)
            if lst_pk:
                try:
                    pack_ = lst_pk[0].strip()
                    printDBG('packed = '+pack_)
                    tmp = decodeAA(pack_)
                    printDBG('unpacked = '+tmp)
                    data = data.replace(pack_,tmp)	
                except Exception:
                    printExc()
        if 'sibnet' in baseUrl: data = data.replace('player.src','sources')
        if 'imdb.com' in baseUrl: data = data.replace('encodings','sources')
        lst_data = re.findall('sources.{,9}?(\[.*?\])', data, re.S)
        if not lst_data:
            lst_data0 = re.findall('(eval\(function\(p.*?)</script>', data, re.S)
            if lst_data0:
                printDBG('eval trouver='+lst_data0[0].strip()+'#')
                data0 = cPacker().unpack(lst_data0[0].strip())
                lst_data = re.findall('sources.*?(\[.*?\])', data0, re.S)
                if not lst_data:
                    lst_data = re.findall('holaplayer.*?src:"(.*?)"', data0, re.S)
                    if not lst_data:
                        lst_data = re.findall('src\((.*?])', data0, re.S)		
                        if not lst_data:
                            lst_data = re.findall('.setup.*?file:["\'](.*?)["\']', data0, re.S)	
                            if not lst_data:
                                lst_data = re.findall('file.*?"(.*?)"', data, re.S)
                                if not lst_data:
                                    lst_data = re.findall('<video.*?src="(.*?)"', data, re.S)
            else:
                lst_data = re.findall('<source.*?src="(.*?)"', data, re.S)
                if not lst_data:
                    lst_data = re.findall('.setup\({.*?file:.*?["\'](.*?)["\']', data, re.S)
        if lst_data:
            videoTab = self.parserUNI01_GET(lst_data,baseUrl,HTTP_HEADER)
        else:
            if 'Video is processing now.' in data: SetIPTVPlayerLastHostError('Video is processing now.')
            elif 'Video not available!' in data: SetIPTVPlayerLastHostError('Video not available!')	
        return videoTab	




    def parserUNI01_GET(self, lst_data,baseUrl,HTTP_HEADER):
        hlsTab  = []
        mp4Tab  = []
        dashTab = []
        src = str(lst_data[0])
        src = src.replace('label:','"label":').replace('file:','"file":').replace('fileType:','"fileType":').replace('src:','"file":').replace('type:','"type":').replace('res:','"res":').replace('size:','"label":').replace('\\/','/').replace('\\\'','"')
        src = src.replace('"definition":','"label":').replace('"videoUrl":','"file":')
        printDBG('src='+'#'+src+'#')
        src =src.replace(',]',']')
        if ('[' not in src) and ('{' not in src): src='["'+src+'"]'
        src = src.replace(',}','}')
        printDBG('src='+'#'+src+'#')
        items = json.loads(src)
        printDBG('items='+str(items))
        cookieHeader = self.cm.getCookieHeader(GetCookieDir('UNI01.cookie'))
        for item in items:
            printDBG('item='+str(item))
            if not IsPython3():
                if isinstance(item, unicode):
                    item = str(item)
            if isinstance(item, str): 
                if not item.startswith('http'): item = urlparser.getDomain(baseUrl,False)+item
                url = strwithmeta(item,  {'Cookie':cookieHeader,'Referer':baseUrl, 'User-Agent':HTTP_HEADER['User-Agent']})
                label = ''
                type_ = ''				
            else:
                url = item.get('file','')
                if not url.startswith('http'): url = urlparser.getDomain(baseUrl,False)+url
                if '.stardima.' not in baseUrl:
                    url = strwithmeta(url, {'Cookie':cookieHeader,'Referer':baseUrl, 'User-Agent':HTTP_HEADER['User-Agent']})
                label = item.get('label','')
                type_ = item.get('type','').lower()				
            if 'm3u8' in url:
                hlsTab.extend(getDirectM3U8Playlist(url, checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
            elif ('mp4' in url) or ('mp4' in type_):
                if label=='':
                    label = 'MP4'
                else:
                    label = 'MP4 [%s]' % label
                mp4Tab.append({'name':label, 'url':url})
            #elif 'mdp' in url:
            #	dashTab.extend(getMPDLinksWithMeta(url, False))								
        videoTab = []
        videoTab.extend(hlsTab)		
        videoTab.extend(mp4Tab)
        videoTab.extend(dashTab)
        return videoTab	
        

    def parserVIDTODOCOM(self, baseUrl):
        printDBG("parserVIDTODOCOM baseUrl[%r]" % baseUrl)
        url = baseUrl
        if 'emb.html?' in baseUrl:
            id_tab = re.findall('\?(.*?)=', baseUrl, re.S)
            if id_tab:
                url='https://vidtodo.com/embed-'+id_tab[0]+'.html?auto=1'
        return self.parserUNI01(url)

    def parserFEURL(self, baseUrl):
        printDBG("parserFEURL baseUrl[%r]" % baseUrl)
        cnt = 'feurl.com'
        cnt = 'vanfem.com'
        url = baseUrl.replace('/v/','/api/source/').replace('playvid.pw',cnt).replace('mg-play.info',cnt).replace('fsimg.info',cnt).replace('fembed.net',cnt).replace('www.','')
        HTTP_HEADER= {'User-Agent':"Mozilla/5.0"}
        urlParams = {'header': HTTP_HEADER}
        post_data = {'r':'','d':cnt}
        sts, data = self.cm.getPage(url, urlParams,post_data)
        printDBG('data='+'#'+str(data)+'#')
        if not sts: return False
        lst_data = re.findall('"data":(\[.*?])', data, re.S)
        if lst_data:
            videoTab = self.parserUNI01_GET(lst_data,baseUrl,HTTP_HEADER)		
            return videoTab
        else:
            return []
            
    def parserDUSTREAMING(self, baseUrl):
        printDBG("parserDUSTREAMING baseUrl[%r]" % baseUrl)
        url = baseUrl.replace('/v/','/api/source/').replace('playvid.pw','feurl.com').replace('mg-play.info','feurl.com').replace('fsimg.info','feurl.com').replace('fcdn.stream','feurl.com').replace('www.','')
        HTTP_HEADER= {'User-Agent':"Mozilla/5.0"}
        urlParams = {'header': HTTP_HEADER}
        post_data = {'r':'','d':'dustreaming.fr'}
        sts, data = self.cm.getPage(url, urlParams,post_data)
        printDBG('data='+'#'+str(data)+'#')
        if not sts: return False
        lst_data = re.findall('"data":(\[.*?])', data, re.S)
        if lst_data:
            videoTab = self.parserUNI01_GET(lst_data,baseUrl,HTTP_HEADER)		
            return videoTab
        else:
            return []
            
    def parserABCVIDEO(self, baseUrl):
        printDBG("parserABCVIDEO baseUrl[%r]" % baseUrl)
        url = baseUrl.replace('embed-','')
        HTTP_HEADER= {'User-Agent':"Mozilla/5.0"}
        urlParams = {'header': HTTP_HEADER}
        sts, data = self.cm.getPage(url, urlParams)
        printDBG('data='+'#'+str(data)+'#')
        if not sts: return False
        lst_data = re.findall('sources:.*?(\[.*?])', data, re.S)
        if lst_data:
            videoTab = self.parserUNI01_GET(lst_data,baseUrl,HTTP_HEADER)		
            return videoTab
        else:
            return []
            
    def parserDEEPMIC(self, baseUrl):
        printDBG("parserDEEPMIC baseUrl[%r]" % baseUrl)
        videoTab = []
        videoTab.append({'name':'MP4', 'url':baseUrl.replace('embed.php','videos.php')})
        return videoTab

    def downUPPOM(self, baseUrl):
        printDBG("downUPPOM baseUrl[%r]" % baseUrl)
        videoTab = []
        url = baseUrl
        HTTP_HEADER= {'User-Agent':"Mozilla/5.0"}
        COOKIE_FILE = GetCookieDir('uppom.cookie')	
        self.cm.clearCookie(COOKIE_FILE, ['__cfduid', 'cf_clearance'])
        urlParams = {'header': HTTP_HEADER, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': COOKIE_FILE}
        sts, data = self.getPageCF(url, urlParams)
        if sts:		
            lst_data = re.findall('<form(.*?)</form', data, re.S|re.IGNORECASE)
            while lst_data:
                post_data = {}
                lst_data1 = re.findall('<input.*?name="(.*?)".*?value="(.*?)"', lst_data[0], re.S|re.IGNORECASE)
                for elm in lst_data1:
                    post_data[elm[0]]=elm[1]
                urlParams['header']['Referer']=url
                sts, data = self.getPageCF(url,urlParams,post_data=post_data)	
                lst_data = re.findall('<form(.*?)</form', data, re.S|re.IGNORECASE)
            printDBG('data1='+'#'+str(data)+'#')		
            lst_data = re.findall('id="direct_link".*?href="(.*?)"', data, re.S|re.IGNORECASE)		
            if lst_data:
                videoTab.append({'name':'DirectLink', 'url':lst_data[0]})			
        return videoTab	
        
    def downSANDUP(self, baseUrl):
        printDBG("downSANDUP baseUrl[%r]" % baseUrl)
        videoTab = []
        url = baseUrl
        HTTP_HEADER= {'User-Agent':"Mozilla/5.0"}
        COOKIE_FILE = GetCookieDir('sandup.cookie')	
        self.cm.clearCookie(COOKIE_FILE, ['__cfduid', 'cf_clearance'])
        urlParams = {'header': HTTP_HEADER, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': COOKIE_FILE}
        sts, data = self.getPageCF(url, urlParams)
        if sts:		
            lst_data = re.findall('<form(.*?)</form', data, re.S|re.IGNORECASE)
            post_data = {}
            lst_data1 = re.findall('<input.*?name="(.*?)".*?value="(.*?)"', lst_data[0], re.S|re.IGNORECASE)
            for elm in lst_data1:
                post_data[elm[0]]=elm[1]
            urlParams['header']['Referer']=url
            sts, data = self.getPageCF(url,urlParams,post_data=post_data)	
            printDBG('data1='+'#'+str(data)+'#')		
            lst_data = re.findall('class="done">.*?href="(.*?)"', data, re.S|re.IGNORECASE)		
            if lst_data:
                videoTab.append({'name':'DirectLink', 'url':lst_data[0]})	
        return videoTab	
        
    def downTA7MEEL(self, baseUrl):
        printDBG("downTA7MEEL baseUrl[%r]" % baseUrl)
        videoTab = []
        url = baseUrl
        HTTP_HEADER= {'User-Agent':"Mozilla/5.0"}
        COOKIE_FILE = GetCookieDir('ta7meel.cookie')	
        self.cm.clearCookie(COOKIE_FILE, ['__cfduid', 'cf_clearance'])
        urlParams = {'header': HTTP_HEADER, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': COOKIE_FILE}
        sts, data = self.getPageCF(url, urlParams)
        if sts:		
            lst_data = re.findall('dl-link">.*?href="(.*?)"', data, re.S|re.IGNORECASE)
            if lst_data:
                videoTab.append({'name':'DirectLink', 'url':lst_data[0]})	
        return videoTab		
        
    def easyload_decode(self, src, t):
        url = ''.join([chr(ord(src[i]) ^ ord(t[i % len(t)])) for i in range(len(src))])
        return url
    def parserEASYLOAD(self, baseUrl):
        videoTab = []
        printDBG("parserFEURL baseUrl[%r]" % baseUrl)
        HTTP_HEADER= {'User-Agent':"Mozilla/5.0"}
        urlParams = {'header': HTTP_HEADER}
        sts, data = self.cm.getPage(baseUrl, urlParams)
        if not sts: return False
        lst_data = re.findall('data="([^"]+)', data, re.S)
        if lst_data:
            result = lst_data[0].replace('&quot;','"')
            result = json_loads (result)
            printDBG('result='+str(result))
            link = result.get('streams',{}).get('0',{}).get('src',{})
            printDBG('link='+str(link))
            link = self.easyload_decode(link, '15')
            printDBG('link='+str(link))
            if 'm3u8' in link:
                videoTab.extend(getDirectM3U8Playlist(link, checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
            else:
                videoTab.append({'name':'[MP4]', 'url':link})				
        return videoTab
        

    def dood_decode(self, data):
        data = data.replace('/', '1').decode('base64')
        data = data.replace('/', 'Z').decode('base64')
        data = data.replace('@', 'a').decode('base64')
        t = string.ascii_letters + string.digits
        return data + ''.join([random.choice(t) for _ in range(10)])
        
    def parserDOOD(self, baseUrl):
        printDBG("parserDOOD baseUrl [%s]" % baseUrl)
        
        httpParams = {
            'header' : {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip',
                'Referer' : baseUrl.meta.get('Referer', baseUrl)
            }, 
            'use_cookie':True,
            'load_cookie':True,
            'save_cookie':True,
            'cookiefile': GetCookieDir("dood.cookie")
        }

        urlsTab = []
        
        if '/d/' in baseUrl:
            baseUrl = baseUrl.replace('/d/','/e/')
        
        sts, data = self.cm.getPage(baseUrl, httpParams)
        
        if sts:
            printDBG("-----------------------")
            printDBG(data)
            printDBG("-----------------------")


        subTracks=[]
        #<track kind="captions" src="https://doodstream.com/srt/00705/s72n7d5hi6qc_Serbian.vtt" srclang="en" label="Serbian" default>
        tracks = self.cm.ph.getAllItemsBeetwenMarkers(data, '<track', '>', withMarkers=True)
        for track in tracks:
            track_kind = self.cm.ph.getSearchGroups(track, '''kind=['"]([^'^"]+?)['"]''')[0]
            if 'caption' in track_kind:
                srtUrl = self.cm.ph.getSearchGroups(track, '''src=['"]([^'^"]+?)['"]''')[0]
                srtLabel= self.cm.ph.getSearchGroups(track, '''label=['"]([^'^"]+?)['"]''')[0]
                srtFormat = srtUrl[-3:]
                params = {'title': srtLabel, 'url': srtUrl, 'lang': srtLabel.lower()[:3], 'format': srtFormat}
                printDBG(str(params))
                subTracks.append(params)

        #$.get('/pass_md5/3526522-87-9-1595176733-d1cadb0bad545cdcc61809e26c0ccf93/p3yuk59uqm525k1zc9boovu4'
        #function makePlay(){for(var a="",t="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",n=t.length,o=0;10>o;o++)a+=t.charAt(Math.floor(Math.random()*n));return a+"?token=p3yuk59uqm525k1zc9boovu4&expiry="+Date.now();};
        pass_md5_url = self.cm.ph.getSearchGroups(data, "\$\.get\('(/pass_md5[^']+?)'")[0]
        makePlay= self.cm.ph.getSearchGroups(data, "(function makePlay\(\)\{.*?\};)")[0]
        if pass_md5_url and makePlay:        
            pass_md5_url = self.cm.getFullUrl(pass_md5_url, self.cm.getBaseUrl(baseUrl))
            sts, new_url = self.cm.getPage(pass_md5_url, httpParams)

            if sts:
                code =  "var url = '%s';\n%s\nconsole.log(url + makePlay());" % (new_url, makePlay)
                
                printDBG("-----------------------")
                printDBG(code)
                printDBG("-----------------------")

                ret = js_execute(code)
                newUrl = ret['data'].replace("\n","")
                if newUrl:
                    if subTracks:
                        newUrl = urlparser.decorateUrl(newUrl, {'Referer': baseUrl,'external_sub_tracks':subTracks})
                    else:
                        newUrl = urlparser.decorateUrl(newUrl, {'Referer': baseUrl})
                    params = {'name': 'link' , 'url': newUrl}
                    printDBG(str(params))
                    urlsTab.append(params)
        
        return urlsTab


    def parserOKSTREAM(self, baseUrl):
        videoTab = []
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/66.0'
        printDBG("parserOKSTREAM baseUrl[%r]" % baseUrl)
        HTTP_HEADER= {'User-Agent':UA}
        urlParams = {'header': HTTP_HEADER}
        sts, data = self.cm.getPage(baseUrl, urlParams)
        if not sts: return False
        lst_data = re.findall('var keys="(.*?)".*?var protection="(.*?)"', data, re.S)
        if lst_data:
            post_data = {'morocco':lst_data[0][0],'mycountry':lst_data[0][1]}
            urlParams['header']['referer'] = baseUrl
            sts, data = self.cm.getPage('https://www.okstream.cc/request/', urlParams,post_data)
            if sts :
                link = strwithmeta(data, {'User-Agent':UA,'Referer':baseUrl})
                videoTab.append({'name':'[MP4]', 'url':link})
        return videoTab

    def parserGOFILE(self, baseUrl):
        videoTab = []
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/66.0'
        printDBG("parserGOFILE baseUrl[%r]" % baseUrl)
        HTTP_HEADER= {'User-Agent':UA}
        urlParams = {'header': HTTP_HEADER}
        if 'c=' in baseUrl:
            id = baseUrl.split('c=')[-1]
        else:
            id = baseUrl.split('/')[-1]
        url = 'https://apiv2.gofile.io/getServer?c='+id
        printDBG('url='+url)
        sts, data = self.cm.getPage(url, urlParams)
        if not sts: return False
        lst_data = re.findall('server":"(.*?)"', data, re.S)
        if lst_data:
            url1 = 'https://'+lst_data[0]+'.gofile.io/getUpload?c='+id
            urlParams['header']['referer'] = url
            sts, data = self.cm.getPage(url1, urlParams)
            if sts :
                lst_data = re.findall('link":"(.*?)"', data, re.S)
                if lst_data:
                    link = strwithmeta(lst_data[0], {'User-Agent':UA,'Referer':url1})
                    videoTab.append({'name':'[MP4]', 'url':link})
        return videoTab




    def parserPROTONVIDEO(self, baseUrl):
        printDBG('PROTONVIDEO= ') 
        videoTab = []
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/66.0'
        printDBG("parserPROTONVIDEO baseUrl[%r]" % baseUrl)
        HTTP_HEADER= {'User-Agent':UA}
        urlParams = {'header': HTTP_HEADER}



        s          = '0123456789abcdef0123456789abcdef'
        iv         = 'abcdef9876543210abcdef9876543210'     
        ciphertext = 'ed7536f576394025afc357216f3a80be'
        #ciphertext = base64.b64decode(ciphertext)
        iv         = unhexlify(iv)
        salt       = unhexlify(s)        
        decrypted  = cryptoJS_AES_decrypt(ciphertext, iv, salt)
        
        #printDBG('code= '+str(code)+' | pass= '+b)
        printDBG('decrypted= '+decrypted)        
        
        
        
        
        sts, data = self.cm.getPage(baseUrl,urlParams)
        if sts:
            #lst_data = re.findall('data-en=.*?[\'"](.*?)[\'"].*?data-p=.*?[\'"](.*?)[\'"]', data, re.S)	
            if False:#lst_data:
                code = Unquote(lst_data[0][0])
                code = json_loads(code.strip())
                b = lst_data[0][1]
                printDBG('code= '+str(code)+' | pass= '+b)
                ciphertext = base64.b64decode(code['ct'])
                iv = unhexlify(code['iv'])
                salt = unhexlify(code['s'])
                decrypted = cryptoJS_AES_decrypt(ciphertext, b, salt)
                printDBG('decrypted= '+decrypted)
                URL = decrypted.replace('\/','/').replace('"','')
                sts, data = self.cm.getPage(URL)
                if sts:	
                    printDBG('data= '+data)
                    lst_data = re.findall('file":"(.*?)"', data, re.S)	
                    if lst_data:
                        if 'm3u8' in lst_data[0]:
                            videoTab.extend(getDirectM3U8Playlist(lst_data[0], checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
                        else:
                            videoTab.append({'name':'[MP4]', 'url':lst_data[0]})	
        return videoTab		



    def parserZIMABDKO(self, baseUrl):
        videoTab = []
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/66.0'
        printDBG("parserFEURL baseUrl[%r]" % baseUrl)
        HTTP_HEADER= {'User-Agent':UA}
        urlParams = {'header': HTTP_HEADER}
        sts, data = self.cm.getPage(baseUrl,urlParams)
        if sts:
            lst_data = re.findall('data-en=.*?[\'"](.*?)[\'"].*?data-p=.*?[\'"](.*?)[\'"]', data, re.S)	
            if lst_data:
                code = Unquote(lst_data[0][0])
                code = json_loads(code.strip())
                b = lst_data[0][1]
                printDBG('code= '+str(code)+' | pass= '+b)
                ciphertext = base64.b64decode(code['ct'])
                iv = unhexlify(code['iv'])
                salt = unhexlify(code['s'])
                decrypted = cryptoJS_AES_decrypt(ciphertext, b, salt)
                printDBG('decrypted= '+decrypted)
                URL = decrypted.replace('\/','/').replace('"','')
                sts, data = self.cm.getPage(URL)
                if sts:	
                    printDBG('data= '+data)
                    lst_data = re.findall('file":"(.*?)"', data, re.S)	
                    if lst_data:
                        if 'm3u8' in lst_data[0]:
                            videoTab.extend(getDirectM3U8Playlist(lst_data[0], checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
                        else:
                            videoTab.append({'name':'[MP4]', 'url':lst_data[0]})	
        return videoTab		
        
        
    def parserSARUCH(self, baseUrl):
        videoTab = []
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/66.0'
        HTTP_HEADER= {'User-Agent':UA,'referer':baseUrl}
        urlParams = {'header': HTTP_HEADER}
        url = baseUrl.replace('/embed/','/videos/').replace('//saruch.co','//api.saruch.co')+'/stream?referrer='+baseUrl
        url = url.replace('//stream','/stream')
        sts, data = self.cm.getPage(url,urlParams)
        if sts:
            lst_data = re.findall('"sources":(\[.*?])', data, re.S)
            if lst_data:
                videoTab = self.parserUNI01_GET(lst_data,baseUrl,HTTP_HEADER)		
                return videoTab
            else:
                return []		
      
    def parserUSERLOAD(self, baseUrl):
        videoTab = []
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/66.0'
        HTTP_HEADER = {'User-Agent':UA,'referer':baseUrl}
        urlParams   = {'header': HTTP_HEADER}
        urlapi      = "https://userload.co/api/assets/userload/js/videojs.js"
        sts, data = self.cm.getPage(urlapi,urlParams)
        if sts:
            #data = data.decode('utf-8')
            printDBG('data='+data)
            printDBG('data='+data.encode().decode('utf-8')) 
        return []	

    def parserLINKBOX(self, baseUrl):
        videoTab = []
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/66.0'
        HTTP_HEADER = {'User-Agent':UA,'referer':baseUrl}
        urlParams   = {'header': HTTP_HEADER}
        if 'player.html?id=' in baseUrl:
            id_ = baseUrl.split('player.html?id=',1)[1]
        printDBG('id='+id_)
        url = 'https://www.linkbox.to/api/open/get_url?itemId=' + id_
        sts, data = self.cm.getPage(url)
        if sts:
            elms = json_loads(data.strip())
            printDBG('data='+str(elms))
            for elm in elms['data']['rList']:
                printDBG('data0='+str(elm))
                videoTab.append({'name':elm['resolution'], 'url':elm['url']})
        return videoTab	
        
    def parserRUMBLE(self, baseUrl):
        videoTab = []
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/66.0'
        HTTP_HEADER = {'User-Agent':UA,'referer':baseUrl}
        urlParams   = {'header': HTTP_HEADER}
        sts, data = self.cm.getPage(baseUrl,urlParams)
        if sts:
            #data = data.decode('utf-8')
            #printDBG('data='+data)
            lst_data = re.findall('"720":{.*?"url":"(.*?)"', data, re.S)
            if lst_data:
                videoTab.append({'name':'[720p]', 'url':lst_data[0].replace('\\','')})	            
            
            lst_data = re.findall('"480":{.*?"url":"(.*?)"', data, re.S)
            if lst_data:
                videoTab.append({'name':'[480p]', 'url':lst_data[0].replace('\\','')})	            
            
            lst_data = re.findall('"360":{.*?"url":"(.*?)"', data, re.S)
            if lst_data:
                videoTab.append({'name':'[360p]', 'url':lst_data[0].replace('\\','')})	
            
            lst_data = re.findall('"240":{.*?"url":"(.*?)"', data, re.S)
            if lst_data:
                videoTab.append({'name':'[240p]', 'url':lst_data[0].replace('\\','')})	           
             
        return videoTab      
        
        
        
        