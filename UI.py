"""
实现一个简单的UI界面，用于修改config.json配置文件
config.json文件中的内容为：
{
    "user_id_list": ["2022252207"],
    "get_weibo": 1
    "get_comment": 1,
    "get_fan": 0,
    "get_follower": 0,
    "filter": 1,
    "since_date": "2023-06-10",
    "end_date": "2023-06-10",
    "max_page": 999,
    "pic_download": 1,
    "video_download": 1
}
对于get_weibo，应该实现两个按钮让用户选择“是”或“否”，若选择“是”，则get_weibo的值为1，若选择“否”，则get_weibo的值为0
对于user_id_list的值，应该实现一个输入框，可以输入user_id_list的值。用户可以输入多个user_id，用英文逗号隔开，例如：141414515,2022252207，而在config.json文件中，user_id_list的值应该为["141414515", "2022252207"]
"get_comment","get_fan","get_follower","filter"的处理方式与get_weibo相同
对于"since_date",应该在同一行实现三个输入框，分别输入年、月、日，形如：_年_月_日，而在config.json文件中，since_date的值应该为"2023-06-10"
"end_date"的处理方式与"since_date"相同
"pic_download": 1,"video_download"的处理方式与get_weibo相同
"max_page","cookie","mongo_db_name"是字符串，应该实现一个输入框，可以输入这些值
在UI界面打开时，应该读取config.json文件，将已有的值显示在按钮上和输入框中
"""

# 增加一个按钮，用于开始爬取微博，点击按钮后，等效于在命令行中输入python -m weibo_spider


import tkinter as tk
import json
import os

class UI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('微博爬虫')
        self.window.geometry('380x770')
        self.window.resizable(width=False, height=False)

        self.user_id_list = tk.StringVar()
        self.user_id_list.set('')
        self.get_weibo = tk.IntVar()
        self.get_weibo.set(0)
        # "get_comment","get_fan","get_follower","filter"的处理方式与get_weibo相同
        self.get_comment = tk.IntVar()
        self.get_comment.set(0)
        self.get_fan = tk.IntVar()
        self.get_fan.set(0)
        self.get_follower = tk.IntVar()
        self.get_follower.set(0)
        self.filter = tk.IntVar()
        self.filter.set(0)
        # 对于"since_date",应该在同一行实现三个输入框，分别输入年、月、日，形如：_年_月_日，而在config.json文件中，since_date的值应该为"2023-06-10"
        # "end_date"的处理方式与"since_date"相同
        self.since_date_year = tk.StringVar()
        self.since_date_year.set('')
        self.since_date_month = tk.StringVar()
        self.since_date_month.set('')
        self.since_date_day = tk.StringVar()
        self.since_date_day.set('')
        self.end_date_year = tk.StringVar()
        self.end_date_year.set('')
        self.end_date_month = tk.StringVar()
        self.end_date_month.set('')
        self.end_date_day = tk.StringVar()
        self.end_date_day.set('')
        # 对于"since_date",应该在同一行实现三个输入框，分别输入年、月、日，形如：_年_月_日，而在config.json文件中，since_date的值应该为"2023-06-10"
        # "end_date"的处理方式与"since_date"相同
        self.pic_download = tk.IntVar()
        self.pic_download.set(0)
        self.video_download = tk.IntVar()
        self.video_download.set(0)
        
        # "max_page","cookie","mongo_db_name"是字符串，应该实现一个输入框，可以输入这些值
        self.max_page = tk.StringVar()
        self.max_page.set('')
        self.cookie = tk.StringVar()
        self.cookie.set('')
        self.mongo_db_name = tk.StringVar()
        self.mongo_db_name.set('')


        self.read_config()
        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        self.label2 = tk.Label(self.window, text='用户ID：')
        self.label2.place(x=50, y=100)
        self.entry = tk.Entry(self.window, textvariable=self.user_id_list)
        self.entry.place(x=150, y=100)
        self.label1 = tk.Label(self.window, text='是否爬取微博：')
        self.label1.place(x=50, y=50)
        self.button1 = tk.Radiobutton(self.window, text='是', variable=self.get_weibo, value=1)
        self.button1.place(x=150, y=50)
        self.button2 = tk.Radiobutton(self.window, text='否', variable=self.get_weibo, value=0)
        self.button2.place(x=200, y=50)

        # "get_comment","get_fan","get_follower","filter"的处理方式与get_weibo相同
        self.label3 = tk.Label(self.window, text='是否爬取评论：')
        self.label3.place(x=50, y=150)
        self.button4 = tk.Radiobutton(self.window, text='是', variable=self.get_comment, value=1)
        self.button4.place(x=150, y=150)
        self.button5 = tk.Radiobutton(self.window, text='否', variable=self.get_comment, value=0)
        self.button5.place(x=200, y=150)
        self.label4 = tk.Label(self.window, text='是否爬取粉丝：')
        self.label4.place(x=50, y=200)
        self.button6 = tk.Radiobutton(self.window, text='是', variable=self.get_fan, value=1)
        self.button6.place(x=150, y=200)
        self.button7 = tk.Radiobutton(self.window, text='否', variable=self.get_fan, value=0)
        self.button7.place(x=200, y=200)
        self.label5 = tk.Label(self.window, text='是否爬取关注：')
        self.label5.place(x=50, y=250)
        self.button8 = tk.Radiobutton(self.window, text='是', variable=self.get_follower, value=1)
        self.button8.place(x=150, y=250)
        self.button9 = tk.Radiobutton(self.window, text='否', variable=self.get_follower, value=0)
        self.button9.place(x=200, y=250)
        self.label6 = tk.Label(self.window, text='是否过滤转发：')
        self.label6.place(x=50, y=300)
        self.button10 = tk.Radiobutton(self.window, text='是', variable=self.filter, value=1)
        self.button10.place(x=150, y=300)
        self.button11 = tk.Radiobutton(self.window, text='否', variable=self.filter, value=0)
        self.button11.place(x=200, y=300)
        # 对于"since_date",应该在同一行实现三个输入框，分别输入年、月、日，形如：_年_月_日，而在config.json文件中，since_date的值应该为"2023-06-10"
        # "end_date"的处理方式与"since_date"相同
        self.label7 = tk.Label(self.window, text='起始日期：')
        self.label7.place(x=50, y=350)
        self.entry1 = tk.Entry(self.window, textvariable=self.since_date_year, width=4)
        self.entry1.place(x=150, y=350)
        self.label8 = tk.Label(self.window, text='年')
        self.label8.place(x=185, y=350)
        self.entry2 = tk.Entry(self.window, textvariable=self.since_date_month, width=2)
        self.entry2.place(x=220, y=350)
        self.label9 = tk.Label(self.window, text='月')
        self.label9.place(x=240, y=350)
        self.entry3 = tk.Entry(self.window, textvariable=self.since_date_day, width=2)
        self.entry3.place(x=275, y=350)

        self.label10 = tk.Label(self.window, text='日')
        self.label10.place(x=295, y=350)

        self.label11 = tk.Label(self.window, text='终止日期：')
        self.label11.place(x=50, y=400)
        self.entry4 = tk.Entry(self.window, textvariable=self.end_date_year, width=4)
        self.entry4.place(x=150, y=400)
        self.label12 = tk.Label(self.window, text='年')
        self.label12.place(x=185, y=400)
        self.entry5 = tk.Entry(self.window, textvariable=self.end_date_month, width=2)
        self.entry5.place(x=220, y=400)
        self.label13 = tk.Label(self.window, text='月')
        self.label13.place(x=240, y=400)
        self.entry6 = tk.Entry(self.window, textvariable=self.end_date_day, width=2)
        self.entry6.place(x=275, y=400)
        self.label14 = tk.Label(self.window, text='日')
        self.label14.place(x=295, y=400)
        # "pic_download": 1,"video_download"的处理方式与get_weibo相同
        self.label15 = tk.Label(self.window, text='是否下载图片：')
        self.label15.place(x=50, y=450)
        self.button12 = tk.Radiobutton(self.window, text='是', variable=self.pic_download, value=1)
        self.button12.place(x=150, y=450)
        self.button13 = tk.Radiobutton(self.window, text='否', variable=self.pic_download, value=0)
        self.button13.place(x=200, y=450)
        self.label16 = tk.Label(self.window, text='是否下载视频：')
        self.label16.place(x=50, y=500)
        self.button14 = tk.Radiobutton(self.window, text='是', variable=self.video_download, value=1)
        self.button14.place(x=150, y=500)
        self.button15 = tk.Radiobutton(self.window, text='否', variable=self.video_download, value=0)
        self.button15.place(x=200, y=500)
        # "max_page","cookie","mongo_db_name"是字符串，应该实现一个输入框，可以输入这些值
        self.label17 = tk.Label(self.window, text='最大页数：')
        self.label17.place(x=50, y=550)
        self.entry7 = tk.Entry(self.window, textvariable=self.max_page, width=10)
        self.entry7.place(x=150, y=550)
        
        self.label18 = tk.Label(self.window, text='cookie：')
        self.label18.place(x=50, y=600)
        # cookie文本可能会很长，所以应该限制显示长度，当长度超过一定值时，应该显示省略号
        self.entry8 = tk.Entry(self.window, textvariable=self.cookie, width=10)
        self.entry8.place(x=150, y=600)

        self.label19 = tk.Label(self.window, text='数据库名称：')
        self.label19.place(x=50, y=650)
        self.entry9 = tk.Entry(self.window, textvariable=self.mongo_db_name, width=10)
        self.entry9.place(x=150, y=650)

        self.button3 = tk.Button(self.window, text='保存配置', command=self.save_config)
        self.button3.place(x=100, y=700)

        # 增加一个按钮，用于开始爬取微博，点击按钮后，等效于在命令行中输入python -m weibo_spider
        self.button4 = tk.Button(self.window, text='开始爬取', command=self.start_spider)
        self.button4.place(x=220, y=700)
        




    def read_config(self):
        if os.path.exists('config.json'):
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.get_weibo.set(config['get_weibo'])
                self.user_id_list.set(','.join(config['user_id_list']))
                # "get_comment","get_fan","get_follower","filter"的处理方式与get_weibo相同
                self.get_comment.set(config['get_comment'])
                self.get_fan.set(config['get_fan'])
                self.get_follower.set(config['get_follower'])
                self.filter.set(config['filter'])
                # 对于"since_date",应该在同一行实现三个输入框，分别输入年、月、日，形如：_年_月_日，而在config.json文件中，since_date的值应该为"2023-06-10"
                # "end_date"的处理方式与"since_date"相同
                self.since_date_year.set(config['since_date'].split('-')[0])
                self.since_date_month.set(config['since_date'].split('-')[1])
                self.since_date_day.set(config['since_date'].split('-')[2])
                self.end_date_year.set(config['end_date'].split('-')[0])
                self.end_date_month.set(config['end_date'].split('-')[1])
                self.end_date_day.set(config['end_date'].split('-')[2])
                # "pic_download": 1,"video_download"的处理方式与get_weibo相同
                self.pic_download.set(config['pic_download'])
                self.video_download.set(config['video_download'])
                # "max_page","cookie","mongo_db_name"是字符串，应该实现一个输入框，可以输入这些值
                self.max_page.set(config['max_page'])
                self.cookie.set(config['cookie'])
                self.mongo_db_name.set(config['mongo_db_name'])



    def save_config(self):
        self.user_id_list.set(self.user_id_list.get().replace('，', ','))
        config = {
            'user_id_list': self.user_id_list.get().split(','),
            'get_weibo': self.get_weibo.get(),
            # "get_comment","get_fan","get_follower","filter"的处理方式与get_weibo相同
            'get_comment': self.get_comment.get(),
            'get_fan': self.get_fan.get(),
            'get_follower': self.get_follower.get(),
            'filter': self.filter.get(),
            # 对于"since_date",应该在同一行实现三个输入框，分别输入年、月、日，形如：_年_月_日，而在config.json文件中，since_date的值应该为"2023-06-10"
            # "end_date"的处理方式与"since_date"相同
            'since_date': self.since_date_year.get() + '-' + self.since_date_month.get() + '-' + self.since_date_day.get(),
            'end_date': self.end_date_year.get() + '-' + self.end_date_month.get() + '-' + self.end_date_day.get(),
            # "max_page","cookie","mongo_db_name"是字符串，应该实现一个输入框，可以输入这些值
            'max_page': self.max_page.get(),
            'cookie': self.cookie.get(),
            'mongo_db_name': self.mongo_db_name.get(),
            'random_wait_pages': [1, 5],
            'random_wait_seconds': [6, 10],
            'global_wait': [[1000, 3600], [500, 2000]],
            'write_mode': ["mongo"],
            # "pic_download": 1,"video_download"的处理方式与get_weibo相同
            'pic_download': self.pic_download.get(),
            'video_download': self.video_download.get(),
            'file_download_timeout': [5, 5, 10],
	        'result_dir_name': 0,
            'mysql_config': {
                "host": "localhost",
                "port": 3306,
                "user": "root",
                "password": "123456",
                "charset": "utf8mb4"
            },
            'kafka_config': {
                "bootstrap-server": "127.0.0.1:9092",
                "weibo_topics": ["spider_weibo"],
                "user_topics": ["spider_weibo"]
            },
            'sqlite_config': "weibo.db",
            'mongo_config': {
                "connection_string": "mongodb://localhost:27017/"

    },
        }
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        self.window.destroy()
    
    # 增加一个按钮，用于开始爬取微博，点击按钮后，等效于在命令行中输入python -m weibo_spider
    def start_spider(self):
        self.save_config()
        os.system('python -m weibo_spider')



if __name__ == '__main__':
    UI()

