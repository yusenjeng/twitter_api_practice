import time
import config

from sys import argv
from pymongo import MongoClient, DESCENDING, GEOSPHERE, TEXT, GEO2D
from pymongo.errors import OperationFailure


class RemoteDB(object):
    def __init__(self, dbname='bittiger'):
        self.db = None
        self.dbname = dbname

    def connect(self):
        # Connect to remote mongodb and keep the tweets collection
        client = MongoClient(config.MONGO_ADDRESS, config.MONGO_PORT)
        self.db = client[self.dbname]
        self.db.authenticate(config.MONGO_USER, config.MONGO_PASSWD)
        self.tweets = self.db.tweets

    def createIndex(self, hours=1):
        # Create three indices here:
        #
        # GEO2D for spatial query
        # TEXT for full-text search
        # expireAfterSeconds for the TTL, default parameter is 1 hour

        try:
            self.tweets.create_index([('coordinates.coordinates', GEO2D)])
            self.tweets.create_index([('text', TEXT)])
            self.tweets.create_index(
                [('created_at', DESCENDING)],
                expireAfterSeconds=hours * 60 * 60)

            print('Create indices on collection tweets.')
        except OperationFailure as err:
            print('Write error: {0}'.format(err))

    def timeit_start(self):
        self.time_start = time.time()

    def timeit_end(self):
        self.time_diff = time.time() - self.time_start
        print('timeit:', self.time_diff * 1000, 'ms')

    def insertTweet(self, doc):
        mongo_tweet_id = self.tweets.insert_one(doc).inserted_id
        print('Insert tweet "', doc['text'], '" with _id=', mongo_tweet_id)

    def findTweets(self, keyword, lon=None, lat=None, radius=10):
        self.timeit_start()

        # Merge query parameters into the dict
        opt = {}

        if lon is not None and lat is not None:
            lon = float(lon)
            lat = float(lat)
            radius = float(radius)
            opt['coordinates'] = {'$within': {'$center': [[lon, lat], radius]}}

        if keyword is not None:
            opt['$text'] = {'$search': keyword}

        sort = [('created_at', DESCENDING)]

        # Fetch the most recent 100 tweets
        results = self.tweets.find(opt, sort=sort).limit(100)

        # Pretty print
        inc = 1
        for doc in list(results):
            print(inc, '\t', doc['_id'], doc['created_at'], doc['coordinates'])
            print('\t', doc['text'])
            inc += 1

        print('Query operators:', opt)

        self.timeit_end()

    def deleteTweets(self):
        # Delete everything in the tweets
        deleted_count = self.tweets.delete_many({}).deleted_count
        print('Delete', deleted_count, 'documents.')


if __name__ == '__main__':
    remotedb = RemoteDB()
    remotedb.connect()

    # CLI for the database management
    if 'clear' in argv:
        remotedb.deleteTweets()
    elif 'index' in argv:
        remotedb.createIndex(24)
    elif 'test' in argv:
        remotedb.findTweets('NBA')
        remotedb.findTweets(None, -122.75, 36.8, 10)
        remotedb.findTweets('MEDICAL', -122.75, 36.8, 10)
