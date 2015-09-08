import xml.etree.ElementTree as ET
import urllib, urllib2, time
from datetime import date, timedelta, datetime
from pymongo import MongoClient
from articlesearch import Domains

AppKey = 'sPzLhSbLMsXN9s8w'
ApiMethod = 'http://api.eventful.com/rest/events/search'
domain2id = {
    'Arts': ['art', 'performing_arts', 'music'],
    'Education': ['learning_education'],
    'Health': ['support'],
    'Science': ['science'],
    'Sports': ['sports']
}
eventInfoFields = ['url', 'title', 'description', 'venue_name', 'venue_address', 'city_name', 'region_name']

class EventSearcher:
    def __init__(self, domains, begin_date = date.today(), end_date = None, num_per_dm = 1000):
        self.domains = Domains
        self.begin_date = begin_date
        self.end_date = end_date
        if self.end_date is None:
            self.end_date = self.begin_date + timedelta(days = 6)
        self.npd = num_per_dm
        client = MongoClient()
        self.collection = client.test.events

    def getInitialQParams(self, domain):
        qparams = {}
        qparams['app_key'] = AppKey
        #qparams['keywords'] = 'Obama'
        qparams['location'] = 'United States'
        qparams['category'] = ','.join(domain2id[domain])
        qparams['date'] = '{0}00-{1}00'.format(self.begin_date.strftime('%Y%m%d'), self.end_date.strftime('%Y%m%d'))
        #qparams['sort_order'] = 'date'
        qparams['page_size'] = 50
        qparams['page_number'] = 1
        return qparams

    # Query on the ApiMethod with params
    def getXmlResponse(self, qparams):
        qstr = urllib.urlencode(qparams)
        ### print '?'.join([ApiMethod, qstr]) ###
        req = urllib2.Request('?'.join([ApiMethod, qstr]))
        f = urllib2.urlopen(req)
        return ET.parse(f)

    #Search all specified domains separately for articles
    def searchAll(self):
        for domain in self.domains:
            print domain
            print self.search(domain), 'events in total'

    def search(self, domain):
        # first-time query
        qparams = self.getInitialQParams(domain)
        etree = self.getXmlResponse(qparams)
        root = etree.getroot()
        page_count = int(root.find('page_count').text)
        ### print root.find('total_items').text ###
        count = self.addEvents(root.find('events'), domain)
        # continue querying till enough events are got
        for p_num in range(2, page_count + 1):
            qparams['page_number'] = p_num
            etree = self.getXmlResponse(qparams)
            count += self.addEvents(etree.getroot().find('events'), domain)
            if count >= self.npd:
                break
        return count

    def addEvents(self, events, domain):
        time.sleep(0.1) # prevent frequent query
        count = 0
        for eNode in list(events):
            if eNode.find('country_abbr') is None or eNode.find('country_abbr').text.lower() != 'usa':
                continue
            event = {}
            for term in eventInfoFields:
                event[term] = eNode.find(term).text
            event['start_time'] = datetime.strptime(eNode.find('start_time').text, '%Y-%m-%d %H:%M:%S')
            raw_lati = eNode.find('latitude').text
            if raw_lati is None:
                continue
            event['latitude'] = float(raw_lati)
            event['longitude'] = float(eNode.find('longitude').text)
            event['domain'] = domain
            self.collection.insert_one(event)
            count += 1
        return count

if __name__ == '__main__':
    eventSearcher = EventSearcher(Domains)
    eventSearcher.searchAll()
