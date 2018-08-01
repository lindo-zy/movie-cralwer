# -*- coding: utf-8 -*-
# MongoDB处理工具
from pymongo import MongoClient
import re


# client_win = MongoClient('mongodb://120.76.172.204:27017')
# db_win = client_win['movie']
# coll_win = db_win['movie4_web']
# result=coll_win.find().limit(3)
# 修改电影国家为空的值，list类型
# coll_win.update_many({'movie_area':[]},{"$set":{'movie_area':['无']}})
# 修改电影年份能为空的值，list类型
# coll_win.update_many({'movie_year':[]},{"$set":{'movie_year':['无']}})
# if coll_win.find({'movie_area':[]}).count()==0 and coll_win.find({'movie_year':[]}).count()==0:
#     print("更新成功")

# 1.年份必须以数字开头和结尾，长度为4 2.不满足就更新为无


# 以函数的形式调用
def delete_one(collection):
    # client_ali = MongoClient('mongodb://120.76.172.204:27017')
    # db_ali = client_ali['movie']
    # coll_ali = db_ali['movie4_web']
    try:
        collection.delete_one({"movie_name": "用百度网盘在线观看本站电影"})
        print("无效记录,清理成功")
    except Exception as e:
        print(e)


def clean_movie_year(collection):
    # client_ali = MongoClient('mongodb://120.76.172.204:27017')
    # db_ali = client_ali['movie']
    # coll_ali = db_ali['movie4_web']
    # collection=coll_ali
    result = collection.find()
    count = 0
    for i in result:
        count += 1
        # print(i["movie_year"])
        temp = str(i["movie_year"][0])
        # print(str,type(temp))
        temp = re.findall(r'\d+', temp)
        if len(temp) > 0:
            data = temp[0]
            # print(temp[0])
        else:
            data = '无'
        if len(data) != 4:
            data = '无'
        # print(data,"---",count)
        print(i["movie_name"], "--年份:", data, type(data), [data])
        try:
            collection.update_many({'movie_name': i["movie_name"]}, {"$set": {'movie_year': [data]}})
        except Exception as e:
            print(e)
    print("电影年份数据清理成功！")


def clean_movie_area(collection):
    # result = collection.find()
    try:
        collection.update_many({'movie_area': []}, {"$set": {'movie_area': ["无"]}})
    except Exception as e:
        print(e)
    print("电影国家清理完成！")


def clean_movie_class(collection):
    try:
        collection.update_many({'movie_class': []}, {"$set": {'movie_class': ["无"]}})
    except Exception as e:
        print(e)
    print("电影类别清理完成！")


def clean_DouBan_score(collection):
    # client_ali = MongoClient('mongodb://120.76.172.204:27017')
    # db_ali = client_ali['movie']
    # coll_ali = db_ali['movie4_web']
    # collection=coll_ali
    result = collection.find()
    count = 0
    for i in result:
        count += 1
        # print(i["DouBan_score"])
        temp = i["DouBan_score"]
        # print(temp,type(temp))
        if isinstance(temp, list):
            # print(temp,type(temp))
            douban_str = re.findall(r'\d.\d', str(temp))
            # print(douban_str,len(douban_str),count)
        else:
            douban_str = "0"
        if len(douban_str) >= 1:
            douban_str = str(douban_str[0])
        else:
            douban_str = "0"
        print(douban_str, count)
        try:
            collection.update_many({'movie_name': i["movie_name"]}, {"$set": {'DouBan_score': [douban_str]}})
        except Exception as e:
            print(e)
    print("电影豆瓣评分清理完成!")


def clean_IMDB_score(collection):
    # client_ali = MongoClient('mongodb://120.76.172.204:27017')
    # db_ali = client_ali['movie']
    # coll_ali = db_ali['movie4_web']
    # collection=coll_ali
    result = collection.find()
    count = 0
    for i in result:
        count += 1
        # print(i["DouBan_score"])
        temp = i["IMDb_score"]
        # print(temp,type(temp))
        if isinstance(temp, list):
            # print(temp,type(temp))
            douban_str = re.findall(r'\d.\d', str(temp))
            # print(douban_str,len(douban_str),count)
        else:
            douban_str = "0"
        if len(douban_str) >= 1:
            douban_str = str(douban_str[0])
        else:
            douban_str = "0"
        print(douban_str, count)
        try:
            collection.update_many({'movie_name': i["movie_name"]}, {"$set": {'IMDb_score': [douban_str]}})
        except Exception as e:
            print(e)
    print("电影IMDB评分清理完成!")


def all_clean(collection):
    clean_movie_year(collection)
    delete_one(collection)
    clean_movie_area(collection)
    clean_DouBan_score(collection)
    clean_IMDB_score(collection)
    print("全部清理完成")


if __name__ == '__main__':
    # 设置链接
    # 本地mongodb
    client_win = MongoClient('mongodb://localhost:27017')
    # 连接的数据库
    db_win = client_win['movie']
    # 连接的数据集
    coll_win = db_win['movie4_web']

    # 腾讯云mongodb
    client_tencent = MongoClient('mongodb://root:123456@118.24.83.187:27017')
    db_tencent = client_tencent['movie']
    coll_tencent = db_tencent['movie4_web']

    # 阿里云mongodb
    client_ali = MongoClient('mongodb://120.76.172.204:27017')
    db_ali = client_ali['movie']
    coll_ali = db_ali['movie4_web']

    # clean_movie_year(coll_ali)
    # delete_one(coll_ali)
    # clean_movie_area(coll_ali)
    # clean_DouBan_score(coll_ali)
    # clean_IMDB_score(coll_ali)
