#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Philipp Kats (c) June 2015
## scraping MID : официальные заявления

import requests, scraperwiki #, json, urllib, time,random
from datetime import datetime
import lxml.html


def scrapePageSMI(link, earl):
    '''
    scraping page from MID: answers to SMI; example link: http://mid.ru/bdomp/brp_4.nsf/pressotofpr!OpenView&Start=1
    '''
    unique_keys = ('link', 'date')
    html = requests.get(link)
    
    if html.status_code != requests.codes.ok:
        # if something went bad
        print 'server goes bad'
        print html.status_code
        return
    
    dom = lxml.html.fromstring(html.content)
    rows = dom.cssselect("#content > div > div > table tr") # remove first two rows
    
    for row in rows:
        try:
            date=datetime.strptime(row.cssselect("td > font")[0].text , "%d.%m.%Y")
            title=row.cssselect("td a")[0].text
            l='http://mid.ru' + row.cssselect("td a")[0].get('href')
            # print date, title,link
                
            page = lxml.html.fromstring(requests.get(l).content)
            text = page.cssselect("div.doc-text")[0].text_content().replace('\n', ' ').replace('\r', '').strip()
                
            scraperwiki.sql.save(unique_keys, {'link':l,  'date':date, 'title':title, 'text':text})
        except Exception, e:
            # print str(e)
            print 'ой, не тот ряд'
            
        
    # print date
    # теперь выясним, не стоит ли остановиться
    if date < earl:
        # если слишком далеко закопались
        return None
    
    n = dom.cssselect("#content > div > div > a")[-1]
    if n.cssselect('img')[0].get('alt') != u'Вперед':
        return None
        pass
    
    newLink = n.get('href')
    
    if newLink in link:
        # если та же самая ссылка
        return None
        pass
    
    # печатаем и возвращаем ссылку на сл.
    r = 'http://mid.ru' + newLink
    print r
    return r
  
earl = datetime.strptime('01/06/2012' , "%d/%m/%Y") #earliest date to parse
link = 'http://mid.ru/bdomp/brp_4.nsf/spsza!OpenView&Start=2.10' #стартовая позиция        

# link = scrapePageSMI(link, earl)
while True:
    link = scrapePageSMI(link, earl)
    if link == None:
        break
    
    


