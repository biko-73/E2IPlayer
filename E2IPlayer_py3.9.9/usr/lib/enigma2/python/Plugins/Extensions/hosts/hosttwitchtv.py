# -*- coding: utf-8 -*-

from datetime import timedelta

from Plugins.Extensions.IPTVPlayer.compat import (e2Json_loads, urllib_quote,
                                                  urllib_quote_plus)
from Plugins.Extensions.IPTVPlayer.components.ihost import (CBaseHostClass,
                                                            CHostBase)
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import \
    TranslateTXT as _
from Plugins.Extensions.IPTVPlayer.libs.urlparser import urlparser
from Plugins.Extensions.IPTVPlayer.libs.urlparserhelper import \
    getDirectM3U8Playlist
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import (GetDefaultLang,
                                                           MergeDicts, byteify,
                                                           printDBG, printExc)
from Plugins.Extensions.IPTVPlayer.tools.manipulateStrings import ensure_str


def GetConfigList():
    optionList = []
    return optionList


def gettytul():
    return 'https://twitch.tv/'


def jstr(item, key, default=''):
    v = item.get(key, default)
    if None == v:
        return default
    else:
        return ensure_str(v)


class Twitch(CBaseHostClass):

    def __init__(self):
        CBaseHostClass.__init__(self, {'history': 'Twitch', 'cookie': 'Twitch.cookie'})

        self.HTTP_HEADER = self.cm.getDefaultHeader()
        self.defaultParams = {'header': self.HTTP_HEADER}

        self.DEFAULT_ICON_URL = 'http://s.jtvnw.net/jtv_user_pictures/hosted_images/GlitchIcon_WhiteonPurple.png'
        self.MAIN_URL = 'https://www.twitch.tv/'
        self.API1_URL = 'https://api.twitch.tv/'
        self.API2_URL = 'https://gql.twitch.tv/'

        self.CHANNEL_TOKEN_URL = self.getFullUrl('/api/channels/{0}/access_token')
        self.LIVE_URL = 'http://usher.justin.tv/api/channel/hls/{0}.m3u8?token={1}&sig={2}&allow_source=true'
        self.CHANNEL_TOKEN_URL = self.API1_URL + 'api/channels/{0}/access_token?need_https=false&oauth_token&platform=web&player_backend=mediaplayer&player_type=embed'

        self.VOD_TOKEN_URL = self.API1_URL + 'api/vods/{0}/access_token?need_https=true&oauth_token&platform=web&player_backend=mediaplayer&player_type=embed'
        self.VOD_URL = 'https://usher.ttvnw.net/vod/{0}.m3u8?token={1}&sig={2}&allow_source=true'

        self.platformFilters = [{'title': _('All Platforms'), 'platform_type': 'all'}, {'title': _('Xbox One'), 'platform_type': 'xbox'}, {'title': _('PlayStation 4'), 'platform_type': 'ps4'}]
        self.languagesFilters = [
            # nice of them to change from meaningful identifers to guid
            # screwing things up with the language filtering.  CM
            {'lang': "73cc486a-e56b-41ed-a1df-7afedbc84f6f", 'title': "العربية"},
            {'lang': "21d85c73-701f-4259-8c4e-4321265847b5", 'title': "български"},
            {'lang': "a6cddaba-f0ce-4526-9087-6de2f603a24d", 'title': "Čeština"},
            {'lang': "43e598cc-918b-4247-b02c-b13543a1eac9", 'title': "Dansk"},
            {'lang': "9166ad14-41f1-4b04-a3b8-c8eb838c6be6", 'title': "Deutsch"},
            {'lang': "902f6815-a655-4918-99e7-48c74a71feac", 'title': "Ελληνικά"},
            {'lang': "6ea6bca4-4712-4ab9-a906-e3336a9d8039", 'title': "English"},
            {'lang': "d4bb9c58-2141-4881-bcdc-3fe0505457d1", 'title': "Español"},
            {'lang': "220eb274-ab25-425b-8a9b-826103404997", 'title': "Suomi"},
            {'lang': "6f655045-9989-4ef7-8f85-1edcec42d648", 'title': "Français"},
            {'lang': "a298cca5-d408-47c7-a1e7-0c76ca878bc6", 'title': "Magyar"},
            {'lang': "5b9935eb-1e9a-4217-98ad-62bda5cff0d1", 'title': "Italiano"},
            {'lang': "6ba1d230-e52f-4d81-b1e0-41f25a8a9f5d", 'title': "日本語"},
            {'lang': "ab2975e3-b9ca-4b1a-a93e-fb61a5d5c3a4", 'title': "한국어"},
            {'lang': "e13e6734-37ae-4d85-897b-3015f0168355", 'title': "Nederlands"},
            {'lang': "5647bf35-f99e-49aa-8578-0e07d936188c", 'title': "Norsk"},
            {'lang': "f9d04efa-6e25-49bf-bf0a-da3e2addaf1b", 'title': "Polski"},
            {'lang': "39ee8140-901a-4762-bfca-8260dea1310f", 'title': "Português"},
            {'lang': "75a99c80-0f15-4159-b1fd-3812c25b4aca", 'title': "Română"},
            {'lang': "0569b171-2a2b-476e-a596-5bdfb45a1327", 'title': "Русский"},
            {'lang': "9b773670-05f8-4c06-ac99-e6649f906171", 'title': "Slovenčina"},
            {'lang': "145b073b-cb70-4e91-b170-f5fab2ebba05", 'title': "Svenska"},
            {'lang': "f19c7524-c18d-41af-9f39-034c8d0b0fee", 'title': "ภาษาไทย"},
            {'lang': "f08d5873-f0c7-4912-94ba-a41933b4c141", 'title': "Türkçe"},
            {'lang': "ba3b69fe-899c-4518-ac46-707275e3eba1", 'title': "TiếngViệt"},
            {'lang': "0c8c6543-4019-47d0-9b8a-57a81ee6ace5", 'title': "中文(粵語)"},
            {'lang': "74c92063-a389-4fd2-8460-b1bb82b04ec7", 'title': "中文"},
            {'lang': '5ad4b978-495f-4093-9461-c194f58201ab', 'title': 'American Sign Language'},
            {'lang': 'fd76c790-0505-4c4c-865a-d6bd139c0901', 'title': 'Other'}
        ]

        lang = GetDefaultLang()
        default = None
        defaultEn = None
        self.langItems = []
        for item in self.languagesFilters:
            if lang == item['lang']:
                default = item
                continue
            if 'en' == item['lang']:
                defaultEn = item
                continue
            self.langItems.append(item)
        if defaultEn:
            self.langItems.insert(0, defaultEn)
        if default:
            self.langItems.insert(0, default)
        self.langItems.insert(0, {'title': _('All')})

        self.VIDEOS_TYPES_TAB = [
            {'title': _('All')},
            {'title': _('Past premieres'), 'videos_type': 'PAST_PREMIERE'},
            {'title': _('Archive'), 'videos_type': 'ARCHIVE'},
            {'title': _('Highlights'), 'videos_type': 'HIGHLIGHT'},
            {'title': _('Uploads'), 'videos_type': 'UPLOAD'}, ]

        self.VIDEOS_SORT_TAB = [
            {'title': _('Popular'), 'sort': 'VIEWS'},
            {'title': _('Recent'), 'sort': 'TIME'}, ]

        self.CLIPS_FILTERS_TAB = [
            {'title': _('Trending'), 'clips_filter': 'TRENDING'},
            {'title': _('Last day'), 'clips_filter': 'LAST_DAY'},
            {'title': _('Last week'), 'clips_filter': 'LAST_WEEK'},
            {'title': _('Last month'), 'clips_filter': 'LAST_MONTH'},
            {'title': _('All time'), 'clips_filter': 'ALL_TIME'}, ]

        self.GAME_CAT_TAB = [
            {'category': 'game_lang', 'next_category': 'game_channels', 'title': _('Channels')},
            {'category': 'game_lang', 'next_category': 'game_videos_types', 'title': _('Videos')},
            {'category': 'game_lang', 'next_category': 'game_clips_filters', 'title': _('Clips')},]

    def getPage(self, baseUrl, addParams={}, post_data=None):
        if addParams == {}:
            addParams = dict(self.defaultParams)
        if 'api.twitch.tv' in baseUrl:
            addParams['header'] = MergeDicts(addParams['header'], {'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': 'jzkbprff40iqj646a697cyrvl0zt2m6'})
        elif 'gql.twitch.tv' in baseUrl:
            addParams['header'] = MergeDicts(addParams['header'], {'Accept': '*/*', 'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko'})
        return self.cm.getPage(baseUrl, addParams, post_data)

    def listMain(self, cItem):
        printDBG("Twitch.listMain")

        MAIN_CAT_TAB = [{'category': 'browse', 'title': _('Browse')},
                        {'category': 'search', 'title': _('Search'), 'search_item': True},
                        {'category': 'search_history', 'title': _('Search history'), }]
        self.listsTab(MAIN_CAT_TAB, cItem)

    def listDirectories(self, cItem):
        printDBG(f"Twitch.listDirectories [{cItem}]")

        dirChannels = []
        for pItem in self.platformFilters:
            params = MergeDicts(cItem, pItem)
            subItems = [MergeDicts(params, x, {'category': 'dir_channels'}) for x in self.langItems]
            params.update({'category': 'sub_items', 'sub_items': subItems})
            dirChannels.append(params)

        TAB = [
            {'category': 'dir_games', 'title': _('Games')},
            {'category': 'sub_items', 'title': _('Channels'), 'sub_items': dirChannels},]
        self.listsTab(TAB, cItem)

    def _listChannels(self, cItem, nextCategory, streamsData):
        try:
            cursor = ''
            for item in streamsData['edges']:
                cursor = jstr(item, 'cursor')
                item = item['node']
                descTab = []
                if item.get('broadcaster'):
                    title = jstr(item['broadcaster'], 'displayName')
                    icon = self.getFullIconUrl(jstr(item, 'previewImageURL'), self.cm.meta['url'])
                    descTab.append(f"[{jstr(item, 'type')}] {jstr(item, 'title')}")
                    descTab.append(f"{jstr(item, '__typename')} | {_(f"{item['viewersCount']} viewers")}")
                    if item.get('broadcaster'):
                        descTab.append(f"{jstr(item['broadcaster'], '__typename')}: {jstr(item['broadcaster'], 'displayName')}")
                    if item.get('game'):
                        descTab.append(f"{jstr(item['game'], '__typename')}: {jstr(item['game'], 'name')}")
                    params = {'good_for_fav': True, 'name': 'category', 'type': 'category', 'category': nextCategory, 'title': title, 'user_login': str(item['broadcaster']['login']), 'icon': icon, 'desc': '[/br]'.join(descTab)}
                    self.addDir(params)

            if cursor != '' and streamsData['pageInfo']['hasNextPage']:
                self.addDir(MergeDicts(cItem, {'title': _('Next page'), 'cursor': cursor}))
        except Exception:
            printExc()

    def listDirChannels(self, cItem, nextCategory):
        printDBG(f"Twitch.listDirChannels [{cItem}]")

        lang = f'"{cItem["lang"].upper()}"' if 'lang' in cItem else ''
        cursor = f',"cursor":"{cItem["cursor"]}"' if 'cursor' in cItem else ''
        type = cItem.get('platform_type', 'all')
        post_data = f'[{{"operationName":"BrowsePage_Popular","variables":{{"limit":30,"platformType":"{type}","options":{{"tags":[{lang}]}},"sortTypeIsRecency":false{cursor}}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"b32fa28ffd43e370b42de7d9e6e3b8a7ca310035fdbb83932150443d6b693e4d"}}}}}}]'
        url = self.getFullUrl('/gql', self.API2_URL)
        sts, data = self.getPage(url, MergeDicts(self.defaultParams, {'raw_post_data': True}), post_data)
        if not sts:
            return
        try:
            data = e2Json_loads(data)
            self._listChannels(cItem, nextCategory, data[0]['data']['streams'])
        except Exception:
            printExc()

    def listDirGames(self, cItem, nextCategory):
        printDBG(f"Twitch.listDirGames [{cItem}]")

        cursor = f',"cursor":"{cItem["cursor"]}"' if 'cursor' in cItem else ''
        post_data = f'[{{"operationName":"BrowsePage_AllDirectories","variables":{{"limit":30,"options":{{"recommendationsContext":{{"platform":"web"}},"sort":"VIEWER_COUNT","tags":[]}}{cursor}}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"78957de9388098820e222c88ec14e85aaf6cf844adf44c8319c545c75fd63203"}}}}}}]'
        url = self.getFullUrl('/gql', self.API2_URL)
        sts, data = self.getPage(url, MergeDicts(self.defaultParams, {'raw_post_data': True}), post_data)
        if not sts:
            return
        try:
            cursor = ''
            data = e2Json_loads(data)
            for item in data[0]['data']['directoriesWithTags']['edges']:
                cursor = jstr(item, 'cursor')
                item = item['node']
                if item['__typename'] == 'Game':
                    title = jstr(item, 'displayName')
                    icon = self.getFullIconUrl(jstr(item, 'avatarURL'), self.cm.meta['url'])
                    desc = f"{jstr(item, '__typename')} | {_(f'{item["viewersCount"]} viewers')}"
                    params = {'good_for_fav': True, 'name': 'category', 'category': nextCategory, 'title': title, 'game_id': str(item['id']), 'game_name': jstr(item, 'name'), 'icon': icon, 'desc': desc}
                    self.addDir(params)

            if cursor != '' and data[0]['data']['directoriesWithTags']['pageInfo']['hasNextPage']:
                self.addDir(MergeDicts(cItem, {'title': _('Next page'), 'cursor': cursor}))

        except Exception:
            printExc()

    def listGameChannels(self, cItem, nextCategory):
        printDBG(f"Twitch.listGameChannels [{cItem}]")
        lang = f'"{cItem["lang"].upper()}"' if 'lang' in cItem else ''
        cursor = f',"cursor":"{cItem["cursor"]}"' if 'cursor' in cItem else ''
        # post_data updated as per changes to their api.  CM
        post_data = f'[{{"operationName":"DirectoryPage_Game","variables":{{"name":"{cItem["game_name"]}","options":{{"sort":"VIEWER_COUNT","recommendationsContext":{{"platform":"web"}},"requestID":"a40436b85daf0810","tags":[{lang}]}},"sortTypeIsRecency":false,"limit":30{cursor}}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"c250a5fa4134a24c3d96abff9450391fd621b1c973c47f3d6adda3be6098c850"}}}}}}]'
        url = self.getFullUrl('/gql', self.API2_URL)
        sts, data = self.getPage(url, MergeDicts(self.defaultParams, {'raw_post_data': True}), post_data)
        if not sts:
            return

        try:
            data = e2Json_loads(data)
            self._listChannels(cItem, nextCategory, data[0]['data']['game']['streams'])
        except Exception:
            printExc()

    def listChannel(self, cItem):
        printDBG(f"Twitch.listChannel {cItem['user_login']}")

        login = cItem['user_login']
        post_data = []
        post_data.append(f'{{"operationName":"ChannelShell","variables":{{"login":"{login}"}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"d6b850262351d0a1e01369809ca87ef837c45e148301053a8f6a9dc440d3c806"}}}}}}')
        post_data.append(f'{{"operationName":"ChannelPage_ChannelHeader","variables":{{"login":"{login}"}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"32f05e9f36086c6e6930e3f3d0d515eea61cc3263bf7f92870f97c9aae024593"}}}}}}')
        post_data.append(f'{{"operationName":"ChannelPage_StreamType_User","variables":{{"channelLogin":"{login}"}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"43b152e4f17090ece0b50a5bc41e4690c7a6992ad3ed876d88bf7292be2d2cba"}}}}}}')
        post_data.append(f'{{"operationName":"ChannelPage__ChannelViewersCount","variables":{{"login":"{login}"}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"3b5b233b59cc71f5ab273c74a30c46485fa52901d98d7850d024ad0669270184"}}}}}}')
        post_data.append(f'{{"operationName":"StreamMetadata","variables":{{"channelLogin":"{login}"}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"1c719a40e481453e5c48d9bb585d971b8b372f8ebb105b17076722264dfa5b3e"}}}}}}')

        url = self.getFullUrl('/gql', self.API2_URL)
        sts, data = self.getPage(url, MergeDicts(self.defaultParams, {'raw_post_data': True}), f"[{','.join(post_data)}]")
        if not sts:
            return

        icon = ''
        try:
            data = e2Json_loads(data)
            try:
                if data[2]['data']['user']['stream']['type'] == 'live':
                    descTab = []
                    viewers = str(data[3]['data']['user']['stream']['viewersCount'])
                    descTab.append(_(f'{viewers} viewers'))
                    title = jstr(data[4]['data']['user']['lastBroadcast'], 'title')
                    item = data[4]['data']['user']['stream']
                    if item.get('game'):
                        descTab.append(f"{jstr(item['game'], '__typename')}: {jstr(item['game'], 'name')}")
                        icon = self.getFullIconUrl(jstr(item['game'], 'boxArtURL'), self.cm.meta['url'])
                    else:
                        icon = ''

                    params = {'good_for_fav': False, 'title': title, 'game_id': str(item['id']), 'video_type': 'live', 'channel_id': login, 'icon': icon, 'desc': '[/br]'.join(descTab)}
                    self.addVideo(params)
            except Exception:
                printExc()

            item = data[1]['data']['user']
            icon = self.getFullIconUrl(jstr(item, 'profileImageURL'), self.cm.meta['url'])
            videosCount = int(item['videos']['totalCount'])
            if videosCount:
                params = dict(cItem)
                params.update({'good_for_fav': False, 'category': 'videos_types', 'title': _(f'Videos {videosCount}'), 'icon': icon, 'desc': ''})
                self.addDir(params)
        except Exception:
            printExc()

        params = MergeDicts(cItem, {'good_for_fav': False, 'category': 'clips_filters', 'title': _('Clips'), 'icon': icon, 'desc': ''})
        self.addDir(params)

    def _listVideos(self, cItem, videosData):
        printDBG(f"Twitch._listVideos [{cItem}]")
        try:
            cursor = ''
            for item in videosData['edges']:
                cursor = jstr(item, 'cursor')
                item = item['node']
                descTab = []
                descTab.append(f"{timedelta(seconds=item['lengthSeconds'])}")
                descTab.append(_(f'{item["viewCount"]} viewers'))
                descTab.append(jstr(item, 'publishedAt'))
                descTab = [' | '.join(descTab)]

                icon = self.getFullIconUrl(jstr(item, 'previewThumbnailURL'), self.cm.meta['url'])
                title = jstr(item, 'title')

                if item.get('owner'):
                    descTab.append(f"{jstr(item['owner'], '__typename')}: {jstr(item['owner'], 'displayName')}")
                if item.get('game'):
                    descTab.append(f"{jstr(item['game'], '__typename')}: {jstr(item['game'], 'name')}")

                params = {'good_for_fav': True, 'title': title, 'video_type': 'video', 'video_id': jstr(item, 'id'), 'icon': icon, 'desc': '[/br]'.join(descTab)}
                self.addVideo(params)

            if cursor != '' and videosData['pageInfo']['hasNextPage']:
                self.addDir(MergeDicts(cItem, {'title': _('Next page'), 'cursor': cursor}))
        except Exception:
            printExc()

    def listVideos(self, cItem):
        printDBG(f"Twitch.listVideos [{cItem}]")
        cursor = f',"cursor":"{cItem["cursor"]}"' if 'cursor' in cItem else ''
        broadcastType = f'"{cItem["videos_type"]}"' if 'videos_type' in cItem else 'null'
        post_data = f'[{{"operationName":"FilterableVideoTower_Videos","variables":{{"limit":30,"channelOwnerLogin":"{cItem["user_login"]}","broadcastType":{broadcastType},"videoSort":"{cItem["sort"]}"{cursor}}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"352ca6e327523f88b08390bf79d1b1d6e5f67b46981c900cf41eca56ef9d3cfc"}}}}}}]'
        url = self.getFullUrl('/gql', self.API2_URL)
        sts, data = self.getPage(url, MergeDicts(self.defaultParams, {'raw_post_data': True}), post_data)
        if not sts:
            return

        try:
            data = e2Json_loads(data)
            self._listVideos(cItem, data[0]['data']['user']['videos'])
        except Exception:
            printExc()

    def listGameVideos(self, cItem):
        printDBG(f"Twitch.listGameVideos [{cItem}]")
        cursor = f',"followedCursor":"{cItem["cursor"]}"' if 'cursor' in cItem else ''
        broadcastType = f',"broadcastTypes":["{cItem["videos_type"].lower()}"]' if 'videos_type' in cItem else ''
        post_data = f'[{{"operationName":"DirectoryVideos_Game","variables":{{"gameName":"{cItem["game_name"]}","videoLimit":30,"tags":[{broadcastType}],"videoSort":"{cItem["sort"]}"{cursor}}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"643351f6cff5d248aa2b827f912c80bf387b918c01089526b05d628cf04a5706"}}}}}}]'
        url = self.getFullUrl('/gql', self.API2_URL)
        sts, data = self.getPage(url, MergeDicts(self.defaultParams, {'raw_post_data': True}), post_data)
        if not sts:
            return

        try:
            data = e2Json_loads(data)
            self._listVideos(cItem, data[0]['data']['game']['videos'])
        except Exception:
            printExc()

    def _listClips(self, cItem, clipsData):
        try:
            cursor = ''
            for item in clipsData['edges']:
                cursor = jstr(item, 'cursor')
                item = item['node']
                descTab = []

                descTab.append(jstr(item, 'language'))
                descTab.append(f"{timedelta(seconds=item['durationSeconds'])}")
                descTab.append(_(f"{item['viewCount']} viewers"))
                descTab = [' | '.join(descTab)]

                icon = self.getFullIconUrl(jstr(item, 'thumbnailURL'), self.cm.meta['url'])
                title = f"[{jstr(item, 'createdAt')}] {jstr(item, 'title')}"

                if item.get('curator'):
                    descTab.append(f"{jstr(item['curator'], '__typename')}: {jstr(item['curator'], 'displayName')}")
                if item.get('broadcaster'):
                    descTab.append(f"{jstr(item['broadcaster'], '__typename')}: {jstr(item['broadcaster'], 'displayName')}")
                if item.get('game'):
                    descTab.append(f"{jstr(item['game'], '__typename')}: {jstr(item['game'], 'name')}")

                params = {'good_for_fav': True, 'title': title, 'url': jstr(item, 'url'), 'video_type': 'clip', 'clip_slug': jstr(item, 'slug'), 'clip_id': jstr(item, 'id'), 'icon': icon, 'desc': '[/br]'.join(descTab)}
                self.addVideo(params)

            if cursor != '' and clipsData['pageInfo']['hasNextPage']:
                self.addDir(MergeDicts(cItem, {'title': _('Next page'), 'cursor': cursor}))

        except Exception:
            printExc()

    def listClips(self, cItem):
        printDBG(f"Twitch.listClips [{cItem}]")
        cursor = f',"cursor":"{cItem["cursor"]}"' if 'cursor' in cItem else ''
        post_data = f'[{{"operationName":"ClipsCards__User","variables":{{"login":"{cItem["user_login"]}","limit":20,"criteria":{{"filter":"{cItem["clips_filter"]}"}}{cursor}}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"b661fa0b88f774135c200d64b7248ff21263c12db79e0f7d33aeedb0315cdcbb"}}}}}}]'
        url = self.getFullUrl('/gql', self.API2_URL)
        sts, data = self.getPage(url, MergeDicts(self.defaultParams, {'raw_post_data': True}), post_data)
        if not sts:
            return

        try:
            data = e2Json_loads(data)
            self._listClips(cItem, data[0]['data']['user']['clips'])
        except Exception:
            printExc()

    def listGameClips(self, cItem):
        printDBG(f"Twitch.listGameClips [{cItem}]")
        lang = f'"{cItem["lang"].upper()}"' if 'lang' in cItem else ''
        cursor = f',"cursor":"{cItem["cursor"]}"' if 'cursor' in cItem else ''
        post_data = f'[{{"operationName":"ClipsCards__Game","variables":{{"gameName":"{cItem["game_name"]}","limit":20,"criteria":{{"tags":[{lang}],"filter":"{cItem["clips_filter"]}"}}{cursor}}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"0d8d0eba9fc7ef77de54a7d933998e21ad7a1274c867ec565ac14ffdce77b1f9"}}}}}}]'
        url = self.getFullUrl('/gql', self.API2_URL)
        sts, data = self.getPage(url, MergeDicts(self.defaultParams, {'raw_post_data': True}), post_data)
        if not sts:
            return

        try:
            data = e2Json_loads(data)
            self._listClips(cItem, data[0]['data']['game']['clips'])
        except Exception:
            printExc()

    def listSubItems(self, cItem):
        printDBG("Twitch.listSubItems")
        self.currList = cItem['sub_items']

    def listV5Channels(self, cItem):
        printDBG(f"Twitch.listV5Channels [{cItem}]")
        offset = cItem.get('offset', 0)
        url = cItem['url'] + str(offset)
        sts, data = self.getPage(url)
        if not sts:
            return
        try:
            data = e2Json_loads(data)
            for item in data['channels']:
                descTab = [_(f'Language: {jstr(item, "language")}')]
                descTab.append(_(f'{item["views"]} views'))
                descTab.append(_(f'{item["followers"]} followers'))
                params = {'good_for_fav': True, 'name': 'category', 'type': 'category', 'category': 'list_channel', 'user_login': jstr(item, 'name'), 'title': jstr(item, 'display_name'), 'icon': jstr(item, 'logo'), 'desc': '[/br]'.join(descTab)}
                self.addDir(params)
            offset += len(self.currList)
            if offset < data['_total']:
                self.addDir(MergeDicts(cItem, {'title': _('Next page'), 'offset': offset}))
        except Exception:
            printExc()

    def listV5Channels(self, cItem):
        printDBG(f"Twitch.listV5Channels [{cItem}]")
        offset = cItem.get('offset', 0)
        url = cItem['url'] + str(offset)
        sts, data = self.getPage(url)
        if not sts:
            return
        try:
            data = e2Json_loads(data)
            for item in data['channels']:
                descTab = [_(f'Language: {jstr(item, "language")}')]
                descTab.append(_(f'{item["views"]} views'))
                descTab.append(_(f'{item["followers"]} followers'))
                params = {'good_for_fav': True, 'name': 'category', 'type': 'category', 'category': 'list_channel', 'user_login': jstr(item, 'name'), 'title': jstr(item, 'display_name'), 'icon': jstr(item, 'logo'), 'desc': '[/br]'.join(descTab)}
                self.addDir(params)
            offset += len(self.currList)
            if offset < data['_total']:
                self.addDir(MergeDicts(cItem, {'title': _('Next page'), 'offset': offset}))
        except Exception:
            printExc()

    def listV5Games(self, cItem):
        printDBG(f"Twitch.listV5Games [{cItem}]")
        offset = cItem.get('offset', 0)
        url = cItem['url'] + str(offset)
        sts, data = self.getPage(url)

        if not sts:
            return
        try:
            data = e2Json_loads(data)
            for item in data['games']:
                params = {'good_for_fav': True, 'name': 'category', 'type': 'category', 'category': 'browse_game', 'game_name': jstr(item, 'name'), 'game_id': str(item['_id']), 'title': jstr(item, 'localized_name'), 'icon': jstr(item['box'], 'medium'), 'desc': _('Popularity: ?')}
                self.addDir(params)
            offset += len(self.currList)
            if offset < data.get('_total', 0):
                self.addDir(MergeDicts(cItem, {'title': _('Next page'), 'offset': offset}))
        except Exception:
            printExc()

    def listV5Streams(self, cItem):
        printDBG(f"Twitch.listV5Streams [{cItem}]")
        offset = cItem.get('offset', 0)
        url = cItem['url'] + str(offset)
        sts, data = self.getPage(url)
        if not sts:
            return
        try:
            data = e2Json_loads(data)
            for item in data['streams']:
                descTab = [_(f'Language: {jstr(item["channel"], "broadcaster_language")}')]
                descTab.append(_(f'{item["viewers"]} viewers'))
                descTab.append(_(f'Broadcaster: {jstr(item["channel"], "display_name")}'))
                descTab.append(_(f'Game: {jstr(item, "game")}'))
                title = f'[{jstr(item, "stream_type")}] {jstr(item["channel"], "status")}'
                params = {'good_for_fav': False, 'title': title, 'video_type': jstr(item, 'stream_type'), 'channel_id': jstr(item['channel'], 'name'), 'icon': jstr(item['preview'], 'medium'), 'desc': '[/br]'.join(descTab)}
                self.addVideo(params)
            offset += len(self.currList)
            if offset < data['_total']:
                self.addDir(MergeDicts(cItem, {'title': _('Next page'), 'offset': offset}))
        except Exception:
            printExc()

    def listSearchResult(self, cItem, searchPattern, searchType):
        if searchType == 'channels':
            url = f'{self.API1_URL}kraken/search/channels?query={urllib_quote_plus(searchPattern)}&limit=25&offset='
            cItem = MergeDicts(cItem, {'url': url, 'category': 'v5_channels'})
            self.listV5Channels(cItem)
        elif searchType == 'games':
            url = f'{self.API1_URL}kraken/search/games?query={urllib_quote_plus(searchPattern)}&limit=25&offset='
            cItem = MergeDicts(cItem, {'url': url, 'category': 'v5_games'})
            self.listV5Games(cItem)
        elif searchType == 'streams':
            url = f'{self.API1_URL}kraken/search/streams?query={urllib_quote_plus(searchPattern)}&limit=25&offset='
            cItem = MergeDicts(cItem, {'url': url, 'category': 'v5_streams'})
            self.listV5Streams(cItem)

    def getLinksForVideo(self, cItem):
        printDBG(f"Twitch.getLinksForVideo [{cItem}]")
        urlTab = []

        id = ''
        if cItem['video_type'] == 'clip':
            post_data = f'[{{"operationName":"VideoAccessToken_Clip","variables":{{"slug":"{cItem["clip_slug"]}"}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"9bfcc0177bffc730bd5a5a89005869d2773480cf1738c592143b5173634b7d15"}}}}}}]'
            url = self.getFullUrl('/gql', self.API2_URL)
            sts, data = self.getPage(url, MergeDicts(self.defaultParams, {'raw_post_data': True}), post_data)
            if not sts:
                return urlTab
            try:
                data = byteify(e2Json_loads(data))
                for item in data[0]['data']['clip']['videoQualities']:
                    urlTab.append({'name': f"{item['quality']}p, {item['frameRate']}fps", 'url': item['sourceURL'], 'need_resolve': 0})
            except Exception:
                printExc()
        elif cItem['video_type'] == 'live':
            id = cItem['channel_id']
            tokenUrl = self.CHANNEL_TOKEN_URL
            vidUrl = self.LIVE_URL
            liveStream = True
        else:
            id = cItem.get('video_id', '')
            tokenUrl = self.VOD_TOKEN_URL
            vidUrl = self.VOD_URL
            liveStream = False

        if id != '':
            url = tokenUrl.format(id)
            sts, data = self.getPage(url)
            if sts:
                try:
                    data = e2Json_loads(data)
                    url = vidUrl.format(id, urllib_quote(jstr(data, 'token')), jstr(data, 'sig'))
                    data = getDirectM3U8Playlist(url, checkExt=False)
                    for item in data:
                        item['url'] = urlparser.decorateUrl(item['url'], {'iptv_proto': 'm3u8', 'iptv_livestream': liveStream})
                        urlTab.append(item)
                except Exception:
                    printExc()

        return urlTab

    def handleService(self, index, refresh=0, searchPattern='', searchType=''):
        printDBG('handleService start')

        CBaseHostClass.handleService(self, index, refresh, searchPattern, searchType)

        name = self.currItem.get("name", '')
        category = self.currItem.get("category", '')
        printDBG(f"handleService: ||| name[{name}], category[{category}] ")
        self.currList = []

    # MAIN MENU
        if name == None:
            self.listMain({'name': 'category', 'type': 'category'})

        elif category == 'browse':
            self.listDirectories(self.currItem)

        elif category == 'sub_items':
            self.listSubItems(self.currItem)

        elif category == 'dir_channels':
            self.listDirChannels(self.currItem, 'list_channel')
        elif category == 'list_channel':
            self.listChannel(self.currItem)

        elif category == 'videos_types':
            self.listsTab(self.VIDEOS_TYPES_TAB, MergeDicts(self.currItem, {'category': 'videos_sort'}))
        elif category == 'videos_sort':
            self.listsTab(self.VIDEOS_SORT_TAB, MergeDicts(self.currItem, {'category': 'list_videos'}))
        elif category == 'list_videos':
            self.listVideos(self.currItem)

        elif category == 'clips_filters':
            self.listsTab(self.CLIPS_FILTERS_TAB, MergeDicts(self.currItem, {'category': 'list_clips'}))
        elif category == 'list_clips':
            self.listClips(self.currItem)

        elif category == 'dir_games':
            self.listDirGames(self.currItem, 'browse_game')
        elif category == 'browse_game':
            self.listsTab(self.GAME_CAT_TAB, self.currItem)
        elif category == 'game_lang':
            self.listsTab(self.langItems, MergeDicts(self.currItem, {'category': self.currItem['next_category']}))
        elif category == 'game_channels':
            self.listGameChannels(self.currItem, 'list_channel')

        elif category == 'game_videos_types':
            self.listsTab(self.VIDEOS_TYPES_TAB, MergeDicts(self.currItem, {'category': 'game_videos_sort'}))
        elif category == 'game_videos_sort':
            self.listsTab(self.VIDEOS_SORT_TAB, MergeDicts(self.currItem, {'category': 'game_list_videos'}))
        elif category == 'game_list_videos':
            self.listGameVideos(self.currItem)

        elif category == 'game_clips_filters':
            self.listsTab(self.CLIPS_FILTERS_TAB, MergeDicts(self.currItem, {'category': 'game_list_clips'}))
        elif category == 'game_list_clips':
            self.listGameClips(self.currItem)

        elif category == 'v5_channels':
            self.listV5Channels(self.currItem)
        elif category == 'v5_games':
            self.listV5Games(self.currItem)
        elif category == 'v5_streams':
            self.listV5Streams(self.currItem)

    # SEARCH
        elif category in ["search", "search_next_page"]:
            cItem = dict(self.currItem)
            cItem.update({'search_item': False, 'name': 'category'})
            self.listSearchResult(cItem, searchPattern, searchType)
    # HISTORIA SEARCH
        elif category == "search_history":
            self.listsHistory({'name': 'history', 'category': 'search'}, 'desc', _("Type: "))
        else:
            printExc()

        CBaseHostClass.endHandleService(self, index, refresh)


class IPTVHost(CHostBase):

    def __init__(self):
        CHostBase.__init__(self, Twitch(), True, [])

    def getSearchTypes(self):
        searchTypesOptions = []
        searchTypesOptions.append((_("Games"), "games"))
        searchTypesOptions.append((_("Live streams"), "streams"))
        searchTypesOptions.append((_("Channles"), "channels"))
        return searchTypesOptions
