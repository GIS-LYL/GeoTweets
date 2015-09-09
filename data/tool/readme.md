# Data Tools

## articlesearch.py - Search for Articles in Different Domains
Search articles from The New York Times and save them in separated json files.
> Run before twittwerprocess.py

## datamodules.py - Data Modules of Twitters and Articles
- Article
- Corpus
- Twitter
- TwitterList

## eventful.py - Search for Events of Different Categories
Search events from Eventful and store in the database.

## twitterprocess.py - Calculate the Importance of Each Tweet
Calculate word importance from articles in different domains using TF/IDF algorithm.
Then the importance of each tweet.
> Run after articlesearch.py and twitterstream.py

## twitterstream.py - Get Realtime Tweets
Collect tweets in the US using tweepy.