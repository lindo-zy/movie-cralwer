# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item


class UrlItem(Item):  # 存在redis调度
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = Field()
    link_text = Field()
    # time=Field()


class ContentItem(Item):  # 存在MongoDB
    movie_name = Field()
    movie_image = Field()
    movie_year = Field()
    movie_area = Field()
    movie_class = Field()
    IMDb_score = Field()
    DouBan_score = Field()
    # movie_downlink = Field()
    movie_rate = Field()
    movie_url = Field()


class MoiveItem(Item):  # 存在本地
    movie = Field()  # 文件夹名字
    movie_image = Field()  # 封面
    magnet_link = Field()
    ed2k_link = Field()
    ftp_link = Field()
    torrent_link = Field()
