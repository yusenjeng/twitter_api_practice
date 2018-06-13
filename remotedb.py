import time
import config

from sys import argv
from pymongo import MongoClient, DESCENDING, GEO2D, TEXT
from pymongo.errors import OperationFailure


class RemoteDB(object):
    def __init__(self, dbname='bittiger'):
        self.db = None
        self.dbname = dbname

    def connect(self):
        client = MongoClient(config.MONGO_ADDRESS, config.MONGO_PORT)
        self.db = client[self.dbname]
        self.db.authenticate(config.MONGO_USER, config.MONGO_PASSWD)
        self.tweets = self.db.tweets

    def createIndex(self, hours=1):
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

        opt = {}

        if lon is not None and lat is not None:
            lon = float(lon)
            lat = float(lat)
            radius = float(radius)
            opt['coordinates'] = {'$within': {'$center': [[lon, lat], radius]}}

        if keyword is not None:
            opt['$text'] = {'$search': keyword}

        sort = [('created_at', DESCENDING)]

        results = self.tweets.find(opt, sort=sort).limit(100)

        inc = 1
        for doc in list(results):
            print(inc, '\t', doc['_id'], doc['created_at'], doc['coordinates'])
            print('\t', doc['text'])
            inc += 1

        print(opt)

        self.timeit_end()

    def findTweetsNear(self, lon=-122.75, lat=36.8, radius=10):
        radius = float(radius)
        opt = {"coordinates": {"$within": {"$center": [[lon, lat], radius]}}}
        results = self.tweets.find(opt).limit(100)

        inc = 1
        for doc in list(results):
            print(inc, doc['_id'], doc['coordinates'], doc['text'])
            inc += 1

    def findTweetsContains(self, keyword='NBA'):
        opt = {'$text': {'$search': keyword}}
        results = self.tweets.find(opt).limit(100)

        inc = 1
        for doc in list(results):
            print(inc, doc['_id'], doc['coordinates'], doc['text'])
            inc += 1

    def deleteTweets(self):
        deleted_count = self.tweets.delete_many({}).deleted_count
        print('Delete', deleted_count, 'documents.')


if __name__ == '__main__':
    remotedb = RemoteDB()
    remotedb.connect()

    if 'clear' in argv:
        remotedb.deleteTweets()
    elif 'index' in argv:
        remotedb.createIndex(24)
    elif 'keyword' in argv:
        remotedb.findTweetsContains(argv[2])
    elif 'geo' in argv:
        remotedb.findTweetsNear(radius=argv[2])
    else:
        remotedb.findTweets('NBA')
        remotedb.findTweets(None, -122.75, 36.8, 10)
        remotedb.findTweets('MEDICAL', -122.75, 36.8, 10)
