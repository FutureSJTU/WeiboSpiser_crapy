本项目在https://github.com/dataabc/weiboSpider的基础上继续开发，基于crapy框架实现了读取评论、关注列表、粉丝列表的功能

# Weibo Spider

本程序可以连续爬取**一个**或**多个**新浪微博用户（如[胡歌](https://weibo.cn/u/1223178222)、[迪丽热巴](https://weibo.cn/u/1669879400)、[郭碧婷](https://weibo.cn/u/1729370543)）的数据，并将结果信息写入**文件**或**数据库**。写入信息几乎包括用户微博的所有数据，包括**用户信息**和**微博信息**两大类。因为内容太多，这里不再赘述，详细内容见[获取到的字段](#获取到的字段)。如果只需要用户信息，可以通过设置实现只爬取微博用户信息的功能。本程序需设置cookie来获取微博访问权限，后面会讲解[如何获取cookie](#如何获取cookie)。如果不想设置cookie，可以使用[免cookie版](https://github.com/dataabc/weibo-crawler)，二者功能类似。

爬取结果可写入文件和数据库，具体的写入文件类型如下：

- **txt文件**（默认）
- **csv文件**（默认）
- **json文件**（可选）
- **MySQL数据库**（可选）
- **MongoDB数据库**（可选）
- **SQLite数据库**（可选）

同时支持下载微博中的图片和视频，具体的可下载文件如下：

- **原创**微博中的原始**图片**（可选）
- **转发**微博中的原始**图片**（可选）
- **原创**微博中的**视频**（可选）
- **转发**微博中的**视频**（可选）


### 用户信息

- 用户id：微博用户id，如"1669879400"，其实这个字段本来就是已知字段
- 昵称：用户昵称，如"Dear-迪丽热巴"
- 性别：微博用户性别
- 生日：用户出生日期
- 所在地：用户所在地
- 学习经历：用户上学时学校的名字和时间
- 工作经历：用户所属公司名字和时间
- 微博数：用户的全部微博数（转发微博+原创微博）
- 关注数：用户关注的微博数量
- 关注列表
- 粉丝数：用户的粉丝数
- 粉丝列表
- 简介：用户简介
- 认证信息：为认证用户特有，用户信息栏显示的认证信息

### 微博信息

- 微博id：微博唯一标志
- 微博内容：微博正文
- 头条文章url：微博中头条文章的url，若微博中不存在头条文章，则值为''
- 原始图片url：原创微博图片和转发微博转发理由中图片的url，若某条微博存在多张图片，每个url以英文逗号分隔，若没有图片则值为"无"
- 视频url: 微博中的视频url，若微博中没有视频，则值为"无"
- 微博发布位置：位置微博中的发布位置
- 微博发布时间：微博发布时的时间，精确到分
- 点赞数：微博被赞的数量
- 转发数：微博被转发的数量
- 评论数：微博被评论的数量
- 微博发布工具：微博的发布工具，如iPhone客户端、HUAWEI Mate 20 Pro等
- 结果文件：保存在当前目录weibo文件夹下以用户昵称为名的文件夹里，名字为"user_id.csv"和"user_id.txt"的形式
- 微博图片：原创微博中的图片和转发微博转发理由中的图片，保存在以用户昵称为名的文件夹下的img文件夹里
- 微博视频：原创微博中的视频，保存在以用户昵称为名的文件夹下的video文件夹里
- 微博评论，默认输出到mongodb数据库中，Comments簇下
## 示例

如果想要知道程序的具体运行结果，可以查看[示例文档](https://github.com/FutureSJTU/WeiboSpiser_crapy/blob/main/docs/example.md)，该文档介绍了爬取[迪丽热巴微博](https://weibo.cn/u/1669879400)的例子，并附有部分结果文件截图。

## 运行环境

- 开发语言：python2/python3
- 系统： Windows/Linux/macOS

## 使用说明

### 1.程序设置

要了解程序设置，请查看[程序设置文档](https://github.com/FutureSJTU/WeiboSpiser_crapy/blob/main/docs/settings.md)。

### 2.运行程序

在weiboSpider_crapy目录运行如下命令

```bash
$ python3 -m weibo_spider
```

第一次执行，会自动在当前目录创建config.json配置文件，配置好后执行同样的命令就可以获取微博了。

如果你已经有config.json文件了，也可以通过config_path参数配置config.json路径，运行程序，命令行如下：

```bash
$ python3 -m weibo_spider --config_path="config.json"
```

如果你想指定文件（csv、txt、json、图片、视频）保存路径，可以通过output_dir参数设定。假如你想把文件保存到/home/weibo/目录，可以运行如下命令：

```bash
$ python3 -m weibo_spider --output_dir="/home/weibo/"
```

如果你想通过命令行输入user_id，可以使用参数u，可以输入一个或多个user_id，每个user_id以英文逗号分开，如果这些user_id中有重复的user_id，程序会自动去重。命令行如下：

```bash
$ python3 -m weibo_spider --u="1669879400,1223178222"
```

程序会获取user_id分别为1669879400和1223178222的微博用户的微博，后面会讲[如何获取user_id](#如何获取user_id)。该方式的所有user_id使用config.json中的since_date和end_date设置，通过修改它们的值可以控制爬取的时间范围。若config.json中的user_id_list是文件路径，每个命令行中的user_id都会自动保存到该文件内，且自动更新since_date；若不是路径，user_id会保存在当前目录的user_id_list.txt内，且自动更新since_date，若当前目录下不存在user_id_list.txt，程序会自动创建它。

## 个性化定制程序（可选）

本部分为可选部分，如果不需要个性化定制程序或添加新功能，可以忽略此部分。

本程序主体代码位于weibo_spider.py文件，程序主体是一个 Spider 类，上述所有功能都是通过在main函数调用 Spider 类实现的，默认的调用代码如下：

```python
        config = get_config()
        wb = Spider(config)
        wb.start()  # 爬取微博信息
```

用户可以按照自己的需求调用或修改 Spider 类。通过执行本程序，我们可以得到很多信息。

<details>

<summary>点击查看详情</summary>

- wb.user['nickname']：用户昵称；
- wb.user['gender']：用户性别；
- wb.user['location']：用户所在地；
- wb.user['birthday']：用户出生日期；
- wb.user['description']：用户简介；
- wb.user['verified_reason']：用户认证；
- wb.user['talent']：用户标签；
- wb.user['education']：用户学习经历；
- wb.user['work']：用户工作经历；
- wb.user['weibo_num']：微博数；
- wb.user['following']：关注数；
- wb.user['followers']：粉丝数；

</details>

**wb.weibo**：除不包含上述信息外，wb.weibo包含爬取到的所有微博信息，如**微博id**、**微博正文**、**原始图片url**、**发布位置**、**发布时间**、**发布工具**、**点赞数**、**转发数**、**评论数**等。如果爬的是全部微博(原创+转发)，除上述信息之外，还包含被**转发微博原始图片url**、**是否为原创微博**等。wb.weibo是一个列表，包含了爬取的所有微博信息。wb.weibo[0]为爬取的第一条微博，wb.weibo[1]为爬取的第二条微博，以此类推。当filter=1时，wb.weibo[0]为爬取的第一条**原创**微博，以此类推。wb.weibo[0]['id']为第一条微博的id，wb.weibo[0]['content']为第一条微博的正文，wb.weibo[0]['publish_time']为第一条微博的发布时间，还有其它很多信息不在赘述，大家可以点击下面的"详情"查看具体用法。

<details>

<summary>详情</summary>

若目标微博用户存在微博，则：

- id：存储微博id。如wb.weibo[0]['id']为最新一条微博的id；
- content：存储微博正文。如wb.weibo[0]['content']为最新一条微博的正文；
- article_url：存储微博中头条文章的url。如wb.weibo[0]['article_url']为最新一条微博的头条文章url，若微博中不存在头条文章，则值为''；
- original_pictures：存储原创微博的原始图片url和转发微博转发理由中的图片url。如wb.weibo[0]['original_pictures']为最新一条微博的原始图片url，若该条微博有多张图片，则存储多个url，以英文逗号分割；若该微博没有图片，则值为"无"；
- retweet_pictures：存储被转发微博中的原始图片url。当最新微博为原创微博或者为没有图片的转发微博时，则值为"无"，否则为被转发微博的图片url。若有多张图片，则存储多个url，以英文逗号分割；
- publish_place：存储微博的发布位置。如wb.weibo[0]['publish_place']为最新一条微博的发布位置，如果该条微博没有位置信息，则值为"无"；
- publish_time：存储微博的发布时间。如wb.weibo[0]['publish_time']为最新一条微博的发布时间；
- up_num：存储微博获得的点赞数。如wb.weibo[0]['up_num']为最新一条微博获得的点赞数；
- retweet_num：存储微博获得的转发数。如wb.weibo[0]['retweet_num']为最新一条微博获得的转发数；
- comment_num：存储微博获得的评论数。如wb.weibo[0]['comment_num']为最新一条微博获得的评论数；
- publish_tool：存储微博的发布工具。如wb.weibo[0]['publish_tool']为最新一条微博的发布工具。

</details>

## 定期自动爬取微博（可选）

要想让程序每隔一段时间自动爬取，且爬取的内容为新增加的内容（不包括已经获取的微博），请查看[定期自动爬取微博](https://github.com/FutureSJTU/WeiboSpiser_crapy/blob/main/docs/automation.md)。

## 如何获取cookie

要了解获取cookie方法，请查看[cookie文档](https://github.com/FutureSJTU/WeiboSpiser_crapy/blob/main/docs/cookie.md)。

## 如何获取user_id

要了解获取user_id方法，请查看[user_id文档](https://github.com/FutureSJTU/WeiboSpiser_crapy/blob/main/docs/userid.md)，该文档介绍了如何获取一个及多个微博用户user_id的方法。

## 常见问题

如果运行程序的过程中出现错误，可以查看[常见问题](https://github.com/FutureSJTU/WeiboSpiser_crapy/blob/main/docs/FAQ.md)页面

## 注意事项

1. user_id不能为爬虫微博的user_id。因为要爬微博信息，必须先登录到某个微博账号，此账号我们姑且称为爬虫微博。爬虫微博访问自己的页面和访问其他用户的页面，得到的网页格式不同，所以无法爬取自己的微博信息
2. cookie有期限限制，大约三个月。若提示cookie错误或已过期，需要重新更新cookie
