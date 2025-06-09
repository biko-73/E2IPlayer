# -*- coding: utf-8 -*-
###################################################
# E2iPlayer host for arablionz
###################################################
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import TranslateTXT as _
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, printExc
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.hosts.hosttools import IPTVHost, BaseHostClass
import re
import base64

###################################################

def getinfo():
    info_ = {}
    info_['name'] = 'Arablionz'
    info_['version'] = '2.0 18/07/2022'
    info_['dev'] = 'RGYSoft'
    info_['cat_id'] = '21'
    info_['desc'] = 'أفلام و مسلسلات عربية و اجنبية'
    info_['icon'] = 'https://i.ibb.co/861LmCL/Sans-titre.png'
    info_['recherche_all'] = '1'
    info_['host'] = 'https://arlionztv.cam'
    return info_

###################################################

class ArablionzHost(BaseHostClass):

    def __init__(self, host='https://arlionztv.cam'):
        BaseHostClass.__init__(self, {'cookie': 'arablionz1.cookie'})
        self.MAIN_URL = host
        self.DEFAULT_ICON_URL = getinfo()['icon']
        self.HEADER = {'User-Agent': 'Mozilla/5.0', 'Accept': 'text/html'}
        self.defaultParams = {'header': self.HEADER, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        self.cacheLinks = {}

    def _getFullUrl(self, url):
        if url.startswith('http'):
            return url
        return self.MAIN_URL + url

    def showmenu(self, cItem):
        menuTab = [
            {'category': 'list_items', 'title': _('أفلام'), 'url': self.MAIN_URL + '/category/movies/', 'icon': self.DEFAULT_ICON_URL},
            {'category': 'list_items', 'title': _('مسلسلات'), 'url': self.MAIN_URL + '/category/series/', 'icon': self.DEFAULT_ICON_URL},
            {'category': 'search', 'title': _('بحث'), 'search_item': True, 'icon': 'https://i.ibb.co/dQg0hSG/search.png'},
        ]
        self.listsTab(menuTab, cItem)

    def listItems(self, cItem):
        page = cItem.get('page', 1)
        url = cItem['url']
        if page > 1:
            url += 'page/{}/'.format(page)
        sts, data = self.getPage(url)
        if not sts:
            return
        items = re.findall('Posts--Single--Box">.*?href="(.*?)".*?title="(.*?)".*?image="(.*?)"(.*?)</a>', data, re.S)
        for (url, title, image, desc) in items:
            params = dict(cItem)
            params.update({
                'title': ph.clean_html(title),
                'url': self._getFullUrl(url),
                'icon': self._getFullUrl(image),
                'desc': ph.clean_html(desc),
                'category': 'video_links'
            })
            self.addVideo(params)
        # NEXT PAGE
        if '>&raquo;</a>' in data:
            params = dict(cItem)
            params.update({'title': _('Next page'), 'page': page+1})
            self.addDir(params)

    def getLinksForVideo(self, cItem):
        videoUrl = cItem['url']
        urlTab = []
        sts, data = self.getPage(videoUrl)
        if not sts:
            return []
        # Find the server id for video links
        server_ids = re.findall('"watch".*?data-id="(.*?)"', data, re.S)
        if server_ids:
            servers_url = self.MAIN_URL + '/PostServersWatch/' + server_ids[0]
            params = dict(self.defaultParams)
            params['header']['X-Requested-With'] = 'XMLHttpRequest'
            sts, data = self.getPage(servers_url, params, {})
            if sts:
                servers = re.findall('<li.*?data-i="(.*?)".*?data-id="(.*?)".*?<em>(.*?)<', data, re.S)
                for (i, id_, name) in servers:
                    # This is a placeholder for the real link resolving
                    urlTab.append({'name': ph.clean_html(name), 'url': 'hst#arablionz#{}|||{}'.format(i, id_), 'need_resolve': 1})
        return urlTab

    def getVideoLinks(self, videoUrl):
        # videoUrl is in the form 'hst#arablionz#i|||id'
        urlTab = []
        try:
            i, id_ = videoUrl.split('|||')
        except Exception:
            return []
        embed_url = self.MAIN_URL + '/Embedder/{}/{}'.format(id_, i)
        params = dict(self.defaultParams)
        params['header']['X-Requested-With'] = 'XMLHttpRequest'
        sts, data = self.getPage(embed_url, params, {})
        if sts:
            links = re.findall('<iframe.*?src=["\'](.*?)["\']', data, re.IGNORECASE)
            for url in links:
                urlTab.append({'name': 'stream', 'url': url, 'need_resolve': 0})
        return urlTab

    def getArticleContent(self, cItem):
        descTab = []
        sts, data = self.getPage(cItem['url'])
        if not sts:
            return []
        # Example: extract description, genre, quality, story, etc.
        time = ph.search(data, 'runtime">(.*?)</li>')[0]
        genre = ph.search(data, 'Geners">(.*?)</ul>')[0]
        story = ph.search(data, 'Story">(.*?)</p>')[0]
        desc = '{}\nGenre: {}\n{}'.format(time, genre, story)
        icon = cItem.get('icon', self.DEFAULT_ICON_URL)
        return [{'title': cItem['title'], 'text': desc, 'images': [{'title': '', 'url': icon}], 'other_info': {}}]

    def handleService(self, index, refresh=0, searchPattern='', searchType=''):
        printDBG('ArablionzHost.handleService start')
        BaseHostClass.handleService(self, index, refresh, searchPattern, searchType)
        name = self.currItem.get("name", '')
        category = self.currItem.get("category", '')

        if name == None:
            self.showmenu(self.currItem)
        elif category == 'list_items':
            self.listItems(self.currItem)
        elif category == 'search':
            self.listSearchResult(self.currItem, searchPattern)
        elif category == 'video_links':
            self.getLinksForVideo(self.currItem)

    def listSearchResult(self, cItem, searchPattern):
        # Simple search implementation
        url = self.MAIN_URL + '/search/{}/'.format(searchPattern)
        params = dict(cItem)
        params.update({'url': url, 'category': 'list_items'})
        self.listItems(params)

###################################################

def gettytul():
    return 'arablionz'

def getinfo():
    return getinfo()

def get_host_class():
    return ArablionzHost

###################################################