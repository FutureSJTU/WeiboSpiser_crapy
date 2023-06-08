"""
从mongodb中获取大V的用户id
具体的操作是从名为weibo2的数据库下的名为user的collection中获取用户的id
该collection中数据的格式为：
{
  "_id": {
    "$oid": "64734af08816416f159ac567"
  },
  "id": "1735937570",
  "nickname": "江南都市报",
  "gender": "男",
  "location": "江西",
  "birthday": "0001-00-00",
  "description": "微言大义   公信天下",
  "verified_reason": "江南都市报官方微博",
  "talent": "",
  "education": "",
  "work": "",
  "weibo_num": 44349,
  "following": 710,
  "followers": 11305000
}
如果"verified_reason"的内容不为空，则该用户为大V用户
将大v用户的user_id存入famous_user_id.txt文件中
"""

import pymongo
import os

# 连接数据库
client = pymongo.MongoClient(host='localhost', port=27017)
db = client.weibo2
collection = db.user

# 获取用户id
user_id = []
for item in collection.find():
    if item['verified_reason'] != '':
        user_id.append(item['id'])

# 将用户id写入到文件中
with open(os.path.join(os.path.dirname(__file__), 'famous_user_id.txt'), 'w', encoding='utf-8') as f:
    for item in user_id:
        f.write(item + '\n')

