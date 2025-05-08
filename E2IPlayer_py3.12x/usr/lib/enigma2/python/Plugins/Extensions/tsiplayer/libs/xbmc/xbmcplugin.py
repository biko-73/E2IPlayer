# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, GetCacheSubDir
import json

SORT_METHOD_NONE = 0
SORT_METHOD_EPISODE = 1

def addDirectoryItems(iHandler, listing, count=0):
    MyPath = GetCacheSubDir('Tsiplayer') + 'Matrix_listing.json'
    data = []
    tab = {}
    if (listing[-1][1].getItems().get('sId','') == 'globalSearch') and (listing[-1][1].getItems().get('sFav','') == 'DoNothing'):
        printDBG('listing_dernier='+str(listing[-1][1].getItems())) 
        titre_search = listing[-2][1].getItems()
        for elm in listing:
            sId   = elm[1].getItems().get('sId','')
            title = elm[1].getItems().get('title','')
            if 'Aucun élément' not in title:
                name  = sId.title()
                printDBG('namenamenamenamenamename='+str(name)+':'+str(title))
                count = tab.get(sId,{}).get('count',0) + 1
                tab.update( {sId : {'name':name,'count':count}} )
        data.append(titre_search)
        id_ = 1
        for sId in tab.keys():
            if sId != 'globalSearch':
                count = str(tab[sId]['count'])
                name = tab[sId]['name']
                titre  = '[COLOR yellow]%s[/COLOR]. [COLOR lightcoral]%s[/COLOR] ([COLOR violet]%s[/COLOR] items found)' % (id_, name, count)
                icon   = 'special://home/addons/plugin.video.xxxx/resources/art/sites/'+sId+'.png'
                data.append({'title':titre,'sId':sId,'sFav':'DoNothing','icon':icon})
                for elm in listing:
                    if elm[1].getItems().get('sId','')==sId:
                        data.append(elm[1].getItems())
                        printDBG('listing_='+str(elm[1].getItems())) 
                id_ = id_ +1
        if id_ == 1: data.append({'title':'[COLOR redl]No information[/COLOR]','sId':'','sFav':'DoNothing','icon':''})
    else:
        for elm in listing:
            data.append(elm[1].getItems())        
            #data = sorted(data, key=lambda d: d['sId']) 
    printDBG('data='+str(data))   
    with open(MyPath, "w") as f:
        json.dump(data, f,ensure_ascii=False)
    printDBG('end data') 
def setPluginCategory(iHandler, txt=''):
    printDBG('setPluginCategory')

def setContent(iHandler, CONTENT):
    printDBG('setContent'+str(CONTENT))

def addSortMethod(iHandler, SORT_METHOD):
    printDBG('addSortMethod')

def endOfDirectory(iHandler, succeeded=True, cacheToDisc=True):
    printDBG('endOfDirectory')