from sys import argv, exit
from args import args_crawler
from pymongo import MongoClient

import json
import config
import tweepy
import datetime


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        doc = status._json
        # doc['created_at'] = datetime.datetime.strptime(doc['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        print(doc)
        print( type(doc))
        exit()

    def on_error(self, status_code):
        print('Error with status code:', status_code)
        return True

    def on_timeout(self):
        print('Timeout!')
        return True


class TwitterCrawler(object):
    def __init__(self):
        self.__api = None

    def connect(self):
        auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY,
                                   config.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(config.TWITTER_ACCESS_TOKEN,
                              config.TWITTER_ACCESS_TOKEN_SECRET)
        self.__api = tweepy.API(auth)
        self.__stream = tweepy.streaming.Stream(auth, CustomStreamListener())

    def pull(self, lon, lat):
        # The equatorial circumference of Earth is about 24,900 miles.
        if lon is not None and lat is not None:
            self.__stream.filter(
                locations=[lon - 1, lat - 1, lon + 1, lat + 1])
        else:
            self.__stream.filter(locations=[-180, -90, 180, 90])

    def test(self):
        public_tweets = self.__api.home_timeline()
        for tweet in public_tweets:
            print(tweet)
            print()


if __name__ == '__main__':
    args = args_crawler(argv)
    twitter = TwitterCrawler()
    twitter.connect()
    twitter.pull(args['lon'], args['lat'])
    print(args)