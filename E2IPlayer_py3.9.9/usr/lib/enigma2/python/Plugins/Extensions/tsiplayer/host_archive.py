# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost
import re

def getinfo():
	info_={}
	name = 'Quran (Archive.Org)'
	hst = 'https://archive.org'
	info_['old_host'] = hst
	hst_ = tshost(name)	
	if hst_!='': hst = hst_
	info_['host']= hst
	info_['name']=name
	info_['version']='1.3 20/05/2019'
	info_['dev']='RGYSoft'
	info_['cat_id']='24'
	info_['desc']='تسجيلات لتفسير و تلاوة القرآن'
	info_['icon']='https://img.yumpu.com/62618769/1/358x516/holy-quran.jpg?quality=85'
	info_['recherche_all']='0'
	info_['update']='Add Rokia Chariya'

	return info_


class TSIPHost(TSCBaseHostClass):
	def __init__(self):
		TSCBaseHostClass.__init__(self,{'cookie':'archive.cookie'})
		self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
		self.MAIN_URL = getinfo()['host']
		self.HEADER = {'User-Agent': self.USER_AGENT, 'Connection': 'keep-alive', 'Accept-Encoding':'gzip', 'Content-Type':'application/x-www-form-urlencoded','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
		self.defaultParams = {'header':self.HEADER, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
		self.getPage = self.cm.getPage
		
	def showmenu(self,cItem):
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'تفسير القرآن للشيخ الشعراوي','url':'https://archive.org/download/movie-tafseer-alsha3rawi-video-full','icon':'https://upload.wikimedia.org/wikipedia/en/8/8b/Muhamad_Motwali_Alsharawi.png','mode':'20'})	

		self.addMarker({'title':tscolor('\c00????00')+'رواية حفص','icon':cItem['icon']})
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'المصحف المرتل المصور برواية حفص - ماهر المعيقلي','url':'https://archive.org/download/alfirdwsiy2018_gmail_554222222222222222222222','icon':'http://cdn.marketplaceimages.windowsphone.com/v8/images/413798a4-da4b-4a3d-b56f-339f7bc8202f?imageType=ws_icon_large','mode':'20'})	
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'المصحف المصور - المنشاوي','url':'https://archive.org/download/Alfirdwsiy143fffffffffffffffffffffffffffffffffffffffffffffffff524547768986785634','icon':'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Elminshwey.jpg/280px-Elminshwey.jpg','mode':'20'})	
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'الختمة المجودة المنوعة - المجد','url':'https://archive.org/download/alfirdwsi4765780990756434678909087956mail_30','icon':'https://www.almajdtv.com/images/ch/quran.png','mode':'20'})	
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'المصحف المصور - ماهر المعيقلي','url':'https://archive.org/download/002SuratAl3568568BaqarahMaherAlMuaiqly_201704','icon':'http://cdn.marketplaceimages.windowsphone.com/v8/images/413798a4-da4b-4a3d-b56f-339f7bc8202f?imageType=ws_icon_large','mode':'20'})	
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'مصحف المنشاوي معلم مع ترديد الاطفال','url':'https://archive.org/download/video-semsem-chanal-alminshawi----teacher-repeat-kids-high-quality','icon':'https://archive.org/download/video-semsem-chanal-alminshawi----teacher-repeat-kids-high-quality/video-semsem-chanal-alminshawi----teacher-repeat-kids-high-quality.thumbs/001-_000057.jpg','mode':'20'})	
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'القرآن الكريم  رافع العامري','url':'https://archive.org/download/Alfirdfwtgtytkojhgfwetyetiuoiuopiitytwetyiiuoppiouotere1801','icon':'http://www.ruqayah.net/pic/rafee-aameri-quran.jpg','mode':'20'})	
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'حيدر الغالبي مصحف مصور معلم','url':'https://archive.org/download/Alfirdwsiy1433_gmaigfghui7oiopouyytrqeetyuioipupyurerw1','icon':cItem['icon'],'mode':'20'})	

		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'خالد الجليل القرآن كامل','url':'https://archive.org/download/Koran_201701','icon':'https://lh5.ggpht.com/G5bA6O35ULxADBCZqlt0hAbWO37p83fmfSohCnsilDLW6zSPoGC3oYWjhvLjmNIdSIXg=w300','mode':'20'})	
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'مقتطفات من مصحف خالد الجليل 1437','url':'https://archive.org/download/alfirdwsiy1433_gm35688888888888888888888568ail_1437','icon':'https://lh5.ggpht.com/G5bA6O35ULxADBCZqlt0hAbWO37p83fmfSohCnsilDLW6zSPoGC3oYWjhvLjmNIdSIXg=w300','mode':'20'})	
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'عبد الباسط عبد الصمد الختمة المرتلة','url':'https://archive.org/download/aa_HD_20160130_0603','icon':'https://i.pinimg.com/236x/e4/ef/89/e4ef89509170860e71ad8deaa383292a--quran-people.jpg','mode':'20'})			
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'المكتبة الشاملة لتراث الشيخ عبد الباسط عبدالصمد : تلاوات المحافل الخارجية','url':'https://archive.org/download/Comprehensive-Library-Heritage-Sheikh-Abdul-Basit-Abdul-Samad-Recitations-Foreign-Forums','icon':'https://i.pinimg.com/236x/e4/ef/89/e4ef89509170860e71ad8deaa383292a--quran-people.jpg','mode':'20','sub_mode':'2'})			




		self.addMarker({'title':tscolor('\c00????00')+'رواية شعبة','icon':cItem['icon']})
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'المصحف المرتل المصور برواية شعبة عن عاصم  بصوت الشيخ عبدالرشيد صوفي','url':'https://archive.org/download/Alfirdwsiy1BV346579889HFS_201801','icon':cItem['icon'],'mode':'20'})	

		self.addMarker({'title':tscolor('\c00????00')+'رواية قالون','icon':cItem['icon']})
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'المصحف المرتل المصور برواية قالون - محمود خليل الحصري','url':'https://archive.org/download/Alfirdwsiy15hjj8579645632557809p67732478903g_002._201801','icon':'https://upload.wikimedia.org/wikipedia/ar/a/a9/%D8%A7%D9%84%D8%AD%D8%B5%D8%B1%D9%8A.jpg','mode':'20'})	
		
		self.addMarker({'title':tscolor('\c00????00')+'رواية ورش','icon':cItem['icon']})				
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'المصحف المصور المعلم-  ياسين الجزائري برواية ورش عن نافع','url':'https://archive.org/download/alfirdwsiy146779674794794679464679796479gmail_28','icon':'https://www.tvquran.com/uploads/authors/images/%D9%8A%D8%A7%D8%B3%D9%8A%D9%86%20%D8%A7%D9%84%D8%AC%D8%B2%D8%A7%D8%A6%D8%B1%D9%8A.jpg','mode':'20'})	
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'المصحف المعلم المصور المرمز بالألوان رواية ورش بصوت الشيخ محمود خليل الحصري','url':'https://archive.org/download/abdelsattar57_hotmail_1_201805','icon':'https://upload.wikimedia.org/wikipedia/ar/a/a9/%D8%A7%D9%84%D8%AD%D8%B5%D8%B1%D9%8A.jpg','mode':'20','sub_mode':'1'})	

		self.addMarker({'title':tscolor('\c00????00')+'رواية أبي الحارث','icon':cItem['icon']})
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'المصحف المرتل برواية أبي الحارث عن الكسائي بصوت الشيخ عبدالرشيد صوفي','url':'https://archive.org/download/aVC2535468955GFDSAlfirdwsiy1433_gmail_201801','icon':cItem['icon'],'mode':'20'})	

		self.addMarker({'title':tscolor('\c00????00')+'رواية ابن وردان','icon':cItem['icon']})
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'المصحف المرتل المصور برواية ابن وردان عن أبي جعفر بصوت الشيخ يوسف بن نوح','url':'https://archive.org/download/alfirdwsiy2018111111111111111ail_002.11111','icon':cItem['icon'],'mode':'20'})	
		
		self.addMarker({'title':tscolor('\c00????00')+'رواية ابن جماز','icon':cItem['icon']})
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':' مصحف مصور معلم برواية إبن جماز عن أبي جعفر للشيخ عيسى الشاذلى','url':'https://archive.org/download/999999999999999999999999955553339999','icon':cItem['icon'],'mode':'20'})	

		self.addMarker({'title':tscolor('\c00????00')+'مواد اخرة','icon':cItem['icon']})
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'مكتبة الرقية الشرعية بأصوات عدة قراء','url':'https://archive.org/download/Roquia_23','icon':cItem['icon'],'mode':'20'})	
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'اناشيد مشارى العفاسى','url':'https://archive.org/download/all--album--mshary--al3afasy--mp3-anasheed-anashed-anashid','icon':cItem['icon'],'mode':'20'})	
		self.addDir({'good_for_fav':True,'import':cItem['import'],'category' : 'host2','title':'اناشيد ماهر زين','url':'https://archive.org/download/maher-zean-----anashid----mp3---without---music--anashed_668','icon':cItem['icon'],'mode':'20'})	


			
	def showitms(self,cItem):
		Url=cItem.get('url','')	
		gnr=cItem.get('sub_mode','')
			
		if gnr=='' or gnr=='2':
			if gnr=='2':
				self.addAudio({'import':cItem['import'],'title':'قصار السور ل عبد الباسط مع صدى الصوت الرهيب بجودة رهيبة','url':'https://ia801609.us.archive.org/31/items/sada-soot-abd-albasit-abd-alsamad-9essar-alsowar-32kb/Abdubasit1_all.mp3','desc':'','icon':cItem['icon'],'hst':'direct'})
			sts, data = self.getPage(Url)
			if sts:
				Liste_cat_data = re.findall('<tr >.*?href="(.*?)">(.*?)<.*?<td>.*?<td>(.*?)<', data, re.S)
				for (url,titre,desc) in Liste_cat_data:
					if ('.mkv' in titre) or ('.mp4' in titre) or ('.mp3' in titre):
						titre=titre.replace('من المصحف المرتل المصور برواية قالون عن نافع بصوت الشيخ محمود خليل الحصري','')
						url=Url+'/'+url	
						if '.mp3' in titre :
							self.addAudio({'import':cItem['import'],'title':titre,'url':url,'desc':desc,'icon':cItem['icon'],'hst':'direct'})							
						else:
							self.addVideo({'import':cItem['import'],'title':titre,'url':url,'desc':desc,'icon':cItem['icon'],'hst':'direct'})
		else:
			sts, data = self.getPage(Url)
			if sts:
				lst=[]
				Liste_cat_data = re.findall('<tr >.*?href="(.*?)">(.*?)<.*?<td>.*?<td>(.*?)<', data, re.S)
				for (url,titre,desc) in Liste_cat_data:
					printDBG(url)
					if ('.mkv' in titre) or ('.mp4' in titre) or ('.mp3' in titre):
						url=url.replace('%D8%B3%D9%88%D8%B1%D8%A9%20%D8%A7%D9%84%D9%81%D8%A7%D8%AA%D8%AD%D8%A9%20%D9%85%D9%86%20%D8%A7%D9%84%D9%85%D8%B5%D8%AD%D9%81%20%D8%A7%D9%84%D9%85%D8%B9%D9%84%D9%85%20%D8%A7%D9%84%D9%85%D8%B5%D9%88%D8%B1%20%20%D8%A7%D9%84%D9%85%D8%B1%D9%85%D8%B2%20%D8%A8%D8%A7%D9%84%D8%A3%D9%84%D9%88%D8%A7%D9%86_%20%D8%B1%D9%88%D8%A7%D9%8A%D8%A9%20%D9%88%D8%B1%D8%B4%20_%20%20%D8%A8%D8%B5%D9%88%D8%AA%20%D8%A7%D9%84%D8%B4%D9%8A%D8%AE%20%D9%85%D8%AD%D9%85%D9%88%D8%AF%20%D8%AE%D9%84%D9%8A%D9%84%20%D8%A7%D9%84%D8%AD%D8%B5%D8%B1%D9%8A','__')
						code_data = re.findall('([0-9]+?)_', url, re.S)
						if code_data:
							code=int(code_data[0])
						else:
							code=78
							desc=desc+' JOZE AMMA FULL'
						url=Url+'/'+url	
						lst.append((code,url,titre,desc))
				if len(lst)>1:
					lst=sorted(lst, key=lambda x: (x[0]))
				for (code,url,titre,desc) in lst:
					if code>0:
						self.addVideo({'import':cItem['import'],'title':str(code),'url':url,'desc':titre+' ('+desc+')','icon':cItem['icon'],'hst':'direct'})


	def start(self,cItem):
		mode=cItem.get('mode', None)
		if mode=='00':
			self.showmenu(cItem)	
		elif mode=='20':
			self.showitms(cItem)		
		return True
