#!/usr/bin/env python
# encoding: utf-8

import os
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.comment import CommentSpider
from spiders.follower import FollowerSpider
from spiders.fan import FanSpider
from pymongo import MongoClient

def crapy_spider():
    os.environ['SCRAPY_SETTINGS_MODULE'] = f'settings'
    config_path = os.getcwd() + os.sep + 'config.json'
    with open(config_path) as T:
        config = json.loads(T.read())
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    if config['get_comment'] == 1:
        process.crawl(CommentSpider)
    if config['get_fan'] == 1:
        process.crawl(FanSpider)
    if config['get_follower'] == 1:
        process.crawl(FollowerSpider)
    process.start()
    print('爬取结束，开始整理数据库')
    get_replied_user_id(config['mongo_db_name'])
    print('整理数据库完成')

# 爬取完成后，整理数据库，根据用户名匹配，填入被回复者的用户id
def get_replied_user_id(db):

    # 连接数据库
    client = MongoClient()
    db = client[db]
    collection = db['Comments']

    # 对于每一条评论
    for doc0 in collection.find():
        # 判断这条评论是否是回复
        if doc0['replied_user_name'] != '':
            # 遍历所有评论
            for doc1 in collection.find():
                # 如果找到了评论的用户名与被回复者的用户名相同的评论
                if doc1['comment_user_name'] == doc0['replied_user_name']:
                    # 将这条评论的用户id填入到这条评论的被回复者id中
                    collection.update_one(
                        {'_id': doc0['_id']},
                        {'$set': {'replied_user_id': doc1['comment_user_id']}})


    
