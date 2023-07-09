#!/usr/bin/env python
# encoding: utf-8

import os
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.comment import CommentSpider
from spiders.follower import FollowerSpider
from spiders.fan import FanSpider
from spiders.relationship import RelationshipSpider
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
    # 若 config['get_follower']或config['get_fan']为1
    # if config['get_follower'] == 1 or config['get_fan'] == 1:
    #      process.crawl(RelationshipSpider)
    process.start()
    print('爬取结束，开始整理数据库')
    Refactoring_database(config['mongo_db_name'])
    print('整理数据库完成')

# 爬取完成后，整理数据库，根据用户名匹配，填入被回复者的用户id
def Refactoring_database(db):
    config_path = os.getcwd() + os.sep + 'config.json'
    with open(config_path) as T:
        config = json.loads(T.read())
    # 连接数据库
    client = MongoClient()
    db = client[db]
    weibo = db['weibo']
    Comments = db['Comments']
    Relationships = db['Relationships']
    user = db['user']

    if config['get_comment'] == 1:
        # 补全评论中的被回复者id
        for doc0 in Comments.find():
            # 判断这条评论是否是回复
            if doc0['replied_user_name'] != '':
                # 遍历所有评论
                for doc1 in Comments.find():
                    # 如果找到了评论的用户名与被回复者的用户名相同的评论
                    if doc1['comment_user_name'] == doc0['replied_user_name']:
                        # 将这条评论的用户id填入到这条评论的被回复者id中
                        Comments.update_one(
                            {'_id': doc0['_id']},
                            {'$set': {'replied_user_id': doc1['comment_user_id']}})
                        continue

                    # 如果完成遍历，仍没有找到评论的用户名与被回复者的用户名相同的评论
    if config['get_fan'] == 1 or config['get_follower'] == 1:
        # 将同一用户的关注列表和粉丝列表合并
        for user_id in config["user_id_list"]:
            # 初始化该用户的关注列表和粉丝列表
            fan_id_list = []
            follow_id_list = []
            # 遍历Relationships簇中的所有数据
            for doc in Relationships.find():
                # 如果该条数据的关注列表和粉丝列表已经存在，且该条数据的user_id与该用户相同，则将该条数据删除，否则跳过
                if 'fan_id_list' in doc and 'follow_id_list' in doc:
                    if doc['user_id'] == user_id:
                        Relationships.delete_one({'_id': doc['_id']})
                    continue
                # 如果数据中的user_id和fan_id与该用户相同，则将该数据中的followed_id添加到该用户的follow_id_list中
                if doc['user_id'] == user_id and doc['fan_id'] == user_id :
                    follow_id_list.append(doc['followed_id'])
                    # 删除该条数据
                    Relationships.delete_one({'_id': doc['_id']})
                # 如果数据中的user_id和followed_id与该用户相同，则将该数据中的fan_id添加到该用户的fan_id_list中
                if doc['user_id'] == user_id and doc['followed_id'] == user_id :
                    fan_id_list.append(doc['fan_id'])
                    # 删除该条数据
                    Relationships.delete_one({'_id': doc['_id']})

            # 将该用户的关注列表和粉丝列表合并
            Relationships.update_one(
                {'user_id': user_id},
                {'$set': {'fan_id_list': fan_id_list, 'follow_id_list': follow_id_list}})
            # 创建一条新数据
            Relationships.insert_one(
                {'user_id': user_id, 'fan_id_list': fan_id_list, 'follow_id_list': follow_id_list})

    # 将同一用户的微博合并
    for user_id in config["user_id_list"]:
        # 初始化该用户的微博列表
        weibo_list = []
        # 遍历weibo簇中的所有数据
        for doc in weibo.find():
            # 如果该条数据的微博列表已经存在，且该条数据的user_id与该用户相同，则将该条数据删除，否则跳过
            if 'content_list' in doc:
                if doc['user_id'] == user_id:
                    weibo.delete_one({'_id': doc['_id']})
                continue
            # 如果数据中的user_id与该用户相同，则将该数据添加到该用户的weibo_list中
            if doc['user_id'] == user_id:
                # 删除该条数据中的冗余元素user_id
                del doc['user_id']
                weibo_list.append(doc)
                # 删除该条数据
                weibo.delete_one({'_id': doc['_id']})
        user_info = {}
        # 在user簇中查找id与user_id相同的数据项
        for doc in user.find():
            if doc['id'] == user_id:
                # 将该用户的基本信息记录为user_info
                user_info = doc        
                break

        # 将该用户的微博合并与用户基本信息
        weibo.insert_one({'user_id': user_id, 'user_info':user_info ,'content_list': weibo_list})