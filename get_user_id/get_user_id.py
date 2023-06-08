"""
本脚本的作用是从mongodb数据库中获取用户的id
具体的操作是从名为weibo的数据库下的名为WUYUETIAN_by_keywords的collection中获取用户的id
该collection中数据的格式为：
{
  "id": "4906356454720841",
  "bid": "N2FmljO6B",
  "user_id": "3446032624",
  "screen_name": "某只蔡猪",
  "text": "五月天家人们大麦好抢一点还是纷玩岛好抢一点",
  "article_url": "",
  "location": "",
  "at_users": "",
  "topics": "",
  "reposts_count": "0",
  "comments_count": "1",
  "attitudes_count": "0",
  "created_at": "2023-05-28 12:59",
  "source": "五月天超话",
  "pics": "",
  "video_url": "",
  "retweet_id": ""
}
其中user_id即为我们需要的用户id
获取到的用户id写入到名为user_id.txt的文件中
"""

import pymongo
import os

# 连接数据库
client = pymongo.MongoClient(host='localhost', port=27017)
db = client.weibo
collection = db.WUYUETIAN_by_keywords

# 获取用户id
user_id = []
for item in collection.find():
    user_id.append(item['user_id'])

# 将用户id写入到文件中
with open(os.path.join(os.path.dirname(__file__), 'user_id.txt'), 'w', encoding='utf-8') as f:
    for item in user_id:
        f.write(item + '\n')





