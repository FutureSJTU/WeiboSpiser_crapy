# 根据给定关键词，建立参与该话题的大v库，以便后续分析使用。
## 1. 根据关键词爬取微博：
使用项目weibo-search-master，根据关键词爬取微博（以五月天热搜为例），结果存入mongodb数据库weibo.WUYUETIAN_by_keywords中
在该项目的settings.py中设置关键词、日期等参数
## 2. 从爬取到的微博信息中提取用户id：
运行本目录下的get_user_id.py，从weibo.WUYUETIAN_by_keywords中提取用户id，存入user_id.txt中
## 3. 根据user_id.txt爬取用户信息：
使用本项目，将config.json中的user_id_list改为本目录下的"./get_user_id/user_id.txt"，并将get_weibo等一系列选择置为0（只需要用户基本信息），运行本项目，爬取用户信息，结果存入mongodb数据库weibo2.user中
## 4. 筛选出大v的用户id：
运行本目录下的get_famous_user.py，根据存入数据库的用户信息，从user_id.txt中筛选出大v的用户id，存入famous_user_id.txt中
## 5. 根据大v的用户id爬取大v的用户信息和微博：
使用本项目，将config.json中的user_id_list改为本目录下的"./get_user_id/famous_user_id.txt",并将get_weibo置为1，运行本项目，爬取大v的用户信息和微博，结果存入mongodb数据库famous_user.user和famous_user.weibo中
## 6. 将大v的基本信息和微博合并，组建大v库：
运行本目录下的merge_famous_user.py，将大v的基本信息和微博合并，组建大v库，结果存入mongodb数据库famous_user.user_allinfo中