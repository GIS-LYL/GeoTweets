# -*- coding: utf-8 -*-
from ToolClass import Corpus
from articlesearch import *
'''import sys
from pymongo import MongoClient

client = MongoClient()
db = client.test'''

corpus = Corpus('..', domains)
corpus.countDocsOnWords()
corpus.calculateTFIDF()
#corpus.display()
keywords = corpus.getKeywords(10000)

'''
domainKeywords = {} # keywords related to domain
for article in corpus.corpus:
    if domainKeywords.has_key(article.domain) == False:
        domainKeywords[article.domain] = []
    domainKeywords[article.domain] = list(set(domainKeywords[article.domain]).union(set(article.keywords)))

for domain in domainKeywords.keys():
    print domainKeywords[domain]
    Domain.insert_one({"domain":domain,"keywords":domainKeywords[domain]})

print 'finished'
'''