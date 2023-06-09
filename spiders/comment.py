#!/usr/bin/env python
# encoding: utf-8
import os
import re
import json
from lxml import etree
from scrapy import Spider
from scrapy.http import Request
import time
from items import CommentItem
from spiders.utils import extract_comment_content, time_fix
from pymongo import MongoClient

class CommentSpider(Spider):
    name = "comment_spider"
    base_url = "https://weibo.cn"

    def start_requests(self):
        file_path = os.getcwd() + os.sep + 'weibo_spider' + os.sep + 'weibo_id_list.txt'
        f = open(file_path,"r")   
        tweet_ids = f.readlines()
        # tweet_ids = ['MCGZFDJ1j']
        urls = [f"{self.base_url}/comment/{tweet_id}?rl=1&page=1" for tweet_id in tweet_ids]
        for url in urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                all_page = all_page if all_page <= 50 else 50
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield Request(page_url, self.parse, dont_filter=True, meta=response.meta)
        tree_node = etree.HTML(response.body)
        comment_nodes = tree_node.xpath('//div[@class="c" and contains(@id,"C_")]')
        for comment_node in comment_nodes:
            comment_user_url = comment_node.xpath('.//a[contains(@href,"/u/")]/@href')
            if not comment_user_url:
                continue
            comment_item = CommentItem()
            comment_item['crawl_time'] = int(time.time())
            comment_item['weibo_id'] = response.url.split('/')[-1].split('?')[0]
            comment_item['comment_user_id'] = re.search(r'/u/(\d+)', comment_user_url[0]).group(1)
            comment_item['comment_user_name'] = comment_node.xpath('.//a[contains(@href,"/u/")]/text()')[0]
            comment_item['content'] = extract_comment_content(etree.tostring(comment_node, encoding='unicode'))
            comment_item['_id'] = comment_node.xpath('./@id')[0]
            created_at_info = comment_node.xpath('.//span[@class="ct"]/text()')[0]
            like_num = comment_node.xpath('.//a[contains(text(),"赞[")]/text()')[-1]
            comment_item['like_num'] = int(re.search('\d+', like_num).group())
            comment_item['created_at'] = time_fix(created_at_info.split('\xa0')[0])
            # 判断是否是对别人评论的回复
            if comment_node.xpath('.//span[@class="ctt"]/a[contains(@href,"/n/")]'):
                # 被回复者的用户名
                replied_user_name = comment_node.xpath('.//span[@class="ctt"]/a[contains(@href,"/n/")]/text()')[0]
                comment_item['replied_user_name'] = replied_user_name[1:]
                print(comment_item['replied_user_name'])
                # # 从数据库中找到被回复者的id
                # config_path = os.getcwd() + os.sep + 'config.json'
                # with open(config_path) as T:
                #     config = json.loads(T.read())
                # client = MongoClient()
                # db = client[config['mongo_db_name']]
                # collection = db['Comments']
                # for doc1 in collection.find():
                # # 如果找到了评论的用户名与被回复者的用户名相同的评论
                #     if doc1['comment_user_name'] == comment_item['replied_user_name']:
                #     # 将这条评论的用户id填入到这条评论的被回复者id中
                #         comment_item['replied_user_id'] =doc1['comment_user_id']
                #         print(comment_item['获取到被回复者id'])
                #     continue
            else:
                comment_item['replied_user_name'] = ''
            comment_item['replied_user_id'] = ''         
            yield comment_item
