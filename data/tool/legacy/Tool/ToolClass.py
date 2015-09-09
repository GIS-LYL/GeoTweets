import os
import math
import json
from string import punctuation
from pymongo import MongoClient
from nltk.corpus import stopwords

class Article:
    'Article Class'
    def __init__(self, filepath, domain):
        self.filepath = filepath
        self.wordDic = {}
        self.wordAmount = 0
        self.domain = domain
        
    def getTF(self):
        f = open(self.filepath,'r')
        for line in f.readlines():
            line = "".join([c for c in line if c not in punctuation]) # remove all punctuation in line
            vector = line.split(' ')
            for i in range(len(vector)):
                if(self.wordDic.has_key(vector[i])):
                    self.wordDic[vector[i]] += 1.0
                else:
                    self.wordDic[vector[i]] = 1.0
            self.wordAmount += len(vector)
    
        for key in self.wordDic.keys():
            self.wordDic[key] /= self.wordAmount
    
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
            print keyword

class Corpus:
    'Corpus Class'
    def __init__(self, rootdir):
        self.rootdir = rootdir
        self.domain = os.listdir(self.rootdir)
        self.corpus = []
        for entry in self.domain:
            for name in os.listdir(self.rootdir + '\\' + entry):
                article = Article(self.rootdir + '\\' + entry + '\\' + name, entry)
                self.corpus.append(article)

    def calculateTF(self):
        for i in range(len(self.corpus)):
            self.corpus[i].getTF()
    
    def calculateTFIDF(self):
        for article in self.corpus:
            for word in article.wordDic.keys():
                count = 0
                for i in range(len(self.corpus)):
                    if(self.corpus[i].wordDic.has_key(word)):
                        count += 1
                article.wordDic[word] *= math.log(len(self.corpus) / count)

    def getKeywords(self, count):
        for article in self.corpus:
            article.sortDic()
            article.getKeywords(count)
    
    def display(self):
        for article in self.corpus:
            article.display()

class Twitter:
    'Twitter Class'
    def __init__(self, JSONObject):
        self.json = JSONObject
        self.text = JSONObject['text']
        self.dic = {}
        self.wordAmount = 0.0
        self.TFIDF = {}
    
    def getTF(self):
        text = "".join([c for c in self.text if c not in punctuation]) # remove all punctuation in self.text
        vector = text.split(' ')
        for i in range(len(vector)):
            if(self.dic.has_key(vector[i])):
                self.dic[vector[i]] += 1.0
            else:
                self.dic[vector[i]] = 1.0
        self.wordAmount += len(vector)
        
        for key in self.dic.keys():
            self.dic[key] /= self.wordAmount

class TwitterList:
    def __init__(self):
        self.twitterList = []
        self.client = MongoClient()
        self.db = self.client.test
        self.collection = self.db.Twitter
        cursor = self.collection.find()
        for document in cursor:
            JSONObject = document
            twitter = Twitter(JSONObject)
            self.twitterList.append(twitter)
            
    def calculateTF(self):
        for twitter in self.twitterList:
            twitter.getTF()
            
    def calculateTFIDF(self):
        for twitter in self.twitterList:
            for word in twitter.dic.keys():
                count = 0
                for i in range(len(self.twitterList)):
                    if(self.twitterList[i].dic.has_key(word)):
                        count += 1
                twitter.dic[word] *= math.log(len(self.twitterList) / count)

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
        return self.data