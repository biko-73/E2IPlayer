# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,gethostname
import re


from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import \
    TranslateTXT as _
from Plugins.Extensions.IPTVPlayer.libs import ph


def getinfo():
    info_={}
    name = 'MovizTime'
    hst = 'https://movt.site'
    info_['old_host'] = hst
    hst_ = tshost(name)
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='1.2 02/08/2023'
    info_['dev']='MOHAMED_OS'
    info_['cat_id']='21'
    info_['desc']='أفلام, مسلسلات اجنبية'
    info_['icon']='https://i.ibb.co/QNp7dsj/moviztime.png'
    info_['recherche_all']='1'
    return info_


class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{})
        self.MAIN_URL       =  getinfo()['host']
        self.cacheLinks = {}

    def showmenu(self,cItem):
        TAB = [(tscolor('\c0000??00') + ' تصفية متقدمة','','10','filter'),('أفـــــلام','','10','film'),('مــسـلـسـلات','/category/مسلسلات-أجنبية-مترجمة-d/','20','serie'),
            ('الأنـمـي','','10','anime'),('برامج تلفزيونية','/category/برامج-تلفزيونية/','20','other')]
        self.add_menu(cItem,'','','','','',TAB=TAB,search=False)
        self.addDir({'import':cItem['import'],'category' : 'search','title': _('Search'), 'search_item':True,'page':1,'hst':'tshost','icon':cItem['icon']})

    def showmenu1(self,cItem):
        gnr = cItem['sub_mode']
        if gnr == 'film':
            self.MovizTime_TAB = [
                {'category':'host2','title': 'أفــلام أجنـبيـة','url':self.MAIN_URL+'/category/أفلام-أجنبية/', 'mode':'20'},
                {'category':'host2','title': 'أفــلام أوروبـية','url':self.MAIN_URL+'/category/أفلام-أوروبية/',  'mode':'20'},
                {'category':'host2','title': 'أفــلام تـركـيـة','url':self.MAIN_URL+'/category/أفلام-تركية/',  'mode':'20'},
                {'category':'host2','title': 'أفــلام هنــديـة','url':self.MAIN_URL+'/category/أفلام-هندية/',  'mode':'20'},
                {'category':'host2','title': 'أفــلام آسـيـويـة','url':self.MAIN_URL+'/category/أفلام-آسيوية-مترجمة/',  'mode':'20'},
                {'category':'host2','title': 'أفــلام وثائـقـية','url':self.MAIN_URL+'/category/أفلام-وثائقية/',  'mode':'20'}]
        elif gnr == 'anime':
            self.MovizTime_TAB = [
                {'category':'host2','title': 'أفــلام أنـمـي','url':self.MAIN_URL+'/category/قائمة-الأنمي-b/أفلام-أنمي/', 'mode':'20'},
                {'category':'host2','title': 'مسـلـسـلات أنـمـي','url':self.MAIN_URL+'/category/قائمة-الأنمي-b/مسلسلات-أنمي/',  'mode':'20'}]
        elif gnr == 'filter':
            self.MovizTime_TAB = [
                {'category':'host2','title': 'IMDb Top 250','url':self.MAIN_URL+'/category/imdb-top-250/', 'mode':'20'},
                {'category':'host2','title': 'أكـشــن','url':self.MAIN_URL+'/category/أفلام-أجنبية/action/', 'mode':'20'},
                {'category':'host2','title': 'أنيميشن','url':self.MAIN_URL+'/category/أنيميشن/',  'mode':'20'},
                {'category':'host2','title': 'كوميديا','url':self.MAIN_URL+'/category/أفلام-أجنبية/comedy/',  'mode':'20'},
                {'category':'host2','title': 'قصة حقيقية','url':self.MAIN_URL+'/category/قصة-حقيقية/',  'mode':'20'},
                {'category':'host2','title': 'دراما','url':self.MAIN_URL+'/category/أفلام-أجنبية/drama/',  'mode':'20'},
                {'category':'host2','title': 'رعب','url':self.MAIN_URL+'/category/أفلام-أجنبية/رعب-مترجم/', 'mode':'20'},
                {'category':'host2','title': 'عائلى','url':self.MAIN_URL+'/category/عائلي/',  'mode':'20'},
                {'category':'host2','title': 'حروب','url':self.MAIN_URL+'/category/حروب/',  'mode':'20'},
                {'category':'host2','title': 'الجريمة','url':self.MAIN_URL+'category/أفلام-أجنبية/افلام-جريمة/',  'mode':'20'},
                {'category':'host2','title': 'رومانسى','url':self.MAIN_URL+'/category/أفلام-أجنبية/رومانسي/', 'mode':'20'},
                {'category':'host2','title': 'خيال علمى','url':self.MAIN_URL+'/category/خيال-علمي/',  'mode':'20'},
                {'category':'host2','title': 'اثارة','url':self.MAIN_URL+'/category/اثارة/',  'mode':'20'},
                {'category':'host2','title': 'وثائقى','url':self.MAIN_URL+'/category/وثائقي/',  'mode':'20'},
                {'category':'host2','title': 'غموض','url':self.MAIN_URL+'/category/غموض/',  'mode':'20'}]

        self.listsTab(self.MovizTime_TAB, {'import':cItem.get('import',''),'icon':cItem.get('icon','')})

    def showitms(self,cItem):
        if 'أفلام-تركية' in cItem.get('url'):
            URL = cItem.get('url')
        else:
            page = cItem.get('page',1)
            URL = cItem.get('url','')+'page/'+str(page)+'/'

        sts, data = self.getPage(URL)
        if sts:
            Liste_els = re.findall(r'class="thumb">.+?href="([^"]+)" title="([^"]+)">.+?src="([^"]+)', data, re.S)
            for (url,titre,image) in Liste_els:
                info  = self.std_title(ph.clean_html(titre),with_ep=True)
                self.addDir({'import':cItem['import'],'category' : 'host2','title':info.get('title_display'),'icon':self.std_url(image),'desc':info.get('desc'),'mode':'21','url':url,'good_for_fav':True,'EPG':True,'hst':'tshost'})
        if 'page' in URL:
            self.addDir({'import':cItem['import'],'category' : 'host2','title':tscolor('\c00????00')+'Next Page >>'+tscolor('\c00??????'),'icon':cItem['icon'],'desc':'','mode':'20','url':cItem['url'],'page':page+1})


    def showelms(self,cItem):
        URL = cItem.get('url')
        sts, data = self.getPage(URL)
        if sts:
            if 'series' in URL or 'anime' in URL:
                sData = re.findall('servers-block">(.*?)servers-block">', data, re.S)[0]
                Liste_els = re.findall("selected.+?\">([^>]+)</", sData, re.S)
                if Liste_els:
                    for titre in Liste_els:
                        self.addVideo({'import':cItem['import'], 'hst':'tshost', 'url':cItem['url'], 'title':ph.clean_html(titre), 'desc':'','icon':cItem['icon'],'good_for_fav':True,'EPG':True,'hst':'tshost'})
            else:
                self.addVideo({'import':cItem['import'], 'hst':'tshost', 'url':cItem['url'], 'title':cItem['title'], 'desc':'','icon':cItem['icon'],'good_for_fav':True,'EPG':True,'hst':'tshost'})

    def get_links(self,cItem):
        URL = cItem.get('url')
        sTitel = cItem.get('title')
        if 'series' in URL or 'anime' in URL:
            return self.ServerLink2(URL,sTitel)
        else:
            return self.ServerLink(URL)

    def SearchResult(self,str_ch,page,extra):
        URL=self.MAIN_URL+'/search/'+str_ch+'/page/'+str(page)
        sts, data = self.getPage(URL)
        if sts:
            Liste_els = re.findall(r'class="thumb">.+?href="([^"]+)" title="([^"]+)">.+?src="([^"]+)', data, re.S)
            for (url,titre,image) in Liste_els:
                info  = self.std_title(titre,with_ep=True)
                sTitel = info.get('title_display')
                desc_ = info.get('desc')
                self.addDir({'import':extra,'category' : 'host2','title':sTitel,'icon':self.std_url(image),'desc':desc_,'mode':'21','url':url,'good_for_fav':True})

    def getArticle(self,cItem):
        URL = cItem.get('url')
        if 'series' in URL or 'anime' in URL:
            Desc = [('Year','ttl">سنة الإنتاج:.+?cntt">(.+?)</','\n',''),('Generes','ttl">نوع المسلسل:.+?cntt">(.+?)</','\n',''),('Quality','ttl">جودة المسلسل:.+?cntt">(.+?)</','\n',''),('Story','ttl">قصة المسلسل:.+?cntt">(.+?)</','\n',''),
                    ('Season','ttl">الموسم:.+?cntt">(.+?)</','\n',''),('Episode','ttl">عدد الحلقات:.+?cntt">(.+?)</','\n','')]
        else:
            Desc = [('Year','ttl">سنة الإنتاج:.+?cntt">(.+?)</','\n',''),('Generes','ttl">نوع الفيلم:.+?cntt">(.+?)</','\n',''),('Rate','ttl">تقييم الفيلم:.+?cntt">(.+?)</','\n',''),
                    ('Quality','ttl">جودة الفيلم:.+?cntt">(.+?)</','\n',''),('Story','ttl">قصة الفيلم:.+?cntt">(.+?)</','\n','')]
        desc = self.add_menu(cItem,'','@media(.+?)shorten_post_url"','','desc',Desc=Desc)
        if desc =='': desc = cItem.get('desc','')
        return [{'title':cItem['title'], 'text': desc, 'images':[{'title':'', 'url':cItem.get('icon','')}], 'other_info':{}}]

    # Show Server Movei
    def ServerLink(self,BaseUrl):
        urlTab = []
        sts, data = self.getPage(BaseUrl)
        if sts:
            sRefer = re.findall(r'<p class="logo">.+?<a href="([^"]+)' , data, re.S)[0]
            url_dat_1 = re.findall(r'data-src="([^"]+)', data, re.S)
            for Url in url_dat_1:
                #urlTab.append({'name':'|Watch Server| '+ gethostname(Url,True), 'url':Url+'|Referer='+sRefer, 'need_resolve':1,'type':'local'})
                urlTab.append({'name':'|Watch Server| '+ gethostname(Url), 'url':Url+'|Referer='+sRefer, 'need_resolve':1,'type':'local'})
            url_dat_2 = re.findall(r'data-target-tab.+?href="([^"]+)"', data, re.S)[0]
            if url_dat_2:
                sts, data = self.getPage(url_dat_2)
                if sts:
                    sData = re.findall(r'@media(.+?)</div>', data, re.S)[0]
                    if sData:
                        siteUrl = re.findall(r'href="([^"]+)"', sData, re.S)
                        for url_2 in siteUrl:
                            urlTab.append({'name':'|Downl Server| '+ gethostname(url_2), 'url':url_2, 'need_resolve':1,'type':'local'})
        return urlTab

    # Show Server Tv Show
    def ServerLink2(self,BaseUrl,BaseTitel):
        urlTab = []
        siteUrl = []
        sts, data = self.getPage(BaseUrl)
        if sts:
            sRefer = re.findall(r'<p class="logo">.+?<a href="([^"]+)' , data, re.S)[0]
            sName1 = {}
            Server1 = re.findall(r'<div class="title">السيرفر الأول</div>(.+?)<div class="servers-block">', data, re.S)
            if Server1:
                data1 = re.findall(r"onclick=.+?.href='([^']+).+?>(.+?)</button>", Server1[0], re.S)
                for (value,key) in data1:
                    sName1.setdefault(key,value)
            sName2 = {}
            Server2 = re.findall(r'<div class="title">السيرفر الثاني</div>(.+?)<style type="text/css">', data, re.S)
            if Server2:
                data2 = re.findall(r"onclick=.+?.href='([^']+).+?>(.+?)</button>", Server2[0], re.S)
                for (value,key) in data2:
                    sName2.setdefault(key,value)

            siteUrl.append(sName1.get(BaseTitel))
            siteUrl.append(sName2.get(BaseTitel))

            for Url in siteUrl:
                urlTab.append({'name':'|Watch Server| '+ gethostname(Url), 'url':Url+'|Referer='+sRefer, 'need_resolve':1,'type':'local'})
            url_dat_2 = re.findall(r'download_btn.+?href="([^"]+)"', data, re.S)[0]
            if url_dat_2:
                sts, data = self.getPage(url_dat_2)
                if sts:
                    sData = re.findall(r'@media(.+?)</div>', data, re.S)[0]
                    if sData:
                        siteUrl = re.findall(r'href="([^"]+)"', sData, re.S)
                        for url_2 in siteUrl:
                            urlTab.append({'name':'|Downl Server| '+ gethostname(url_2), 'url':url_2, 'need_resolve':1,'type':'local'})
        return urlTab

