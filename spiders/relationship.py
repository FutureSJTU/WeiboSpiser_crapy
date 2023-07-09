#!/usr/bin/env python
# encoding: utf-8

import re
import os
import json
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from items import RelationshipItem
import time


class RelationshipSpider(Spider):
    name = "Relationship_spider"
    base_url = "https://weibo.cn"

    def start_requests(self):
        config_path = os.getcwd() + os.sep + 'config.json'
        with open(config_path) as f:
            config = json.loads(f.read())
        user_ids = config['user_id_list']
        fan_urls = [f"{self.base_url}/{user_id}/fans?page=1" for user_id in user_ids]
        follow_urls = [f"{self.base_url}/{user_id}/follow?page=1" for user_id in user_ids]
        if config['get_fan'] == 1:
            for url in fan_urls:
                yield Request(url, callback=self.fan_parse)
        for url in follow_urls:
            yield Request(url, callback=self.parse)

    def fan_parse(self, response):
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield Request(page_url, self.parse, dont_filter=True, meta=response.meta)
        selector = Selector(response)
        urls = selector.xpath('//a[text()="关注他" or text()="关注她" or text()="移除"]/@href').extract()
        uids = re.findall('uid=(\d+)', ";".join(urls), re.S)
        ID = re.findall('(\d+)/fans', response.url)[0]


        # 将爬取结果暂时写入fan.txt
        with open('fan.txt', 'a') as f:
            for uid in uids:
                f.write(ID + '-' + uid + '\n')


    def parse(self, response):
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield Request(page_url, self.parse, dont_filter=True, meta=response.meta)
        selector = Selector(response)
        urls = selector.xpath('//a[text()="关注他" or text()="关注她" or text()="取消关注"]/@href').extract()
        
        ID = re.findall('(\d+)/follow', response.url)[0]
        relationships_item = RelationshipItem()
        relationships_item["user_id"] = ID
        relationships_item["fan_id_list"] = ''
        relationships_item["follow_id_list"] = ''

        config_path = os.getcwd() + os.sep + 'config.json'
        with open(config_path) as f:
            config = json.loads(f.read())

        if config['get_follower'] == 1:
            uids = re.findall('uid=(\d+)', ";".join(urls), re.S)
            for uid in uids:
                # 将uid加入relationships_item["follow_id_list"]，中间用逗号隔开
                relationships_item["follow_id_list"] = relationships_item["follow_id_list"] + ',' + uid

        # 将暂存在fan.txt中的爬取结果写入relationships_item["fan_id_list"]中
        # fan.txt中的内容形如ID-uid
        if config['get_fan'] == 1:
            with open('fan.txt', 'r') as f:
                for line in f.readlines():
                    if line.startswith(ID):
                        relationships_item["fan_id_list"] = relationships_item["fan_id_list"] + ',' + line.split('-')[1].strip('\n')          
                      
        yield relationships_item
