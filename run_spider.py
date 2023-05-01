#!/usr/bin/env python
# encoding: utf-8

import os
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.comment import CommentSpider
from spiders.follower import FollowerSpider
from spiders.fan import FanSpider


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

