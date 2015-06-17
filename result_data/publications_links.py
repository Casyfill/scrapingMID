#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Philipp Kats (c) June 2015
## scraping MID : Публикации
import requests, scraperwiki #, json, urllib, time,random
from datetime import datetime
import lxml.html


def scrapePageSMI(link, earl):
    '''
    scraping page from MID: answers to SMI;
    '''
    unique_keys = ('link', 'date')
    html = requests.get(link)
    
    if html.status_code != requests.codes.ok:
        # if something went bad
        print 'server goes bad'
        print html.status_code
        return
    
    dom = lxml.html.fromstring(html.content)
    rows = dom.cssselect("#content > div > div > font > table tr") # remove first two rows
    
    for row in rows:
        try:
            date=datetime.strptime(row.cssselect("td > b > font > a ")[0].text , "%m/%d/%Y")
            title=row.cssselect("td a")[1].text
            
            l='http://mid.ru' + row.cssselect("td a")[1].get('href')
            print date, title,l
            
            # page = lxml.html.fromstring(requests.get(l).content)
            # text = page.cssselect("div.doc-text")[0].text_content().replace('\n', ' ').replace('\r', '').strip()
            
            scraperwiki.sql.save(unique_keys, {'link':l,  'date':date, 'title':title})
        except Exception, e:
            print str(e)
            print 'ой, не тот ряд: ' #, row.cssselect("td > b > font")[0].text
    
    # print date
    # теперь выясним, не стоит ли остановиться
    if date < earl:
        # если слишком далеко закопались
        return None
    return '!'

  
earl = datetime.strptime('01/06/2012' , "%d/%m/%Y") #earliest date to parse
baselink = 'http://mid.ru/ns_publ.nsf/rdipl?open&Start=' #стартовая позиция        

for x in xrange(0,16):
    link = baselink + str(1+30*x)
    print link
    l = scrapePageSMI(link, earl)
    if l ==None: break
