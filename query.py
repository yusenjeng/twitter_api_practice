from sys import argv
from args import args_query
from pymongo import MongoClient

if __name__ == '__main__':
    args = args_query(argv)
    print(args)