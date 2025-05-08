import time,os
import os.path
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import GetCacheSubDir
def getInfoLabel(txt):
    if txt == 'system.buildversion': return '18'
    else: return '0'

def getCondVisibility(txt):
    return True    
    
   
def sleep(int_):
    time.sleep(int_/float(1000))
    
def executebuiltin(int_):
    pass

class Keyboard():
    def __init__(self,sDefaultText):
        self.MyPath = GetCacheSubDir('Tsiplayer')
        pass

    def setHeading(self,heading):
        pass
        
    def doModal(self):
        pass

    def isConfirmed(self):
        return True       

    def getText(self): 
        txt_def = ''
        if os.path.isfile(self.MyPath +'searchSTR'):
            with open(self.MyPath + 'searchSTR','r') as f:
                txt_def = f.read().strip()
        return txt_def