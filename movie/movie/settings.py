# -*- coding: utf-8 -*-

# Scrapy settings for movie project

import os

BOT_NAME = 'movie'

SPIDER_MODULES = ['movie.spiders']
NEWSPIDER_MODULE = 'movie.spiders'

# 遵守robots.txt
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32


# 设置下载延迟
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16


# cookie设置
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'movie.middlewares.MovieSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'movie.middlewares.MovieDownloaderMiddleware': 543,
    'movie.middlewares.RandomUserAgentMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'movie.pipelines.MoviePipeline': 400,
    'movie.pipelines.MongoPipeline': 200,
    # 'movie.pipelines.RedisPipeline': 301,
    # 'scrapy.contrib.pipeline.images.ImagesPipeline': 1
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 配置mongoDB
MONGO_URI = 'localhost'
MONGO_DATABASE = 'movie'

# 开启日志
LOG_FILE = os.path.abspath(os.path.dirname(__file__)) + '/log/mylog.log'
LOG_ENABLED = True
LOG_LEVEL = 'INFO'

# 修改调度器，使用redis
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 去重，使用redis
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 指定redis连接,腾讯云主机
# REDIS_URL = 'redis://root:pass@127.0.0.1:6379'
REDIS_URL = 'redis://root:zy123456@118.24.83.187:6379'
# 设置redis持久化,程序结束不清空redis，可能存在空跑的问题，需要改写一些方法
SCHEDULER_PERSIST = True

# 设置redis非持久化，跑完时清空redis
# SCHEDULER_PERSIST = False


IMAGES_STORE = os.path.abspath(os.path.dirname(__file__)) + '/movies/'.replace('\\', '/')

# 结束时候发送邮件
EMAIL_ENABLE = True
# 邮件配置，使用前请确保你已经开启邮箱的smtp服务
EMAIL_SETTING = {'mail_host': 'smtp.163.com',  # 发件host
                 'mail_user': 'poxiaozy@163.com',  # smtp服务邮箱
                 'mail_pass': 'zy1994211xy',  # smtp服务密码
                 'sender': 'poxiaozy@163.com',  # 发件人
                 'receivers': 'lindozy@163.com',  # 收件人
                 'content': '请登录服务器查看抓取内容，详情已保存到日志！发送者IP为：',  # 邮件内容
                 'title': '爬虫运行结束'}  # 邮件标题

# 设置爬虫运行时间，单位为s
# CLOSESPIDER_TIMEOUT = 14400  # 运行4小时
CLOSESPIDER_TIMEOUT = 120  # 运行2分钟

# 设置调度方式 默认使用优先队列
# SCHEDULER_QUEUE_CLASS='scrapy_redis.queue.PriorityQueue'
# SCHEDULER_QUEUE_CLASS='scrapy_redis.queue.FifoQueue'
# SCHEDULER_QUEUE_CLASS='scrapy_redis.queue.LifoQueue'

# 修改调度器,使用布隆过滤器调度器
# SCHEDULER = 'scrapy_redis_bloomfilter.scheduler.Scheduler'
# 使用布隆过滤器
# DUPEFILTER_CLASS = 'scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter'
# 设置散列函数个数,默认为6
# BLOOMFILTER_HASH_NUMBER = 6
# 设置bit参数，默认为30，占用128M空间，去重级别1亿
# BLOOMFILTER_BIT = 30
