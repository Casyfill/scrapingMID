#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Philipp Kats (c) June 2015
## scraping MID : опровержения

import requests, scraperwiki #, json, urllib, time,random
from datetime import datetime
import lxml.html


def scrapePageSMI(link):
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
    rows = dom.cssselect("#content > div > div > font > table tr")
    
    # print 'строк:', len(rows)
    for row in rows:
        try:
            date=datetime.strptime(row.cssselect("td > b > font > a")[0].text , "%m/%d/%Y")
            title=row.cssselect("td a")[1].text
            l='http://mid.ru' + row.cssselect("td a")[1].get('href')
            print date, l,title
                
            # page = lxml.html.fromstring(requests.get(l).content)
            # text = page.cssselect("#content > div.center-block")[0].text_content().replace('\n', ' ').replace('\r', '').strip()
                
            scraperwiki.sql.save(unique_keys, {'link':l,  'date':date, 'title':title})
        except Exception, e:
            print str(e)
            print 'ой, не тот ряд'
            
        
  

links = ['http://mid.ru/ns_publ.nsf/opr?open&Start=1','http://mid.ru/ns_publ.nsf/opr?open&Start=31','http://mid.ru/ns_publ.nsf/opr?open&Start=61'] #стартовая позиция        

for link in links:
    print link
    scrapePageSMI(link)

# print 'start'   
# ll='http://mid.ru/bdomp/ns_publ.nsf/71efd0b697409f85c3256fc7002e091d/a42a3ce87af0536443257e2300216b1d!OpenDocument'
# html = requests.get(ll)
# print html.status_code
# p = lxml.html.fromstring(html.content)

# text = p.cssselect("#content > div.center-block")[0].text_content().replace('\n', ' ').replace('\r', '').strip()



