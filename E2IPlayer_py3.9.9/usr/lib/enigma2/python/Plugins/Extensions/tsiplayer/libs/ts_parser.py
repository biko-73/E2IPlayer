# -*- coding: utf8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools              import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs               import dom_parser
from Plugins.Extensions.IPTVPlayer.libs                         import ph
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools       import tscolor
import re

def parseDOM(html, name='', attrs=None, ret=False):
    if attrs: attrs = dict((key, re.compile(value + ('$' if value else ''))) for key, value in attrs.iteritems())
    results = dom_parser.parse_dom(html, name, attrs, ret)
    if ret:
        results = [result.attrs[ret.lower()] for result in results]
    else:
        results = [result.content for result in results]
    return results


def get_imdb_items(data):
	items  = parseDOM(data, 'div', attrs = {'class': 'lister-item .+?'})
	items += parseDOM(data, 'div', attrs = {'class': 'list_item.+?'})
	elms=[]
	for item in items:
		elm ={}
		title = parseDOM(item, 'a')[1]
		title = str(ph.clean_html(title))
		elm['title']=title
		year  = parseDOM(item, 'span', attrs = {'class': 'lister-item-year.+?'})
		year += parseDOM(item, 'span', attrs = {'class': 'year_type'})
		try: year = re.compile('(\d{4})').findall(str(year))[0]
		except: year = '0'
		elm['year']=year
		imdb = parseDOM(item, 'a', ret='href')[0]
		imdb = re.findall('(tt\d*)', imdb)[0]
		elm['imdb']=imdb
		try: poster = parseDOM(item, 'img', ret='loadlate')[0]
		except: poster = '0'
		if '/nopicture/' in poster: poster = '0'
		poster = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX300.', poster)
		poster = ph.clean_html(poster)
		elm['poster']=poster
		try: genre = parseDOM(item, 'span', attrs = {'class': 'genre'})[0]
		except: genre = '0'
		genre = ' / '.join([i.strip() for i in genre.split(',')])
		if genre == '': genre = '0'
		genre = ph.clean_html(genre)
		elm['genre']=genre
		try: duration = re.findall('(\d+?) min(?:s|)', item,re.S)[-1]
		except: duration = '0'
		elm['duration']=duration
		rating = '0'
		try: rating = parseDOM(item, 'span', attrs = {'class': 'rating-rating'})[0]
		except: pass
		try: rating = parseDOM(rating, 'span', attrs = {'class': 'value'})[0]
		except: rating = '0'
		try: rating = parseDOM(item, 'div', ret='data-value', attrs = {'class': '.*?imdb-rating'})[0]
		except: pass
		if rating == '' or rating == '-': rating = '0'
		rating = ph.clean_html(rating)
		elm['rating']=rating
		try: votes = parseDOM(item, 'div', ret='title', attrs = {'class': '.*?rating-list'})[0]
		except: votes = '0'
		try: votes = re.findall('\((.+?) vote(?:s|)\)', votes,re.S)[0]
		except: votes = '0'
		if votes == '': votes = '0'
		votes = ph.clean_html(votes)
		elm['votes']=votes
		try: mpaa = parseDOM(item, 'span', attrs = {'class': 'certificate'})[0]
		except: mpaa = '0'
		if mpaa == '' or mpaa == 'NOT_RATED': mpaa = '0'
		mpaa = mpaa.replace('_', '-')
		mpaa = ph.clean_html(mpaa)
		elm['mpaa']=mpaa
		try: director = re.findall('Director(?:s|):(.+?)(?:\||</div>)', str(item),re.S)[0]
		except: director = '0'
		director = parseDOM(director, 'a')
		director = ' / '.join(director)
		if director == '': director = '0'
		director = ph.clean_html(director)
		elm['director']=director
		try: cast0 = re.findall('Stars(?:s|):(.+?)(?:\||</div>)', item, re.S)[0]
		except: cast0 = '0'
		cast = parseDOM(cast0, 'a')
		if cast == []: cast = '0'
		elm['cast']=cast
		plot = '0'
		try: plot = parseDOM(item, 'p', attrs = {'class': 'text-muted'})[0]
		except: pass
		try: plot = parseDOM(item, 'div', attrs = {'class': 'item_description'})[0]
		except: pass
		plot = plot.rsplit('<span>', 1)[0].strip()
		plot = re.sub('<.+?>|</.+?>', '', plot)
		if plot == '': plot = '0'
		plot = ph.clean_html(plot)
		elm['plot']=plot
		desc=''
		if rating!='0'    : desc=desc+tscolor('\c00????00')+'Rating: '+tscolor('\c00??????')+str(rating)+'/10 | '
		if year!='0'      : desc=desc+tscolor('\c00????00')+'Year: '+tscolor('\c00??????')+str(year)+' | '
		if mpaa!='0'      : desc=desc+tscolor('\c00????00')+'Type: '+tscolor('\c00??????')+str(mpaa)+' | '
		if duration!='0'  : desc=desc+tscolor('\c00????00')+'Duration: '+tscolor('\c00??????')+str(duration)+' | '
		if genre!='0'     : desc=desc+'\n'+tscolor('\c00????00')+'Genre: '+tscolor('\c00??????')+str(genre)
		if plot!='0'      : desc=desc+'\n'+tscolor('\c00????00')+'Plot: '+tscolor('\c0000????')+str(plot)
		elm['desc']=desc
		elms.append(elm)
	return elms
