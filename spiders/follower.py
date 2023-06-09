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


class FollowerSpider(Spider):
    name = "follower_spider"
    base_url = "https://weibo.cn"

    def start_requests(self):
        config_path = os.getcwd() + os.sep + 'config.json'
        with open(config_path) as f:
            config = json.loads(f.read())
        user_ids = config['user_id_list']
        urls = [f"{self.base_url}/{user_id}/follow?page=1" for user_id in user_ids]
        for url in urls:
            yield Request(url, callback=self.parse)

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
        uids = re.findall('uid=(\d+)', ";".join(urls), re.S)
        ID = re.findall('(\d+)/follow', response.url)[0]
        for uid in uids:
            relationships_item = RelationshipItem()
            relationships_item['crawl_time'] = int(time.time())
            relationships_item["fan_id"] = ID
            relationships_item["followed_id"] = uid
            relationships_item["user_id"] = ID
            yield relationships_item
