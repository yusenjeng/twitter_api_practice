from sys import argv
from args import args_query
from remotedb import RemoteDB

remotedb = RemoteDB()
remotedb.connect()

if __name__ == '__main__':
    args = args_query(argv)
    remotedb.findTweets(args['keyword'], args['lon'], args['lat'],
                        args['radius'])
