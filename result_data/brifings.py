#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Philipp Kats (c) June 2015
## scraping MID : Брифинги
import requests, scraperwiki #, json, urllib, time,random
from datetime import datetime
import lxml.html

unique_keys = ('link')
                    
def replaceMonth(txt):
    months = {u'апреля':'04',u'мая':'05',u'июня':'06',u'июля':'07',u'августа':'08',u'сентября':'09',u'октября':'10',u'ноября':'11',u'декабря':'12',u'января':'01',u'февраля':'2',u'марта':'3'}            
    for m in months.keys():
        if m in txt:
            txt.replace(m,months[m])
    return txt
    
link = 'http://mid.ru/bdomp/brp_4.nsf/briefviewmn!OpenView&Start=1&Count=30&Expand=1.3#1.3'


def scrapeState(link):
    html = requests.get(link)
    dom = lxml.html.fromstring(html.content)
    rows = dom.cssselect('tr[valign="top"]')
    # print len(rows)
    for row in rows:
        if len(row.cssselect('td'))==10:
            date = row.cssselect('td > b >font ')[0].text[8:-5].replace(' ','.')
            date = replaceMonth(date)
            # print date
            lnk='http://mid.ru' +  row.cssselect('td > font > a ')[0].get('href')
            print date, lnk
            scraperwiki.sql.save(unique_keys, {'link':lnk,  'date':date})

baseLink = "http://mid.ru/bdomp/brp_4.nsf/briefviewmn!OpenView&Start=1&Count=30&Expand=*#*"
for x in xrange(1,8):
    for y in xrange(1,13):
        ID = '%d.%d' % (x,y)
        print ID
        link = baseLink.replace('*',ID)
        scrapeState(link)