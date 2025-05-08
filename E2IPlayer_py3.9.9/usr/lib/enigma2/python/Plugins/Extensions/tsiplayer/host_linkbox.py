# -*- coding: utf-8 -*-

from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass, tscolor, tshost
import re
from Plugins.Extensions.IPTVPlayer.libs import ph


def getinfo():
    info_={}
    name = 'Telebox '+tscolor('\c0000????') +'- Linkbox -'
    hst = 'https://www.linkbox.to'
    info_['old_host'] = hst
    hst_ = tshost(name)
    if hst_!='': hst = hst_
    info_['host']    = hst
    info_['name']    = name
    info_['version'] = '1.0 02/04/2023'
    info_['dev']     = 'RGYSoft'
    info_['cat_id']  = '21'
    txt = 'LinkBox - A Box Linking The World. Stockage cloud gratuit, synchronisation et partage'
    info_['desc']    = txt
    info_['icon']    = 'https://i.ibb.co/dLqLt8f/linkbox.png'
    return info_


class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{})
        self.MAIN_URL = getinfo()['host']
        self.nb_elm = 50

    def showmenu(self,cItem):
        lst = [
            ('AflamHQ','bNA04cJ','3735764'),
            ('Anime Box','app01e2f1adf1aca0a1a1a4a7a2a0adf2aca0a1a1a4a7a2a0','6772146'),
            ('Htm.Animes','app01e2f1adf2acaeafa1a3a1a0a0adf1acaeafa1a3a1a0a0','8975766'),
            ('Bein Movies','app01e2f1adf1aca5a4a7aea7a0a4adf2aca5a4a7aea7a0a4','3218162'),
            ('Cinema Baghdad','UiLE7sU','614406'),
            ('Cinema-Club (أفلام)','app01e2f1adf1aca4a3a2a1a7aea4adf2aca4a3a2a1a7aea4','2547182'),
            ('Cinema-Club (مسلسلات)','app01e2f1adf1aca4a1afaea4a5a1adf2aca4a1afaea4a5a1','2798237'),
            ('Cinema-Club (أفلام و مسلسلات الأنمي)','app01e2f1adf1aca4a3a5aea3aea0adf2aca4a3a5aea3aea0','2538586'),
            ('Cinema Crown','app01e2f1adf1aca7a4a5a3a1a3aeadf2aca7a4a5a3a1a3ae','1235758'),
            ('Cinema Dose','_ig_app01e2f1adf0f2acf0e6a5e7e5e1a6a6a4a1eefe_10100689_6184','10100689'),
            ('Cinema mix','app01e2f1adf1aca5aea7afa0a6a5adf2aca5aea7afa0a6a5','3819603'),
            ('Cinema sold','app01e2f1adf1aca0a3a1a1a0a0adf2aca0a3a1a1a0a0','657766'),
            ('cimaabdo','_ig_esEuECt_609855_299a','609855'),
            ('CiMA Now TV','app01e2f1adf1aca5a3a3a5a3a7adf2aca5a3a3a5a3a7','355351'),
            ('Dopanime Movies','_ig_app01e2f1adf0f2acf0e6a5e6faf9a6a6a7afa5e2_9389145_6e86','9389145'),
            ('Egybest','xgLMOew','7040626'),
            ('EGY-BEST','app01e2f1adf2aca7a3a6a0a1a1a5adf1aca7a3a6a0a1a1a5','1506773'),
            ('ايجي بست EgyBest','_ig_app01e2f1adf0f2acf0e6a5fbf9e5a6a6a6eefdf8_3589656_8ed8','3589656'),
            ('|| For You','ho3FrEE','11017991'),
            ('Kowaya Cinema','_ig_app01e2f1adf0f2acf0e6a5f9e4f1a6a6a5fcfba2_4250624_a55c','4250624'),
            ('MARVEL MOROCCO','SD9p5bO','6496365'),
            ('Movies Plus - أفلام','app01e2f1adf1aca0a2a3a1a0a6adf2aca0a2a3a1a0a6','645760'),
            ('Netflix','_ig_app01e2f1adf0f2acf0e6a5fda0aea6a6a6f3afe0_2674587_0ddd','2674587'),
            ('افلام و مسلسلات netflix','_ig_2z1IFpK_4702801_f98c','4702801'),
            ('افلام _مسلسلات_برامج متنوعه netfilx2022','app01e2f1adf2acaea1aea1afa0adf1acaea1aea1afa0','878796'),
            ('New q','_ig_app01e2f1adf0f2acf0e6a5fafae5a6a6f4f2aff4_4606358_e7ba','4606358'),
            ('ONE cima TV','app01e2f1adf1aca7a5a2a5a5a4a2adf2aca7a5a2a5a5a4a2','1343324'),
            ('Star Cinema','app01e2f1adf1aca1afaea6a7adf2aca1afaea6a7','79801'),
            ('Showtime Movies','app01e2f1adf1aca2a4a7afa5afa7adf2aca2a4a7afa5afa7','4219391'),
            ('The Movie Night','app01e2f1adf2acaeafa3a3afa3adf1acaeafa3a3afa3','895595'),
            ('films english 🎬🎥 افلام اجنبي','_ig_app01e2f1adf0f2acf0e6a5f1e2a6a6a6a5a6efe3_752951_b7af','752951'),
            ('THE Movies','app01e2f1adf2aca5a5a2a3a3a4aeadf1aca5a5a2a3a3a4ae','3345528'),
            ('THROW LOB(رياضة)','NZKr9gl','607863'),
            ('The Movie Muse','ZmM9DaP','6896445'),
            ('world1movies','app01e2f1adf2aca0a6a7a5aea3adf1aca0a6a7a5aea3','601385'),
            ('افلام ومسلسلات عربيه واجنبيه مترجمه Various movies','app01e2f1adf2aca7a2aea3a1a6aeadf1aca7a2aea3a1a6ae','1485708'),
            ('مجتمع الأفلام والمسلسلات | Documentary Films','app01e2f1adf2acaea7a5a2a3a5a4adf1acaea7a5a2a3a5a4','8134532'),
            ('فرجني شكرا 🎬 Faragny','_ig_app01e2f1adf0f2acf0e6a5fcaff5a6a6a6afa7fe_2609502_fdae','2609502'),
            ('Marvel Movies أفلام و مسلسلات','_ig_app01e2f1adf0f2acf0e6a5fbf1fda6a6a2f7a6fa_935938_2c28','935938'),
            ('افلام shof_ha','app01e2f1adf2aca4afa5a5a6a2aeadf1aca4afa5a5a6a2ae','2933048'),
            ('يلا Movies','app01e2f1adf2aca3a5afa1aea4a4adf1aca3a5afa1aea4a4','5397822'),
            ('سيما هاوس & cima house','app01e2f1adf1aca7a2a0a2a3a0a2adf2aca7a2a0a2a3a0a2','1464564'),
            ('موطن المفيز movies المدبلج','app01e2f1adf2aca0aea6a2a5a3adf1aca0aea6a2a5a3','680435'),
            ('سينما موفيز | 𝙼𝚘𝚟𝚒𝚎 ᴄɪɴᴇᴍᴀ','app01e2f1adf1aca7a6a2a6a0a0a3adf2aca7a6a2a6a0a0a3','1040665'),
            ('سينما أونلاين','app01e2f1adf1aca5a2aea1a2a6a3adf2aca5a2aea1a2a6a3','3487405'),
            ('عشاق الافلام','app01e2f1adf2acafafa4a2a3a2adf1acafafa4a2a3a2','992454'),
            ('إجي بيست','DERRaVk','3767665'),
            ('اجي بيست','_ig_app01e2f1adf0f2acf0e6a5f9faa2a6a6a2e6f4e2_2751140_2b6c','2751140'),
            ('مسلسلات:دراما نيوز','_ig_app01e2f1adf0f2acf0e6a5fde3aea6a6a6aff7f2_3576258_c91a','3576258'),
            ('⏎مــــــسلســــــلات ⇍كل المسلــسلات والافـلام','app01e2f1adf1aca3a7afa4a0a0a0adf2aca3a7afa4a0a0a0','5192666'),
            ('أفلام ومسلسلات أجنبية','_ig_app01e2f1adf0f2acf0e6a5fae2fda6a6a6f1a3ae_1077534_cc7b','1077534'),
            ('مسلسلات أجنبية أكشن إثارة','_ig_app01e2f1adf0f2acf0e6a5fbe6fda6a6a6eef4ff_6032611_496c','6032611'),
            ('تلفازك المتنقل','_ig_app01e2f1adf0f2acf0e6a5fdf3aea6a6a5e6f8af_3519730_d7ac','3519730'),
            ('جميع الاقسام دراماتك','_ig_app01e2f1adf0f2acf0e6a5faf1a6a6a6a5a3ecf8_4462318_8a7c','4462318'),
            ('الربيعي موفيز','app01e2f1adf2aca3a5a5a4a1a0a1adf1aca3a5a5a4a1a0a1','5332767'),
            ('أفلام مجان نت','app01e2f1adf2aca4a7a5a7a0aeafadf1aca4a7a5a7a0aeaf','2131689'),
            ('مسلسلات و أفلام2023','app01e2f1adf2aca5aea1a5aea0a2adf1aca5aea1a5aea0a2','3873864'),
            ('أفلام ومسلسلات نتفليكس','vhOWCrx','3742384'),
            ('كيدراما (الأسيوية)','app01e2f1adf1aca4a3a6afa0a6adf2aca4a3a6afa0a6','250960'),
            ('مسلسلات وأفلام أسيوية','app01e2f1adf2aca0a0a0afa0aeadf1aca0a0a0afa0ae','666968'),
            ('إستراحة المنوعات','app01e2f1adf2aca5a4afa7a7aea6adf1aca5a4afa7a7aea6','3291180'),
            ('عرب سينما','app01e2f1adf2aca5a5a3a4aea0adf1aca5a5a3a4aea0','335286'),
            ('سلاسل أفلام','_ig_app01e2f1adf0f2acf0e6a5fbefe1a6a6fca0fff2_728149_b0d7','728149'),
            ('تسس موفيز','app01e2f1adf2aca5a2a6afafa7adf1aca5a2a6afafa7','340991'),
            ('موفيز لاند | 🇸🇦','app01e2f1adf1aca1afafa4a7a7adf2aca1afafa4a7a7','799211'),
            ('اكوام افلام ومسلسلات 🍿🎬','app01e2f1adf2acafa3a4a6a3adf1acafa3a4a6a3','95205'),
            ('جميع المسلسلات والافلام','app01e2f1adf2aca5a0a3a3a2a6aeadf1aca5a0a3a3a2a6ae','3655408'),
            ('مسلسلات اجنبية وافلام اجنبية','ypev9W9','1304151'),
            ('أنميات','app01e2f1adf2acaeaea5a2aea4afadf1acaeaea5a2aea4af','8834829'),
            ('شانكس ساما ( إنمي)','app01e2f1adf2aca0aeaeafa2a1adf1aca0aeaeafa2a1','688947'),
            ('تارو ساما ( إنمي)','app01e2f1adf2aca0a5a5a3a0adf1aca0a5a5a3a0','63356'),
            ('؏ـ(🌏)ـالم اݪانــٓـــٓـمــــٴ͜ـــي','app01e2f1adf2aca4aea5a4a6a1a3adf1aca4aea5a4a6a1a3','2832075'),
            ('لوفي ساما ( (إنمي','lUprnhl','1287040')]
        for elm in lst:
            icon = elm[2]
            if icon != '':
                icon = 'https://avatar.fuplink.net/avatar/dircover/'+icon
            else:
                icon = cItem.get('icon','')
            self.addDir({'import':cItem['import'],'category' : 'host2','url':'lst','shareToken':elm[1],'good_for_fav':True,'title':elm[0],'desc':'','icon':icon,'mode':'10','first':True})
        self.addDir({'import':cItem['import'],'category' :'host2','title':'Search'  ,'icon':'https://i.ibb.co/dQg0hSG/search.png','mode':'51','section': 'All'})


    def showmenu1(self,cItem):

        for elm in self.get_items(cItem):
            category = elm.get('category','')
            if category == 'video':
                self.addVideo(elm)
            elif category == 'audio':
                self.addAudio(elm)
            else:
                self.addDir(elm)

    def get_items(self,cItem={}):
        #print(cItem)
        __ = False
        elms       = []
        extra      = cItem.get('import')
        str_ch     = cItem.get('str_ch')
        page       = cItem.get('page', 1)
        url_       = cItem.get('url', '')
        type_      = cItem.get('type_', '')
        first      = cItem.get('first',False)
        shareToken = cItem.get('shareToken','')
        pid        = cItem.get('pid',0)
        if type_ == 'All':
            url0 = 'https://www.zain3.com/api/search?kw='+str_ch+'&pageSize='+str(self.nb_elm)+'&pageNo='+str(page)
        elif url_=='':
            url0 = self.MAIN_URL + '/api/file/share_file_list/web?sortField=utime&sortAsc=0&pageNo='+str(page)+'&pageSize='+str(self.nb_elm)+'&'+'token='+shareToken+'&pid='+str(pid)+'&name='+str_ch+'&needTpInfo=1&scene=singleGroup&name=&platform=web&pf=web&lan=en'
        else:
            url0 = self.MAIN_URL + '/api/file/share_out_list/?sortField=name&sortAsc=1&pageNo='+str(page)+'&pageSize='+str(self.nb_elm)+'&'+'shareToken='+shareToken+'&pid='+str(pid)+'&needTpInfo=1&scene=singleGroup&name=&platform=web&pf=web&lan=en'
        sts, data = self.getPage(url0)
        if sts:
            data = json_loads(data)
            if data.get('data',{}) == None:
                url0 = url0.replace('&scene=singleGroup','&scene=singleItem')
                sts, data = self.getPage(url0)
                if sts:
                    data = json_loads(data)

            pageProps = data.get('pageProps',{})
            elm_count = 0
            if 'api/search' in url0:
                data = data.get('data',{})
                data = data.get('list',[])
                for elm in data:
                    print(elm)
                    elm_count = elm_count + 1
                    titre = elm.get('name','').replace('<em>','').replace('</em>','')
                    url = elm.get('url','')
                    if '/f/' in url: url = url.replace('/f/','/s/')
                    if ('/s/' in url):
                        shareToken = url.split('/s/')[1]
                        if '?pid=' in shareToken:
                            shareToken,pid = shareToken.split('?pid=')
                        else:
                            pid = ''
                        elms.append({'import':cItem['import'],'category' : 'host2','url':'lst','shareToken':shareToken,'pid':pid,'good_for_fav':True,'title':titre,'desc':'','icon':cItem.get('icon',''),'mode':'10'})

            elif False and (pageProps != {}):
                data = pageProps.get('resultList',[])
                for elm in data:
                    elm_count = elm_count + 1
                    titre = elm.get('name','').replace('<em>',tscolor('\c00????30')).replace('</em>',tscolor('\c00??????'))
                    url = elm.get('url','')
                    if '/f/' in url: url = url.replace('/f/','/s/')
                    if ('/s/' in url):
                        shareToken = url.split('/s/')[1]
                        if '?pid=' in shareToken:
                            shareToken,pid = shareToken.split('?pid=')
                        else:
                            pid = ''
                        elms.append({'import':cItem['import'],'category' : 'host2','url':'lst','shareToken':shareToken,'pid':pid,'good_for_fav':True,'title':titre,'desc':'','icon':cItem.get('icon',''),'mode':'10'})
            else:
                data = data.get('data',{})
                data = data.get('list',[])
                if not data: data = []
                for elm in data:
                    print(elm)
                    titre = elm.get('name','')
                    type__ = elm.get('type','')
                    pid   = elm.get('id','')
                    desc  = ''
                    icon  = elm.get('cover',cItem.get('icon',''))
                    if '&x-image-process' in icon: icon = icon.split('&x-image-process',1)[0]
                    link  = elm.get('url','')
                    elm_count = elm_count + 1
                    if (('للكبار' not in titre) and ('+18' not in titre)) or __:
                        if type__=='dir':
                            elms.append({'import':cItem['import'],'category' : 'host2','url':url_,'shareToken':shareToken,'pid':pid,'good_for_fav':True,'title':titre,'desc':'','icon':cItem.get('icon',''),'mode':'10'})
                        elif type__=='video':
                            elms.append({'import':cItem['import'],'category' : 'video','url': link,'good_for_fav':True,'title':titre,'desc':desc,'icon':icon,'hst':'direct','type':'video'})
                        elif type__=='audio':
                            elms.append({'import':cItem['import'],'category' : 'audio','url': link,'good_for_fav':True,'title':titre,'desc':desc,'icon':icon,'hst':'direct','type':'audio'})
                        else:
                            print('pas dir:'+titre)
            if elm_count + 1 > self.nb_elm:
                if url_=='':
                    mode = '51'
                    extra = cItem['import']+'||'+shareToken+'||'+pid
                else:
                    mode = '10'
                    extra = cItem['import']
                elms.append({'import':cItem['import'],'category' : 'host2','url':url_,'shareToken':shareToken,'pid':cItem.get('pid',0),'page':page+1,'good_for_fav':True,'title':'Next','desc':'','icon':cItem.get('icon',''),'extra': extra,'mode':mode,'type_':type_,'str_ch':str_ch,'section': 'All'})
            if False:#first:
                extra = cItem['import']+'||'+str(shareToken)+'||'+str(pid)
                elms.append({'import':cItem['import'],'category' :'host2','title':'Search','icon':'https://i.ibb.co/7nr1vgq/almo7eb-sea.png','mode':'51','shareToken':shareToken,'extra': extra,'pid':cItem.get('pid',0)})
        return elms

    def SearchAll(self,str_ch,page=1,extra='',type_=''):
        elms = []
        print('type_='+type_)
        if '||' in extra:
            import_,shareToken,pid = extra.split('||')
            r1 = self.get_items({'page':page,'import':import_,'str_ch':str_ch,'shareToken':shareToken,'pid':pid,'type_':type_})
        else:
            import_ = extra
            r1 = self.get_items({'page':page,'import':import_,'str_ch':str_ch,'shareToken':'','pid':'','type_':type_})
        for elm in r1:
            elms.append(elm)
        return elms



