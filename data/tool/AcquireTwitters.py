#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
from pymongo import MongoClient
import json, re

#Variables that contains the user credentials to access Twitter API 
access_token = "3280889479-MLEhITVvUXIvQ7T5CSjBGelBLFdeIkbKvgQg1pX"
access_token_secret = "IL6wKgy0XVewesq7gTuA5VUKHdzKXoOfU6kOY5c2uYOrp"
consumer_key = "5pyBtBTuRlMjC83raXrBy65dz"
consumer_secret = "SV3MND7VmYqhSvpyJhYKeQG3kVEpyFvNM2xAufw3ufoK6spmgZ"

#This is a basic listener that overrides on_data method
class GeoTweetsListener(StreamListener):
    def __init__(self):
        StreamListener.__init__(self)
        self.dataAmount = 0
        self.client = MongoClient()
        self.twitterCollection = self.client.test.Twitter
        # for text preprocessing
        self.wordMacher = re.compile(r'[a-z]+')
        self.urlMacher = re.compile(r'http[s]?://[\S]+')
        self.atMacher = re.compile(r'[\S]*@[\S]+')

    # Split text to words
    def split(self, text):
        for url in self.urlMacher.findall(text):
            text = text.replace(url, '')
        for at in self.atMacher.findall(text):
            text = text.replace(at, '')
        return self.wordMacher.findall(text.lower())

    # Add validate tweet to database
    def add(self, jsonObj):
        words = self.split(jsonObj['text'])
        if len(words) == 0:
            return

        mediaURLs = []
        if jsonObj['entities'].has_key('media'):
            for item in jsonObj['entities']['media']:
                mediaURLs.append(item['media_url'])
        document = {
            'created_at': jsonObj['created_at'],
            'id': jsonObj['id_str'],
            'text': jsonObj['text'],
            'user': {
                'name': jsonObj['user']['name'],
                'location': jsonObj['user']['location']
            },
            'coordinates': {
                'longitude': jsonObj['coordinates']['coordinates'][0],
                'latitude': jsonObj['coordinates']['coordinates'][1]
            },
            #'place': {
            #    'name': jsonObj['place']['full_name'],
            #    'country': jsonObj['place']['country']
            #},
            'media_urls': mediaURLs,
            ###'filter_level': jsonObj['filter_level'],
            'timestamp_ms': jsonObj['timestamp_ms'],
            'words': words
        }
        ###print document
        self.twitterCollection.insert_one(document)
        self.dataAmount += 1

    # Override method that is called many times
    def on_data(self, data):
        JSONObject = json.loads(data)
        if not JSONObject.has_key('coordinates') or JSONObject['coordinates'] is None:
            return
        self.add(JSONObject)
        ###return False
        if self.dataAmount == 1000:
            return False

    def on_status(self, status):
        print status

    def on_error(self, status_code):
        print status_code
        return False

if __name__ == '__main__':

    #This handles Twitter authentication and the connection to Twitter Streaming API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener = GeoTweetsListener(), retry_count = 100)

    #Filter Twitter Streams to capture data by the keywords list
    '''client = MongoClient()
    db = client.test
    Domain = db.Domain
    cursor = Domain.find()
    domainKeywords = []
    for document in cursor:
        domainKeywords = list(set(domainKeywords).union(set(document['keywords'])))
    stream.filter(track = domainKeywords)'''
    stream.filter(locations = [-124.848974, 24.396308, -66.885444, 49.384358]) # U.S. geographic boundary box

    print 'finished'