# Title: Article Search
# Description: Get articles in diffrent domains for The New York Times.
# Author: Dstray

import urllib2, urllib, os
import json, codecs, time
from datetime import date, timedelta
from pyquery import PyQuery as pq

root_path = '../' # store articles here
response_fields = ['web_url', 'abstract', 'headline', 'keywords', 'pub_date', 'word_count', 'section_name', 'subsection_name']

Domains = ['Arts', 'Education', 'Health', 'Science', 'Sports']
BaseURI = 'http://api.nytimes.com/svc/search/v2/articlesearch.json'
APIKey = 'd6e7999f5dee748975dac3228b6b5ddf:19:72790999'

class ArticleSearchEngine:
    # Init this engine
    def __init__(self, domains, num_per_dm = float('inf'), end_date = date.today(), begin_date = None):
        self.domains = Domains
        self.num_per_dm = num_per_dm # required num of articles per domain
        self.end_date = end_date
        self.begin_date = begin_date
        assert num_per_dm != float('inf') or begin_date is not None

    # Get params needed for the first-time request
    def getInitialQParams(self, domain):
        qparams = {}
        qparams['api-key'] = APIKey
        #qparams['q'] = 'Obama'
        qparams['fq'] = 'section_name:("%s") AND source:("The New York Times")' % domain
        if self.begin_date is None:
            qparams['begin_date'] = self.end_date.strftime("%Y%m%d")
        else:
            qparams['begin_date'] = self.begin_date.strftime("%Y%m%d")
        qparams['end_date'] = self.end_date.strftime("%Y%m%d")
        #qparams['fl'] = 'web_url,abstract,headline,keywords,pub_date,word_count'#,section_name,subsection_name
        qparams['page'] = 0
        #qparams['facet_field'] = ''
        #qparams['facet_filter'] = True
        return qparams

    # Query on the BaseURI with params
    def getJsonResponse(self, qparams):
        qstr = urllib.urlencode(qparams)
        ### print '?'.join([BaseURI, qstr]) ###
        req = urllib2.Request('?'.join([BaseURI, qstr]))
        f = urllib2.urlopen(req)
        return json.loads(f.read())['response']

    #Search all specified domains separately for articles
    def searchAll(self):
        for domain in self.domains:
            print domain
            print self.search(domain), 'docs in total'

    def search(self, domain):
        # first-time query
        qparams = self.getInitialQParams(domain)
        response = self.getJsonResponse(qparams)
        n_hit = response['meta']['hits'] # num of result docs in total
        count = self.addDocs(response['docs'], domain, 0); end_date = self.end_date
        ### return count ###
        # continue querying till enough docs are got
        while True:
            while qparams['page'] < n_hit / 10 and count < self.num_per_dm:
                print 'page', qparams['page'], count, 'docs'
                qparams['page'] += 1
                response = self.getJsonResponse(qparams)
                assert qparams['page'] * 10 == response['meta']['offset']
                count += self.addDocs(response['docs'], domain, count)
            if self.begin_date is not None or count >= self.num_per_dm:
                break
            # modify date and restart query
            end_date -= timedelta(1)
            qparams['page'] = 0
            qparams['begin_date'] = qparams['end_date'] = end_date.strftime("%Y%m%d")
            response = self.getJsonResponse(qparams)
            n_hit = response['meta']['hits']
            count += self.addDocs(response['docs'], domain, count)
        return count

    # Filter and add docs in one response
    # count: num of docs already added
    def addDocs(self, docs, domain, count):
        time.sleep(0.1) # prevent frequent query
        start_count = count
        for doc in docs:
            ### print doc['_id'], doc['word_count']
            if doc['word_count'] is None or int(doc['word_count']) < 200:
                continue
            self.saveDoc(doc, domain)
            count += 1
            if count == self.num_per_dm:
                break
        return count - start_count

    # Save article to json file
    def saveDoc(self, doc, domain):
        new_doc = {}
        new_doc['article'] = self.getFullArticle(doc['web_url'])
        if new_doc['article'] == '':
            print doc['word_count']
        for field in response_fields:
            new_doc[field] = doc[field]
        path = root_path + domain + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        f = codecs.open(path + doc['_id'] + '.json', 'w', 'utf-8')
        json.dump(new_doc, f)
        f.close()

    # Get full text of the article from original website
    def getFullArticle(self, url):
        ### print url ###
        webpage = pq(url = url)
        article = webpage("article:first")
        paras = article.children('div:first').find('p.story-body-text,.interactive-summary')
        content = unicode(paras) #.text()
        #paras.each(lambda idx: content.append(paras(':eq(%d)' % idx).text()))
        ### print content ###
        return content


# Start the engine here
if __name__ == '__main__':
    articleSE = ArticleSearchEngine(domains, 20)
    articleSE.searchAll()