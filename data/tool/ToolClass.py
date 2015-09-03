import os, math
import json, codecs, re
from pyquery import PyQuery as pq
from string import punctuation
from pymongo import MongoClient
#from nltk.corpus import stopwords
from types import *

class Article:
    'Article Class'
    def __init__(self, filepath, domain):
        f = codecs.open(filepath, 'r', 'utf-8')
        self.doc = json.loads(f.read())
        f.close()
        self.domain = domain
        self.wordCount = {}
        self.n_words = self.countWords(
            pq(self.doc['article'])('p').text().lower()
        )
        self.maxn = max(self.wordCount.values())

    def countWords(self, text):
        wordMacher = re.compile(r'[a-z]+')
        words = wordMacher.findall(text)
        for w in words:
            if w in self.wordCount:
                self.wordCount[w] += 1
            else:
                self.wordCount[w] = 1
        return float(len(words))

    def tf(self, word):
        #return self.wordCount.get(word, 0) / self.n_words
        k = 0.01
        return k + (1 - k) * self.wordCount.get(word, 0) / self.n_words
'''
    def sortDic(self):
        self.sortedWordList = sorted(self.wordDic.iteritems(),key=lambda d:d[1],reverse=True) # Dic sort
    
    def getKeywords(self, count):
        self.keywords = []
        for word in self.sortedWordList:
            if word[0].lower() not in set(stopwords.words('english')):
                self.keywords.append(word[0])
                if len(self.keywords) == count:
                    break
    
    def display(self):
        print 'wordAmount: %d' % self.wordAmount
        print 'Different words: %d' % len(self.wordDic.keys())
        for keyword in self.keywords:
            print keyword'''


class Corpus:
    'Corpus Class'
    def __init__(self, rootdir, domains):
        self.rootdir = rootdir
        self.domains = domains
        self.corpus = {}
        for entry in self.domains:
            self.corpus[entry] = []
            for name in os.listdir(self.rootdir + '/' + entry):
                article = Article(self.rootdir + '/' + entry + '/' + name, entry)
                self.corpus[entry].append(article)
        self.docCount = {} # count for idf computation
        self.n_docs = {}
        self.tiTable = {} # tf-idf table

    def countDocsOnWords(self):
        docCount = {}
        for d in self.corpus:
            self.n_docs[d] = 0
            for article in self.corpus[d]:
                self.n_docs[d] += 1
                for w in article.wordCount:
                    if w in docCount:
                        docCount[w] += 1
                    else:
                        docCount[w] = 1
        self.N = float(sum(self.n_docs.values())) # docs in total
        # filter words that appear more than once
        for w in docCount:
            if docCount[w] > 1:
                self.docCount[w] = docCount[w]

    def idf(self, word):
        return math.log(self.N / self.docCount[word])
    
    def calculateTFIDF(self):
        idfTable = {}
        for w in self.docCount:
            self.tiTable[w] = {}
            idf = idfTable[w] = self.idf(w)
            for d in self.corpus:
                l = self.tiTable[w][d] = []
                for article in self.corpus[d]:
                    l.append(article.tf(w) * idf)
        # save table
        json.dump(self.tiTable, open('tf-idf_table.json', 'w'))
        json.dump(idfTable, open('idf_table.json', 'w'))

    def getKeywords(self, count):
        keywords = {}
        for d in self.corpus:
            keywords[d] = sorted(
                [(k, sum(v[d])) for (k, v) in self.tiTable.iteritems()],
                key = lambda e: e[1],
                reverse = True
            )[:count]
        json.dump(keywords, open('keywords.json', 'w'))
        return keywords
'''
    def display(self, domains = None, limit = 50):
        if type(domains) is not list:
            domains = self.corpus.keys()
        count = 0
        domains = set(domains) & set(self.corpus.keys())
        for w in self.tiTable:
            count += 1
            print w, ':'
            for d in domains:
                print d + ':', self.tiTable[w][d]
            if count == limit:
                break'''


class Twitter:
    'Twitter Class'
    def __init__(self, doc):
        self.doc = doc
        self.wordCount = {}
        self.countWords()
        self.importance = {}
    
    def countWords(self):
        for w in self.doc['words']:
            if w in self.wordCount:
                self.wordCount[w] += 1
            else:
                self.wordCount[w] = 1

    def calculateImportance(self, keywords, normelem):
        dcount = {}
        for domain in keywords:
            self.importance[domain] = 0
            dcount[domain] = 0
        for w in self.wordCount:
            count = self.wordCount[w]
            for d in keywords:
                impor = keywords[d].get(w, None)
                if impor is not None:
                    self.importance[d] += impor * count
                    dcount[d] += count
        for domain in self.importance:
            if dcount[domain] != 0:
                self.importance[domain] /= (dcount[domain] * normelem)

    def addImportanceTo(self, collection):
        for d in self.importance:
            if self.importance[d] > 0:
                collection.insert_one({
                    'id': self.doc['_id'],
                    'domain': d,
                    'importance': self.importance[d]
                })



class TwitterList:
    def __init__(self):
        self.twitterList = []
        self.client = MongoClient()
        self.db = self.client.test
        self.twitterCollection = self.db.twitters
        self.imporCollection = self.db.importances
        cursor = self.twitterCollection.find()
        for document in cursor:
            JSONObject = document
            twitter = Twitter(JSONObject)
            self.twitterList.append(twitter)

    def loadKeywords(self, filename):
        self.keywords = json.loads(open(filename, 'r').read())
        weight = []
        for d in self.keywords:
            weight.append(self.keywords[d][0][1])
            self.keywords[d] = dict(self.keywords[d])
        self.weight = max(weight)

    def calculateImportance(self):
        for twitter in self.twitterList:
            twitter.calculateImportance(self.keywords, self.weight)

    def addImportanceToDB(self):
        for twitter in self.twitterList:
            twitter.addImportanceTo(self.imporCollection)
'''
    def getCorrelation(self, domain, keywords):
        for twitter in self.twitterList:
            twitter.TFIDF[domain] = 0
            for keyword in keywords:
                if twitter.dic.has_key(keyword):
                    twitter.TFIDF[domain] += twitter.dic[keyword]
        #self.twitterList.sort(key=lambda x:x.TFIDF,reverse=True) # List sorted by TFIDF 

    def updateToDatabase(self):
        for twitter in self.twitterList:
            result = self.collection.update_one({"_id":twitter.json['_id']},{"$set":{"importance":twitter.TFIDF}})
            if result.matched_count != 1:
                return False
        return True

    def display(self):
        for twitter in self.twitterList:
            print twitter.TFIDF

class DataTransformer:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test
        self.collection = self.db.Twitter
        self.data = ""
    
    def toJson(self):
        self.data += '{"type":"FeatureCollection","id":"tweetsyoulike.c22ab257","features":['
        cursor = self.collection.find()
        amount = self.collection.count()
        for document in cursor:
            dic = {}
            dic['type'] = 'Feature'
            dic['id'] = str(document['_id'])
            dic['geometry'] = {'coordinates':document['coordinates'], 'type':'Point'}
            dic['properties'] = {'id':str(document['_id']), 'time':document['created_at'], 
                                 'name':document['name'], 'text':document['text'], 
                                 'location':document['location'], 'media_url':document['media_url'], 
                                 'marker-size':'medium', 'marker-color':'#7ec9b1', 'marker-symbol':'3',
                                 'importance':document['importance']}
            tmp = str(json.dumps(dic))
            self.data += tmp
            
            amount -= 1
            if amount != 0:
                self.data += ','
        self.data += ']}'
        return self.data'''