# -*- coding: utf-8 -*-
import json
import logging
import logging.config
import pymongo
import sys
import os
import shutil
from pymongo.errors import DuplicateKeyError
from settings import MONGO_HOST, MONGO_PORT
from absl import app, flags
FLAGS = flags.FLAGS

class MongoDBPipeline(object):
    def __init__(self):
        # config = _get_config()
        # mongo_config = config['mongo_config']
        # db = pymongo.MongoClient(mongo_config['connection_string'])
        client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        config_path = os.getcwd() + os.sep + 'config.json'
        with open(config_path) as T:
            config = json.loads(T.read())
        db_name = config['mongo_db_name']
        db = client[db_name]
        self.Comments = db["Comments"]
        self.Relationships = db["Relationships"]
        self.Reposts = db["Reposts"]

    def process_item(self, item, spider):
        if spider.name == 'comment_spider':
            self.insert_item(self.Comments, item)
        elif spider.name == 'fan_spider':
            self.insert_item(self.Relationships, item)
        elif spider.name == 'follower_spider':
            self.insert_item(self.Relationships, item)
        elif spider.name == 'relationship_spider':
            self.insert_item(self.Relationships, item)
        return item
    

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert_one(dict(item))
        except DuplicateKeyError:
            pass

def _get_config():
    """获取config.json数据"""
    src = os.path.split(
        os.path.realpath(__file__))[0] + os.sep + 'config_sample.json'
    config_path = os.getcwd() + os.sep + 'config.json'
    if FLAGS.config_path:
        config_path = FLAGS.config_path
    elif not os.path.isfile(config_path):
        shutil.copy(src, config_path)
        sys.exit()
    try:
        with open(config_path) as f:
            config = json.loads(f.read())
            return config
    except ValueError:
        sys.exit()
