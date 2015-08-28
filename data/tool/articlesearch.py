import urllib2, urllib, json
from datetime import date, timedelta
from pyquery import PyQuery as pq

domains = ['Arts', 'Education', 'Health', 'Science', 'Sports']

BaseURI = 'http://api.nytimes.com/svc/search/v2/articlesearch.json'
APIKey = 'd6e7999f5dee748975dac3228b6b5ddf:19:72790999'

class ArticleSearchEngine:
    # Init this engine
    def __init__(self, domains, num_per_dm = float('inf'), end_date = date.today(), begin_date = None):
        self.domains = domains
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
            qparams['begin_date'] = self.end_date.strftime("%y%m%d")
        else:
            qparams['begin_date'] = self.begin_date.strftime("%y%m%d")
        qparams['end_date'] = self.end_date.strftime("%y%m%d")
        #qparams['fl'] = 'web_url,abstract,headline,keywords,pub_date,word_count'#,section_name,subsection_name
        qparams['page'] = 0
        #qparams['facet_field'] = ''
        #qparams['facet_filter'] = True
        return qparams

    # Query on the BaseURI with params
    def getJsonResponse(self, qparams):
        qstr = urllib.urlencode(qparams)
        req = urllib2.Request('?'.join([BaseURI, qstr]))
        f = urllib2.urlopen(req)
        return json.loads(f.read())['response']

    # Filter and add docs in one response
    # count: num of docs already added
    def addDocs(self, docs, count):
        pass

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
        count = self.addDocs(response['docs'], 0); end_date = self.end_date
        # continue querying till enough docs are got
        while True:
            while qparams['page'] < n_hit / 10 and count < self.num_per_dm:
                print 'page', qparams['page'], count, 'docs'
                qparams['page'] += 1
                response = self.getJsonResponse(qparams)
                assert page * 10 == response['meta']['offset']
                count += self.addDocs(response['docs'], count)
            if self.begin_date is not None or count >= self.num_per_dm:
                break
            # modify date and restart query
            end_date -= timedelta(1)
            qparams['page'] = 0
            qparams['begin_date'] = qparams['end_date'] = end_date.strftime("%y%m%d")
            response = self.getJsonResponse(qparams)
            n_hit = response['meta']['hits']
            count += self.addDocs(response['docs'], count)


if __name__ == '__main__':
    data = urllib.urlencode(qparams)
    print data
    req = urllib2.Request(BaseURI, data)