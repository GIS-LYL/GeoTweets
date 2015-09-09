#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient
import json

#Variables that contains the user credentials to access Twitter API 
access_token = "3280889479-MLEhITVvUXIvQ7T5CSjBGelBLFdeIkbKvgQg1pX"
access_token_secret = "IL6wKgy0XVewesq7gTuA5VUKHdzKXoOfU6kOY5c2uYOrp"
consumer_key = "5pyBtBTuRlMjC83raXrBy65dz"
consumer_secret = "SV3MND7VmYqhSvpyJhYKeQG3kVEpyFvNM2xAufw3ufoK6spmgZ"

#This is a basic listener that overrides on_data method
class StdOutListener(StreamListener):
    
    # Override method that is called many times
    def on_data(self, data):
        if hasattr(self, 'dataAmount') == False:
            self.dataAmount = 0
        if hasattr(self, 'client') == False:
            self.client = MongoClient()
        if hasattr(self, 'db') == False:
            self.db = self.client.test
        if hasattr(self, 'twitterCollection') == False:
            self.twitterCollection = self.db.Twitter
        if self.dataAmount == 0 or self.dataAmount % 100 != 0:
            JSONObject = json.loads(data)
            if JSONObject.has_key('coordinates') == False or JSONObject['coordinates'] == None:
                return
            mediaURLs = []
            if JSONObject['entities'].has_key('media') == True:
                for item in JSONObject['entities']['media']:
                    mediaURLs.append(item['media_url']) 
            document = {'text':JSONObject['text'],'coordinates':JSONObject['coordinates']['coordinates'],
                        'created_at':JSONObject['created_at'],'media_url':mediaURLs,
                        'name':JSONObject['user']['name'],'location':JSONObject['user']['location']}
            self.twitterCollection.insert_one(document)
            self.dataAmount += 1
            print self.dataAmount
            '''for key in JSONObject.keys():
                print "key: %s value: %s\n" % (key,JSONObject[key])'''
        if self.dataAmount % 100 == 0:
            return False
               
    def on_error(self, status):
        print status

if __name__ == '__main__':

    #This handles Twitter authentication and the connection to Twitter Streaming API
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener, retry_count=100)

    #Filter Twitter Streams to capture data by the keywords list
    client = MongoClient()
    db = client.test
    Domain = db.Domain
    cursor = Domain.find()
    domainKeywords = []
    for document in cursor:
        domainKeywords = list(set(domainKeywords).union(set(document['keywords'])))
    stream.filter(track = domainKeywords)

    print 'finished'