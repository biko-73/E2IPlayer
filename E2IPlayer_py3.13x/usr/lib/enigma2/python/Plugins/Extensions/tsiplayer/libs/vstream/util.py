#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import GetCookieDir, GetCacheSubDir
import re,sys,time,os
try:
    import htmlentitydefs
    import urllib
    import urllib2

except ImportError:
    import html.entities as htmlentitydefs
    import urllib.parse as urllib
    import urllib.request as urllib2

import unicodedata
import string

class none_(object):
    def __new__(cls, *args):
        return object.__new__(cls)
    def __init__(self, *args):
        pass
    def __getattr__(self, name):
        return self
    def __call__(self, *args, **kwargs):
        return self
    def __int__(self):
        return 0
    def __float__(self):
        return 0
    def __str__(self):
        return '0'
    def __nonzero__(self):
        return False
    def __getitem__(self, key):
        return self
    def __setitem__(self, key, value):
        pass
    def __delitem__(self, key):
        pass
    def __len__(self):
        return 3
    def __iter__(self):
        return iter([self, self, self])

DialogProgress = none_()
Dialog         = none_()


class cPremiumHandler(object):
    def __init__(self, *args):
        pass
        
    def isPremiumModeAvailable(self):
        return False

class xbmc(object):
    def __init__(self, *args):
        pass

    def sleep(self, int_):
        time.sleep(int_/float(1000))
        
    def getInfoLabel(self,txt):
        if txt == 'system.buildversion': return '18'
        else: return '0'
        

def translatePath(url, asURL = False):
    return url
    
def VSlog(e, level=''):
    printDBG('VSlog: '+str(e))
    return

def VSPath(path):
    path = path.replace('special://temp/',GetCacheSubDir('Tsiplayer'))
    path = path.replace('special://home/userdata/addon_data/plugin.video.vstream/',GetCacheSubDir('Tsiplayer'))
    return path




def isMatrix():
    return False 
        
class GestionCookie():
    PathCache = GetCookieDir('')
    def DeleteCookie(self,Domain):
        Name = ''.join([self.PathCache, "cookie_%s.txt"]) % (Domain)
        try:
            os.remove(Name)
        except:
            pass

    def SaveCookie(self,Domain,data):
        Name = ''.join([self.PathCache, "cookie_%s.txt"]) % (Domain)
        f = open(Name, 'w')
        f.write(data)
        f.close()

    def Readcookie(self,Domain):
        Name = ''.join([self.PathCache, "cookie_%s.txt"]) % (Domain)
        try:
            f = open(Name,'r')
            data = f.read()
            f.close()
        except:
            return ''
        return data

    def AddCookies(self):
        cookies = self.Readcookie(self.__sHosterIdentifier)
        return 'Cookie=' + cookies    

class addon():

    def __int__(self):
        return 0
        
    def VSlang(self, lang):
        ret = str(lang)
        return ret
    def VSsetting(self, name, value=False):
        return None
        
    def getSetting(self, name):
        if name == 'poster_tmdb':  return 'w342' 
        elif name == 'poster_tmdb':  return 'w1280'
        elif name == 'api_tmdb':     return 'b7cf9324cbeb6f4fb811144aa9397093'    
        elif name == 'tmdb_session': return ''
        elif name.startswith('plugin_'): return 'true' 
        return None        
    
        
        

class progress():
    def VScreate(self, title='vStream', desc=''):
        return ''
    def VSupdate(self, dialog, total, text=''):
        count=0
    def VSupdatesearch(self, dialog, total, text=''):
        count=0
    def VSclose(self, dialog=''):
        return

class dialog():
    def __init__(self, *args):
        pass
        
    def VSok(self, desc, title='vStream'):
        return ''

    def VSyesno(self, desc, title='vStream'):
        return ''

    def VSselect(self, desc, title='vStream'):
        return ''

    def VSselectqual(self, list_qual, list_url):
        VSlog('start:'+str(list_url))
        if len(list_url) == 0:
            return ''
        if len(list_url) == 1:
            return list_url[0]
        ret = 0
        i=0
        urlout = ''
        for url in list_url:
            urlout=urlout+url+'|tag:'+list_qual[i]+'||'
            i=i+1
        VSlog('start:'+str(urlout))
        return urlout

    def VSinfo(self, desc, title='vStream', iseconds=0, sound = False):
        return ''
    def VSerror(self, e):
        printDBG('VSerror: '+str(e))
        return
  
class cParser:

    def parseSingleResult(self, sHtmlContent, sPattern):
        aMatches = re.compile(sPattern).findall(sHtmlContent)
        if (len(aMatches) == 1):
            aMatches[0] = self.__replaceSpecialCharacters(aMatches[0])
            return True, aMatches[0]
        return False, aMatches

    def __replaceSpecialCharacters(self, sString):
        """ /!\ pas les mêmes tirets, tiret moyen et cadratin."""
        return sString.replace('\r', '').replace('\n', '').replace('\t', '').replace('\\/', '/').replace('&amp;', '&')\
                      .replace('&#039;', "'").replace('&#8211;', '-').replace('&#8212;', '-').replace('&eacute;', 'é')\
                      .replace('&acirc;', 'â').replace('&ecirc;', 'ê').replace('&icirc;', 'î').replace('&ocirc;', 'ô')\
                      .replace('&hellip;', '...').replace('&quot;', '"').replace('&gt;', '>').replace('&egrave;', 'è')\
                      .replace('&ccedil;', 'ç').replace('&laquo;', '<<').replace('&raquo;', '>>').replace('\xc9', 'E')\
                      .replace('&ndash;', '-').replace('&ugrave;', 'ù').replace('&agrave;', 'à').replace('&lt;', '<')\
                      .replace('&rsquo;', "'").replace('&lsquo;', '\'').replace('&nbsp;', '').replace('&#8217;', "'")\
                      .replace('&#8230;', '...').replace('&#8242;', "'").replace('&#884;', '\'').replace('&#39;', '\'')\
                      .replace('&#038;', '&').replace('&iuml;', 'ï').replace('–', '-').replace('—', '-')

    def parse(self, sHtmlContent, sPattern, iMinFoundValue=1):
        sHtmlContent = self.__replaceSpecialCharacters(str(sHtmlContent))
        aMatches = re.compile(sPattern, re.IGNORECASE).findall(sHtmlContent)

        # extrait la page html après retraitement vStream
        # fh = open('c:\\test.txt', "w")
        # fh.write(sHtmlContent)
        # fh.close()

        if (len(aMatches) >= iMinFoundValue):
            return True, aMatches
        return False, aMatches

    def replace(self, sPattern, sReplaceString, sValue):
        return re.sub(sPattern, sReplaceString, sValue)

    def escape(self, sValue):
        return re.escape(sValue)

    def getNumberFromString(self, sValue):
        sPattern = '\d+'
        aMatches = re.findall(sPattern, sValue)
        if (len(aMatches) > 0):
            return aMatches[0]
        return 0

    def titleParse(self, sHtmlContent, sPattern):
        sHtmlContent = self.__replaceSpecialCharacters(str(sHtmlContent))
        aMatches = re.compile(sPattern, re.IGNORECASE)
        try:
            [m.groupdict() for m in aMatches.finditer(sHtmlContent)]
            return m.groupdict()
        except:
            return {'title': sHtmlContent}

    def abParse(self, sHtmlContent, start, end=None, startoffset=0):
        # usage oParser.abParse(sHtmlContent, 'start', 'end')
        # startoffset (int) décale le début pour ne pas prendre en compte start dans le résultat final si besoin
        # la fin est recherchée forcement après le début
        # la recherche de fin n'est pas obligatoire
        # usage2 oParser.abParse(sHtmlContent, 'start', 'end', 6)
        # ex youtube.py
        
        startIdx = sHtmlContent.find(start)
        if startIdx == -1:  # rien trouvé, retourner le texte complet
            return sHtmlContent
        
        if end:
            endIdx = sHtmlContent[startoffset + startIdx:].find(end)
            if endIdx > 0:
                return sHtmlContent[startoffset + startIdx: startoffset + startIdx + endIdx]
        return sHtmlContent[startoffset + startIdx:]
class cOutputParameterHandler:

    def __init__(self):
        self.__aParams = {}

    def addParameter(self, sParameterName, mParameterValue):
        if not mParameterValue:
            return
        #test du 20/10
        #self.__aParams[sParameterName] = urllib.unquote_plus(str(mParameterValue))
        self.__aParams[sParameterName] = urllib.unquote(str(mParameterValue))

    def getParameterAsUri(self):
        if len(self.__aParams) > 0:
                return urllib.urlencode(self.__aParams)
        return 'params=0'
    
    def getValue(self, sParamName):
        if (self.exist(sParamName)):
                sParamValue = self.__aParams[sParamName]
                #test du 20/10
                #return urllib.unquote_plus(sParamValue)
                return urllib.unquote(sParamValue)
        return False
            
    def exist(self, sParamName):
        return self.__aParams.has_key(sParamName)

class cInputParameterHandler:

    def __init__(self):          
            aParams = dict()
            if len(sys.argv)>=2 and len(sys.argv[2])>0:
                    aParams = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
          
            self.__aParams = aParams

    def getAllParameter(self):
            return self.__aParams

    def getValue(self, sParamName):
            if (self.exist(sParamName)):
                    sParamValue = self.__aParams[sParamName]
                    #return urllib.unquote_plus(sParamValue)
                    #en test depuis le 20/10
                    if not sParamValue.startswith('http'):
                        return urllib.unquote_plus(sParamValue)
                    else:
                        return urllib.unquote(sParamValue)
            return False

    def exist(self, sParamName):
            return self.__aParams.has_key(sParamName)

class cPluginHandler:

    def getPluginHandle(self):
        try:
            return int(sys.argv[1])
        except:
            return 0

    def getPluginPath(self):
        try:
            return sys.argv[0]
        except:
            return ''

    def __getFileNamesFromFolder(self, sFolder):
        aNameList = []
        folder, items = xbmcvfs.listdir(sFolder)
        items.sort()
        for sItemName in items:

            if not sItemName.endswith(".py"):
                continue

            sFilePath = "/".join([sFolder, sItemName])

            # xbox hack
            sFilePath = sFilePath.replace('\\', '/')

            VSlog("Load Plugin %s" % sItemName)

            if (xbmcvfs.exists(sFilePath) == True):
                if (sFilePath.lower().endswith('py')):
                    sItemName = sItemName.replace('.py', '')
                    aNameList.append(sItemName)
        return aNameList

    def __importPlugin(self, sName):
        try:
            exec("from resources.sites import " + sName, globals())
            exec("sSiteName = " + sName + ".SITE_NAME", globals())
            exec("sSiteDesc = " + sName + ".SITE_DESC", globals())
            sPluginSettingsName = 'plugin_' + sName
            return sSiteName, sPluginSettingsName, sSiteDesc
        except Exception as e:
            VSlog("Cannot import plugin " + str(sName))
            VSlog("Detail de l\'erreur " + str(e))
            return False, False

    def getAvailablePlugins(self, force=False):
        addons = addon()

        sFolder = "special://home/addons/plugin.video.vstream/resources/sites"
        sFolder = sFolder.replace('\\', '/')
        VSlog("Sites Folder " + sFolder)

        aFileNames = self.__getFileNamesFromFolder(sFolder)

        aPlugins = []
        for sFileName in aFileNames:
            # wir versuchen das plugin zu importieren
            aPlugin = self.__importPlugin(sFileName)
            if (aPlugin[0] != False):
                sSiteName = aPlugin[0]
                sPluginSettingsName = aPlugin[1]
                sSiteDesc = aPlugin[2]

                # existieren zu diesem plugin die an/aus settings
                bPlugin = addons.getSetting(sPluginSettingsName)
                if (bPlugin != ''):
                    # settings gefunden
                    if (bPlugin == 'true') or (force == True):
                        aPlugins.append(self.__createAvailablePluginsItem(sSiteName, sFileName, sSiteDesc))
                else:
                    # settings nicht gefunden, also schalten wir es trotzdem sichtbar
                    aPlugins.append(self.__createAvailablePluginsItem(sSiteName, sFileName, sSiteDesc))

        return aPlugins

    def getAllPlugins(self):
        sFolder = "special://home/addons/plugin.video.vstream/resources/sites"
        sFolder = sFolder.replace('\\', '/')
        VSlog("Sites Folder " + sFolder)

        aFileNames = self.__getFileNamesFromFolder(sFolder)

        aPlugins = []
        for sFileName in aFileNames:
            # wir versuchen das plugin zu importieren
            aPlugin = self.__importPlugin(sFileName)
            if (aPlugin[0] != False):
                sSiteName = aPlugin[0]
                sPluginSettingsName = aPlugin[1]
                sSiteDesc = aPlugin[2]

                # settings nicht gefunden, also schalten wir es trotzdem sichtbar
                aPlugins.append(self.__createAvailablePluginsItem(sSiteName, sFileName, sSiteDesc))

        return aPlugins

    def __createAvailablePluginsItem(self, sPluginName, sPluginIdentifier, sPluginDesc):
        aPluginEntry = []
        aPluginEntry.append(sPluginName)
        aPluginEntry.append(sPluginIdentifier)
        aPluginEntry.append(sPluginDesc)
        return aPluginEntry




class cUtil:

    def CheckOrd(self, label):
        count = 0
        try:
            label = label.lower()
            label = label.strip()
            label = unicode(label, 'utf-8')
            label = unicodedata.normalize('NFKD', label).encode('ASCII', 'ignore')
            for i in label:
                count += ord(i)
        except:
            pass

        return count

    def CheckOccurence(self,str1,str2):

        Ignoreliste = ['du', 'la', 'le', 'les', 'de', 'un', 'une','des']

        str1 = str1.replace('+',' ').replace('%20',' ')
        str1 = str1.lower()
        str2 = str2.lower()
        try:
            str1 = unicode(str1, 'utf-8')
        except:
            pass
        try:
            str2 = unicode(str2, 'utf-8')
        except:
            pass
        str1 = unicodedata.normalize('NFKD', str1).encode('ASCII', 'ignore')
        str2 = unicodedata.normalize('NFKD', str2).encode('ASCII', 'ignore')

        #xbmc.log(str1 + ' ---- ' + str2, xbmc.LOGNOTICE)

        i = 0
        for part in str1.split(' '):
            if (part in str2) and (part not in Ignoreliste):
                i = i + 1
        return i

    def removeHtmlTags(self, sValue, sReplace = ''):
        p = re.compile(r'<.*?>')
        return p.sub(sReplace, sValue)


    def formatTime(self, iSeconds):
        iSeconds = int(iSeconds)

        iMinutes = int(iSeconds / 60)
        iSeconds = iSeconds - (iMinutes * 60)
        if (iSeconds < 10):
            iSeconds = '0' + str(iSeconds)

        if (iMinutes < 10):
            iMinutes = '0' + str(iMinutes)

        return str(iMinutes) + ':' + str(iSeconds)

    def urlDecode(self, sUrl):
        return urllib.unquote(sUrl)

    def urlEncode(self, sUrl):
        return urllib.quote(sUrl)

    def unquotePlus(self, sUrl):
        return urllib.unquote_plus(sUrl)

    def quotePlus(self, sUrl):
        return urllib.quote_plus(sUrl)

    def DecoTitle(self, string):
        return string


    def DecoTitle2(self, string):

        #on vire ancienne deco en cas de bug
        string = re.sub('\[\/*COLOR.*?\]','',str(string))

        #pr les tag Crochet
        string = re.sub('([\[].+?[\]])',' [COLOR coral]\\1[/COLOR] ', string)
        #pr les tag parentheses
        string = re.sub('([\(](?![0-9]{4}).{1,7}[\)])',' [COLOR coral]\\1[/COLOR] ', string)
        #pr les series
        string = self.FormatSerie(string)
        string = re.sub('(?i)(.*) ((?:[S|E][0-9\.\-\_]+){1,2})','\\1 [COLOR coral]\\2[/COLOR] ', string)

        #vire doubles espaces
        string = re.sub(' +',' ',string)

        return string

    def unescape(self,text):
        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text # leave as is
        return re.sub("&#?\w+;", fixup, text)


    def CleanName(self,name):
        #vire accent et '\'
        try:
            name = unicode(name, 'utf-8')#converti en unicode pour aider aux convertions
        except:
            pass
        name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("unicode_escape")
        name = name.encode("utf-8") #on repasse en utf-8

        #on cherche l'annee
        annee = ''
        m = re.search('(\([0-9]{4}\))', name)
        if m:
            annee = str(m.group(0))
            name = name.replace(annee,'')

        #vire tag
        name = re.sub('[\(\[].+?[\)\]]','', name)
        #les apostrohes remplacer par des espaces
        name = name.replace("'", " ")
        #vire caractere special
        #name = re.sub("[^a-zA-Z0-9 ]", "",name)
        #Modif du 15/12 caractere special
        name = re.sub("[^a-zA-Z0-9 : -]", "",name)
        #tout en minuscule
        name = name.lower()
        #vire espace double
        name = re.sub(' +',' ',name)

        #vire espace a la fin
        if name.endswith(' '):
            name = name[:-1]

        #on remet l'annee
        if annee:
            name = name + ' ' + annee

        return name

    def FormatSerie(self, string):

        # vire doubles espaces
        string = re.sub(' +', ' ', string)

        # vire espace a la fin
        if string.endswith(' '):
            string = string[:-1]

        # vire espace au debut
        if string.startswith(' '):
            string = string[1:]

        SXEX = ''
        m = re.search('(?i)(\wpisode ([0-9\.\-\_]+))', string, re.UNICODE)
        if m:
            # ok y a des episodes
            string = string.replace(m.group(1), '')
            # SXEX + '%02d' % int(m.group(2))
            SXEX = m.group(2)
            if len(SXEX) < 2:
                SXEX = '0' + SXEX
            SXEX = 'E' + SXEX

            # pr les saisons
            m = re.search('(?i)(s(?:aison )*([0-9]+))', string)
            if m:
                string = string.replace(m.group(1), '')
                SXEX = 'S' + '%02d' % int(m.group(2)) + SXEX
            string = string + ' ' + SXEX

        else:
            # pas d'episode mais y a t il des saisons ?
            m = re.search('(?i)(s(?:aison )*([0-9]+))(?:$| )', string)
            if m:
                string = string.replace(m.group(1), '')
                SXEX = 'S' + '%02d' % int(m.group(2))

                string = string + ' ' + SXEX

        # reconvertion utf-8
        return string.encode('utf-8')

    def EvalJSString(self,s):
        s = s.replace(' ','')
        try:
            s = s.replace('!+[]','1').replace('!![]','1').replace('[]','0')
            s = re.sub(r'(\([^()]+)\+\[\]\)','(\\1)*10)',s)  # si le bloc fini par +[] >> *10
            s = re.sub(r'\[([^\]]+)\]','str(\\1)',s)
            # s = s.replace('[','(').replace(']',')')
            if s[0]=='+':
                s = s[1:]
            val = int(eval(s))
            return val
        except:
            return 0

class cPacker():
    def detect(self, source):
        """Detects whether `source` is P.A.C.K.E.R. coded."""
        return source.replace(' ', '').startswith('eval(function(p,a,c,k,e,')

    def unpack(self, source):
        """Unpacks P.A.C.K.E.R. packed js code."""
        payload, symtab, radix, count = self._filterargs(source)
        
        #correction pour eviter bypass
        if (len(symtab) > count) and (count > 0):
            del symtab[count:]
        if (len(symtab) < count) and (count > 0):
            symtab.append('BUGGED')   

        if count != len(symtab):
            raise UnpackingError('Malformed p.a.c.k.e.r. symtab.')
        
        try:
            unbase = Unbaser(radix)
        except TypeError:
            raise UnpackingError('Unknown p.a.c.k.e.r. encoding.')

        def lookup(match):
            """Look up symbols in the synthetic symtab."""
            word  = match.group(0)
            return symtab[unbase(word)] or word

        source = re.sub(r'\b\w+\b', lookup, payload)
        return self._replacestrings(source)

    def _cleanstr(self, str):
        str = str.strip()
        if str.find("function") == 0:
            pattern = (r"=\"([^\"]+).*}\s*\((\d+)\)")
            args = re.search(pattern, str, re.DOTALL)
            if args:
                a = args.groups()
                def openload_re(match):
                    c = match.group(0)
                    b = ord(c) + int(a[1])
                    return chr(b if (90 if c <= "Z" else 122) >= b else b - 26)

                str = re.sub(r"[a-zA-Z]", openload_re, a[0]);
                str = urllib2.unquote(str)

        elif str.find("decodeURIComponent") == 0:
            str = re.sub(r"(^decodeURIComponent\s*\(\s*('|\"))|(('|\")\s*\)$)", "", str);
            str = urllib2.unquote(str)
        elif str.find("\"") == 0:
            str = re.sub(r"(^\")|(\"$)|(\".*?\")", "", str);
        elif str.find("'") == 0:
            str = re.sub(r"(^')|('$)|('.*?')", "", str);

        return str

    def _filterargs(self, source):
        """Juice from a source file the four args needed by decoder."""
        
        source = source.replace(',[],',',0,')

        juicer = (r"}\s*\(\s*(.*?)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*\((.*?)\).split\((.*?)\)")
        args = re.search(juicer, source, re.DOTALL)
        if args:
            a = args.groups()
            try:
                return self._cleanstr(a[0]), self._cleanstr(a[3]).split(self._cleanstr(a[4])), int(a[1]), int(a[2])
            except ValueError:
                raise UnpackingError('Corrupted p.a.c.k.e.r. data.')

        juicer = (r"}\('(.*)', *(\d+), *(\d+), *'(.*)'\.split\('(.*?)'\)")
        args = re.search(juicer, source, re.DOTALL)
        if args:
            a = args.groups()
            try:
                return a[0], a[3].split(a[4]), int(a[1]), int(a[2])
            except ValueError:
                raise UnpackingError('Corrupted p.a.c.k.e.r. data.')

        # could not find a satisfying regex
        raise UnpackingError('Could not make sense of p.a.c.k.e.r data (unexpected code structure)')



    def _replacestrings(self, source):
        """Strip string lookup table (list) and replace values in source."""
        match = re.search(r'var *(_\w+)\=\["(.*?)"\];', source, re.DOTALL)

        if match:
            varname, strings = match.groups()
            startpoint = len(match.group(0))
            lookup = strings.split('","')
            variable = '%s[%%d]' % varname
            for index, value in enumerate(lookup):
                source = source.replace(variable % index, '"%s"' % value)
            return source[startpoint:]
        return source
        
def UnpackingError(Exception):
    #Badly packed source or general error.#
    #xbmc.log(str(Exception))
    print (Exception)
    pass


class Unbaser(object):
    """Functor for a given base. Will efficiently convert
    strings to natural numbers."""
    ALPHABET = {
        62: '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        95: (' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'
             '[\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
    }

    def __init__(self, base):
        self.base = base
        
        #Error not possible, use 36 by defaut
        if base == 0 :
            base = 36
        
        # If base can be handled by int() builtin, let it do it for us
        if 2 <= base <= 36:
            self.unbase = lambda string: int(string, base)
        else:
            if base < 62:
                self.ALPHABET[base] = self.ALPHABET[62][0:base]
            elif 62 < base < 95:
                self.ALPHABET[base] = self.ALPHABET[95][0:base]
            # Build conversion dictionary cache
            try:
                self.dictionary = dict((cipher, index) for index, cipher in enumerate(self.ALPHABET[base]))
            except KeyError:
                raise TypeError('Unsupported base encoding.')

            self.unbase = self._dictunbaser

    def __call__(self, string):
        return self.unbase(string)

    def _dictunbaser(self, string):
        """Decodes a  value to an integer."""
        ret = 0
        
        for index, cipher in enumerate(string[::-1]):
            ret += (self.base ** index) * self.dictionary[cipher]
        return ret

class JSUnfuck(object):
    numbers = None
    words = {
        "(![]+[])": "false",
        "([]+{})": "[object Object]",
        "(!![]+[])": "true",
        "([][[]]+[])": "undefined",
        "(+{}+[])": "NaN",
        "([![]]+[][[]])": "falseundefined",
        "([][f+i+l+t+e+r]+[])": "function filter() { [native code] }",
        "(!![]+[][f+i+l+t+e+r])": "truefunction filter() { [native code] }",
        "(+![]+([]+[])[c+o+n+s+t+r+u+c+t+o+r])": "0function String() { [native code] }",
        "(+![]+[![]]+([]+[])[c+o+n+s+t+r+u+c+t+o+r])": "0falsefunction String() { [native code] }",
        "([]+[][s+o+r+t][c+o+n+s+t+r+u+c+t+o+r](r+e+t+u+r+n+ +l+o+c+a+t+i+o+n)())": "https://123movies.to",
        "([]+[])[f+o+n+t+c+o+l+o+r]()": '<font color="undefined"></font>',
        "(+(+!![]+e+1+0+0+0)+[])": "Infinity",
        "(+[![]]+[][f+i+l+t+e+r])": 'NaNfunction filter() { [native code] }',
        '(+[![]]+[+(+!+[]+(!+[]+[])[3]+[1]+[0]+[0]+[0])])': 'NaNInfinity',
        '([]+[])[i+t+a+l+i+c+s]()': '<i></i>',
        '[[]][c+o+n+c+a+t]([[]])+[]': ',',
        '([][f+i+l+l]+[])': 'function fill() {    [native code]}',
        '(!![]+[][f+i+l+l])': 'truefunction fill() {    [native code]}',
        '((+[])[c+o+n+s+t+r+u+c+t+o+r]+[])': 'function Number() {[native code]}  _display:45:1',
        '(+(+!+[]+[1]+e+[2]+[0])+[])': '1.1e+21',
        '([]+[])[c+o+n+s+t+r+u+c+t+o+r][n+a+m+e]': 'S+t+r+i+n+g',
        '([][e+n+t+r+i+e+s]()+[])': '[object Array Iterator]',
        '([]+[])[l+i+n+k](")': '<a href="&quot;"></a>',
        '(![]+[0])[i+t+a+l+i+c+s]()': '<i>false0</i>',
		# dummy to force array dereference
        'DUMMY1': '6p',
        'DUMMY2': '2x',
        'DUMMY3': '%3C',
        'DUMMY4': '%5B',
        'DUMMY5': '6q',
        'DUMMY6': '4h',
		# add rgy
        '([][+[]]+[])[!+[]+!![]+!![]+!![]+!![]]': 'i',
        '(+{}+[])[+!![]]': 'a',	
    }
    
    uniqs = {
        '[t+o+S+t+r+i+n+g]': 1,
        '[][f+i+l+t+e+r][c+o+n+s+t+r+u+c+t+o+r](r+e+t+u+r+n+ +e+s+c+a+p+e)()': 2,
        '[][f+i+l+t+e+r][c+o+n+s+t+r+u+c+t+o+r](r+e+t+u+r+n+ +u+n+e+s+c+a+p+e)()': 3,
        '[][s+o+r+t][c+o+n+s+t+r+u+c+t+o+r](r+e+t+u+r+n+ +e+s+c+a+p+e)()': 2,
        '[][s+o+r+t][c+o+n+s+t+r+u+c+t+o+r](r+e+t+u+r+n+ +u+n+e+s+c+a+p+e)()': 3,
    }
    
    def __init__(self, js):
        self.js = js
        
    def decode(self, replace_plus=True):
        while True:
            start_js = self.js
            printDBG('1:'+self.js)
            self.repl_words(self.words)
            printDBG('2:'+self.js)            
            self.repl_numbers()
            printDBG('3:'+self.js)           
            self.repl_arrays(self.words)
            printDBG('4:'+self.js)            
            self.repl_uniqs(self.uniqs)
            if start_js == self.js:
                break
        printDBG('5:'+self.js)      
        if replace_plus:
            self.js = self.js.replace('+', '')
        self.js = re.sub('\[[A-Za-z]*\]', '', self.js)
        self.js = re.sub('\[(\d+)\]', '\\1', self.js)
        printDBG('6:'+self.js)          
        #foutu ici pr le moment
        self.js = self.js.replace('(+)','0')
        self.js = self.js.replace('(+!!)','1')
        printDBG('7:'+self.js)          
        return self.js
    
    def repl_words(self, words):
        while True:
            start_js = self.js
            for key, value in sorted(words.items(), key=lambda x: len(x[0]), reverse=True):
                self.js = self.js.replace(key, value)
    
            if self.js == start_js:
                break
    
    def repl_arrays(self, words):
        for word in sorted(words.values(), key=lambda x: len(x), reverse=True):
            for index in range(0, 100):
                try:
                    repl = word[index]
                    self.js = self.js.replace('%s[%d]' % (word, index), repl)
                except:
                    pass
        
    def repl_numbers(self):
        if self.numbers is None:
            self.numbers = self.__gen_numbers()
            
        while True:
            start_js = self.js
            for key, value in sorted(self.numbers.items(), key=lambda x: len(x[0]), reverse=True):
                self.js = self.js.replace(key, value)
    
            if self.js == start_js:
                break
        
    def repl_uniqs(self, uniqs):
        for key, value in uniqs.items():
            if key in self.js:
                if value == 1:
                    self.__handle_tostring()
                elif value == 2:
                    self.__handle_escape(key)
                elif value == 3:
                    self.__handle_unescape(key)
                                                
    def __handle_tostring(self):
        for match in re.finditer('(\d+)\[t\+o\+S\+t\+r\+i\+n\+g\](\d+)', self.js):
            repl = to_base(match.group(1), match.group(2))
            self.js = self.js.replace(match.group(0), repl)
    
    def __handle_escape(self, key):
        while True:
            start_js = self.js
            offset = self.js.find(key) + len(key)
            if self.js[offset] == '(' and self.js[offset + 2] == ')':
                c = self.js[offset + 1]
                self.js = self.js.replace('%s(%s)' % (key, c), urllib.quote(c))
            
            if start_js == self.js:
                break
    
    def __handle_unescape(self, key):
        start = 0
        while True:
            start_js = self.js
            offset = self.js.find(key, start)
            if offset == -1: break
            
            offset += len(key)
            expr = ''
            extra = ''
            last_c = self.js[offset - 1]
            abort = False
            for i, c in enumerate(self.js[offset:]):
                extra += c
                if c == ')':
                    break
                elif (i > 0 and c == '(') or (c == '[' and last_c != '+'):
                    abort = True
                    break
                elif c == '%' or c in string.hexdigits:
                    expr += c
                last_c = c
                 
            if not abort:
                self.js = self.js.replace(key + extra, urllib.unquote(expr))
            
                if start_js == self.js:
                    break
            else:
                start = offset
        
    def __gen_numbers(self):
        n = {'(+[]+[])': '0', '(+![]+([]+[]))': '0', '[+[]]': '[0]',
             '(+!![]+[])': '1', '[+!+[]]': '[1]', '[+!![]]': '[1]', 
             '[+!+[]+[+[]]]': '[10]', '+(1+1)': '11', '(+20)': '20'}
        
        for i in range(2, 20):
            key = '+!![]' * (i - 1)
            key = '!+[]' + key
            n['(' + key + ')'] = str(i)
            key += '+[]'
            n['(' + key + ')'] = str(i)
            n['[' + key + ']'] = '[' + str(i) + ']'
     
        for i in range(2, 10):
            key = '!+[]+' * (i - 1) + '!+[]'
            n['(' + key + ')'] = str(i)
            n['[' + key + ']'] = '[' + str(i) + ']'
             
            key = '!+[]' + '+!![]' * (i - 1)
            n['[' + key + ']'] = '[' + str(i) + ']'
                
        for i in range(0, 10):
            key = '(+(+!+[]+[%d]))' % (i)
            n[key] = str(i + 10)
            key = '[+!+[]+[%s]]' % (i)
            n[key] = '[' + str(i + 10) + ']'
            
        for tens in range(2, 10):
            for ones in range(0, 10):
                key = '!+[]+' * (tens) + '[%d]' % (ones)
                n['(' + key + ')'] = str(tens * 10 + ones)
                n['[' + key + ']'] = '[' + str(tens * 10 + ones) + ']'
        
        for hundreds in range(1, 10):
            for tens in range(0, 10):
                for ones in range(0, 10):
                    key = '+!+[]' * hundreds + '+[%d]+[%d]))' % (tens, ones)
                    if hundreds > 1: key = key[1:]
                    key = '(+(' + key
                    n[key] = str(hundreds * 100 + tens * 10 + ones)
        return n
    
def to_base(n, base, digits="0123456789abcdefghijklmnopqrstuvwxyz"):
    n, base = int(n), int(base)
    if n < base:
        return digits[n]
    else:
        return to_base(n // base, base, digits).lstrip(digits[0]) + digits[n % base]

class JJDecoder(object):

	def __init__(self, jj_encoded_data):
		self.encoded_str = jj_encoded_data

		
	def clean(self):
		return re.sub('^\s+|\s+$', '', self.encoded_str)

		
	def checkPalindrome(self, Str):
		startpos = -1
		endpos = -1
		gv, gvl = -1, -1

		index = Str.find('"\'\\"+\'+",')

		if index == 0:
			startpos = Str.find('$$+"\\""+') + 8
			endpos = Str.find('"\\"")())()')
			gv = Str[Str.find('"\'\\"+\'+",')+9:Str.find('=~[]')]
			gvl = len(gv)
		else:
			gv = Str[0:Str.find('=')]
			gvl = len(gv)
			startpos = Str.find('"\\""+') + 5
			endpos = Str.find('"\\"")())()')

		return (startpos, endpos, gv, gvl)

		
	def decode(self):
		
		self.encoded_str = self.clean()
		startpos, endpos, gv, gvl = self.checkPalindrome(self.encoded_str)

		if startpos == endpos:
			raise Exception('No data!')

		data = self.encoded_str[startpos:endpos]

		b = ['___+', '__$+', '_$_+', '_$$+', '$__+', '$_$+', '$$_+', '$$$+', '$___+', '$__$+', '$_$_+', '$_$$+', '$$__+', '$$_$+', '$$$_+', '$$$$+']

		str_l = '(![]+"")[' + gv + '._$_]+'
		str_o 	= gv + '._$+'
		str_t = gv + '.__+'
		str_u = gv + '._+'
		
		str_hex = gv + '.'

		str_s = '"'
		gvsig = gv + '.'

		str_quote = '\\\\\\"'
		str_slash = '\\\\\\\\'

		str_lower = '\\\\"+'
		str_upper = '\\\\"+' + gv + '._+'

		str_end	= '"+'

		out = ''
		while data != '':
			# l o t u
			if data.find(str_l) == 0:
				data = data[len(str_l):]
				out += 'l'
				continue
			elif data.find(str_o) == 0:
				data = data[len(str_o):]
				out += 'o'
				continue
			elif data.find(str_t) == 0:
				data = data[len(str_t):]
				out += 't'
				continue
			elif data.find(str_u) == 0:
				data = data[len(str_u):]
				out += 'u'
				continue

			# 0123456789abcdef
			if data.find(str_hex) == 0:
				data = data[len(str_hex):]
				
				for i in range(len(b)):
					if data.find(b[i]) == 0:
						data = data[len(b[i]):]
						out += '%x' % i
						break
				continue

			# start of s block
			if data.find(str_s) == 0:
				data = data[len(str_s):]

				# check if "R
				if data.find(str_upper) == 0: # r4 n >= 128
					data = data[len(str_upper):] # skip sig
					ch_str = ''
					for i in range(2): # shouldn't be more than 2 hex chars
						# gv + "."+b[ c ]
						if data.find(gvsig) == 0:
							data = data[len(gvsig):]
							for k in range(len(b)): # for every entry in b
								if data.find(b[k]) == 0:
									data = data[len(b[k]):]
									ch_str = '%x' % k
									break
						else:
							break

					out += chr(int(ch_str, 16))
					continue

				elif data.find(str_lower) == 0: # r3 check if "R // n < 128
					data = data[len(str_lower):] # skip sig
					
					ch_str = ''
					ch_lotux = ''
					temp = ''
					b_checkR1 = 0
					for j in range(3): # shouldn't be more than 3 octal chars
						if j > 1: # lotu check
							if data.find(str_l) == 0:
								data = data[len(str_l):]
								ch_lotux = 'l'
								break
							elif data.find(str_o) == 0:
								data = data[len(str_o):]
								ch_lotux = 'o'
								break
							elif data.find(str_t) == 0:
								data = data[len(str_t):]
								ch_lotux = 't'
								break
							elif data.find(str_u) == 0:
								data = data[len(str_u):]
								ch_lotux = 'u'
								break

						# gv + "."+b[ c ]
						if data.find(gvsig) == 0:
							temp = data[len(gvsig):]
							for k in range(8): # for every entry in b octal
								if temp.find(b[k]) == 0:
									if int(ch_str + str(k), 8) > 128:
										b_checkR1 = 1
										break

									ch_str += str(k)
									data = data[len(gvsig):] # skip gvsig
									data = data[len(b[k]):]
									break

							if b_checkR1 == 1:
								if data.find(str_hex) == 0: # 0123456789abcdef
									data = data[len(str_hex):]
									# check every element of hex decode string for a match
									for i in range(len(b)):
										if data.find(b[i]) == 0:
											data = data[len(b[i]):]
											ch_lotux = '%x' % i
											break
									break
						else:
							break

					out += chr(int(ch_str,8)) + ch_lotux
					continue

				else: # "S ----> "SR or "S+
					# if there is, loop s until R 0r +
					# if there is no matching s block, throw error
					
					match = 0;
					n = None

					# searching for matching pure s block
					while True:
						n = ord(data[0])
						if data.find(str_quote) == 0:
							data = data[len(str_quote):]
							out += '"'
							match += 1
							continue
						elif data.find(str_slash) == 0:
							data = data[len(str_slash):]
							out += '\\'
							match += 1
							continue
						elif data.find(str_end) == 0: # reached end off S block ? +
							if match == 0:
								raise '+ no match S block: ' + data
							data = data[len(str_end):]
							break # step out of the while loop
						elif data.find(str_upper) == 0: # r4 reached end off S block ? - check if "R n >= 128
							if match == 0:
								raise 'no match S block n>128: ' + data
							data = data[len(str_upper):] # skip sig
							
							ch_str = ''
							ch_lotux = ''

							for j in range(10): # shouldn't be more than 10 hex chars
								if j > 1: # lotu check
									if data.find(str_l) == 0:
										data = data[len(str_l):]
										ch_lotux = 'l'
										break
									elif data.find(str_o) == 0:
										data = data[len(str_o):]
										ch_lotux = 'o'
										break
									elif data.find(str_t) == 0:
										data = data[len(str_t):]
										ch_lotux = 't'
										break
									elif data.find(str_u) == 0:
										data = data[len(str_u):]
										ch_lotux = 'u'
										break

								# gv + "."+b[ c ]
								if data.find(gvsig) == 0:
									data = data[len(gvsig):] # skip gvsig
									for k in range(len(b)): # for every entry in b
										if data.find(b[k]) == 0:
											data = data[len(b[k]):]
											ch_str += '%x' % k
											break
								else:
									break # done
							out += chr(int(ch_str, 16))
							break # step out of the while loop
						elif data.find(str_lower) == 0: # r3 check if "R // n < 128
							if match == 0:
								raise 'no match S block n<128: ' + data

							data = data[len(str_lower):] # skip sig

							ch_str = ''
							ch_lotux = ''
							temp = ''
							b_checkR1 = 0

							for j in range(3): # shouldn't be more than 3 octal chars
								if j > 1: # lotu check
									if data.find(str_l) == 0:
										data = data[len(str_l):]
										ch_lotux = 'l'
										break
									elif data.find(str_o) == 0:
										data = data[len(str_o):]
										ch_lotux = 'o'
										break
									elif data.find(str_t) == 0:
										data = data[len(str_t):]
										ch_lotux = 't'
										break
									elif data.find(str_u) == 0:
										data = data[len(str_u):]
										ch_lotux = 'u'
										break

								# gv + "."+b[ c ]
								if data.find(gvsig) == 0:
									temp = data[len(gvsig):]
									for k in range(8): # for every entry in b octal
										if temp.find(b[k]) == 0:
											if int(ch_str + str(k), 8) > 128:
												b_checkR1 = 1
												break

											ch_str += str(k)
											data = data[len(gvsig):] # skip gvsig
											data = data[len(b[k]):]
											break

									if b_checkR1 == 1:
										if data.find(str_hex) == 0: # 0123456789abcdef
											data = data[len(str_hex):]
											# check every element of hex decode string for a match
											for i in range(len(b)):
												if data.find(b[i]) == 0:
													data = data[len(b[i]):]
													ch_lotux = '%x' % i
													break
								else:
									break
							out += chr(int(ch_str, 8)) + ch_lotux
							break # step out of the while loop
						elif (0x21 <= n and n <= 0x2f) or (0x3A <= n and n <= 0x40) or ( 0x5b <= n and n <= 0x60 ) or ( 0x7b <= n and n <= 0x7f ):
							out += data[0]
							data = data[1:]
							match += 1
					continue
			print ('No match : ' + data)
			break
		return out

class AADecoder(object):
    def __init__(self, aa_encoded_data):
        self.encoded_str = aa_encoded_data.replace('/*´∇｀*/','')

        self.b = ["(c^_^o)", "(ﾟΘﾟ)", "((o^_^o) - (ﾟΘﾟ))", "(o^_^o)",
                  "(ﾟｰﾟ)", "((ﾟｰﾟ) + (ﾟΘﾟ))", "((o^_^o) +(o^_^o))", "((ﾟｰﾟ) + (o^_^o))",
                  "((ﾟｰﾟ) + (ﾟｰﾟ))", "((ﾟｰﾟ) + (ﾟｰﾟ) + (ﾟΘﾟ))", "(ﾟДﾟ) .ﾟωﾟﾉ", "(ﾟДﾟ) .ﾟΘﾟﾉ",
                  "(ﾟДﾟ) ['c']", "(ﾟДﾟ) .ﾟｰﾟﾉ", "(ﾟДﾟ) .ﾟДﾟﾉ", "(ﾟДﾟ) [ﾟΘﾟ]"]

    def is_aaencoded(self):
        idx = self.encoded_str.find("ﾟωﾟﾉ= /｀ｍ´）ﾉ ~┻━┻   //*´∇｀*/ ['_']; o=(ﾟｰﾟ)  =_=3; c=(ﾟΘﾟ) =(ﾟｰﾟ)-(ﾟｰﾟ); ")
        if idx == -1:
            return False

        if self.encoded_str.find("(ﾟДﾟ)[ﾟoﾟ]) (ﾟΘﾟ)) ('_');", idx) == -1:
            return False

        return True

    def base_repr(self, number, base=2, padding=0):
        digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if base > len(digits):
            base = len(digits)

        num = abs(number)
        res = []
        while num:
            res.append(digits[num % base])
            num //= base
        if padding:
            res.append('0' * padding)
        if number < 0:
            res.append('-')
        return ''.join(reversed(res or '0'))

    def decode_char(self, enc_char, radix):
        end_char = "+ "
        str_char = ""
        while enc_char != '':
            found = False
            
            for i in range(len(self.b)):
                if enc_char.find(self.b[i]) == 0:
                    str_char += self.base_repr(i, radix)
                    enc_char = enc_char[len(self.b[i]):]
                    found = True
                    break

            if not found:
                for i in range(len(self.b)):             
                    enc_char=enc_char.replace(self.b[i], str(i))
                
                startpos=0
                findClose=True
                balance=1
                result=[]
                if enc_char.startswith('('):
                    l=0
                    
                    for t in enc_char[1:]:
                        l+=1
                        if findClose and t==')':
                            balance-=1;
                            if balance==0:
                                result+=[enc_char[startpos:l+1]]
                                findClose=False
                                continue
                        elif not findClose and t=='(':
                            startpos=l
                            findClose=True
                            balance=1
                            continue
                        elif t=='(':
                            balance+=1
                 

                if result is None or len(result)==0:
                    return ""
                else:
                    
                    for r in result:
                        value = self.decode_digit(r, radix)
                        if value == "":
                            return ""
                        else:
                            str_char += value
                            
                    return str_char

            enc_char = enc_char[len(end_char):]

        return str_char

        
              
    def decode_digit(self, enc_int, radix):

        #enc_int=enc_int.replace('(ﾟΘﾟ)','1').replace('(ﾟｰﾟ)','4').replace('(c^_^o)','0').replace('(o^_^o)','3')  

        rr = '(\(.+?\)\))\+'
        rerr=enc_int.split('))+')
        v = ''
        
        #new mode
        if (True):

            for c in rerr:
                
                if len(c)>0:
                    if c.strip().endswith('+'):
                        c=c.strip()[:-1]

                    startbrackets=len(c)-len(c.replace('(',''))
                    endbrackets=len(c)-len(c.replace(')',''))
                    
                    if startbrackets>endbrackets:
                        c+=')'*startbrackets-endbrackets
                    
                    #fh = open('c:\\test.txt', "w")
                    #fh.write(c)
                    #fh.close()
                    
                    c = c.replace('!+[]','1')
                    c = c.replace('-~','1+')
                    c = c.replace('[]','0')
                    
                    v+=str(eval(c))
                    
            return v
         
        # mode 0=+, 1=-
        mode = 0
        value = 0

        while enc_int != '':
            found = False
            for i in range(len(self.b)):
                if enc_int.find(self.b[i]) == 0:
                    if mode == 0:
                        value += i
                    else:
                        value -= i
                    enc_int = enc_int[len(self.b[i]):]
                    found = True
                    break

            if not found:
                return ""

            enc_int = re.sub('^\s+|\s+$', '', enc_int)
            if enc_int.find("+") == 0:
                mode = 0
            else:
                mode = 1

            enc_int = enc_int[1:]
            enc_int = re.sub('^\s+|\s+$', '', enc_int)

        return self.base_repr(value, radix)

    def decode(self):

        self.encoded_str = re.sub('^\s+|\s+$', '', self.encoded_str)

        # get data
        pattern = (r"\(ﾟДﾟ\)\[ﾟoﾟ\]\+ *(.+?)\(ﾟДﾟ\)\[ﾟoﾟ\]\)")
        result = re.search(pattern, self.encoded_str, re.DOTALL)
        if result is None:
            print ("AADecoder: data not found")
            return False

        data = result.group(1)

        # hex decode string
        begin_char = "(ﾟДﾟ)[ﾟεﾟ]+"
        alt_char = "(oﾟｰﾟo)+ "

        out = ''

        while data != '':
            # Check new char
            if data.find(begin_char) != 0:
                print ("AADecoder: data not found")
                return False

            data = data[len(begin_char):]

            # Find encoded char
            enc_char = ""
            if data.find(begin_char) == -1:
                enc_char = data
                data = ""
            else:
                enc_char = data[:data.find(begin_char)]
                data = data[len(enc_char):]

            
            radix = 8
            # Detect radix 16 for utf8 char
            if enc_char.find(alt_char) == 0:
                enc_char = enc_char[len(alt_char):]
                radix = 16

            str_char = self.decode_char(enc_char, radix)
            
            if str_char == "":
                print ("no match :  ")
                print  (data + "\nout = " + out + "\n")
                return False
            
            out += chr(int(str_char, radix))

        if out == "":
            print ("no match : " + data)
            return False

        return out

#version 2 si l'autre fonctionne pas.
#https://github.com/alfa-addon/addon/blob/master/plugin.video.alfa/lib/aadecode.py
# ------------------------------------------------------------
# Modified by jsergio
#
def decodeAA(text):
    text = re.sub(r"\s+|/\*.*?\*/", "", text)
    data = text.split("+(ﾟДﾟ)[ﾟoﾟ]")[1]
    chars = data.split("+(ﾟДﾟ)[ﾟεﾟ]+")[1:]

    txt = ""
    for char in chars:
        char = char \
            .replace("(oﾟｰﾟo)", "u") \
            .replace("c", "0") \
            .replace("(ﾟДﾟ)['0']", "c") \
            .replace("ﾟΘﾟ", "1") \
            .replace("!+[]", "1") \
            .replace("-~", "1+") \
            .replace("o", "3") \
            .replace("_", "3") \
            .replace("ﾟｰﾟ", "4") \
            .replace("(+", "(")
        char = re.sub(r'\((\d)\)', r'\1', char)

        c = "";
        subchar = ""
        for v in char:
            c += v
            try:
                x = c; subchar += str(eval(x)); c = ""
            except:
                pass
        if subchar != '': txt += subchar + "|"
    txt = txt[:-1].replace('+', '')

    txt_result = "".join([chr(int(n, 8)) for n in txt.split('|')])

    return toStringCases(txt_result)


def toStringCases(txt_result):
    sum_base = ""
    m3 = False
    if ".toString(" in txt_result:
        if "+(" in txt_result:
            m3 = True
            try: sum_base = "+" + re.search(".toString...(\d+).", txt_result, re.DOTALL).groups(1)
            except: sum_base = ""
            txt_pre_temp = re.findall("..(\d),(\d+).", txt_result, re.DOTALL)
            txt_temp = [(n, b) for b, n in txt_pre_temp]
        else:
            txt_temp = re.findall('(\d+)\.0.\w+.([^\)]+).', txt_result, re.DOTALL)
        for numero, base in txt_temp:
            code = toString(int(numero), eval(base + sum_base))
            if m3:
                txt_result = re.sub(r'"|\+', '', txt_result.replace("(" + base + "," + numero + ")", code))
            else:
                txt_result = re.sub(r"'|\+", '', txt_result.replace(numero + ".0.toString(" + base + ")", code))
    return txt_result


def toString(number, base):
    string = "0123456789abcdefghijklmnopqrstuvwxyz"
    if number < base:
        return string[number]
    else:
        return toString(number // base, base) + string[number % base]


def Unquote(sUrl):
    return urllib.unquote(sUrl)

def Quote(sUrl):
    return urllib.quote(sUrl)

def UnquotePlus(sUrl):
    return urllib.unquote_plus(sUrl)

def QuotePlus(sUrl):
    return urllib.quote_plus(sUrl)

def QuoteSafe(sUrl):
    return urllib.quote(sUrl,safe=':/?=')
    
def urlEncode(sUrl):
    return urllib.urlencode(sUrl)
    
def Noredirection():
    class NoRedirection(urllib2.HTTPErrorProcessor):
        def http_response(self, request, response):
            return response

        https_response = http_response

    opener = urllib2.build_opener(NoRedirection)
    return opener
    
class cMultiup:
    def __init__(self):
        self.id = ''
        self.list = []

    def GetUrls(self, url):
        return False