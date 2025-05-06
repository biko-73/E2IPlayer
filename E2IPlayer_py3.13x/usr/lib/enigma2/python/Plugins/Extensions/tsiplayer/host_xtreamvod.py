# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,xtream_get_conf,tscolor

import re


def getinfo():
	info_={}
	info_['name']='Xtream IPTV (VOD)'
	info_['version']='1.0 24/04/2019'
	info_['dev']='RGYSoft'
	info_['cat_id']='11'
	info_['desc']='مشاهدة القنوات مباشر من اشتراكات xtream'
	info_['icon']='https://i.ibb.co/nPHsSDp/xtream-code-iptv.jpg'
	info_['recherche_all']='1'
	info_['filtre']='xtream_active'
			
	return info_

class TSIPHost(TSCBaseHostClass):
	def __init__(self):
		TSCBaseHostClass.__init__(self,{'cookie':'xtream.cookie'})
		self.USER_AGENT = 'Mozilla/5.0 (Linux; Android 4.4.2; SAMSUNG-SM-N900A Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36'
		self.MAIN_URL = ''
		self.HEADER = {'User-Agent': self.USER_AGENT, 'X-Requested-With': 'com.sportstv20.app','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
		self.defaultParams = {'header':self.HEADER, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
		
		
	def showmenu0(self,cItem):
		multi_tab=xtream_get_conf()
		if len(multi_tab)==0:
			self.addMarker({'title':'Please configure xstream first','icon':cItem['icon'],'desc':'Please configure xstream first, (add user,pass &host in tsiplayer params or add your config file in /etc/tsiplayer_xtream.conf)'})	
		elif len(multi_tab)==1:
			self.showmenu1({'import':cItem['import'],'icon':cItem['icon'],'xuser':multi_tab[0][2],'xpass':multi_tab[0][3],'xhost':multi_tab[0][1],'xua':multi_tab[0][4]})
		else:	
			for elm in multi_tab:
				self.addDir({'import':cItem['import'],'category' : 'host2','title': elm[0],'icon':cItem['icon'],'xuser':elm[2],'xpass':elm[3],'xhost':elm[1],'xua':elm[4],'mode':'20'})	
			self.addDir({'import':cItem['import'],'name':'search','category':'search'  ,'title': _('Search'),'search_item':True,'page':-1,'hst':'tshost','icon':cItem['icon']})

	def showmenu1(self,cItem):
		try:
			self.addMarker({'category' : 'xtream_vod','title':tscolor('\c0000??00')+'Films','icon':'','desc':''})
			Url=cItem['xhost']+'/player_api.php?username='+cItem['xuser']+'&password='+cItem['xpass']+'&action=get_vod_categories'
			sts, data = self.cm.getPage(Url)
			data = json_loads(data)
			self.addDir({'import':cItem['import'],'category' : 'host2','category_id':'','title':'All','desc':'','xuser':cItem['xuser'],'xpass':cItem['xpass'],'xhost':cItem['xhost'],'xua':cItem['xua'],'mode':'21','icon':cItem['icon']} )
			for elm in data:
				self.addDir({'import':cItem['import'],'good_for_fav':True,'category' : 'host2','category_id': elm['category_id'],'title':elm['category_name'].strip(),'desc':'','xuser':cItem['xuser'],'xpass':cItem['xpass'],'xhost':cItem['xhost'],'xua':cItem['xua'],'mode':'21','icon':cItem['icon']} )	
		except:
			pass					
		try:	
			self.addMarker({'category' : 'xtream_vod','title':tscolor('\c0000??00')+'Series','icon':'','desc':''})
			Url=cItem['xhost']+'/player_api.php?username='+cItem['xuser']+'&password='+cItem['xpass']+'&action=get_series_categories'
			sts, data = self.cm.getPage(Url)
			data = json_loads(data)
			self.addDir({'import':cItem['import'],'name':'categories','category' : 'host2','category_id': '','title':'All','desc':'','xuser':cItem['xuser'],'xpass':cItem['xpass'],'xhost':cItem['xhost'],'xua':cItem['xua'],'mode':'22','icon':cItem['icon']} )	
			for elm in data:
				self.addDir({'import':cItem['import'],'good_for_fav':True,'name':'categories','category' : 'host2','category_id': elm['category_id'],'title':elm['category_name'].strip(),'desc':'','xuser':cItem['xuser'],'xpass':cItem['xpass'],'xhost':cItem['xhost'],'xua':cItem['xua'],'mode':'22','icon':cItem['icon']} )	
		except:
			pass
		self.addDir({'import':cItem['import'],'name':'search','category':'search'  ,'title': _('Search'),'search_item':True,'page':-1,'hst':'tshost','icon':cItem['icon']})
		
	def showmenu_films(self,cItem):
		Url=cItem['xhost']+'/player_api.php?username='+cItem['xuser']+'&password='+cItem['xpass']+'&action=get_vod_streams&category_id='+str(cItem['category_id'])
		sts, data = self.cm.getPage(Url)
		data = json_loads(data)
		for elm in data:
			Url=cItem['xhost']+'/movie/'+cItem['xuser']+'/'+cItem['xpass']+'/'+str(elm['stream_id'])+'.'+elm['container_extension']
			if cItem['xua']!='': Url  = strwithmeta(Url,{'User-Agent' : cItem['xua']})
			if elm['stream_icon']: stream_icon =elm['stream_icon']
			else: stream_icon = ''
			rating = elm.get('rating','')
			if rating: desc = tscolor('\c00????00')+'RATING: '+tscolor('\c00??????')+str(rating)+'/10 \n'
			else:
				desc = ''
			titre = elm['name']
			if r'\u' in titre: titre = str(titre.decode('unicode-escape'))
			url_inf = cItem['xhost']+'/player_api.php?username='+cItem['xuser']+'&password='+cItem['xpass']+'&action=get_vod_info&vod_id='+str(elm['stream_id'])
			self.addVideo({'import':cItem['import'],'good_for_fav':True,'name':'categories','category' : 'host2','url': Url,'url_inf':url_inf,'title':titre,'icon':stream_icon,'desc':desc,'hst':'direct','EPG':True})
		
		
	def showmenu_series(self,cItem):		
		Url=cItem['xhost']+'/player_api.php?username='+cItem['xuser']+'&password='+cItem['xpass']+'&action=get_series&category_id='+str(cItem['category_id'])
		sts, data = self.cm.getPage(Url)
		data = json_loads(data)
		for elm in data:
			stream_icon =elm.get('cover','')
			rating = str(elm.get('rating',''))
			plot = str(elm.get('plot',''))
			genre = str(elm.get('genre',''))
			desc = tscolor('\c00????00')+'GENRE: '+tscolor('\c00??????')+str(genre)+'\n'+tscolor('\c00????00')+' RATING:'+tscolor('\c00??????')+str(rating)+'/10 \n'+tscolor('\c00????00')+'Plot: '+tscolor('\c00??????')+str(plot)
			titre = elm['name']
			if r'\u' in titre: titre = str(titre.decode('unicode-escape'))
			url_inf = cItem['xhost']+'/player_api.php?username='+cItem['xuser']+'&password='+cItem['xpass']+'&action=get_series_info&series_id='+str(elm['series_id'])
			self.addDir({'import':cItem['import'],'good_for_fav':True,'name':'categories','category' : 'host2','url_inf':url_inf,'url': str(elm['series_id']),'title':titre,'icon':stream_icon,'desc':desc,'hst':'xtream_vod','xuser':cItem['xuser'],'xpass':cItem['xpass'],'xhost':cItem['xhost'],'xua':cItem['xua'],'mode':'23','EPG':True})
		
	def showmenu_saisons(self,cItem):			
		xuser=cItem['xuser']
		xpass=cItem['xpass']
		xhost=cItem['xhost']
		xua=cItem['xua']
		Url=xhost+'/player_api.php'
		id_=cItem['url']
		img_=cItem['icon']
		liste = []
		post_data = {'username':xuser, 'password':xpass, 'action':'get_series_info','series_id':id_}
		sts, data = self.cm.getPage(Url, post_data=post_data)
		Liste_films_data2 = re.findall('"episodes":\{(.*)', data, re.S)
		if Liste_films_data2:
			data2=Liste_films_data2[0]
		else:
			data2=''
		Live_Cat_data = re.findall('id":"(.*?)"episode_num":(.*?)"title":"(.*?)".*?season":(.*?),',data2, re.S)
		for (id2_,x1,titre,season) in Live_Cat_data:
			elm = ('Season '+season,id_+'|'+season)
			if ( elm not in liste ):
				liste.append(elm)	 
				params = {'import':cItem['import'],'good_for_fav':True,'name':'categories','category' : 'host2','desc':cItem.get('desc',''),'url': season,'title':'Season '+season,'icon':img_,'id_':id_,'xuser':xuser,'xpass':xpass,'xhost':xhost,'xua':xua,'mode':'24'} 
				self.addDir(params)	
		
	def showmenu_episodes(self,cItem):			
		xuser=cItem['xuser']
		xpass=cItem['xpass']
		xhost=cItem['xhost']
		xua=cItem['xua']	
		Url=xhost+'/player_api.php'
		id_=cItem['id_']
		saison=cItem['url']		
		img_=cItem['icon']
		post_data = {'username':xuser, 'password':xpass, 'action':'get_series_info','series_id':id_}
		sts, data = self.cm.getPage(Url, post_data=post_data)
		Liste_films_data2 = re.findall('"episodes":\{(.*)', data, re.S)
		if Liste_films_data2:
			data2=Liste_films_data2[0]
		else: 
			data2=''
		Live_Cat_data = re.findall('id":"(.*?)","episode_num":(.*?)"title":"(.*?)","container_extension":"(.*?)".*?season":(.*?),',data2, re.S)
		for (id_,x1,titre,ext,season) in Live_Cat_data:
			link = xhost+'/series/'+xuser+'/'+xpass+'/'+id_+'.'+ext
			if ( season == saison):
				if xua!='':
					link  = strwithmeta(link,{'User-Agent' : xua})
				if r'\u' in titre: titre = str(titre.decode('unicode-escape'))
				params = {'import':cItem['import'],'good_for_fav':True,'name':'categories','category' : 'video','url': link,'title':titre,'icon':img_,'desc':cItem.get('desc',''),'hst':'direct'} 
				self.addVideo(params)	

	def getArticle(self, cItem):
		printDBG('ssssssssssssssssssssssssssssss')
		otherInfo1 = {}
		icon = cItem.get('icon','')
		desc = cItem.get('desc','')
		url = cItem.get('url_inf','')		
		sts, data = self.cm.getPage(url)
		if sts:
			data = json_loads(data)
			inf = data.get('info',[])
			if inf != []:
				desc = inf.get('plot','')
				#icon = inf.get('cover_big',inf.get('cover',icon))
				if inf.get('age','')         != '': otherInfo1['age_limit']   = inf.get('age','')
				if inf.get('country','')     != '': otherInfo1['country']     = inf.get('country','')
				if inf.get('genre','')       != '': otherInfo1['genre']       = inf.get('genre','')	
				if inf.get('duration','')    != '': otherInfo1['duration']    = inf.get('duration','')				
				if inf.get('episode_run_time','0')    != '0': otherInfo1['duration']    = inf.get('episode_run_time','')
				if inf.get('releasedate','') != '': otherInfo1['year'] = inf.get('releasedate','')				
				if inf.get('releaseDate','') != '': otherInfo1['year'] = inf.get('releasedate','')					
				
		title = cItem['title']		
		return [{'title':title, 'text': desc, 'images':[{'title':'', 'url':icon}], 'other_info':otherInfo1}]


	def SearchResult(self,str_ch,page,extra):
		multi_tab=xtream_get_conf()
		for elm in multi_tab:
			xhost_=elm[1]
			self.addMarker({'title':' ** '+elm[0]+' ** ','icon':'','desc':''})	
			try:
				Url=xhost_+'/player_api.php?username='+elm[2]+'&password='+elm[3]+'&action=get_vod_streams'
				sts, data = self.cm.getPage(Url)
				data = json_loads(data)
				printDBG('fffffffffffff'+str_ch.lower())
				
				for elm0 in data:
					if str_ch.lower() in elm0['name'].lower():
						Url=xhost_+'/movie/'+elm[2]+'/'+elm[3]+'/'+str(elm0['stream_id'])+'.'+elm0['container_extension']
						if elm[4]!='': Url  = strwithmeta(Url,{'User-Agent' : elm[4]})
						if elm0['stream_icon']: stream_icon =elm0['stream_icon']
						else: stream_icon = ''
						if elm0['rating']: rating = str(elm0['rating'])
						else: rating = ''			
						self.addVideo({'import':extra,'good_for_fav':True,'name':'categories','category' : 'video','url': Url,'title':elm0['name'],'icon':stream_icon,'desc':'Rating: '+rating,'hst':'direct'})	
			except:
				pass
			try:				
				Url=xhost_+'/player_api.php?username='+elm[2]+'&password='+elm[3]+'&action=get_series'
				sts, data = self.cm.getPage(Url)
				data = json_loads(data)
				for elm0 in data:
					if str_ch.lower() in elm0['name'].lower():
						if elm0['cover']: stream_icon =elm0['cover']
						else: stream_icon = ''
						if elm0['rating']: rating = str(elm0['rating'])
						else: rating = ''
						if elm0['plot']: plot = str(elm0['plot'])
						else: plot = ''
						if elm0['genre']: genre = str(elm0['genre'])
						else: genre = ''
						desc = 'GENRE:'+genre+' RATING:'+rating+'/10 \nPlot: '+plot
						self.addDir({'import':extra,'good_for_fav':True,'name':'categories','category' : 'host2','url': str(elm0['series_id']),'title':elm0['name'],'icon':stream_icon,'desc':desc,'xuser':elm[2],'xpass':elm[3],'xhost':xhost_,'xua':elm[4],'mode':'23'})
			except:
				pass	

	def start(self,cItem):
		mode=cItem.get('mode', None)
		if mode=='00':
			self.showmenu0(cItem)	
		if mode=='20':
			self.showmenu1(cItem)			
		elif mode=='21':
			self.showmenu_films(cItem)
		elif mode=='22':
			self.showmenu_series(cItem)
		elif mode=='23':
			self.showmenu_saisons(cItem)
		elif mode=='24':
			self.showmenu_episodes(cItem)
		return True
