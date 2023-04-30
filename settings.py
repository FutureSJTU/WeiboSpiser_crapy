# -*- coding: utf-8 -*-

BOT_NAME = 'spider'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

ROBOTSTXT_OBEY = False

# change cookie to yours
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie': 'SUB=_2A25JTXehDeRhGeFL61YX-C7FyD-IHXVqzhnprDV6PUJbkdANLWitkW1NQo4LyoUPFTd4-Yi8jp4XxtiiZPto9e3m; SCF=AmR9KXAT8hg73O9EnBd0xbCI31CiHKmXK-8z94ek70pwDqiQsswzTzatI2kfDANRGz-cLgLmPIM3Fb4QI8yYYy8.; SSOLoginState=1682507761; _T_WM=82175302422; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode=20000174&uicode=20000174'}
  
CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 3

HTTPERROR_ALLOWED_CODES = [302]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'middlewares.IPProxyMiddleware': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 101,
}

ITEM_PIPELINES = {
    'pipelines.MongoDBPipeline': 300,
}

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
