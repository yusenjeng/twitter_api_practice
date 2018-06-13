import config

from sys import argv
from pymongo import MongoClient, DESCENDING, GEO2D


class RemoteDB(object):
    def __init__(self, dbname='bittiger'):
        self.db = None
        self.dbname = dbname

    def connect(self):
        client = MongoClient(config.MONGO_ADDRESS, config.MONGO_PORT)
        self.db = client[self.dbname]
        self.db.authenticate(config.MONGO_USER, config.MONGO_PASSWD)
        self.tweets = self.db.tweets

    def createIndex(self, hours=24):
        self.tweets.create_index(
            [("coordinates", GEO2D)], expireAfterSeconds=hours * 60 * 60)
        print('Create GEO2D index on collection tweets.')

    def insertTweet(self, doc):
        mongo_tweet_id = self.db.tweets.insert_one(doc).inserted_id
        print('Insert tweet "', doc['text'], '" with _id=', mongo_tweet_id)

    def filterTweets(self, keyword, lon, lat, radius):
        pass

    def deleteTweets(self):
        deleted_count = self.tweets.delete_many({}).deleted_count
        print('Delete', deleted_count, 'documents.')


if __name__ == '__main__':
    remotedb = RemoteDB()
    remotedb.connect()

    if 'clear' in argv:
        remotedb.deleteTweets()
    elif 'index' in argv:
        print('index')
