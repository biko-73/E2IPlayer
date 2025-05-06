#-*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
import sys

try:
    import urllib2
    import urllib
    from contextlib import closing
except ImportError:
    import urllib.request as urllib2
    import urllib.parse as urllib
  
def IsPython3():
    if sys.version_info[0] < 3:
        return False
    else:
        return True

def Unquote(sUrl):
    return urllib.unquote(sUrl)

def Quote(sUrl):
    return urllib.quote(sUrl)

def UnquotePlus(sUrl):
    return urllib.unquote_plus(sUrl)

def QuotePlus(sUrl):
    return urllib.quote_plus(sUrl)
    

def download_url(url, save_path):
    if IsPython3():
        with urllib2.urlopen(url) as dl_file:
            with open(save_path, 'wb') as out_file:
                out_file.write(dl_file.read())
    else:
        with closing(urllib2.urlopen(url)) as dl_file:
            with open(save_path, 'wb') as out_file:
                out_file.write(dl_file.read())

def string_escape(s, encoding='utf-8'):
    return str(s.encode().decode('unicode-escape'))
