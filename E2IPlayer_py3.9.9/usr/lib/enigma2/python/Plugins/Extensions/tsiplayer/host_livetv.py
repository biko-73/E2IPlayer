# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import SetIPTVPlayerLastHostError
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,gethostname
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
import re,urllib
import base64
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.packer import cPacker
from Plugins.Extensions.IPTVPlayer.libs.urlparserhelper import getDirectM3U8Playlist
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads
import json


def getinfo():
    info_={}
    info_['name']= 'LIVE TV'
    info_['version']='1.0 08/12/2021'
    info_['dev']='RGYSoft'
    info_['cat_id']='10'
    info_['desc']='Rotana Vod'
    info_['icon']='https://i.ibb.co/dKB2VhP/c-1650978192.jpg'
    info_['recherche_all']='1'
    info_['update']='New Site'
    return info_
 
def hunter_decode(My_Var):
    #My_Var = ("loTPTBBPTlJPTloPTUUPTUTPloTPUVJPTBlPTUJPTBUPTloPTUTPTUoPTUlPTBUPTUlPloTPUloPloTPTTTPTloPUVJPTlTPTBUPUllPloTPlJTPUUlPTlUPTBVPTBBPTBUPlJTPlVlPloTPTBBPUVJPTUTPUllPloTPTTTPTloPUVJPTlTPTBUPUllPloTPlJTPUUoPTBVPTloPUVJPTBJPlJTPTTJPTTJPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPTBlPTlJPTBoPUoBPUVJPTlTPTBUPloTPUloPloTPUVJPTBlPTUJPTBUPTloPTUTPTUoPTUlPTBUPTUlPlVTPTBlPTlJPTBoPUlVPlVTPTloPUVJPTlTPTBUPUlUPloTPTBBPTlJPTloPTUUPTlJPTlUPTBUPlVTPTlUPTlJPTBoPlJoPTBlPTlJPTBoPUoBPUVJPTlTPTBUPlJJPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPTBTPTlJPTUlPTlTPUUlPTUoPTUTPTBJPUJBPTUlPTlUPloTPUloPloTPTBTPTUoPTloPTBBPTUTPTBVPTlJPTloPloTPlJoPTBlPUVJPTUTPUVJPlJJPloTPTTTPloTPTBVPTBTPloTPlJoPTUTPTTlPTlVPTBUPTlJPTBTPloTPTBlPUVJPTUTPUVJPlVTPTUUPTBBPTlJPTBlPTBUPloTPUloPUloPUloPloTPlJTPTUoPTloPTBlPTBUPTBTPTBVPTloPTBUPTBlPlJTPloTPTToPTToPloTPTUTPTTlPTlVPTBUPTlJPTBTPloTPTBlPUVJPTUTPUVJPlVTPTUTPTUUPloTPUloPUloPUloPloTPlJTPTUoPTloPTBlPTBUPTBTPTBVPTloPTBUPTBlPlJTPlJJPloTPTTTPloTPTUlPTBUPTUTPTUoPTUlPTloPloTPlJTPlJTPUlUPloTPTTJPloTPTUlPTBUPTUTPTUoPTUlPTloPloTPTUVPTBVPTloPTBlPTlJPTUVPlVTPUVJPTUTPTlJPUVVPlJoPUVJPTUoPTUTPTBJPUUTPUVJPTlUPTlUPUJBPTUlPTlUPlJJPloTPlVBPloTPlJTPUlVPTUUPTUTPTUlPTBUPUVJPTlTPUloPlJTPloTPlVBPloTPTUoPTloPTUBPTBVPTUoPTBUPUTUPTBlPloTPlVBPloTPlJTPlJUPTUUPTBBPTlJPTBlPTBUPUloPlJTPloTPlVBPloTPTBlPUVJPTUTPUVJPlVTPTUUPTBBPTlJPTBlPTBUPloTPlVBPloTPlJTPlJUPTBUPTTBPTlVPTBVPTUlPTBUPTUUPUloPlJTPloTPlVBPloTPTBlPUVJPTUTPUVJPlVTPTUTPTUUPUlUPloTPTTJPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPTBTPTlJPTUlPTBBPTBUPUToPTBVPTlUPTlUPTlVPTlUPUVJPTTlPTBUPTUlPloTPUloPloTPTBTPTUoPTloPTBBPTUTPTBVPTlJPTloPloTPlJoPlJJPloTPTTTPloTPUVJPTUoPTUTPTBJPUJBPTUlPTlUPloTPUloPloTPlJTPlJTPUlUPloTPTlVPTlUPUVJPTTlPTBUPTUlPUolPUVVPTlBPlVTPTUUPTUTPTlJPTlVPlJoPlJJPUlUPloTPTlVPTlUPUVJPTTlPTBUPTUlPUolPUVVPTlBPlVTPTUlPTBUPTlTPTlJPTUJPTBUPlJoPlJJPUlUPloTPTBBPTlUPTBUPUVJPTUlPUoVPTBVPTlTPTBUPTlJPTUoPTUTPlJoPTBlPTBUPUVJPTUoPTUTPTBJPTBBPTUlPTlJPTloPlJJPUlUPloTPUVJPTlBPTTBPUooPTBUPTUBPTUoPTBUPTUUPTUTPlVTPUVJPUVVPTlJPTUlPTUTPlJoPlJJPUlUPloTPTBVPTBTPloTPlJoPTlVPTlUPUVJPTTlPTBUPTUlPUolPUVVPTlBPlVTPTBlPTBUPTUUPTUTPTUlPTlJPTTlPlJJPloTPTTTPloTPTlVPTlUPUVJPTTlPTBUPTUlPUolPUVVPTlBPlVTPTBlPTBUPTUUPTUTPTUlPTlJPTTlPlJoPlJJPUlUPloTPTTJPloTPTBVPTBTPloTPlJoPTBlPTlJPUooPTBUPTBlPTBVPTUlPTBUPTBBPTUTPlJJPloTPTTTPloTPTUVPTBVPTloPTBlPTlJPTUVPlVTPTlUPTlJPTBBPUVJPTUTPTBVPTlJPTloPloTPUloPloTPlJTPTUTPTBUPTBBPTBJPTBVPTUUPTUUPTUoPTBUPlVTPTBJPTUTPTlTPTlUPlJTPUlUPloTPTTJPloTPTTJPUlUPloTPTlUPTBUPTUTPloTPTBlPTBUPUVJPTUoPTUTPTBJPTBBPTUlPTlJPTloPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPTBUPTloPUVJPUVVPTlUPTBUPUoUPTBUPTBUPTUlPloTPUloPloTPlVVPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPTBUPTloPUVJPUVVPTlUPTBUPUoUPTBUPTBUPTUlPUUTPUVJPTBBPTBJPTBUPloTPUloPloTPlVVPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPTBBPTBJPTBUPTBBPTllPUoUPTBUPTBUPTUlPloTPUloPloTPTlVPUBBPTlVPTlTPTlUPlVTPTBJPTlUPTUUPTlBPTUUPlVTPUUJPTloPTBoPTBVPTloPTBUPlVTPTBVPTUUPUoJPTUoPTlVPTlVPTlJPTUlPTUTPTBUPTBlPlJoPlJJPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPTBlPTlJPUooPTBUPTBlPTBVPTUlPTBUPTBBPTUTPloTPUloPloTPlVVPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPTBlPTlJPUUlPTUoPTUTPTBJPUUTPTBJPTBUPTBBPTllPloTPUloPloTPTBTPTUoPTloPTBBPTUTPTBVPTlJPTloPloTPlJoPlJJPloTPTTTPloTPTBVPTBTPloTPlJoPTBBPTBJPTBUPTBBPTllPUoUPTBUPTBUPTUlPloTPlJUPlJUPloTPUVJPTUoPTUTPTBJPUJBPTUlPTlUPloTPlooPUloPUloPloTPlJTPlJTPlJJPloTPTTTPloTPUVJPTlBPTTBPUooPTBUPTUBPTUoPTBUPTUUPTUTPloTPUloPloTPlJBPlVTPUVJPTlBPUVJPTTBPlJoPTTTPloTPTUoPTUlPTlUPUllPloTPUVJPTUoPTUTPTBJPUJBPTUlPTlUPlVlPloTPTBlPUVJPTUTPUVJPUoVPTTlPTlVPTBUPUllPloTPlJTPTlBPTUUPTlJPTloPlJTPlVlPloTPTUTPTBVPTlTPTBUPTlJPTUoPTUTPUllPloTPUBTPlVJPlVJPlVJPlVlPloTPTUUPTUoPTBBPTBBPTBUPTUUPTUUPUllPloTPTBTPTUoPTloPTBBPTUTPTBVPTlJPTloPloTPlJoPTUlPTBUPTUUPTlVPTlJPTloPTUUPTBUPlJJPloTPTTTPloTPUVJPTUoPTUTPTBJPUJBPTUlPTlUPloTPUloPloTPTBTPTlJPTUlPTlTPUUlPTUoPTUTPTBJPUJBPTUlPTlUPlJoPTUlPTBUPTUUPTlVPTlJPTloPTUUPTBUPlJJPUlUPloTPTBlPTBUPUVJPTUoPTUTPTBJPTBBPTUlPTlJPTloPloTPUloPloTPTUUPTBUPTUTPUoVPTBVPTlTPTBUPTlJPTUoPTUTPlJoPTBlPTlJPUUlPTUoPTUTPTBJPUUTPTBJPTBUPTBBPTllPlVlPloTPUBlPlVJPlVJPlVJPlVJPlVJPlJJPUlUPloTPTTJPlVlPloTPTBUPTUlPTUlPTlJPTUlPUllPloTPTBTPTUoPTloPTBBPTUTPTBVPTlJPTloPloTPlJoPlJJPloTPTTTPloTPTBVPTBTPloTPlJoPTBTPUVJPTBVPTlUPUUTPTlJPTUoPTloPTUTPloTPUlTPloTPUBBPlJJPloTPTTTPloTPTBlPTBUPUVJPTUoPTUTPTBJPTBBPTUlPTlJPTloPloTPUloPloTPTUUPTBUPTUTPUoVPTBVPTlTPTBUPTlJPTUoPTUTPlJoPTBlPTlJPUUlPTUoPTUTPTBJPUUTPTBJPTBUPTBBPTllPlVlPloTPUBTPlVJPlVJPlVJPlJJPUlUPloTPTBTPUVJPTBVPTlUPUUTPTlJPTUoPTloPTUTPlVBPlVBPUlUPloTPTTJPloTPTBUPTlUPTUUPTBUPloTPTTTPloTPTBTPTlJPTUlPTBBPTBUPUToPTBVPTlUPTlUPTlVPTlUPUVJPTTlPTBUPTUlPlJoPlJJPUlUPloTPTTJPloTPTTJPlVlPloTPTUUPTUTPUVJPTUTPTUoPTUUPUUTPTlJPTBlPTBUPUllPloTPTTTPloTPUBUPUBUPUBUPUllPloTPTBTPTUoPTloPTBBPTUTPTBVPTlJPTloPloTPlJoPlJJPloTPTTTPloTPTBTPTlJPTUlPTBBPTBUPUToPTBVPTlUPTlUPTlVPTlUPUVJPTTlPTBUPTUlPlJoPlJJPUlUPloTPTTJPlVlPloTPUBUPlVVPlVJPUllPloTPTBTPTUoPTloPTBBPTUTPTBVPTlJPTloPloTPlJoPlJJPloTPTTTPloTPTBTPTlJPTUlPTBBPTBUPUToPTBVPTlUPTlUPTlVPTlUPUVJPTTlPTBUPTUlPlJoPlJJPUlUPloTPTTJPlVlPloTPUBUPlVJPUBlPUllPloTPTBTPTUoPTloPTBBPTUTPTBVPTlJPTloPloTPlJoPlJJPloTPTTTPloTPTBTPTlJPTUlPTBBPTBUPUToPTBVPTlUPTlUPTlVPTlUPUVJPTTlPTBUPTUlPlJoPlJJPUlUPloTPTTJPloTPTTJPloTPTTJPlJJPUlUPloTPTTJPloTPTTJPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPUVJPTUoPTUTPTBJPUUTPUVJPTlUPTlUPUJBPTUlPTlUPloTPUloPloTPlJTPUVJPUTlPUooPlVJPTBBPUTlPUTVPUBoPUTJPTTlPUlBPTUlPUJJPUJTPTllPTUoPTBBPUBBPUJlPTlBPUVJPUBBPUJlPUBTPTBBPUBBPUJlPTTlPTBlPTBVPUBTPTUTPUJJPUoTPUloPUloPlJTPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPTlVPTlUPUVJPTTlPTBUPTUlPUTUPTBlPloTPUloPloTPlJTPTllPUBTPTBBPUBlPTUJPUBlPTTUPUlBPTBTPUBJPlJTPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPTUoPTloPTUBPTBVPTUoPTBUPUTUPTBlPloTPUloPloTPlJTPTBoPUBJPTBlPUlBPTUlPUBVPTlBPUBlPTTlPUBJPTBTPlVVPTlTPUlBPUVJPUBBPTUlPUBJPTUJPUBUPlJTPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPTUJPTBVPTBlPTBUPTlJPUJBPTUlPTlUPloTPUloPloTPlJTPUVJPUTlPUooPlVJPTBBPUTlPUTVPUBoPUTJPTTlPUlBPTlJPUJJPTTlPlVVPTUoPUTVPTBVPUBTPTTUPUVVPUBBPUlBPlVJPUVJPUJUPUoBPTlUPUTJPTlTPUoBPTUJPUVVPUoJPUlBPTUVPUVVPUTlPTlUPUBBPUVJPUJTPUJJPTUJPUTJPUBBPTBBPUBlPUJJPUUoPTlUPTTlPUolPUTBPTlJPTTUPTBUPUoVPTBlPTlTPUTVPUJUPlVJPUBTPUJoPUoVPUTTPTTlPUoBPUBlPUJoPlVJPUTJPUBBPUoBPTlJPTBlPUJUPUBTPTUlPUVVPUTBPTlUPTTUPTBlPUUTPUBTPTUTPUTVPUBlPUJBPUBUPlJTPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPTllPTBUPTlUPUJlPUVJPTlUPloTPUloPloTPlJTPTUUPUBoPTlUPUBlPTUJPUBJPTTlPUBoPTUoPUBUPTBlPUBTPTUJPUBUPlJTPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPTlBPTUVPUVVPUVJPTUUPTBUPTlVPUVJPTUTPTBJPloTPUloPloTPlJTPTBJPTUTPTUTPTlVPTUUPUllPlVoPlVoPTBBPTBlPTloPlVTPTlUPTBVPTUJPTBUPTlVPTlUPTTlPlVTPTlTPTBUPlVoPTUUPTBBPTUlPTBVPTlVPTUTPTUUPlVoPTlVPTlUPUVJPTTlPTBUPTUlPlVoPUBVPlVTPUBBPUBTPlVTPUBVPlVoPlJTPUlUPloTPTlUPTBUPTUTPloTPTBTPUVJPTBVPTlUPUUTPTlJPTUoPTloPTUTPloTPUloPloTPlVVPUlUPloTPTlUPTBUPTUTPloTPUVJPTlBPTTBPUooPTBUPTUBPTUoPTBUPTUUPTUTPUlUPloTPTlUPTBUPTUTPloTPUVJPTUoPTUTPTBJPUJBPTUlPTlUPloTPUloPloTPTBTPTlJPTUlPTlTPUUlPTUoPTUTPTBJPUJBPTUlPTlUPlJoPTTTPloJPTUUPTBBPTlJPTBlPTBUPloJPUllPloTPloJPlVJPTlJPlVUPTUBPTUUPTlVPUUlPUooPUoTPUTVPUoJPlVVPUUlPUUJPUBBPUlBPUBTPUTJPUTUPTllPUTVPTBoPloJPlVlPloTPloJPTUTPTUUPloJPUllPloTPlVVPUBoPUBoPlVVPUlBPUBBPUBlPUlBPUBVPUBlPTTJPlJJPUlUPloTPTBlPTlJPUUlPTUoPTUTPTBJPUUTPTBJPTBUPTBBPTllPlJoPlJJPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPTUlPUVJPTUTPTBVPTlJPloTPUloPloTPlJBPlJoPTUVPTBVPTloPTBlPTlJPTUVPlJJPlVTPTUVPTBVPTBlPTUTPTBJPlJoPlJJPloTPlVoPloTPlJBPlJoPTUVPTBVPTloPTBlPTlJPTUVPlJJPlVTPTBJPTBUPTBVPTBoPTBJPTUTPlJoPlJJPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPUVJPTUUPTlVPTBUPTBBPTUTPUooPUVJPTUTPTBVPTlJPloTPUloPloTPTUlPUVJPTUTPTBVPTlJPloTPUlTPloTPlVVPlVTPUBTPloTPUlVPloTPlJTPUBUPUllPUBlPlJTPloTPUllPloTPlJTPlVVPUBoPUllPUlBPlJTPUlUPloTPTlUPTBUPTUTPloTPTUUPUJUPUVJPTUlPTlTPUUJPTloPTBoPTBVPTloPTBUPloTPUloPloTPTloPTBUPTUVPloTPTlVPUBBPTlVPTlTPTlUPlVTPTBJPTlUPTUUPTlBPTUUPlVTPUUJPTloPTBoPTBVPTloPTBUPlJoPTTTPloTPTUUPTBUPTBoPTlTPTBUPTloPTUTPTUUPUllPloTPTTTPTUUPTUVPUVJPTUlPTlTPUTUPTBlPUllPloTPTUoPTloPTUBPTBVPTUoPTBUPUTUPTBlPTTJPlVlPloTPTlUPTlJPUVJPTBlPTBUPTUlPUllPloTPTTTPloTPTUTPTUlPUVJPTBBPTllPTBUPTUlPUUlPTloPTloPTlJPTUoPTloPTBBPTBUPUllPloTPUJVPlJTPTUVPTUUPTUUPUllPlVoPlVoPUVJPTBTPlVTPTUUPTUVPUVJPTUlPTlTPlVTPTUJPTBVPTBlPTBUPTlJPlJTPUVlPlVlPloTPTBJPTUTPTUTPTlVPUJBPTUUPTBUPUooPUVJPTloPTBoPTBUPTUUPUllPloTPTUTPTUlPTUoPTBUPlVlPloTPUJUPUVJPTBVPTUTPUUVPTlJPTUlPUoVPTUlPUVJPTBBPTllPTBUPTUlPUllPloTPTBUPTloPUVJPUVVPTlUPTBUPUoUPTBUPTBUPTUlPUUTPUVJPTBBPTBJPTBUPlVlPloTPUJUPUVJPTBVPTUTPUUVPTlJPTUlPUoVPTUlPUVJPTBBPTllPTBUPTUlPUUTPTlJPTUoPTloPTUTPTBUPTUlPUllPloTPUBUPUBTPlVJPlVJPloTPTTJPloTPTTJPlJJPUlUPloTPTBBPTlJPTloPTUUPTUTPloTPTlVPTlUPUVJPTTlPTBUPTUlPUolPUVVPTlBPloTPUloPloTPTlBPTUVPTlVPTlUPUVJPTTlPTBUPTUlPlJoPTlVPTlUPUVJPTTlPTBUPTUlPUTUPTBlPlJJPUlUPloTPTlVPTlUPUVJPTTlPTBUPTUlPUolPUVVPTlBPlVTPTUUPTBUPTUTPTUoPTlVPlJoPTTTPloTPTBTPTBVPTlUPTBUPUllPloTPTUVPTBVPTloPTBlPTlJPTUVPlVTPUVJPTUTPTlJPUVVPlJoPTUJPTBVPTBlPTBUPTlJPUJBPTUlPTlUPlJJPlVlPloTPTBBPTlJPTloPTUTPTUlPTlJPTlUPTUUPUllPloTPTUTPTUlPTUoPTBUPlVlPloTPUVJPTUoPTUTPTlJPTUUPTUTPUVJPTUlPTUTPUllPloTPTBTPUVJPTlUPTUUPTBUPlVlPloTPTlTPTUoPTUTPTBUPUllPloTPTBTPUVJPTlUPTUUPTBUPlVlPloTPTBJPTlUPTUUPTBJPTUTPTlTPTlUPUllPloTPTUTPTUlPTUoPTBUPlVlPloTPTBVPTlTPUVJPTBoPTBUPUllPloTPlJTPTBJPTUTPTUTPTlVPTUUPUllPlVoPlVoPTBBPTBlPTloPlVTPTlUPTBVPTUJPTBUPTlVPTlUPTTlPlVTPTlTPTBUPlVoPTBVPTlTPUVJPTBoPTBUPTUUPlVoPTUTPTBJPTUoPTlTPUVVPlVoPTBoPUBJPTBlPUlBPTUlPUBVPTlBPUBlPTTlPUBJPTBTPlVVPTlTPUlBPUVJPUBBPTUlPUBJPTUJPUBUPlVTPTlBPTlVPTBUPTBoPlJTPlVlPloTPTUlPTBUPTUUPTlVPTlJPTloPTUUPTBVPTUJPTBUPUllPloTPTUTPTUlPTUoPTBUPlVlPloTPTUlPTBUPTloPTBlPTBUPTUlPUUTPUVJPTlVPTUTPTBVPTlJPTloPTUUPUoBPUVJPTUTPTBVPTUJPTBUPTlUPTTlPUllPloTPTBTPUVJPTlUPTUUPTBUPlVlPloTPTlUPTBVPTUJPTBUPUoJPTTlPTloPTBBPUUoPTUoPTUlPUVJPTUTPTBVPTlJPTloPUllPloTPUBlPlVJPlVlPloTPUVJPTUUPTlVPTBUPTBBPTUTPTUlPUVJPTUTPTBVPTlJPUllPloTPUVJPTUUPTlVPTBUPTBBPTUTPUooPUVJPTUTPTBVPTlJPlVlPloTPTUVPTBVPTBlPTUTPTBJPUllPloTPlJTPlVVPlVJPlVJPlJlPlJTPlVlPloTPTUTPTTlPTlVPTBUPUllPloTPlJTPTBJPTlUPTUUPlJTPlVlPloTPUVJPTloPTBlPTUlPTlJPTBVPTBlPTBJPTlUPTUUPUllPloTPTUTPTUlPTUoPTBUPlVlPloTPTlUPTlJPUVJPTBlPUUlPTloPTBlPUoUPUVJPTUlPTUUPTBUPUTlPTlUPTUUPUTVPTBUPTUTPUVJPTBlPUVJPTUTPUVJPUllPloTPTBTPUVJPTlUPTUUPTBUPlVlPloTPTllPTBUPTTlPUllPloTPTllPTBUPTlUPUJlPUVJPTlUPlVlPloTPTlVPTUlPTBVPTlTPUVJPTUlPTTlPUllPloTPlJTPTBJPTUTPTlTPTlUPUBTPlJTPlVlPloTPTlVPTUlPTBUPTlUPTlJPUVJPTBlPUllPloTPlJTPTloPTlJPTloPTBUPlJTPlVlPloTPTBJPTlUPTUUPTlBPTUUPTBlPTBUPTBTPUVJPTUoPTlUPTUTPUllPloTPTUTPTUlPTUoPTBUPlVlPloTPTBBPUVJPTUUPTUTPUllPloTPTTTPTTJPlVlPloTPUVVPUVJPTUUPTBUPUllPloTPTlBPTUVPUVVPUVJPTUUPTBUPTlVPUVJPTUTPTBJPloTPTTJPlJJPUlUPloTPTlVPTlUPUVJPTTlPTBUPTUlPUolPUVVPTlBPlVTPTlJPTloPlJoPlJTPTBUPTUlPTUlPTlJPTUlPlJTPlVlPloTPTBTPTlJPTUlPTBBPTBUPUToPTBVPTlUPTlUPTlVPTlUPUVJPTTlPTBUPTUlPlJJPUlUPloTPTlUPTBUPTUTPloTPTBlPTBUPUVVPTlJPTUoPTloPTBBPTBUPUlUPloTPTlVPTlUPUVJPTTlPTBUPTUlPUolPUVVPTlBPlVTPTlJPTloPlJoPlJTPUVVPTUoPTBTPTBTPTBUPTUlPlJTPlVlPloTPTBTPTUoPTloPTBBPTUTPTBVPTlJPTloPloTPlJoPlJJPloTPTTTPloTPTBlPTBUPUVVPTlJPTUoPTloPTBBPTBUPloTPUloPloTPTUUPTBUPTUTPUoVPTBVPTlTPTBUPTlJPTUoPTUTPlJoPTBTPTlJPTUlPTBBPTBUPUToPTBVPTlUPTlUPTlVPTlUPUVJPTTlPTBUPTUlPlVlPloTPlVVPUBTPlVJPlVJPlVJPlJJPUlUPloTPTTJPlJJPUlUPloTPTlVPTlUPUVJPTTlPTBUPTUlPUolPUVVPTlBPlVTPTlJPTloPlJoPlJTPTlVPTlUPUVJPTTlPlJTPlVlPloTPTBTPTUoPTloPTBBPTUTPTBVPTlJPTloPloTPlJoPlJJPloTPTTTPloTPTBBPTlUPTBUPUVJPTUlPUoVPTBVPTlTPTBUPTlJPTUoPTUTPlJoPTBlPTBUPUVVPTlJPTUoPTloPTBBPTBUPlJJPUlUPloTPTTJPlJJPUlUPloTPTlBPTUVPTlVPTlUPUVJPTTlPTBUPTUlPUVTPTBJPTlUPTUUPUVTPTlVPTUlPTlJPTUJPTBVPTBlPTBUPTUlPlVTPUVJPTUTPTUTPUVJPTBBPTBJPlJoPlJJPUlUPloTPTlVPUBBPTlVPTlTPTlUPlVTPTBJPTlUPTUUPTlBPTUUPlVTPTBVPTloPTBVPTUTPUTTPTUVPUoUPTlUPUVJPTTlPTBUPTUlPlJoPTlVPTlUPUVJPTTlPTBUPTUlPUolPUVVPTlBPlVlPloTPTTTPloTPTlUPTBVPTUJPTBUPUoJPTTlPTloPTBBPUUoPTUoPTUlPUVJPTUTPTBVPTlJPTloPUUTPTlJPTUoPTloPTUTPUllPloTPUBJPlVlPloTPTlUPTlJPUVJPTBlPTBUPTUlPUllPloTPTUUPUJUPUVJPTUlPTlTPUUJPTloPTBoPTBVPTloPTBUPlVTPTBBPTUlPTBUPUVJPTUTPTBUPUTJPTlJPUVJPTBlPTBUPTUlPUUTPTlUPUVJPTUUPTUUPlJoPlJJPloTPTTJPlJJPUlUPloTPTUUPTBUPTUTPUoVPTBVPTlTPTBUPTlJPTUoPTUTPlJoPTBTPTlJPTUlPTBBPTBUPUToPTBVPTlUPTlUPTlVPTlUPUVJPTTlPTBUPTUlPlVlPloTPUBBPloTPlJVPloTPUBlPUBoPlVJPlVJPlVJPlVJPlVJPlJJPUlUPlllPTBBPTlJPTloPTUUPTUTPloTPTBTPUVJPTllPTBUPTlUPTlJPTBoPloTPUloPloTPTBTPTUoPTloPTBBPTUTPTBVPTlJPTloPlJoPlJJPloTPTTTPTTJPUlUPllUPTUVPTBVPTloPTBlPTlJPTUVPUJVPlJTPTBBPTlJPTloPTUUPTlJPTlUPTBUPlJTPUVlPUJVPlJTPTlUPTlJPTBoPlJTPUVlPloTPUloPloTPTBTPUVJPTllPTBUPTlUPTlJPTBoPUlUPllUPTUUPTBUPTUTPUTUPTloPTUTPTBUPTUlPTUJPUVJPTlUPlJoPTBTPTUoPTloPTBBPTUTPTBVPTlJPTloPlJoPlJJPTTTPloTPTlUPTBUPTUTPloTPTUUPTUTPUVJPTUlPTUTPUoVPTBVPTlTPTBUPloTPUloPloTPTlVPTBUPTUlPTBTPTlJPTUlPTlTPUVJPTloPTBBPTBUPlVTPTloPTlJPTUVPlJoPlJJPUlUPloTPTBlPTBUPUVVPTUoPTBoPTBoPTBUPTUlPUlUPloTPTlUPTBUPTUTPloTPTUUPTUTPTlJPTlVPUoVPTBVPTlTPTBUPloTPUloPloTPTlVPTBUPTUlPTBTPTlJPTUlPTlTPUVJPTloPTBBPTBUPlVTPTloPTlJPTUVPlJoPlJJPUlUPloTPTBVPTBTPloTPlJoPlJoPTUUPTUTPTlJPTlVPUoVPTBVPTlTPTBUPloTPlVUPloTPTUUPTUTPUVJPTUlPTUTPUoVPTBVPTlTPTBUPlJJPloTPUlJPloTPlVVPlVJPlVJPlJJPloTPTTTPloTPTUVPTBVPTloPTBlPTlJPTUVPlVTPTlUPTlJPTBBPUVJPTUTPTBVPTlJPTloPloTPUloPloTPlJTPTBJPTUTPTUTPTlVPTUUPUllPlVoPlVoPTUVPTUVPTUVPlVTPTTlPTlJPTUoPTUTPTUoPUVVPTBUPlVTPTBBPTlJPTlTPlVoPTUVPUVJPTUTPTBBPTBJPUlVPTUJPUloPTUlPTUBPUJTPUBoPUBTPUooPUTlPUoVPUJUPTUlPUUlPlJTPloTPTTJPllUPTTJPlVlPloTPlVVPlVJPlVJPlJJPUlUPllUPlooPTBTPTUoPTloPTBBPTUTPTBVPTlJPTloPlJoPlJJPloTPTTTPloTPTBTPTUoPTloPTBBPTUTPTBVPTlJPTloPloTPTBlPTBUPTUTPTBUPTBBPTUTPUUoPTBUPTUJPUoVPTlJPTlJPTlUPlJoPUVJPTlUPTlUPTlJPTUVPlJJPloTPTTTPloTPTBVPTBTPlJoPTBVPTUUPUoBPUVJPUoBPlJoPlVBPUVJPTlUPTlUPTlJPTUVPlJJPlJJPloTPUVJPTlUPTlUPTlJPTUVPloTPUloPloTPlVVPlVJPlVJPUlUPloTPTlUPTBUPTUTPloTPTUUPTUTPUVJPTUlPTUTPloTPUloPloTPlVBPTloPTBUPTUVPloTPUUoPUVJPTUTPTBUPlJoPlJJPUlUPloTPTBlPTBUPUVVPTUoPTBoPTBoPTBUPTUlPUlUPloTPTlUPTBUPTUTPloTPTBUPTloPTBlPloTPUloPloTPlVBPTloPTBUPTUVPloTPUUoPUVJPTUTPTBUPlJoPlJJPUlUPloTPTBVPTBTPlJoPTBVPTUUPUoBPUVJPUoBPlJoPTUUPTUTPUVJPTUlPTUTPlJJPloTPTToPTToPloTPTBVPTUUPUoBPUVJPUoBPlJoPTBUPTloPTBlPlJJPloTPTToPTToPloTPTBUPTloPTBlPloTPlVUPloTPTUUPTUTPUVJPTUlPTUTPloTPUlJPloTPUVJPTlUPTlUPTlJPTUVPlJJPloTPTTTPloTPTUVPTBVPTloPTBlPTlJPTUVPlVTPTlUPTlJPTBBPUVJPTUTPTBVPTlJPTloPloTPUloPloTPlJTPTBJPTUTPTUTPTlVPTUUPUllPlVoPlVoPTUVPTUVPTUVPlVTPTTlPTlJPTUoPTUTPTUoPUVVPTBUPlVTPTBBPTlJPTlTPlVoPTUVPUVJPTUTPTBBPTBJPUlVPTUJPUloPTUlPTUBPUJTPUBoPUBTPUooPUTlPUoVPUJUPTUlPUUlPlJTPloTPTTJPloTPTTJPloTPTBVPTBTPlJoPTUVPTBVPTloPTBlPTlJPTUVPlVTPUVJPTUTPTUTPUVJPTBBPTBJPUUJPTUJPTBUPTloPTUTPlJJPloTPTTTPloTPTBVPTBTPloTPlJoPTBlPTlJPTBBPTUoPTlTPTBUPTloPTUTPlVTPTUlPTBUPUVJPTBlPTTlPUoJPTUTPUVJPTUTPTBUPloTPUloPUloPUloPloTPloJPTBBPTlJPTlTPTlVPTlUPTBUPTUTPTBUPloJPloTPTToPTToPloTPTBlPTlJPTBBPTUoPTlTPTBUPTloPTUTPlVTPTUlPTBUPUVJPTBlPTTlPUoJPTUTPUVJPTUTPTBUPloTPUloPUloPUloPloTPloJPTBVPTloPTUTPTBUPTUlPUVJPTBBPTUTPTBVPTUJPTBUPloJPlJJPloTPTTTPloTPTBlPTBUPTUTPTBUPTBBPTUTPUUoPTBUPTUJPUoVPTlJPTlJPTlUPlJoPlJJPUlUPloTPTUVPTBVPTloPTBlPTlJPTUVPlVTPUVJPTUTPTUTPUVJPTBBPTBJPUUJPTUJPTBUPTloPTUTPlJoPlJTPTlJPTloPTUlPTBUPTUUPTBVPTTUPTBUPlJTPlVlPloTPTBlPTBUPTUTPTBUPTBBPTUTPUUoPTBUPTUJPUoVPTlJPTlJPTlUPlJJPUlUPloTPTUVPTBVPTloPTBlPTlJPTUVPlVTPUVJPTUTPTUTPUVJPTBBPTBJPUUJPTUJPTBUPTloPTUTPlJoPlJTPTlJPTloPTlTPTlJPTUoPTUUPTBUPTlTPTlJPTUJPTBUPlJTPlVlPloTPTBlPTBUPTUTPTBUPTBBPTUTPUUoPTBUPTUJPUoVPTlJPTlJPTlUPlJJPUlUPloTPTUVPTBVPTloPTBlPTlJPTUVPlVTPUVJPTUTPTUTPUVJPTBBPTBJPUUJPTUJPTBUPTloPTUTPlJoPlJTPTlJPTloPTBTPTlJPTBBPTUoPTUUPlJTPlVlPloTPTBlPTBUPTUTPTBUPTBBPTUTPUUoPTBUPTUJPUoVPTlJPTlJPTlUPlJJPUlUPloTPTUVPTBVPTloPTBlPTlJPTUVPlVTPUVJPTUTPTUTPUVJPTBBPTBJPUUJPTUJPTBUPTloPTUTPlJoPlJTPTlJPTloPUVVPTlUPTUoPTUlPlJTPlVlPloTPTBlPTBUPTUTPTBUPTBBPTUTPUUoPTBUPTUJPUoVPTlJPTlJPTlUPlJJPUlUPloTPTTJPloTPTBUPTlUPTUUPTBUPloTPTTTPloTPTUUPTBUPTUTPUoVPTBVPTlTPTBUPTlJPTUoPTUTPlJoPUVJPTUlPTBoPTUoPTlTPTBUPTloPTUTPlVTPTBBPUVJPTlUPTlUPTBUPTBUPlVlPloTPlVJPlJJPUlUPloTPTTJPloTPTTJPloTPTBUPTlUPTUUPTBUPloTPTTTPloTPTUVPTBVPTloPTBlPTlJPTUVPlVTPUVJPTBlPTBlPUUJPTUJPTBUPTloPTUTPUTJPTBVPTUUPTUTPTBUPTloPTBUPTUlPlJoPlJTPTlUPTlJPUVJPTBlPlJTPlVlPloTPTBlPTBUPTUTPTBUPTBBPTUTPUUoPTBUPTUJPUoVPTlJPTlJPTlUPlJJPUlUPloTPTUVPTBVPTloPTBlPTlJPTUVPlVTPUVJPTBlPTBlPUUJPTUJPTBUPTloPTUTPUTJPTBVPTUUPTUTPTBUPTloPTBUPTUlPlJoPlJTPTUlPTBUPTUUPTBVPTTUPTBUPlJTPlVlPloTPTBlPTBUPTUTPTBUPTBBPTUTPUUoPTBUPTUJPUoVPTlJPTlJPTlUPlJJPUlUPloTPTUVPTBVPTloPTBlPTlJPTUVPlVTPUVJPTBlPTBlPUUJPTUJPTBUPTloPTUTPUTJPTBVPTUUPTUTPTBUPTloPTBUPTUlPlJoPlJTPTlTPTlJPTUoPTUUPTBUPTlTPTlJPTUJPTBUPlJTPlVlPloTPTBlPTBUPTUTPTBUPTBBPTUTPUUoPTBUPTUJPUoVPTlJPTlJPTlUPlJJPUlUPloTPTUVPTBVPTloPTBlPTlJPTUVPlVTPUVJPTBlPTBlPUUJPTUJPTBUPTloPTUTPUTJPTBVPTUUPTUTPTBUPTloPTBUPTUlPlJoPlJTPTBTPTlJPTBBPTUoPTUUPlJTPlVlPloTPTBlPTBUPTUTPTBUPTBBPTUTPUUoPTBUPTUJPUoVPTlJPTlJPTlUPlJJPUlUPloTPTUVPTBVPTloPTBlPTlJPTUVPlVTPUVJPTBlPTBlPUUJPTUJPTBUPTloPTUTPUTJPTBVPTUUPTUTPTBUPTloPTBUPTUlPlJoPlJTPUVVPTlUPTUoPTUlPlJTPlVlPloTPTBlPTBUPTUTPTBUPTBBPTUTPUUoPTBUPTUJPUoVPTlJPTlJPTlUPlJJPUlUPloTPTTJPllUPTTJPlJoPlJJPUlUP", 68, "BlUToJVPm", 48, 7, 6)
    s = My_Var[0]
    n = My_Var[2]
    t = My_Var[3]
    e = My_Var[4]
    split_char = n[e]
    s_tab = s.split(split_char)
    script = ""
    for elm in s_tab:
        if elm !='':
            elm_ = []
            for ch in elm:
                for i in range(0,len(n)):
                    if ch == n[i]:
                        elm_.append(i)
                        break
            elm_.reverse()
            ch_out = 0
            for j in range (0,len(elm_)):
                ch_out = ch_out + elm_[j] * pow(e,j)
                j = j+1
            ch_out = ch_out - t
            script = script+chr(ch_out)
    return(script)
 
    
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'livetv.cookie'})
        self.MAIN_URL = 'http://livetv.sx'
        self.UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
        self.mode = True
        
    def showmenu(self,cItem):
        TAB = [('SPORT LIVE','/enx/','10',0),('SPORT GENRES','/enx/allupcoming/','10',1),]
               #('SPORT LIVE (Add IPAUDIO)','/enx/','10',10)]
        self.add_menu(cItem,'','','','','',TAB=TAB,search=False)
        self.addMarker({'category':'Marker','title': tscolor('\c00????30') + 'SITES','icon':cItem['icon']})
        TAB = [('liveon.sx','https://liveon.sx', '100',0),]
               #('Maxsport','https://maxsport.one', '101',0),('WikiSport','http://tk.freestreams-live1.com', '102',0),('klubsports.xyz','https://klubsports.xyz', '103',0),]
        self.add_menu(cItem,'','','','','',TAB=TAB,search=False)        
        

    def showmenu1(self,cItem):
        url_   = cItem.get('url','')
        gnr_   = cItem.get('sub_mode',0)
        image  = cItem.get('icon','')
        if (gnr_ == 0) or (gnr_ == 10):
            ipaudio = False
            if (gnr_ == 10): ipaudio = True
            sts, data = self.getPage(url_)
            if sts:        
                data_els = re.findall('<td OnMouseOver.*?alt="(.*?)".*?<td>.<a class="live" href="(.*?)">(.*?)<(.*?)"evdesc">(.*?)<', data, re.S)
                for (image_gif,url,titre,result,desc) in data_els:
                    if url.startswith('/'): url = self.MAIN_URL + url
                    titre = self.cleanHtmlStr(titre).replace('&nbsp;',' ').replace('&ndash;','-').replace('  ',' ').replace('  ','').strip()
                    #printDBG('result====='+result)
                    data_els2 = re.findall('class="live">(.*?)<', result, re.S)
                    if data_els2:
                        rslt = self.cleanHtmlStr(data_els2[0]).replace('&nbsp;',' ').strip()
                        if rslt != '':
                            titre = titre+ tscolor('\c00????00') +' ('+rslt+')'
                    desc = self.cleanHtmlStr(desc).strip()+'\n'+self.cleanHtmlStr(image_gif)
                    self.addDir({'import':cItem['import'],'category' : 'host2','url': url,'title':titre,'desc':desc,'icon':image,'mode':'20','ipaudio':ipaudio})    
        elif gnr_ == 1:
            sts, data = self.getPage(url_)
            if sts:        
                data_els = re.findall('<a class="main".*?<a class="main".*?href="(.*?)".*?<b>(.*?)<.*?class="small".*?<b>(.*?)</b>', data, re.S)
                for (url,titre,info) in data_els:
                    titre = self.cleanHtmlStr(titre)+ tscolor('\c00????00') +' ('+info+')'
                    if url.startswith('/'): url = self.MAIN_URL + url
                    self.addDir({'import':cItem['import'],'category' : 'host2','url': url,'title':titre,'desc':'','icon':image,'mode':'10','sub_mode':2})    
        elif gnr_ == 2:        
            sts, data = self.getPage(url_)
            if sts:        
                data_els = re.findall('<a class="live" href="([^"]+)">([^<]+)</a>\s*(<br><img src=".+?/img/live.gif"><br>|<br>)\s*<span class="evdesc">([^<]+)\s*<br>\s*([^<]+)</span>', data, re.S)
                for (url,titre,live,info,desc) in data_els:
                    if url.startswith('/'): url = self.MAIN_URL + url
                    titre = self.cleanHtmlStr(titre).replace('&nbsp;',' ').strip()
                    if 'live' in live:
                        titre = titre+ tscolor('\c00????00') +' (LIVE)'
                    desc = self.cleanHtmlStr(desc).replace('&nbsp;',' ').strip()+'\n'+self.cleanHtmlStr(info)
                    self.addDir({'import':cItem['import'],'category' : 'host2','url': url,'title':titre,'desc':desc,'icon':image,'mode':'20'})    

    def showitms(self,cItem):
        ipaudio = cItem.get('ipaudio',False)
        url_   = cItem.get('url','')
        image  = cItem.get('icon','')        
        sts, data = self.getPage(url_)
        if sts:        
            data_els = re.findall('<td width=16><img title="(.*?)".*?src="(.*?)".*?class="bitrate.*?">(.*?)</td>(.*?)</div>.*?href="(.*?)"(.*?)</table>', data, re.S)
            for (titre,image,bitrate,qualite,url,type_) in data_els:
                if url.startswith('//'): url = 'http:' + url
                titre = self.cleanHtmlStr(titre).replace('&nbsp;',' ').strip()
                bitrate = self.cleanHtmlStr(bitrate).replace('&nbsp;',' ').strip()
                qualite = self.cleanHtmlStr(qualite).replace('&nbsp;',' ').strip().replace(' ','')
                type_ = self.cleanHtmlStr('<'+type_).replace('&nbsp;',' ').strip()
                if titre == '': titre = 'Pure Live'
                titre = titre+ tscolor('\c00????00') +' ['+qualite+']'
                if bitrate != '': titre = titre+ tscolor('\c0000????') +' ('+bitrate+')'
                if 't=acestream' not in url:
                    mode = True
                    if 'youtube' in url:
                        titre = titre + tscolor('\c0020??20') + ' (Youtube)'
                        mode = False
                        
                    if '=alieztv' in url:
                        titre = titre + tscolor('\c0020??20') + ' (Alieztv)'
                        mode = False
                    if mode:
                        Params = dict(self.defaultParams)
                        Params['header']['User-Agent'] = self.UA
                        sts, data = self.getPage(url,Params)
                        if sts:        
                            data_els = re.findall('<iframe.{1,3}allowFullScreen.*?src="(.*?)"', data, re.S)
                            if data_els:
                                url_ = data_els[0]
                                url_ = url_.replace('\r\n','')
                                if url_.startswith('//'): url_ = 'http:' + url_
                                color_ = tscolor('\c00??????')
                                if 'all.ive.zone'    in url_:   color_ = tscolor('\c0020??20')
                                if 'popofthestream'  in url_:   color_ = tscolor('\c0020??20')
                                if 'wizhdlive'       in url_:   color_ = tscolor('\c0020??20')
                                if 'ettu.tv'         in url_:   color_ = tscolor('\c0020??20')
                                if 'gamehub'         in url_:   color_ = tscolor('\c0020??20')
                                if 'onionstream'     in url_:   color_ = tscolor('\c0020??20')
                                if 'allsport.icu'    in url_:   color_ = tscolor('\c0020??20')
                                if 'telerium'        in url_:   color_ = tscolor('\c0020??20')
                                if 'sportrush.'      in url_:   color_ = tscolor('\c0020??20')
                                if 'ocubel.'         in url_:   color_ = tscolor('\c0020??20')
                                if 'livecenter.'     in url_:   color_ = tscolor('\c0020??20')
                                if 'onhockey.'       in url_:   color_ = tscolor('\c0020??20')
                                if 'vimeo.'          in url_:   color_ = tscolor('\c0020??20')
                                if '.socolive'       in url_:   color_ = tscolor('\c0020??20')
                                if 'sports247.'      in url_:   color_ = tscolor('\c0020??20')                                
                                if 'soccerstreamslive.'  in url_:   color_ = tscolor('\c0020??20')
                                if 'jokerswidget.'   in url_:   color_ = tscolor('\c0020??20')
                                if 'klubsports.'     in url_:   color_ = tscolor('\c0020??20')
                                if 'streamhd247'     in url_:   color_ = tscolor('\c00????20')
                                if 'maxsport'        in url_:   color_ = tscolor('\c00????20')
                                if 'livetvon'        in url_:   color_ = tscolor('\c00??2020')
                                if 'sportcast'       in url_:   color_ = tscolor('\c00??2020')
                                if 'varplatform'     in url_:   color_ = tscolor('\c0020??20')
                                if 'embedstream'     in url_:   color_ = tscolor('\c00??20??')
                                color_ = tscolor('\c00??????')
                                if 'varplatform'     in url_:   color_ = tscolor('\c00??2020')
                                if 'xestreams.'      in url_:   color_ = tscolor('\c0020??20') 
                                if 'sawlive'         in url_:   color_ = tscolor('\c0020??20')   
                                if 'wikisport'       in url_:   color_ = tscolor('\c0020??20')
                                if 'maxsport'        in url_:   color_ = tscolor('\c0020??20')
                                if 'soccerstream100' in url_:   color_ = tscolor('\c0020??20') 
                                if 'sportskart'      in url_:   color_ = tscolor('\c0020??20') 
                                if 'daddylivehd'     in url_:   color_ = tscolor('\c0020??20')
                                if 'livestream'      in url_:   color_ = tscolor('\c0020??20')
                                if 'stream.crichd'   in url_:   color_ = tscolor('\c0020??20')
                                if 'assia24'         in url_:   color_ = tscolor('\c0020??20')                                                               
                                if 'sports-stream.'  in url_:   color_ = tscolor('\c0020??20')
                                if 'ustream.'        in url_:   color_ = tscolor('\c0020??20') 
                                if 'brolel.'         in url_:   color_ = tscolor('\c0020??20')                               
                                if 'embedstream'     in url_:   color_ = tscolor('\c00??20??')
                                if '1socolive'       in url_:   color_ = tscolor('\c00??20??')
                                if 'streamhd247'     in url_:   color_ = tscolor('\c0020??20')
                                if 'wizospor'        in url_:   color_ = tscolor('\c0020??20') 
                                if 'streamingnow'    in url_:   color_ = tscolor('\c0020??20') 
                                if '1l1l.to'         in url_:   color_ = tscolor('\c0020??20')
                                if 'spotles365'      in url_:   color_ = tscolor('\c0020??20')

                                titre = titre +color_+ ' ('+gethostname(url_)+')'
                                self.addVideo({'import':cItem['import'],'category' : 'host2','url': url_,'title':titre,'desc':url_,'icon':image,'mode':'20','sub_mode':1,'hst':'tshost','referer':url,'ipaudio':ipaudio})
                    else:
                        self.addVideo({'import':cItem['import'],'category' : 'host2','url': url,'title':titre,'desc':type_,'icon':image,'mode':'20','hst':'tshost','ipaudio':ipaudio})    



    def get_links(self,cItem): 	
        #urlTab = []
        ipaudio = cItem.get('ipaudio',False)
        url = cItem['url']
        #url = 'http://cdn.livetv573.me/webplayer.php?t=ifr&c=1920607&lang=en&eid=72434397&lid=1920607&ci=4275&si=4'
        urlTab = self.resolve_links(url,cItem.get('referer',''),ipaudio=ipaudio)
        printDBG ('URLTAB='+str(urlTab))
        return urlTab

    def get_links1(self,cItem): 	
        urlTab = []
        urlTab1 = []
        url_ = cItem['url']
        #url_='http://cdn.livetv569.me/webplayer.php?t=ifr&c=1910308&lang=en&eid=67357617&lid=1910308&ci=16&si=1'
        gnr   = cItem.get('sub_mode',0)
        if gnr==1:
            if 'wikisport' in url_:                      
                #URL = self.resolve_links(url_,cItem.get('referer',''))
                urlTab.append({'name':'wikisport', 'url':'hst#tshost#'+url_+'||||'+cItem.get('referer',''), 'need_resolve':1})
            else:
                URL = self.resolve_links(url_,cItem.get('referer',''))
                urlTab.append({'name':'LINK', 'url':URL, 'need_resolve':0})
        else:
            Params = dict(self.defaultParams)
            Params['header']['User-Agent'] = self.UA
            sts, data = self.getPage(url_,Params)
            if sts:        
                data_els = re.findall('<iframe.{1,3}allowFullScreen.*?src="(.*?)"', data, re.S)
                if data_els:
                    url = data_els[0]
                    url = url.replace('\r\n','')
                    printDBG('URL======'+url)
                    #url = 'https://maxsport.one/stream93.php'
                    if 'wikisport' in url:
                        #return self.resolve_links(url,url_)
                        #URL = self.resolve_links(url,url_)
                        #printDBG('URL======'+URL)
                        urlTab.append({'name':'wikisport', 'url':'hst#tshost#'+url+'||||'+url_, 'need_resolve':1})                        
                    else:
                        URL = self.resolve_links(url,url_)
                        printDBG('URL======'+URL)
                        urlTab.append({'name':'LINK', 'url':URL, 'need_resolve':0})
                else:
                    data_els = re.findall('<iframe.{1,30}src="(https://www.youtube.*?)"', data, re.S)
                    if data_els:
                        URL = data_els[0]
                        urlTab.append({'name':'Youtube', 'url':URL, 'need_resolve':1}) 
        
        #url='https://best.globalweb.ru.com/cdn/premium93/mono.m3u8'
        #meta = {'Referer':'https://olacast.live/','User-Agent':self.UA}
        #url_=strwithmeta(url, meta)
        #urlTab1.append({'name':'Youtube', 'url':url_, 'need_resolve':0}) 
        return urlTab

    def resolve_links(self,url,referer,ipaudio=False):
        printDBG('Resolve_links URL = '+url +' | Referer: '+ referer)
        if url.startswith('-http'): url = url.replace('-http','http')
        if 'varplatform' in url:
            return []
            prefix_url = re.findall('(http.*?//.*?)/', url, re.S)
            if prefix_url: prefix_url = prefix_url[0]
            else: prefix_url = ''
            link = ''
            count = 0
            while (link == '') and (count<10):
                count = count+1
                print(str(count)+': '+url)
                sts, data0 = self.getPage(url)
                if sts:
                    data_url = re.findall('<iframe.{0,40}src="(.*?)"', data0, re.S)
                    if data_url: 
                        url =  data_url[0] 
                        if url.startswith('/'): url = prefix_url+url
                    else:
                        data_url = re.findall('file:"(.*?)"', data0, re.S)
                        if data_url: link = data_url[0]
                        else: count = 10
            if link !='': 
                meta = {'Referer':'https://varplatform.top/','Origin':'https://varplatform.top','User-Agent':self.UA}
                link = strwithmeta(link, meta)
                return ([{'name':'LINK', 'url':link, 'need_resolve':0},])              
            else: return []
            #printDBG('Host Not Supported ('+url+')')
            #SetIPTVPlayerLastHostError('Host "'+gethostname(url)+'" not supported.')

        if 'sportcast.life/nginx.php?id=' in url:
            referer = url
            url = url.replace('sportcast.life/nginx.php?id=','sportcast.life/embed10/live')
            if not url.endswith('.php'): url += '.php'
            
        if 'ettu.tv'      in url:    return (self.resolve_EttuTv(url)) 
        if 'emb.apl'      in url:    return (self.resolve_EMB(url,ipaudio))    
        if 'cdn122.com'   in url:    return (self.resolve_CDN(url,referer,ipaudio)) 
        if 'sawlive.tv'   in url:    return (self.resolve_SawLive(url,ipaudio)) 
        if 'livestream.'   in url:    return (self.resolve_LiveStream(url,ipaudio)) 
        if 'wecast.to'    in url:    return (self.resolve_Wecast(url,referer,ipaudio))
        if 'vimeo.com'    in url:    return ([{'name':'vimeo', 'url':url, 'need_resolve':1},])
            
        data_els = re.findall('onhockey.*?channel=(http.*?.m3u8)', url, re.S)
        if data_els:
            meta = {'Referer':'http://onhockey.tv/','User-Agent':self.UA}
            url_=strwithmeta(data_els[0], meta)
            if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
            return ([{'name':'LINK', 'url':url_, 'need_resolve':0},])            
        
        Params = dict(self.defaultParams)
        Params['header']['User-Agent'] = self.UA
        if referer!='':
            Params['header']['Referer'] = referer
            Params['with_metadata'] = True          
        sts, data = self.getPage(url,Params)
        if sts:                    
            #printDBG('URL NOT FOUND DATA0=' + data)
            data = strwithmeta( re.sub("(<!--.*?-->)", "", data, flags=re.DOTALL) , data.meta)
            #printDBG('DATA=' + data) 
            if 'youtube' in url:
                data_els = re.findall('<iframe.{1,30}src="(.{1,10}www.youtube.*?)"', data, re.S)
                if data_els:
                    Embed_URL = data_els[0]
                    if Embed_URL.startswith('//'): Embed_URL = 'https:'+Embed_URL
                    printDBG('Youtube Trouve = '+Embed_URL )
                    return ([{'name':'Youtube', 'url':Embed_URL, 'need_resolve':1},])             
            data_els = re.findall('<iframe.{1,3}allowFullScreen.*?src="(.*?)"', data, re.S)
            if (not data_els) and ('klubsports.' not in url) and ('reddit-soccerstreams' not in url):
                #data_els = re.findall('iframe.{1,70}src=[\'"](.*?)[\'"]', data, re.S)    
                data_els = re.findall('iframe src=[\'"](.*?)[\'"]', data, re.S)
            if (not data_els) and (('soccerstreamslive.' in url) or ('ocubel.' in url) or ('varplatform.' in url) or ('klubsports.' in url)):
                data_els = re.findall('iframe.{1,70}src=[\'"](.*?)[\'"]', data, re.S)             

            if data_els:
                Embed_URL = data_els[0].replace('\r\n','')
                if Embed_URL.strip() != '':
                    printDBG('Embed_URL='+Embed_URL)
                    if Embed_URL.startswith('//'): Embed_URL = 'http:'+Embed_URL
                    if Embed_URL.startswith('./aliez/'): Embed_URL = Embed_URL.replace('./aliez/','http://www.popofthestream.com/embed/aliez/')
                    if Embed_URL.startswith('/'): Embed_URL =     'http://' + gethostname(url) + Embed_URL
                    if Embed_URL.endswith('?id='):
                        data_id = re.findall('<script.*?id=(.*?);.*?fid=(.*?);', data, re.S)
                        if data_id:
                            try:
                                id__ = int(data_id[0][0])
                                fid__ = int(data_id[0][1].replace('id-0x',''),16)
                                fid = str(id__-fid__)
                                Embed_URL = Embed_URL+ fid
                            except:
                                SetIPTVPlayerLastHostError('Wrong ID!!!!')
                                return []
                        else:
                            SetIPTVPlayerLastHostError('Empty ID!!!!')
                            return []                        
                    if ' + chInfos.id + ' in Embed_URL:
                        url_json = url.replace('.html','.json')
                        sts, data0 = self.getPage(url_json)
                        if sts:
                            data_id = re.findall('"id".*?"(.*?)"', data0, re.S)
                            if data_id:
                                Embed_URL = Embed_URL.replace("' + chInfos.id + '",data_id[0])                   
                    printDBG('Embed_URL='+Embed_URL)
                    if ('//ads.' not in Embed_URL) and ('youtube.' not in Embed_URL):
                        return self.resolve_links(Embed_URL,data.meta.get('url',url),ipaudio)           
            data_els = re.findall('const pdettxt = "(.*?)".*?const zmid = "(.*?)".*?const pid =(.*?);.*?const  edm = "(.*?)".*?src="(.*?)"', data, re.S) #live.jokerswidget.org
            if data_els:
                #SetIPTVPlayerLastHostError('Embedstream')
                #return[]
                print(data)
                pdettxt = data_els[0][0]
                zmid    = data_els[0][1]
                pid     = data_els[0][2]
                edm     = data_els[0][3]
                src     = data_els[0][4]
                sts_src, data_src = self.getPage(src)
                if sts_src:                     
                    data_els_src = re.findall("const url=[\"'](.*?);", data_src, re.S)
                    if data_els_src:
                        Embed_URL = data_els_src[0]
                        print (Embed_URL)
                        Embed_URL = Embed_URL.replace('+edm',edm.strip())
                        Embed_URL = Embed_URL.replace('+zmid',zmid.strip())
                        Embed_URL = Embed_URL.replace('"','').replace("'",'').replace('+','')
                        printDBG('Embed_URL 01 =' + Embed_URL)
                        postdata = {"pid":int(pid.strip()),"ptxt":pdettxt.strip(),"v":zmid.strip()}
                        printDBG('postdata =' + str(postdata))
                        
                        Params = dict(self.defaultParams)
                        Params['header']['User-Agent'] = self.UA
                        Params['header']['Referer'] = 'https://embedstream.me/'#url
                        Params['header']['content-type'] = "application/x-www-form-urlencoded"
                        Params['header']['cookie'] = "_pshflg=~; tamedy=1"
                        Params['header']['origin'] = "https://embedstream.me"
                        
                        sts1, data1 = self.getPage(Embed_URL,Params,postdata)                         
                        if sts1:
                            printDBG('ddddata='+data1)
                            data_els = re.findall('String.fromCharCode.*?(\(".*?\))\)', data1, re.S)
                            if data_els:
                                My_Var = eval(data_els[0].strip())
                                printDBG('My_Var='+str(My_Var))
                                My_script = hunter_decode(My_Var)
                                printDBG('My_script='+str(My_script))
                                data_els = re.findall('videoUrl =.*?["\'](.*?)["\']', My_script, re.S)
                                if data_els:
                                    URL_ = base64.b64decode(data_els[0])
                                    printDBG('m3u8 trouver 023=' + URL_)          
                                    meta = {'Referer':'https://www.liveply.me/','Origin':'https://www.liveply.me','User-Agent':self.UA}
                                    url_=strwithmeta(URL_, meta)
                                    if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
                                    return ([{'name':'LINK', 'url':url_, 'need_resolve':0},])                                
                        return []
            #data_els = re.findall("<script>fid=['\"](.+?)['\"].*?src=['\"](.*?)['\"]", data, re.S)
            data_els = re.findall("<script.{0,30}fid=['\"](.+?)['\"].*?src=['\"](.*?)['\"]", data, re.S) #live.jokerswidget.org
            if data_els:
                src = data_els[0][1]
                fid = data_els[0][0]
                if src.startswith('//'): src = 'http:'+src
                #get embed Url
                sts_src, data_src = self.getPage(src)
                if sts_src:                     
                    data_els_src = re.findall('src="(.*?)"', data_src, re.S)
                    if data_els_src:
                        Embed_URL = data_els_src[0]
                        Embed_URL = Embed_URL.replace("'+embedded+'","desktop").replace("'+ embedded +'","desktop")
                        Embed_URL = Embed_URL.replace("'+fid+'",fid).replace("'+ fid +'",fid)
                        if Embed_URL.startswith('//'): Embed_URL = 'http:'+Embed_URL
                        printDBG('Embed_URL 00 =' + Embed_URL)
                        if 'vikistream'   in Embed_URL: return (self.resolve_Vikistream(Embed_URL,url,ipaudio))  
                        if 'jokersplayer' in Embed_URL: return (self.resolve_Jokersplayer(Embed_URL,url,ipaudio))
                        else: return (self.resolve_links(Embed_URL,url,ipaudio))     
                return []
                if 'jokersplayer' in data_els[0][1]:
                    Embed_URL = 'http://www.jokersplayer.xyz/embed.php?u='+data_els[0][0]
                    printDBG('jokersplayer link trouver =' + Embed_URL)    
                    if Embed_URL.startswith('//'): Embed_URL = 'http:'+Embed_URL
                    return (self.resolve_Jokersplayer(Embed_URL,url,ipaudio))                    
                else:
                    Embed_URL = data_els[0][1].replace('.js','.php')+'?player=desktop&live='+data_els[0][0]
                    printDBG('Vikistream link trouver =' + Embed_URL)    
                    if Embed_URL.startswith('//'): Embed_URL = 'http:'+Embed_URL
                    return (self.resolve_Vikistream(Embed_URL,url,ipaudio))
                
            data_els = re.findall("[^/]source:'(.*?)'", data, re.S)
            if data_els:
                URL_ = data_els[0]
                printDBG('m3u8 trouver 02=' + URL_)                    
                if 'globalweb.ru' in URL_:
                    SetIPTVPlayerLastHostError('Host "'+gethostname(URL_)+'" not supported.')
                    return []                
                meta = {'Referer':url,'User-Agent':self.UA}
                url_=strwithmeta(URL_, meta)
                if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
                return ([{'name':'LINK', 'url':url_, 'need_resolve':0},])
            
            data_els = re.findall('Player\(.{1,50}source:.{1,3}["\'](http.*?)["\']', data, re.S)
            if not data_els:
                data_els = re.findall('Player.{1,50}(?:source:|file:).{0,3}["\'](http.*?)["\']', data, re.S)
            if not data_els:
                data_els = re.findall('jwplayer.{1,50}.setup.{1,50}file:.{0,3}["\'](.*?)["\']', data, re.S)
            if data_els:
                URL_ = data_els[0] 
                printDBG('m3u8 trouver 03=' + URL_)          
                meta = {'Referer':url,'User-Agent':self.UA}
                url_=strwithmeta(URL_, meta)
                if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
                printDBG('m3u8 trouver 04=' + url_) 
                return ([{'name':'LINK', 'url':url_, 'need_resolve':0},])
            
            data_els = re.findall('return\((\["h","t","t".*?])', data, re.S)
            if data_els:
                URL_Tab = eval(data_els[0])
                URL_ = ''
                for c in URL_Tab:
                    URL_ += c
                URL_ = URL_.replace('\/','/')
                printDBG('m3u8 trouver 04=' + URL_)          
                meta = {'Referer':url,'User-Agent':self.UA}
                url_=strwithmeta(URL_, meta)
                if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
                return ([{'name':'LINK', 'url':url_, 'need_resolve':0},])            
 
            data_els = re.findall('(eval\(function\(p,a,c,k,e,d\).*?)</script>', data, re.S)
            if data_els:
                data10 = cPacker().unpack(data_els[0].strip())
                lst_data = re.findall('source:[\'"](.*?)[\'"]', data10, re.S)
                if not lst_data:
                    lst_data = re.findall('file:[\'"](.*?)[\'"]', data10, re.S)    
                if lst_data:    
                    url_ = lst_data[0]
                    if url_.startswith('//'): url_ = 'http:' + url_
                    url_ = strwithmeta(url_, {'Referer':url})
                    printDBG('m3u8 trouver 05=' + url_)
                    if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
                    return [{'name':'LINK', 'url':url_, 'need_resolve':0}] 
            
            lst_data = re.findall('(?:source:|strm).{1,10}atob\([\'"](.*?)[\'"]', data, re.S)   #(http://xestreams.com/livetv/tv04.php) 
            if not lst_data:    
                lst_data = re.findall('<input name="crf__.*?value=\'(.*?)\'', data, re.S)   #(https://pelotero.net/foxsportspremium.php) ne marche pas
            if lst_data:
                auth = ''
                url_ = base64.b64decode(lst_data[0]).decode('utf8',errors='ignore')
                print(url_)
                if url_.startswith('//'): url_ = 'http:' + url_
                ref = url
                if 'xestreams' in url:
                    ref ='https://xestreams.com'
                    meta = {'Origin':ref,'Referer':ref+'/','User-Agent':self.UA}
                elif 'tutele.' in url:                    
                    ref = 'https://www.tutele.nl'
                    lst_data0 = re.findall('"auth":"(.*?)"', data, re.S)
                    if lst_data0:
                        auth = lst_data0[0].replace('\/','/')
                    meta = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
                        'Xauth': '5jnX9+oBu6TjHHZNOB5FK4yfN0o1zNR+cvP4YNmItKGvvJJAFxpaBsDaO0z51F3Uqc7iOKwuwobmfNe3epleNGhBuJuC1r9x5znS4YOaxpbxhedlyeThQ9oEsrE+fL1fl3FEnu22YEmkaD2WQgNoRAWj8EYa46AyUPA9I9KPlp8v1l8ycZNROatzwj4CmEq5voO35ZFRrYqavv7LWzrwTOn273DZY2Bi3rCv9zcexhk9MMKDgC+9UV2lfki1nQ6u2ZgoBuYZxoqlDlr308S9L7lEysBzdEGu8x7QpRCjEUyMeuU2MVLcsP1mr3SXMtnasmQtM5DC6SkNPGaDEwt92Q==',
                        'Origin': 'https://www.tutele.nl', 'Referer': 'https://www.tutele.nl/'}
                elif 'wikisport.' in url: 
                    ref ='http://wikisport.click'
                    meta = {'Origin':ref,'User-Agent':self.UA,'Referer':ref+'/'}
                    url_ = strwithmeta(url_, meta)
                    printDBG('m3u8 trouver 06=' + url_)
                    #return getDirectM3U8Playlist(url_, checkExt=True, checkContent=True, sortWithMaxBitrate=999999999)                

                    add_url = 'https://hymmo.herokuapp.com/'
                    #add_url = 'https://hymmo.herokuapp.com/'
                    
                    urlTab0 = getDirectM3U8Playlist(url_, False, checkContent=True, sortWithMaxBitrate=999999999)
                    urlTab1 = []
                    printDBG('urlTab ================ '+str(urlTab0))
                    for elm in urlTab0:
                        elm1 = dict(elm)
                        meta0_ = elm1['url'].meta
                        printDBG('meta_ ================ '+str(meta0_))
                        elm1['url'] = strwithmeta(add_url + elm1['url'],meta0_)
                        urlTab1.append(elm1)
                    return urlTab1

                else:
                    meta = {'Referer':ref,'User-Agent':self.UA}
                url_ = strwithmeta(url_, meta)
                printDBG('m3u8 trouver 07=' + url_)
                if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
                return [{'name':'LINK', 'url':url_, 'need_resolve':0}] 
                
            lst_data = re.findall("<script.{1,50}channel='(.*?)'.{1,20}g='(.*?)'.{1,60}src='https://live.uctnew", data, re.S)    
            if lst_data:
                Embed_URL = 'https://live.uctnew.com/hembedplayer/'+lst_data[0][0]+'/'+lst_data[0][1]+'/700/480'
                return self.resolve_links(Embed_URL,'https://new.socolive.pro/',ipaudio) 

            lst_data = re.findall('hlsUrl = "(.{1,80}pk=)', data, re.S)    
            if lst_data:
                Embed_URL = lst_data[0]
                lst_data0 = re.findall('var pk = "(.*?)"', data, re.S) 
                if lst_data0:
                    index = 53
                    pk = lst_data0[0]
                    printDBG('pk0='+pk)
                    pk = pk[0 : index : ] + pk[index + 1 : :]
                    printDBG('pk1='+pk)
                    Embed_URL = Embed_URL + pk
                    printDBG ('Embed_URL0='+Embed_URL)
                    lst_data1 = re.findall('ea = "(.{3,40})"', data, re.S) 
                    if lst_data1:
                        if '" + ea + "' in Embed_URL:
                            Embed_URL = Embed_URL.replace('" + ea + "',lst_data1[0])
                            printDBG ('Embed_URL1='+Embed_URL)
                            url_ = strwithmeta(Embed_URL, {'Referer':url})
                            printDBG('m3u8 trouver 08=' + url_)
                            if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
                            return [{'name':'LINK', 'url':url_, 'need_resolve':0}]                             
                
                return self.resolve_links(Embed_URL,'https://new.socolive.pro/',ipaudio)             
            printDBG('URL NOT FOUND DATA=' + data)             

        return []
        
        
        
        
        #if 'all.ive' in url: return (self.resolve_all_ive(url))
        #elif '1l1l.to' in url: return (self.resolve_all_ive(url))
        #elif 'l1l1.to' in url: return (self.resolve_L1L1(url))
        #elif 'emb.apl' in url: return (self.resolve_EMB(url))
        #elif 'maxsport.one' in url: return (self.resolve_MaxSport(url))
        #elif 'maxsport.one' in url: return (self.resolve_MaxSport(url))
        #if 'wikisport' in url: return (self.resolve_WikiSport(url,referer))

    def resolve_CDN(self,Embed_URL,referer,ipaudio=False):
        Params = dict(self.defaultParams)
        Params['header']['User-Agent'] = self.UA
        Params['header']['Referer'] = referer
        sts, data = self.getPage(Embed_URL,Params)                
        if sts:
            #printDBG('DATADATA='+data)
            data_els = re.findall('(eval\(function\(p,a,c,k,e,d\).*?)</script>', data, re.S)
            if data_els:
                data = cPacker().unpack(data_els[0].strip())
                lst_data = re.findall('var src="(.*?)"', data, re.S)
                if lst_data:
                    url_ = strwithmeta(lst_data[0], {'Referer':Embed_URL})
                    printDBG('url_='+url_)
                    if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
                    return [{'name':'LINK', 'url':url_, 'need_resolve':0}]        
        return []


    def resolve_Wecast(self,Embed_URL,referer,ipaudio=False):
        Params = dict(self.defaultParams)
        Params['header']['User-Agent'] = self.UA
        Params['header']['Referer'] = referer
        sts, data = self.getPage(Embed_URL,Params)                
        if sts:
            #printDBG('DATADATA='+data)
            data_els = re.findall('(eval\(function\(p,a,c,k,e,d\).*?)</script>', data, re.S)
            if data_els:
                data = cPacker().unpack(data_els[0].strip())
                printDBG('data_='+data)
                lst_data = re.findall('source:"(.*?)"', data, re.S)
                if not lst_data:
                    lst_data = re.findall('file:[\'"](.*?)[\'"]', data, re.S)
                if lst_data:    
                    url_ = strwithmeta(lst_data[0], {'Referer':Embed_URL})
                    printDBG('url_='+url_)
                    if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
                    return [{'name':'LINK', 'url':url_, 'need_resolve':0}]        
        return []




    def resolve_SawLive(self,Embed_URL,ipaudio=False):
        Params = dict(self.defaultParams)
        Params['header']['User-Agent'] = self.UA
        sts, data = self.getPage(Embed_URL,Params)                
        if sts:
            #printDBG('DATADATA='+data)
            data_els = re.findall('src="(.*?)"', data, re.S)
            if data_els:
                url = data_els[0]
                if url.startswith('//'): url = 'https:'+url
                #printDBG('src='+url)
                Params['header']['Referer'] = Embed_URL
                sts, data = self.getPage(url,Params)                
                if sts:
                    #printDBG('DATADATA='+data)
                    data_els = re.findall('var embedded =.{0,2}"(.*?)"', data, re.S)  
                    if not data_els:
                        print('embded not found')
                        return []
                    embedded = data_els[0]

                    #data_els = re.findall('var .+? = "([^;]+);([^\"]+)";', data, re.S)
                    data_els = re.findall('var.{0,20}"player=".*?"(.*?)"', data, re.S)          
                    if data_els:
                        #URL1 = "http://www.sawlive.tv/embedm/stream/" + data_els[0][1] + '/' + data_els[0][0]
                        URL1 = "https://www.sawlive.tv/embed_player.php?player=" + embedded + data_els[0]
                        #printDBG('sawlive Player URL = '+URL1)
                        Params['header']['Referer'] = url
                        sts, data = self.getPage(URL1,Params)                
                        if sts:
                            #printDBG('DATADATA='+data)                         
                            data_els = re.findall("{source:.{0,4}'(.*?)'", data, re.S)
                            if data_els: 
                                url_data = data_els[0]
                                meta = {'Referer':URL1,'User-Agent':self.UA}
                                url_=strwithmeta(url_data, meta)
                                if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
                                return([{'name':'SawLive', 'url':url_, 'need_resolve':0}])                           
                            data_els = re.findall('(eval\(function\(p,a,c,k,e,d\).*?}\)\))', data, re.S)
                            if not data_els:
                                data_els = re.findall('iframe src=[\'"](.*?)[\'"]', data, re.S)
                                if data_els:
                                    url_data = data_els[0]
                                    sts, data = self.getPage(url_data,Params)                                    
                                    if sts:
                                        data_els = re.findall('(eval\(function\(p,a,c,k,e,d\).*?}\)\))', data, re.S)
                            if data_els:    
                                data = cPacker().unpack(data_els[0].strip())
                                printDBG('DATADATA='+data) 
                                lst_data = re.findall('var.*?=.*?(\[.*?\]);', data, re.S)
                                if lst_data:
                                    jameiei = eval(lst_data[0])
                                    url_data = ''
                                    for c in jameiei:
                                        url_data += chr(c)
                                    printDBG('url_data='+url_data)
                                    meta = {'Referer':URL1,'User-Agent':self.UA}
                                    url_=strwithmeta(url_data, meta)
                                    if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
                                    return([{'name':'SawLive', 'url':url_, 'need_resolve':0}])
                            else:
                                data_els = re.findall('iframe src=[\'"](.*?)[\'"]', data, re.S)
                                if data_els:
                                    url_data = data_els[0]
                                    meta = {'Referer':URL1,'User-Agent':self.UA}
                                    url_=strwithmeta(url_data, meta)
                                    if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
                                    return([{'name':'SawLive', 'url':url_, 'need_resolve':0}])
                    else:
                        print('stream id not found!!')                                     
        return []



    def resolve_LiveStream(self,Embed_URL,ipaudio=False):
        data_els = re.findall('https://([^"]+)/player', Embed_URL, re.S)
        if data_els:
            accountid = data_els[0]
            jsonUrl = 'https://player-api.new.' + accountid + '?format=short'    
            printDBG('jsonUrl='+jsonUrl)
            Params = dict(self.defaultParams)
            Params['header']['User-Agent'] = self.UA            
            Params['header']['Referer'] = Embed_URL            
            sts, data = self.getPage(jsonUrl,Params)
            if sts:
                data_els = re.findall('"m3u8_url":"(.+?)"', data, re.S)
                if data_els:                    
                    url_data = data_els[0]
                    printDBG('url_data='+url_data)
                    meta = {'Referer':Embed_URL,'User-Agent':self.UA}
                    url_=strwithmeta(url_data, meta)
                    if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
                    return(getDirectM3U8Playlist(url_, checkExt=True, checkContent=True, sortWithMaxBitrate=999999999))
                    
                    #return([{'name':'LiveStream', 'url':url_, 'need_resolve':0}])
                data_els = re.findall('"start_time":"(.+?)"', data, re.S)
                if data_els:                    
                    start_time = data_els[0] 
                    SetIPTVPlayerLastHostError('Match will Start at: '+start_time)                    
        return []



    def resolve_EttuTv(self,Embed_URL):
        urlTab = []
        printDBG('resolve_EttuTv')
        printDBG('Embed_URL='+Embed_URL)
        id_els = re.findall('embed/(.*?)/', Embed_URL, re.S)
        if id_els:
            Api_Url = 'https://www.ettu.tv/api/v3/contents/'+id_els[0]+'/access/hls'
            Params = dict(self.defaultParams)
            Params['header']['User-Agent'] = self.UA            
            Params['header']['Referer'] = Embed_URL
            sts, data = self.getPage(Api_Url,Params,post_data={})                
            if sts:    
                printDBG('DATADATA='+data)
                response = json_loads(data)
                printDBG(str(response))
                url_ = response.get('data',{}).get('stream','')
                meta = {'Referer':'https://www.ettu.tv/','User-Agent':self.UA}
                url_=strwithmeta(url_, meta)
                urlTab = getDirectM3U8Playlist(url_, checkExt=True, checkContent=True, sortWithMaxBitrate=999999999)
                #urlTab.append({'name':'Youtube', 'url':url_, 'need_resolve':0})                 
        return urlTab 


    def resolve_Jokersplayer(self,Embed_URL,referer,ipaudio=False):
        printDBG('resolve_Jokersplayer')
        printDBG('Embed_URL='+Embed_URL)
        Params = dict(self.defaultParams)
        Params['header']['User-Agent'] = self.UA
        Params['header']['Referer'] = referer
        sts, data = self.getPage(Embed_URL,Params)                
        if sts:
            #printDBG('DATADATA='+data)
            data_els = re.findall("<div id='player'.{1,40}<iframe.{1,150}src=(.*?)>", data, re.S)
            if data_els:
                url_tab = data_els[0]
                printDBG('url_tab='+url_tab)
                Params['header']['Referer'] = Embed_URL
                sts, data = self.getPage(url_tab,Params)                
                if sts:
                    #printDBG('DATADATA='+data)
                    data_els = re.findall("<div id='player'.{1,40}<iframe.{1,150}src=(.*?)>", data, re.S)
                    if data_els:
                        url_tab1 = data_els[0]
                        if not url_tab1.startswith('http'):
                            url_els = re.findall("(http.*?//.*?/)", url_tab, re.S)
                            if url_els:
                                url_tab1 = url_els[0]+url_tab1
                                printDBG('url_tab='+url_tab1)
                                Params['header']['Referer'] = url_tab
                                sts, data = self.getPage(url_tab1,Params)                
                                if sts:
                                    #printDBG('DATADATA='+data)
                                    data_els = re.findall("source:.{1,3}'(.*?)'", data, re.S)
                                    if data_els:
                                        meta = {'Referer':url_tab1,'User-Agent':self.UA}
                                        url_=strwithmeta(data_els[0], meta)
                                        if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
                                        return [{'name':'Jokersplayer', 'url':url_, 'need_resolve':0}]                       
        return []
    
    
    
    
    




    def resolve_Vikistream(self,Embed_URL,referer,ipaudio=False):
        urlTab = []
        printDBG('resolve_Vikistream')
        printDBG('Embed_URL='+Embed_URL)
        Params = dict(self.defaultParams)
        Params['header']['User-Agent'] = self.UA
        Params['header']['Referer'] = referer
        sts, data = self.getPage(Embed_URL,Params)                
        if sts:
            #printDBG('DATADATA='+data)
            data_els = re.findall('return\(\[(.*?)\].*?\+(.*?)\..*?getElementById\("(.*?)"', data, re.S)
            if data_els:
                url_tab = data_els[0][0]
                timeVar = data_els[0][1].strip()
                hashVar = data_els[0][2].strip()
                url_ = ''.join(url_tab.split(','))
                url_ = url_.replace('"','').replace('\/', '/')
                if not url_.startswith('http'): url_ = 'http:' + url_
                printDBG('URL='+url_)
                printDBG('timeVar='+timeVar)
                timeVar_els = re.findall('var '+timeVar+' = \[(.*?)\]', data, re.S)
                hashVarSTR = ''
                timeVarSTR = ''
                if timeVar_els: timeVarSTR = ''.join(timeVar_els[0].split(',')).replace('"', '')
                printDBG('timeVarSTR='+timeVarSTR)
                url_ += timeVarSTR
                printDBG('hashVar='+hashVar) 
                hashVar_els = re.findall(hashVar+'>(.*?)<', data, re.S)
                if hashVar_els: hashVarSTR = ''.join(hashVar_els[0].split(',')).replace('"', '')
                printDBG('hashVarSTR='+hashVarSTR)
                url_ += hashVarSTR                        
                meta = {'Referer':'https://vikistream.com/','User-Agent':self.UA}
                url_=strwithmeta(url_, meta)
                if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
                urlTab.append({'name':'Vikistream', 'url':url_, 'need_resolve':0}) 
        return urlTab


    def resolve_EMB(self,url,ipaudio = False):
        printDBG('resolve_EMB Start')
        sts, data = self.getPage(url)
        if sts:        
            data_els = re.findall("pl.init\('(.*?)'", data, re.S)
            if data_els:
                meta = {'Referer':url,'User-Agent':self.UA}
                url_ = data_els[0]
                if url_.startswith('//'): url_ = 'http:'+url_
                url_=strwithmeta(url_, meta)
                if ipaudio: self.addtoipaudio({'url':url_,'titre':url_})
                return [{'name':'EMB', 'url':url_, 'need_resolve':0}]            
        return []

    def resolve_MaxSport(self,url):
        printDBG('rresolve_MaxSport Start')
        sts, data = self.getPage(url)
        if sts:        
            data_els = re.findall('iframe src="(.*?)"', data, re.S)
            if data_els:
                Url = data_els[0]
                if Url.startswith('//'): Url = 'http:'+Url
                printDBG('DATADATA='+Url)
                sts, data = self.getPage(Url)
                if sts:        
                    data_els = re.findall('iframe src="(.*?)"', data, re.S)
                    if data_els:
                        URL = data_els[0]
                        printDBG('DATADATA='+URL)
                        Params = dict(self.defaultParams)
                        Params['header']['User-Agent'] = self.UA
                        Params['header']['Referer'] = Url
                        sts, data = self.getPage(URL,Params)                
                        if sts:
                            printDBG('DATADATA='+data)
                            data_els = re.findall("[^/]source:'(.*?)'", data, re.S)
                            if data_els:
                                URL_ = data_els[0]
                                printDBG('DATADATA='+URL_)
                                meta = {'Referer':URL,'User-Agent':self.UA}
                                url_=strwithmeta(URL_, meta)
                                return url_                                              
        return ''

    def resolve_WikiSport(self,url,referer):
        urlTab = []
        printDBG('resolve_WikiSport Start')
        Params = dict(self.defaultParams)
        Params['header']['User-Agent'] = self.UA
        Params['header']['Referer'] = referer        
        sts, data = self.getPage(url,Params)
        if sts:        
            data_els = re.findall('<iframe src="(.*?)"', data, re.S)
            if data_els:      
                return self.resolve_all_ive(data_els[0],referer = url)
            if sts:                  
                data_els = re.findall("strm = window.atob\('(.*?)'\)", data, re.S)
                if data_els:    
                    Url = base64.b64decode(data_els[0])
                    if not Url.startswith('http'): Url = 'http://wikisport.click'+Url
                    UA = "ozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
                    meta = {'Referer':'http://wikisport.click/','User-Agent':UA,'Origin':'http://wikisport.click','sec-ch-ua':'"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                            'Accept':'*/*','Accept-Encoding':'gzip, deflate, br','Accept-Language':'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7','Connection':'keep-alive',
                            'Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'cross-site','sec-ch-ua-mobile':'?0','sec-ch-ua-platform':'"Windows"'}
                    url_=strwithmeta(Url, meta)                
                    #urlTab.extend(getDirectM3U8Playlist(url_, checkExt=False, checkContent=True, sortWithMaxBitrate=999999999))
                    printDBG('URLATOB='+  str(url_))  
                    return url_
        return ''







    def resolve_all_ive(self,url,referer=''):
        printDBG('resolve_all_ive tart')
        Params = dict(self.defaultParams)
        Params['header']['User-Agent'] = self.UA
        if referer != '':
            Params['header']['Referer'] = referer         
        sts, data = self.getPage(url,Params)
        if sts:        
            data_els = re.findall("<script>fid=['\"](.+?)['\"].*?src=['\"](.*?)['\"]", data, re.S)        
            if data_els:
                Embed_URL = data_els[0][1].replace('.js','.php')+'?player=desktop&live='+data_els[0][0]
                if Embed_URL.startswith('//'): Embed_URL = 'http:'+Embed_URL
                printDBG('Embed_URL='+Embed_URL)
                Params = dict(self.defaultParams)
                Params['header']['User-Agent'] = self.UA
                Params['header']['Referer'] = url
                sts, data = self.getPage(Embed_URL,Params)                
                if sts:
                    #printDBG('DATADATA='+data)
                    data_els = re.findall('return\(\[(.*?)\].*?\+(.*?)\..*?getElementById\("(.*?)"', data, re.S)
                    if data_els:
                        url_tab = data_els[0][0]
                        timeVar = data_els[0][1].strip()
                        hashVar = data_els[0][2].strip()
                        url_ = ''.join(url_tab.split(','))
                        url_ = url_.replace('"','').replace('\/', '/')
                        if not url_.startswith('http'): url_ = 'http:' + url_
                        printDBG('URL='+url_)
                        printDBG('timeVar='+timeVar)
                        timeVar_els = re.findall('var '+timeVar+' = \[(.*?)\]', data, re.S)
                        hashVarSTR = ''
                        timeVarSTR = ''
                        if timeVar_els: timeVarSTR = ''.join(timeVar_els[0].split(',')).replace('"', '')
                        printDBG('timeVarSTR='+timeVarSTR)
                        url_ += timeVarSTR
                        printDBG('hashVar='+hashVar) 
                        hashVar_els = re.findall(hashVar+'>(.*?)<', data, re.S)
                        if hashVar_els: hashVarSTR = ''.join(hashVar_els[0].split(',')).replace('"', '')
                        printDBG('hashVarSTR='+hashVarSTR)
                        url_ += hashVarSTR                        
                        meta = {'Referer':'https://vikistream.com/','User-Agent':self.UA}
                        url_=strwithmeta(url_, meta)
                        return url_

    def resolve_L1L1(self,url):
        printDBG('resolve_L1L1 Start')
        sts, data = self.getPage(url)
        if sts:        
            data_els = re.findall("<iframe src='(.*?)'", data, re.S)        
            if data_els:
                Embed_URL = data_els[0]
                if Embed_URL.startswith('//'): Embed_URL = 'http:'+Embed_URL
                printDBG('Embed_URL='+Embed_URL)
                Params = dict(self.defaultParams)
                Params['header']['User-Agent'] = self.UA
                Params['header']['Referer'] = url
                sts, data = self.getPage(Embed_URL,Params)                
                if sts:
                    #printDBG('DATADATA='+data)
                    data_els = re.findall('(eval\(function\(p,a,c,k,e,d\).*?)</script>', data, re.S)
                    if data_els:
                        data = cPacker().unpack(data_els[0].strip())
                        lst_data = re.findall('var src="(.*?)"', data, re.S)
                        if lst_data:
                            url_ = strwithmeta(lst_data[0], {'Referer':Embed_URL})
                            printDBG('url_='+url_)
                            return url_        
        return ''


    def show_MaxSport(self,cItem):
        printDBG('MaxSport')
        url   = cItem.get('url','') 
        sts, data = self.getPage(url)
        if sts:
            data_els = re.findall('class="grid-item">.*?href="(.*?)".*?>(.*?)</div>', data, re.S)  
            for (Url,Titre) in data_els:
                    Titre = self.cleanHtmlStr(Titre).strip()
                    if not Url.startswith('http'): Url = url + Url
                    self.addVideo({'import':cItem['import'],'category' : 'host2','url': Url,'title':Titre,'desc':'','icon':cItem.get('icon',''),'sub_mode':1 ,'hst':'tshost'})    
        return ''


    def show_1l1l(self,cItem):
        printDBG('show_1l1l')
        url   = cItem.get('url','') 
        gnr   = cItem.get('sub_mode',0)
        if gnr==0:
            url = url + '/program'
            TAB = [('Online TV',url, '100',1),('Only Live',url, '100',2),]
            self.add_menu(cItem,'','','','','',TAB=TAB)           
        elif gnr==1:
            sts, data = self.getPage(url)
            if sts:
                data_els = re.findall('class="styled-table">(.*?)</table', data, re.S)  
                if data_els:
                    data_els = re.findall('<a href="(.*?)".*?>(.*?)</td>', data_els[0], re.S)
                    for (Url,Titre) in data_els:
                        Titre = self.cleanHtmlStr(Titre).strip()
                        self.addVideo({'import':cItem['import'],'category' : 'host2','url': Url,'title':Titre,'desc':'','icon':cItem.get('icon',''),'sub_mode':1 ,'hst':'tshost'})    
        elif gnr==2:
            sts, data = self.getPage(url)
            if sts:
                data_els = re.findall('<table>(.*?)</table>.*?<div class=.*?>(.*?)</div>', data, re.S)   
                for (data0,titres) in data_els:
                    titres = titres.strip()
                    if '\n' in titres:
                        titre_ = titres.split('\n')
                    else:
                        titre_ = [titres]
                    for titre in titre_:
                        self.addMarker({'title':tscolor('\c0000????')+titre.strip(),'desc':titres})	
                        data_ch = re.findall('class="infoch".*?title="(.*?)"', data0, re.S)
                        if data_ch:
                            ch_name = data_ch[0]
                        else: ch_name = ''
                        data_els = re.findall('<input type="text1".*?title="(.*?)".*?src="(.*?)"', data0, re.S) 
                        for titre0,url in data_els:
                            titre0 = ch_name+' - '+titre0
                            if '1l1l' in url: titre0 = titre0 + ' (1l1l.to)'
                            elif 'l1l1' in url: titre0 = titre0 + ' (l1l1.to)'  
                            elif 'bedsport' in url: titre0 = titre0 + ' (bedsport.live)'                          
                            self.addVideo({'import':cItem['import'],'category' : 'host2','url': url,'title':titre0,'desc':titre0,'icon':cItem.get('icon',''),'sub_mode':1 ,'hst':'tshost'})    
        return ''

    def show_WikiSport(self,cItem):
        printDBG('show_WikiSport')
        url   = cItem.get('url','') 
        gnr   = cItem.get('sub_mode',0)
        if gnr==0:
            TAB = [('Online TV',url + '/live-tv-channel/', '102',1),('Online TV (List2)',url, '102',4),('Live Sport',url, '102',3),]
            self.add_menu(cItem,'','','','','',TAB=TAB)           
        elif gnr==1:
            sts, data = self.getPage(url)
            if sts:
                data_els = re.findall('<section class="elementor-section(.*?)</section', data, re.S)  
                for data0 in data_els:
                    data_els0 = re.findall('data-element_type="column">.*?<a href="(.*?)".*?<img.*?src="(.*?)".*?class="button">(.*?)<', data0, re.S)
                    for (Url,image,Titre) in data_els0:
                        Titre = self.cleanHtmlStr(Titre).strip()
                        self.addDir({'import':cItem['import'],'category' : 'host2','url': Url,'title':Titre,'desc':'','icon':image,'mode':'102','sub_mode':5 })    
        elif gnr==4:
            sts, data = self.getPage(url)
            if sts:
                data_els = re.findall('class="main-nav">(.*?)<div id="footer', data, re.S)  
                for data0 in data_els:
                    data_els0 = re.findall('<li.*?<a href="(.*?)".*?>(.*?)</a>', data0, re.S)
                    for (Url,Titre) in data_els0:
                        Titre = self.cleanHtmlStr(Titre).strip()
                        self.addDir({'import':cItem['import'],'category' : 'host2','url': Url,'title':Titre,'desc':'','icon':cItem.get('icon',''),'mode':'102','sub_mode':5 })    
        elif gnr==5:
            sts, data = self.getPage(url)
            if sts:
                data_els = re.findall('<iframe src="(.*?)"', data, re.S)  
                if data_els:
                    sts, data0 = self.getPage(data_els[0])
                    if sts:
                        data_els0 = re.findall('href="(.*?)".*?>(.*?)</a>', data0, re.S)
                        for (Url,Titre) in data_els0:
                            Titre = self.cleanHtmlStr(Titre).strip()
                            self.addVideo({'import':cItem['import'],'category' : 'host2','url': Url,'title':Titre,'desc':Url,'icon':cItem.get('icon',''),'sub_mode':1,'hst':'tshost','referer':url })    
                    return ''
                data_els = re.findall('<section class="elementor-section(.*?)</section', data, re.S)  
                if data_els:
                    for data0 in data_els:
                        data_els0 = re.findall('data-element_type="column">.*?<a href="(.*?)".*?role="button">(.*?)</span>', data0, re.S)
                        if not data_els0:
                            data_els0 = re.findall('<h4.*?<a href="(.*?)".*?>(.*?)<', data, re.S)
                        for (Url,Titre) in data_els0:
                            Titre = self.cleanHtmlStr(Titre).strip()
                            self.addDir({'import':cItem['import'],'category' : 'host2','url': Url,'title':Titre,'desc':'','icon':cItem.get('icon',''),'mode':'102','sub_mode':5 })    
        return ''

    def show_Klubsports(self,cItem):
        printDBG('show_Klubsports')
        url   = cItem.get('url','') 
        gnr   = cItem.get('sub_mode',0)
        if gnr==0:
            TAB = [('Online TV',url , '103',1),('Live Sport',url, '103',2),]
            self.add_menu(cItem,'','','','','',TAB=TAB)           
        elif gnr==1:
            sts, data = self.getPage(url)
            if sts:
                data_els = re.findall('<a href="(.*?)".*?#ff0000;">(.*?)<', data, re.S)  
                for (Url,Titre) in data_els:
                    Titre = self.cleanHtmlStr(Titre).strip()    
                    if Url.startswith('/'): Url = url+Url
                    self.addVideo({'import':cItem['import'],'category' : 'host2','url': Url,'title':Titre,'desc':Url,'icon':cItem.get('icon',''),'sub_mode':1,'hst':'tshost','referer':url })    
        elif gnr==2:
            sts, data = self.getPage(url)
            if sts:
                data_els0 = re.findall('(?:<br /><br />|<br><p>)(.*?)<.*?>(.*?)<.*?href="(.*?)"', data, re.S)
                for (Titre,ch,Url) in data_els0:
                    Titre = self.cleanHtmlStr(Titre).strip()
                    ch = self.cleanHtmlStr(ch).strip()
                    Titre = Titre+tscolor('\c00????00')+' ('+ch+')'
                    self.addVideo({'import':cItem['import'],'category' : 'host2','url': Url,'title':Titre,'desc':Url,'icon':cItem.get('icon',''),'sub_mode':1,'hst':'tshost','referer':url })          
        return ''
        
    def getVideos(self,videoUrl):
        urlTab = []
        printDBG('GETVIDEOOOOOOO='+videoUrl)
        url,url_ = videoUrl.split('||||')
        URL = self.resolve_links(url,url_)
        if '/hls/' in URL:
            urlTab.append((URL,'0'))	
        else:
            urlTab.append((URL,'7||||http://gytyc.herokuapp.com/'))	
            #printDBG(str(urlTab))
        return urlTab
        
        
    def addtoipaudio(self,cItem):
        #try:
        elm = {"channel":cItem['titre'],"url":cItem['url']}
        with open('/etc/enigma2/ipaudio.json', 'r')as f:
            playlist = json.loads(f.read())
        playlist['playlist'].append(elm)
        with open('/etc/enigma2/ipaudio.json', 'w') as f:
            json.dump(playlist, f, indent=4) 
        self.addMarker({'title':tscolor('\c00????00')+'#'+cItem['titre']+'# Successfully added'})	
        #except Exception as e:
        #    self.addMarker({'title':tscolor('\c00??0000')+'#'+cItem['titre']+'# Not added (Error)','desc':str(e)})	   
        




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
        elif mode=='100':
            self.show_1l1l(cItem)    
        elif mode=='101':
            self.show_MaxSport(cItem)  
        elif mode=='102':
            self.show_WikiSport(cItem)              
        elif mode=='103':
            self.show_Klubsports(cItem)  
        return True    
