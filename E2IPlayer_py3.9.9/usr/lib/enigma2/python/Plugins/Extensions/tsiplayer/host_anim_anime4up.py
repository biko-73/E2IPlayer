# -*- coding: utf-8 -*-
import re

from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import (
    TSCBaseHostClass, tscolor, tshost)


def getinfo():
    info_={}
    name = 'Anime4up'
    hst = tshost(name)
    if hst=='': hst = 'https://w1.anime4up.tv'
    info_['host']= hst
    info_['name']=name
    info_['version']='1.0 22/11/2021'
    info_['dev']='RGYSoft'
    info_['cat_id']='22'
    info_['desc']='جميع الإنميات مترجمة عربي، والأفلام والأوفات'
    info_['icon']='https://i.ibb.co/zxHHDQG/Anime4up.png'
    info_['recherche_all']='0'
    info_['update']='New Site'
    return info_


class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'anime4up.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        self.MAIN_URL = getinfo()['host']
        self.HEADER = {'User-Agent': self.USER_AGENT, 'Connection': 'keep-alive', 'Accept-Encoding':'gzip', 'Content-Type':'application/x-www-form-urlencoded','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
        self.defaultParams = {'header':self.HEADER, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        #self.getPage = self.cm.getPage


    def getPage(self, baseUrl, addParams = {}, post_data = None):
        baseUrl=self.std_url(baseUrl)
        if addParams == {}: addParams = dict(self.defaultParams)
        addParams['cloudflare_params'] = {'cookie_file':self.COOKIE_FILE, 'User-Agent':self.USER_AGENT}
        return self.cm.getPageCFProtection(baseUrl, addParams, post_data)

    def showmenu0(self,cItem):
        hst='host2'
        Animekom_TAB = [
                            {'category':hst,      'title':'قائمة الأنميات'     , 'mode':'30', 'url':self.MAIN_URL+'/anime-list-3/'},
                            {'category':hst,      'title':'قائمة الأفلام'      , 'mode':'30', 'url':self.MAIN_URL+'/anime-type/movie-3/'},
                            {'category':hst,      'title':'آخر الحلقات المضافة'  , 'mode':'30', 'url':self.MAIN_URL+'/episode/','sub_mode':1},
                            #{'category':hst,      'title':'حلقات الأنمي المثبتة'   , 'mode':'21', 'sub_mode':0},
                            #{'category':hst,      'title':'آخر الأنميات المضافة'  , 'mode':'21', 'sub_mode':2},
                            {'category':hst,      'title': tscolor('\c0000??00')+'تصنيف الأنمي'      , 'mode':'22', 'sub_mode':0},
                            {'category':hst,      'title': tscolor('\c0000??00')+'نوع الأنمي'      , 'mode':'22', 'sub_mode':1},
                            {'category':'search', 'title':_('Search')  ,'search_item':True,'page':1,'hst':'tshost'},
                            ]
        self.listsTab(Animekom_TAB, {'icon':cItem['icon'],'import':cItem['import']})

    def showmenu_22(self,cItem):
        Url=self.MAIN_URL+'/anime-type/movie/'
        gnr=cItem.get('sub_mode',0)
        if gnr == 0: pat = 'genresDropdown">(.*?)</ul'
        else:
            pat = 'typeDropdown">(.*?)</ul'
        sts, data = self.getPage(Url)
        if sts:
            Cat_data = re.findall(pat,data, re.S)
            if Cat_data:
                list_cat=re.findall('href="(.*?)">(.*?)<', Cat_data[0], re.S)
                for (url,titre) in list_cat:
                    if '18' not in titre:
                        self.addDir({'import':cItem['import'],'good_for_fav':True,'category' : 'host2','url': url,'title':titre,'desc':titre,'icon':cItem['icon'],'mode':'30','sub_mode':2})

    def showitms(self,cItem):
        Url=cItem['url']
        page=cItem.get('page',1)
        gnr=cItem.get('sub_mode',0)
        sUrl=Url+'page/'+str(page)+'/'
        sts, data = self.getPage(sUrl)
        if sts:
            #_data = re.findall('class="img-responsive.*?src="(.*?)".*?href="(.*?)"(.*?)title="(.*?)"(.*?)</div>',data, re.S)
            _data = re.findall('anime-card-container">(.*?)class="img-responsive.*?src="(.*?)".*?href="(.*?)"(.*?)title="(.*?)"(.*?)</div>',data, re.S)
            for (ep,image,url,desc,titre,desc1) in _data:
                desc=self.cleanHtmlStr('<'+desc+'>')
                desc= tscolor('\c00????00')+'Info: '+tscolor('\c00??????')+desc
                ep =self.cleanHtmlStr(ep+'>')
                if not image.startswith('http'): image = self.MAIN_URL+image
                if ep.strip()!='':
                    titre = self.cleanHtmlStr(titre)+' ['+tscolor('\c0000????')+ep.strip()+tscolor('\c00??????')+'] '
                else: titre = self.cleanHtmlStr(titre)
                _desc = re.findall('data-content="(.*?)"',desc1, re.S)
                if _desc: desc= desc+'\n'+tscolor('\c00????00')+'Story: '+tscolor('\c00??????')+self.cleanHtmlStr(_desc[0])

                if gnr==1:
                    self.addVideo({'import':cItem['import'],'good_for_fav':True,'category' : 'host2','title':titre,'desc':desc,'icon':image,'hst':'tshost','url':url} )
                else:
                    self.addDir({'import':cItem['import'],'good_for_fav':True,'category' : 'host2','url': url,'title':titre,'desc':desc,'icon':image,'hst':'tshost','mode':'31'} )
            if gnr!=2:
                self.addDir({'import':cItem['import'],'category' : 'host2','url': cItem['url'],'title':tscolor('\c0090??20')+_('Next page'),'page':page+1,'icon':cItem['icon'],'mode':'30','sub_mode':gnr} )

    def showelems(self,cItem):
        sts, sHtmlContent = self.getPage(cItem['url'])
        if sts:
            desc = self.get_info(sHtmlContent)
            Liste_Episodes_data = re.findall('(youtu.be.*?)"', sHtmlContent, re.S)
            if not Liste_Episodes_data: Liste_Episodes_data = re.findall('(youtube.com.*?)"', sHtmlContent, re.S)
            if Liste_Episodes_data:
                trailer = Liste_Episodes_data[0].replace('youtu.be/','youtube.com/watch?v=')
                self.addVideo({'import':cItem['import'],'good_for_fav':True,'category' : 'host2','title':'Trailer','desc':desc,'icon':cItem['icon'],'hst':'none','url':'https://www.'+trailer} )
            Name_Episodes_data = re.findall('episodes-card-title">.*?href="(.*?)".*?>(.*?)<.*?src="(.*?)"', sHtmlContent, re.S)
            for (url,titre,image) in Name_Episodes_data:
                self.addVideo({'import':cItem['import'],'good_for_fav':True,'category' : 'host2','title':titre,'desc':desc,'icon':image,'hst':'tshost','url':url} )

    def SearchResult(self,str_ch,page,extra):
        url_=self.MAIN_URL+'/?search_param=animes&s='+str_ch
        sts, data = self.getPage(url_)
        if sts:
            _data = re.findall('anime-card-container">(.*?)class="img-responsive.*?src="(.*?)".*?href="(.*?)"(.*?)title="(.*?)"(.*?)</div>',data, re.S)
            for (ep,image,url,desc,titre,desc1) in _data:
                desc=self.cleanHtmlStr('<'+desc+'>')
                desc= tscolor('\c00????00')+'Info: '+tscolor('\c00??????')+desc
                ep =self.cleanHtmlStr(ep+'>')
                if not image.startswith('http'): image = self.MAIN_URL+image
                if ep.strip()!='':
                    titre = self.cleanHtmlStr(titre)+' ['+tscolor('\c0000????')+ep.strip()+tscolor('\c00??????')+'] '
                else: titre = self.cleanHtmlStr(titre)
                _desc = re.findall('data-content="(.*?)"',desc1, re.S)
                if _desc: desc= desc+'\n'+tscolor('\c00????00')+'Story: '+tscolor('\c00??????')+self.cleanHtmlStr(_desc[0])
                self.addDir({'import':extra,'good_for_fav':True,'category' : 'host2','url': url,'title':titre,'desc':desc,'icon':image,'hst':'tshost','mode':'31'} )

    def get_links(self,cItem):
        urlTab = []
        Url=cItem['url']
        sts, data = self.getPage(Url)
        if sts:
            iframe = re.findall('default" href="(.*?)".*?>(.*?)<',data,re.S|re.IGNORECASE)
            for (url,titre) in iframe:
                urlTab.append({'name':titre, 'url':url, 'need_resolve':1})
        return urlTab

    def getArticle(self, cItem):
        printDBG("Animekom.getVideoLinks [%s]" % cItem)
        otherInfo1 = {}
        desc = cItem['desc']
        sts, data = self.getPage(cItem['url'])
        if sts:
            lst_dat=re.findall('class="details">(.*?)</ul>', data, re.S)
            for (xx) in lst_dat:
                lst_dat0=re.findall('<li>(.*?):(.*?)</li>',xx, re.S)
                for (x1,x2) in lst_dat0:
                    if 'حلقات' in x1: otherInfo1['episodes'] = ph.clean_html(x2.replace('الحلقة',''))
                    if 'لمدة' in x1: otherInfo1['duration'] = ph.clean_html(x2)
                    if 'صاحب' in x1: otherInfo1['station'] = ph.clean_html(x2)
                    if 'لإسم العر' in x1: otherInfo1['alternate_title'] = ph.clean_html(x2)

            lst_dat=re.findall('class="genres">(.*?)</div>', data, re.S)
            if lst_dat: otherInfo1['genres'] = ph.clean_html(lst_dat[0])

            lst_dat=re.findall('class="txt">(.*?)<br />', data, re.S)
            if lst_dat: desc = ph.clean_html(lst_dat[0])

        icon = cItem.get('icon')
        title = cItem['title']
        return [{'title':title, 'text': desc, 'images':[{'title':'', 'url':icon}], 'other_info':otherInfo1}]

    def get_info(self,data):
        inf = ''
        lst_dat=re.findall('class="details">(.*?)</ul>', data, re.S)
        for (xx) in lst_dat:
            lst_dat0=re.findall('<li>(.*?):(.*?)</li>',xx, re.S)
            for (x1,x2) in lst_dat0:
                if 'حلقات' in x1: inf=inf +tscolor('\c00????00')+ 'Episodes: '+tscolor('\c00??????')+ph.clean_html(x2.replace('الحلقة',''))+' | '
                if 'لمدة' in x1: inf=inf +tscolor('\c00????00')+ 'Duration: '+tscolor('\c00??????')+ph.clean_html(x2)+' | '

        lst_dat=re.findall('class="genres">(.*?)</div>', data, re.S)
        if lst_dat: inf = inf+'\n'+tscolor('\c00????00')+'Genre: '+tscolor('\c00??????')+ph.clean_html(lst_dat[0])

        lst_dat=re.findall('class="txt">(.*?)<br />', data, re.S)
        if lst_dat: inf = inf+'\n'+tscolor('\c00????00')+'Story: '+tscolor('\c0000????')+ph.clean_html(lst_dat[0])
        return inf
    def start(self,cItem):
        mode=cItem.get('mode', None)
        if mode=='00':
            self.showmenu0(cItem)
        if mode=='21':
            self.showmenu_21(cItem)
        if mode=='22':
            self.showmenu_22(cItem)
        if mode=='23':
            self.showmenu_23(cItem)
        if mode=='30':
            self.showitms(cItem)
        if mode=='31':
            self.showelems(cItem)
