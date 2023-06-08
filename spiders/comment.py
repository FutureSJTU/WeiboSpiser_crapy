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
import requests


class CommentSpider(Spider):
    name = "comment_spider"
    base_url = "https://weibo.cn"

    def start_requests(self):
        file_path = os.getcwd() + os.sep + 'weibo_spider' + os.sep + 'weibo_id_list.txt'
        f = open(file_path,"r")   
        tweet_ids = f.readlines()
        # tweet_ids = ['MCGZFDJ1j']
        urls = [f"{self.base_url}/comment/hot/{tweet_id}?rl=1&page=1" for tweet_id in tweet_ids]
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
        config_path = os.getcwd() + os.sep + 'config.json'
        with open(config_path) as T:
            config = json.loads(T.read())
        cookie = config['cookie']
        comment_nodes = tree_node.xpath('//div[@class="c" and contains(@id,"C_")]')
        for comment_node in comment_nodes:
            comment_user_url = comment_node.xpath('.//a[contains(@href,"/u/")]/@href')
            if not comment_user_url:
                continue
            comment_item = CommentItem()
            comment_item['crawl_time'] = int(time.time())
            comment_item['weibo_id'] = response.url.split('/')[-1].split('?')[0]
            comment_item['comment_user_id'] = re.search(r'/u/(\d+)', comment_user_url[0]).group(1)
            comment_item['content'] = extract_comment_content(etree.tostring(comment_node, encoding='unicode'))
            comment_item['_id'] = comment_node.xpath('./@id')[0]
            created_at_info = comment_node.xpath('.//span[@class="ct"]/text()')[0]
            like_num = comment_node.xpath('.//a[contains(text(),"赞[")]/text()')[-1]
            comment_item['like_num'] = int(re.search('\d+', like_num).group())
            comment_item['created_at'] = time_fix(created_at_info.split('\xa0')[0])
            """
            一段普通的评论的页面源码如下：
            <div class="c" id="C_4903976829457994">        <a href="/u/7237401773">挪挞煦</a>        : <span class="ctt">入耳舒服</span>    &nbsp;<a href="/spam/?cid=4903976829457994&amp;fuid=7237401773&amp;type=2&amp;rl=1">举报</a>    &nbsp;    <span class="cc">    <a href="/attitude/N1FseDGsi/update?object_type=comment&amp;uid=7504680933&amp;rl=1&amp;st=693837">赞[0]</a></span>        &nbsp;<span class="cc"><a href="/comments/reply/N1EeotQVF/4903976829457994?rl=1&amp;st=693837">回复</a></span>        &nbsp;    <span class="ct">05月21日 23:24&nbsp;来自来自广西    </span></div>

            一段对别人评论的回复的页面源码如下：
            <div class="c" id="C_4903972244292921">        <a href="/u/5847045359">夜澜卧听风就是雨</a>    <img src="https://h5.sinaimg.cn/upload/2016/05/26/319/5338.gif" alt="V">    : <span class="ctt">回复<a href="/n/KK%E6%89%93%E4%BA%86%E4%B8%AA%E5%97%9D">@KK打了个嗝</a>:两种各有优势吧</span>    &nbsp;<a href="/spam/?cid=4903972244292921&amp;fuid=5847045359&amp;type=2&amp;rl=1">举报</a>    &nbsp;    <span class="cc">    <a href="/attitude/N1FkQi0MF/update?object_type=comment&amp;uid=7504680933&amp;rl=1&amp;st=693837">赞[0]</a></span>        &nbsp;<span class="cc"><a href="/comments/reply/N1EeotQVF/4903972244292921?rl=1&amp;st=693837">回复</a></span>        &nbsp;    <span class="ct">05月21日 23:05&nbsp;来自来自山东    </span></div>
            
            可以看到，两者的区别在于，对别人评论的回复中，<span class="ctt"></span> 中的内容中，有"回复"这个关键字，并且有a标签；而普通的评论中，<span class="ctt"></span> 中的的内容中，没有"回复"这个关键字，也没有a标签
            而被回复者的信息，就在"回复"这个关键字的后面的a标签中：
            <a href="/n/KK%E6%89%93%E4%BA%86%E4%B8%AA%E5%97%9D">@KK打了个嗝</a>,其中，“KK打了个嗝”就是被回复者的用户名
            """
            # 判断是否是对别人评论的回复，注意，普通评论的源码中也有"回复"这个关键字，这是用来回复该评论的按钮
            # 但是普通评论的<span class="ctt"></span> 中的内容中，没有"回复"这个关键字，而对别人评论的回复中有
            if comment_node.xpath('.//span[@class="ctt" and contains(text(),"回复")]'):
                # 被回复者的用户名
                reply_user_name = comment_node.xpath('.//span[@class="ctt" and contains(text(),"回复")]/a/text()')[0]
                comment_item['reply_user_name'] = reply_user_name[1:]
                print(comment_item['reply_user_name'])
            else:
                comment_item['reply_user_name'] = ''
                        
            yield comment_item
