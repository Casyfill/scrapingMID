#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Philipp Kats (c) June 2015
## scraping MID : Публикации
import requests, scraperwiki, urllib #, json, urllib, time,random
import time, random
from HTMLParser import HTMLParser

unique_keys = ('link')

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def getLinksFromScraperWiki(baselink, offset=0, steak=10000):
    '''get Data from another ScraperWiki VM'''
    q  =  urllib.quote('SELECT link FROM swdata ORDER BY date ASC LIMIT %d OFFSET %d' %(steak,offset))
    return requests.get(baselink + q).json()


def scrapeMIDtext(link): 
    '''As something bad with article server and markup, 
    we had to parse it ugli, just removing any html tags from raw html'''
    html = requests.get(link)
    
    # cut html
    st = html.content.find('<!--Текст-->')+len('<!--Текст-->')
    end = html.content.find('<center><table><tr>')
    # print st, end
    raw = html.content[st:end]
    # print raw
    
    # title_start= raw.find('<font size="4"') + len('<font size="4"')
    # title_end = raw.find('</font>',title_start)
    # title = raw[title_start:title_end].split('>')[1].strip()
    # print title
    
    txt = strip_tags(raw)
    scraperwiki.sql.save(unique_keys, {'link':link,  'text':txt.decode('utf-8','ignore')})

# link = 'http://mid.ru/bdomp/ns_publ.nsf/cb8e241d18a8904ec3256fc7002ddc0e/ac26746a865e8ade43257e18004d0c8e!OpenDocument'
# scrapeMIDtext(link)

baselink = 'https://premium.scraperwiki.com/uh4itf1/llzitkmwdretqxi/sql/?q='
pool = getLinksFromScraperWiki(baselink,offset=0,steak=250)
random.shuffle(pool)
count=0

for x in pool:
    # print l
    scrapeMIDtext(x['link'])
    # time.sleep(3)
    count+=1
    print count
