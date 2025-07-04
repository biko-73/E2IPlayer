# -*- coding: utf-8 -*-

###################################################
# LOCAL import
###################################################
#from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, printExc, byteify
###################################################

###################################################
# FOREIGN import
###################################################
#try:
import json
#except Exception:
#    import simplejson as json
#e2icjson = None
############################################


def loads(inputString, noneReplacement=None, baseTypesAsString=False, utf8=True):
#    global e2icjson
#    e2icjson = False
#    if e2icjson == None:
#        try:
#            from Plugins.Extensions.IPTVPlayer.libs.e2icjson import e2icjson
#            e2icjson = e2icjson
#        except Exception:
#            e2icjson = False
#            printExc()
#    if e2icjson:
#        printDBG(">> cjson ACELERATION noneReplacement[%s] baseTypesAsString[%s]" % (noneReplacement, baseTypesAsString))
#        out = e2icjson.decode(input, 2 if utf8 else 1)
        #if noneReplacement != None or baseTypesAsString != False:
        #    printDBG(">> cjson ACELERATION byteify")
        #    out = byteify(out, noneReplacement, baseTypesAsString)
#    else:
    return json.loads(inputString)
        #if utf8 or noneReplacement != None or baseTypesAsString != False:
        #    out = byteify(out, noneReplacement, baseTypesAsString)
#    return out


def dumps(inputString, *args, **kwargs):
    return json.dumps(inputString, *args, **kwargs)
