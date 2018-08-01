# -*- coding: utf-8 -*-
import os
import random
import re
import socket

import requests
from scrapy import Request
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import UrlItem, ContentItem, MoiveItem
from bs4 import BeautifulSoup
from ..settings import IMAGES_STORE
import smtplib
from email.mime.text import MIMEText
from ..settings import EMAIL_ENABLE, EMAIL_SETTING


class MoviespiderSpider(CrawlSpider):
    name = 'MovieSpider'
    allowed_domains = ['www.hao6v.com']
    start_urls = ['http://www.hao6v.com/']

    # 挖掘符合规则的全部url
    print('---开始解析---')
    rules = (
        Rule(LinkExtractor(allow=('http://www.hao6v.com/(.*)',), deny=('http://www.hao6v.com/yx/(.*)')),
             callback='parse_urlItem', follow=True),)

    # 解析函数 ,response是 rules挖掘的url
    def parse_urlItem(self, response, last=[0]):
        print(response.url)  # 挖掘出来的不重复的url
        # 计数
        global count
        count = last[0] + 1
        last[0] = count
        print("运行次数:", count)
        urlItem = UrlItem()
        contentItem = ContentItem()
        movieItem = MoiveItem()
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            for i in soup.find_all('div', id='endText'):
                movie_name = i.find('a').get_text()
                print('电影名称：', movie_name, type(movie_name))
                movie_image = i.find('img')['src']  # 只是一个url
                print('电影封面：', movie_image, type(movie_image))
                flag = str(i.find_all('p')).replace('\u3000', '').replace('\xa0 ', '').replace('◎', '')
                # print(str(i.find_all('p')).replace('\u3000', '').replace('\xa0 ', '').replace('◎', ''))

                DouBan_score = re.findall(r'(?<=豆瓣评分)[^/]+', flag)[0:3]
                if DouBan_score:
                    print('豆瓣评分', DouBan_score, type(DouBan_score))
                else:
                    DouBan_score = '0'
                    print('豆瓣评分', DouBan_score, type(DouBan_score))
                IMDb_score = re.findall(r'(?<=IMD[bB]评分)[^/]+', flag)[0:3]
                if IMDb_score:
                    print('IMDb评分', IMDb_score, type(IMDb_score))
                else:
                    IMDb_score = '0'
                    print('IMDb评分', IMDb_score, type(IMDb_score))

                movie_year = re.findall(r'年代(.*)\<', flag)[0:4]
                if movie_year:
                    print('年代', movie_year, type(movie_year))
                else:
                    movie_year = '无'

                movie_area = re.findall('产地.*?\>(.*?)\<', flag)
                if movie_area:
                    print('产地', movie_area, type(movie_area))
                else:
                    movie_area = re.findall('产地(.*)\<', flag)
                    print('产地', movie_area, type(movie_area))

                movie_class = re.findall(r'类别<a.*?>(.*?)</a>', flag)
                if movie_class:
                    print('类别', movie_class, type(movie_class))
                else:
                    movie_class = '无'
                    print('类别', movie_class, type(movie_class))

                magnet_dl = []
                ed2k_dl = []
                ftp_dl = []
                torrent_dl = []
                for l in i.find_all('tbody'):
                    for o in l.find_all('a'):
                        magnet_link = re.findall(r'magnet.*', str(o['href']))
                        ed2k_link = re.findall(r'ed2k.*', str(o['href']))
                        ftp_link = re.findall(r'ftp.*', str(o['href']))
                        torrent_link = re.findall(r'.*torrent', str(o['href']))
                        # baidu_flag = re.findall(r'https://pan.baidu.com/s.*', str(o['href']))
                        if len(magnet_link) != 0:
                            # magnet_dl = magnet_link
                            magnet_dl = magnet_link
                            # print('magnet下载:', magnet_link, type(magnet_link))
                        if len(ed2k_link) != 0:
                            ed2k_dl = ed2k_link
                            # print('ed2k下载:', ed2k_link, type(ed2k_link))
                        if len(ftp_link) != 0:
                            ftp_dl = ftp_link
                        if len(torrent_link) != 0:
                            torrent_dl = torrent_link
                print('magnet下载:', magnet_dl, type(magnet_link))
                print('ed2k下载:', ed2k_dl, type(ed2k_link))
                print('ftp下载:', ftp_dl, type(ftp_link))
                print('torrent下载', torrent_dl, type(torrent_link))
                if self.isMovie(movie_image, movie_year, movie_class) == 1:
                    comment_link = 'http://www.hao6v.com' + soup.find('iframe').get('src')

                    # comment_html = requests.get(comment_link)
                    # comment_html.encoding = comment_html.apparent_encoding
                    # comment_soup = BeautifulSoup(comment_html.text, 'lxml')
                    # movie_rate = comment_soup.find('span', id='fennum').get_text()
                    # print('评论人数:', movie_rate)
                    # yield Request(comment_link, callback=self.parse_commet)
                    contentItem['movie_name'] = movie_name
                    contentItem['movie_year'] = movie_year
                    contentItem['movie_area'] = movie_area
                    contentItem['movie_class'] = movie_class
                    contentItem['IMDb_score'] = IMDb_score
                    contentItem['DouBan_score'] = DouBan_score
                    contentItem['movie_image'] = movie_image
                    # contentItem['movie_rate'] =
                    contentItem['movie_url'] = response.url
                    yield Request(comment_link, meta={'contentItem': contentItem}, callback=self.parse_commet)
                    # # print('-------', response.url)
                    # # contentItem = response.meta['contentItem']
                    # comment_soup = BeautifulSoup(comment_link, 'lxml')
                    # movie_rate = comment_soup.find('span', id='fennum').get_text()
                    # if movie_rate != '':
                    #     contentItem['movie_rate'] = movie_rate
                    #     print('评论人数:', movie_rate)
                    # else:
                    #     contentItem['movie_rate'] = '0'
                    # yield contentItem

                    movieItem['movie'] = movie_name
                    movieItem['movie_image'] = movie_image
                    movieItem['magnet_link'] = magnet_dl
                    movieItem['ed2k_link'] = ed2k_dl
                    movieItem['ftp_link'] = ftp_dl
                    movieItem['torrent_link'] = torrent_dl
                    # yield movieItem

                    # 调用本地存储
                    self.local_store(movie_name, movie_image, magnet_dl, ed2k_dl, ftp_dl, torrent_dl)

                    urlItem['link'] = response.url
                    urlItem['link_text'] = movie_name
                    # yield urlItem



        except Exception as e:
            print('错误信息:', e)

    def local_store(self, movie_name, movie_image, magnet_dl, ed2k_dl, ftp_dl, torrent_dl):
        user_agent_list = [ \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        try:
            fold_name = str(movie_name)
            ua = random.choice(user_agent_list)
            header = {'User-Agent': ua}
            dir_path = IMAGES_STORE
            if os.path.exists(dir_path + fold_name.strip().replace('/', '.').replace(':', '.')):
                print('目录已存在')
            else:
                os.mkdir(dir_path + fold_name.strip().replace('/', '.').replace(':', '.'))
                os.chdir(dir_path + fold_name.strip().replace('/', '.').replace(':', '.'))
                img = requests.get(str(movie_image).replace('https', 'http'), header, timeout=5)
                f = open(fold_name.strip().replace('/', '.').replace(':', '.') + '.jpg', 'ab')
                f.write(img.content)
                t = open('下载地址' + '.txt', 'w')
                down_link = magnet_dl + ed2k_dl + ftp_dl + torrent_dl
                t.writelines(down_link)
                t.flush()
                t.close()
                f.close()
                print('-------------------------------------------')
                print('下载成功!!')
        except Exception as e:
            print(e)

    # 解析评论
    def parse_commet(self, response):
        print('-------', response.url)
        contentItem = response.meta['contentItem']
        comment_soup = BeautifulSoup(response.text, 'lxml')
        movie_rate = comment_soup.find('span', id='fennum').get_text()
        if movie_rate != '':
            contentItem['movie_rate'] = movie_rate
            print('评论人数:', movie_rate)
        else:
            contentItem['movie_rate'] = '0'
        yield contentItem

    # 判断是不是电影
    def isMovie(self, movie_image, movie_year, movie_class):
        try:
            movie_image_flag = 0
            movie_year_flag = 0
            movie_class_flag = 0
            movie_flag = 0
            if len(movie_image) > 0:
                movie_image_flag = 1
            if len(movie_year) > 0:
                movie_year_flag = 1
            if len(movie_class) > 0:
                movie_class_flag = 1
            if (movie_image_flag + movie_year_flag + movie_class_flag) == 3:
                movie_flag = 1
                print('是电影', movie_flag)
            else:
                print('不是电影', movie_flag)  # 丢弃
        except Exception as e:
            print(e)
        return movie_flag

    def sendEmali(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        if EMAIL_ENABLE:
            # 第三方 SMTP 服务
            mail_host = EMAIL_SETTING["mail_host"]  # SMTP服务器
            mail_user = EMAIL_SETTING["mail_user"]  # 用户名
            mail_pass = EMAIL_SETTING["mail_pass"]  # 授权密码，非登录密码
            sender = EMAIL_SETTING["sender"]  # 发件人邮箱
            receivers = EMAIL_SETTING["receivers"]  # 接收邮件
            content = EMAIL_SETTING["content"] + ip  # 邮件内容
            title = EMAIL_SETTING["title"]  # 邮件主题

            message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
            message['From'] = "{}".format(sender)
            message['To'] = receivers
            message['Subject'] = title

            try:
                smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口是465
                smtpObj.login(mail_user, mail_pass)  # 登录验证
                smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
                print("通知邮件成功发送")
            # 获取邮件异常信息
            except smtplib.SMTPException as e:
                print(e)

    def close(self, spider, reason):  # 爬虫结束发送邮件
        self.sendEmali()
        # pass
