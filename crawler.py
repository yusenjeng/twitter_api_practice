from sys import argv
from args import args_crawler
from pymongo import MongoClient


if __name__ == '__main__':
    args = args_crawler(argv)
    print(args)