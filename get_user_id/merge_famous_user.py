"""
基于数据库信息构建大v库
数据来源：mongoDB数据库中famous_user数据库下的user集合和weibo集合
具体操作：是将同一个用户的信息存储在同一个文档中，包括用户的基本信息、和所发的所有微博信息，具体的格式如下(在这里只列举了三条微博，实际上可能远远不止三条，需要将数据库内该用户所发的所有微博合并进去)：
{
  "_id": {
    "$oid": "647355b9fe12bf682c9b1e52"
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
  "weibo_num": 44353,
  "following": 710,
  "followers": 11305000
  "weibo": {
  {
  "_id": {
    "$oid": "647355c7fe12bf682c9b1e54"
  },
  "id": "N2IBhze8O",
  "user_id": "1735937570",
  "content": "【#老师退休前最后一课收到暖心惊喜#】近日，在浙江江山，某高中老师退休前的最后一课上，学生们偷偷为他准备惊喜。网友：#这道题把老师整不会了#。（光明网）新华网的微博视频  ",
  "article_url": "",
  "original_pictures": "无",
  "retweet_pictures": null,
  "original": true,
  "video_url": "https://f.video.weibocdn.com/o0/9ZExGdQHlx085Nhct3na010412005xt70E010.mp4?label=mp4_hd&template=540x960.24.0&Expires=1685283787&ssig=GtuAU6%2FOlj&KID=unistore,video",
  "publish_place": "无",
  "publish_time": "2023-05-28 21:14",
  "publish_tool": "微博视频号",
  "up_num": 0,
  "retweet_num": 0,
  "comment_num": 0
  }
  {
  "_id": {
    "$oid": "647355c7fe12bf682c9b1e55"
  },
  "id": "N2IvcwnsX",
  "user_id": "1735937570",
  "content": "#大学保安凌晨认真背单词#【励志！#大学生凌晨拍到保安背单词#】近日，江苏南京，一名南大学生凌晨离开图书馆时，发现门口保安在背单词。网友：努力的人到哪儿都闪闪发光！ 新华社的微博视频  ",
  "article_url": "",
  "original_pictures": "无",
  "retweet_pictures": null,
  "original": true,
  "video_url": "https://f.video.weibocdn.com/o0/OKYogcAKlx085NqGRC1a010412001Jl70E010.mp4?label=mp4_hd&template=540x960.24.0&Expires=1685283788&ssig=fRNpUgSf8K&KID=unistore,video",
  "publish_place": "无",
  "publish_time": "2023-05-28 20:59",
  "publish_tool": "微博视频号",
  "up_num": 0,
  "retweet_num": 0,
  "comment_num": 0
  }
  {
  "_id": {
    "$oid": "647355c7fe12bf682c9b1e56"
  },
  "id": "N2Ir8qUI3",
  "user_id": "1735937570",
  "content": "【#市民被压车底20多人瞬间跑来救人#】#济南老师儿好样的# 5月26日晚，在窑头路一位市民被压在网约车车底，失去意识。危急时刻，路过此地的济南公交B53路驾驶员和其他热心乘客立即下车救人。唐光华立即拉好手刹，向车上乘客解释并呼吁道：“下来帮个忙吧，老师儿，有人被压在车底下了！”唐光华和车上...全文 ",
  "article_url": "",
  "original_pictures": "无",
  "retweet_pictures": null,
  "original": true,
  "video_url": "https://f.video.weibocdn.com/o0/NtZTAqlclx085MVOg5Xq01041200fzfV0E010.mp4?label=mp4_hd&template=852x480.25.0&Expires=1685283789&ssig=YZhnUlJomc&KID=unistore,video",
  "publish_place": "无",
  "publish_time": "2023-05-28 20:49",
  "publish_tool": "微博视频号",
  "up_num": 0,
  "retweet_num": 0,
  "comment_num": 0
  }
  }
}
其中，用户的基本信息来自于user集合，用户的微博信息来自于weibo集合，两者通过user_id进行关联
将上述文档存入MongoDB数据库中，数据库名为famous_user，集合名为user_allinfo
"""

import pymongo

# 连接数据库
client = pymongo.MongoClient(host='localhost', port=27017)
# 指定数据库
db = client.famous_user
# 指定集合
user = db.user
weibo = db.weibo
user_allinfo = db.user_allinfo

# 从user集合中获取所有用户的id
user_id_list = []
for item in user.find():
    user_id_list.append(item['id'])

# 对于user_id_list中的每一个用户id，从weibo集合中获取其所有微博信息，存入user_allinfo集合中
for user_id in user_id_list:
    weibo_info = []
    for item in weibo.find({'user_id': user_id}):
        weibo_info.append(item)
    user_info = user.find_one({'id': user_id})
    user_info['weibo'] = weibo_info
    user_allinfo.insert_one(user_info)
    









