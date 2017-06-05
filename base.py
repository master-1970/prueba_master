# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canal (base) por Hernan_Ar_c
# ------------------------------------------------------------

import re
from core import logger
from core import config
from core import scrapertools
from core.item import Item
from core import servertools
from core import httptools
from core import tmdb

host = 'url_inicial'

def mainlist(item):
    logger.info()

    itemlist = []
    
    itemlist.append(item.clone(title="Todas",
                               action="lista",
                               thumbnail='https://s12.postimg.org/iygbg8ip9/todas.png',
                               fanart='https://s12.postimg.org/iygbg8ip9/todas.png',
                               url = host
                               ))

    #itemlist.append(item.clone(title="Generos",
    #                           action="generos",
    #                           url=host,
    #                           thumbnail='https://s31.postimg.org/szbr0gmkb/generos.png',
    #                           fanart='https://s31.postimg.org/szbr0gmkb/generos.png'
    #                           ))
    
    

    return itemlist

def get_source(url):
    logger.info()
    data = httptools.downloadpage(url).data
    data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>|\s{2,}', "", data)
    return data

def lista (item):
    logger.info ()
	
    itemlist = []
    data = get_source(item.url)
    logger.debug (data)
    #return
    patron = ''
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedyear, scrapedthumbnail in matches:
        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot= ''
        contentTitle=scrapedtitle
        title = contentTitle
        year = scrapedyear
        fanart =''
        
        itemlist.append(item.clone(action='findvideos' ,
                                   title=title, url=url,
                                   thumbnail=thumbnail,
                                   plot=plot,
                                   fanart=fanart,
                                   contentTitle = contentTitle,
                                   infoLabels ={'year':year}
                                       ))
    #tmdb.set_infoLabels_itemlist(itemlist, seekTmdb =True)
 #Paginacion

    if itemlist !=[]:
        actual_page_url = item.url
        next_page = scrapertools.find_single_match(data,'')
        import inspect
        if next_page !='':
           itemlist.append(item.clone(action = "lista",
                                      title = 'Siguiente >>>',
                                      url = next_page,
                                      thumbnail='https://s32.postimg.org/4zppxf5j9/siguiente.png'
                                      ))
    return itemlist

def findvideos(item):
    logger.info()
    itemlist=[]
    data = get_source(item.url)
    url = scrapertools.find_single_match(data,'')
    itemlist.extend(servertools.find_video_items(data=url))
    if not itemlist:
        patron = ''
        matches = matches = re.compile(patron,re.DOTALL).findall(data)
        for videoitem in matches:
            itemlist.extend(servertools.find_video_items(data=videoitem))

    for videoitem in itemlist:
        videoitem.channel = item.channel
        videoitem.action ='play'
        videoitem.thumbnail = servertools.guess_server_thumbnail(videoitem.url)
        videoitem.infoLabels = item.infoLabels
        #videoitem.title = item.title+' ('+videoitem.server+')'
        videoitem.title = url
    return itemlist

