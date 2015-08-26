# -*- coding: utf-8 -*-
from ToolClass import Article,Corpus
import sys
from pymongo import MongoClient

client = MongoClient()
db = client.test
Domain = db.Domain

corpus = Corpus('C:\\Users\\tianyi\\workspace\\GeoTweets\\Tool\\Articles')
corpus.calculateTF()
corpus.calculateTFIDF()
corpus.getKeywords(3) # get n keywords from each article

domainKeywords = {} # keywords related to domain
for article in corpus.corpus:
    if domainKeywords.has_key(article.domain) == False:
        domainKeywords[article.domain] = []
    domainKeywords[article.domain] = list(set(domainKeywords[article.domain]).union(set(article.keywords)))

for domain in domainKeywords.keys():
    print domainKeywords[domain]
    Domain.insert_one({"domain":domain,"keywords":domainKeywords[domain]})

print 'finished'