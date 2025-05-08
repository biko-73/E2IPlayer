import os.path
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import GetCacheSubDir
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG

def translatePath(path):
    path = path.replace('special://home/addons/plugin.video.matrix/resources/sites','/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/matrix/resources/sites')
    path = path.replace('special://home/addons/plugin.video.matrix/resources/extra','/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/matrix/resources/extra')
    path = path.replace('special://home/userdata/addon_data/plugin.video.matrix/',GetCacheSubDir('Tsiplayer'))
    path = path.replace('special://home/addons/plugin.video.vstream/resources/sites','/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/vstream/resources/sites')
    path = path.replace('special://home/addons/plugin.video.vstream/resources/extra','/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/vstream/resources/extra')
    path = path.replace('special://home/userdata/addon_data/plugin.video.vstream/',GetCacheSubDir('Tsiplayer'))    
    return path

def File(sFile,tp):
    sFile = translatePath(sFile)
    f =  open(sFile, tp)
    return f

def exists(path):
    return os.path.exists(translatePath(path))
      
def listdir(basepath):
    basepath = translatePath(basepath)
    list_dirs  = []
    list_files = []
    for fname in os.listdir(basepath):
        path = os.path.join(basepath, fname)
        if os.path.isdir(path):
            list_dirs.append(fname)
        else:
            list_files.append(fname)
    printDBG('lst_dir='+str(list_dirs))
    printDBG('lst_files='+str(list_files))
    return list_dirs, list_files    

