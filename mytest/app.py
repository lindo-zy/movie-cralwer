# coding=utf-8
import re

from flask import Flask, url_for, render_template, abort, redirect, request, jsonify, g
from mytest import config
# from flask_pymongo import PyMongo
from pymongo import MongoClient, ReadPreference
import pymongo
# 初始化一个flask对象
from mytest.config import MongoDB

app = Flask(__name__)

# 设置配置文件
app.config.from_object(config)
# 本地mongodb
client_win = MongoClient('mongodb://localhost:27017')
db_win = client_win['movie']
coll_win = db_win['movie4']
# 腾讯云mongodb
client_tencent = MongoClient('mongodb://root:123456@118.24.83.187:27017')
db_tencent = client_tencent['movie']
coll_tencent = db_tencent['movie4']
# 阿里云mongodb
client_ali = MongoClient('mongodb://120.76.172.204:27017')
db_ali = client_ali['movie']
coll_ali = db_ali['movie4']


# 路由
@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        tencent_collstats = db_tencent.command('collstats', 'movie4')
        tencent_count = tencent_collstats["count"]

        win_collstats = db_win.command('collstats', 'movie4')
        win_count = win_collstats["count"]

        ali_collstats = db_ali.command('collstats', 'movie4')
        ali_count = ali_collstats["count"]
        all_count = tencent_count + int(win_count) + int(ali_count)

        tencent_rate = '%.2f' % (tencent_count / all_count * 100)
        win_rate = '%.2f' % (win_count / all_count * 100)
        ali_rate = '%.2f' % (ali_count / all_count * 100)
        print("腾讯云记录数：", tencent_count, tencent_count, '占比:', tencent_rate)
        print("本地记录数：", win_count, '占比:', win_rate)
        print("阿里云记录数：", ali_count, '占比:', ali_rate)
        print('记录总数：', all_count)
        tencent_results = coll_tencent.find({}).limit(5)
        win_results = coll_win.find({}).limit(5)
        ali_results = coll_ali.find({}).limit(5)
        # for i in win_results:
        #     print(i)
        return render_template('index.html', **locals())
    except Exception as e:
        print('错误信息：', e)
        return '错误信息为:', e, '\n请刷新重试'


@app.route('/tables/', methods=['GET', 'POST'])
def tables():
    try:
        tencent_results = coll_tencent.find({}).limit(5)
        win_results = coll_win.find({}).limit(5)
        ali_results = coll_ali.find({}).limit(5)

        tencent_collstats = db_tencent.command('collstats', 'movie4')
        tencent_count = tencent_collstats["count"]

        win_collstats = db_win.command('collstats', 'movie4')
        win_count = win_collstats["count"]

        ali_collstats = db_ali.command('collstats', 'movie4')
        ali_count = ali_collstats["count"]

        all_count = tencent_count + int(win_count) + int(ali_count)
        return render_template('tables.html', **locals())
    except Exception as e:
        print(e)


@app.route('/data/', methods=['GET', 'POST'])
def data():
    tencent_results = coll_tencent.find({}).limit(5)
    win_results = coll_win.find({}).limit(5)
    ali_results = coll_ali.find({}).limit(5)

    tencent_collstats = db_tencent.command('collstats', 'movie4')
    tencent_count = tencent_collstats["count"]

    win_collstats = db_win.command('collstats', 'movie4')
    win_count = win_collstats["count"]

    ali_collstats = db_ali.command('collstats', 'movie4')
    ali_count = ali_collstats["count"]

    all_count = tencent_count + int(win_count) + int(ali_count)
    return render_template('data.html', **locals())


@app.route('/getAliPage/', methods=['POST', 'GET'])
def ali_get_page():
    pagenum = request.form.get('pagenum')
    print(pagenum)
    tencent_results = coll_tencent.find({}).limit(5)
    win_results = coll_win.find({}).limit(5)
    ali_results = coll_ali.find({}).limit(int(pagenum)).skip(int(pagenum) - 5)

    movie_name = []
    movie_year = []
    movie_class = []
    movie_area = []
    douban_score = []
    imdb_score = []
    movie_rate = []
    for i in ali_results:
        # print(i["movie_name"])
        movie_name.append(i["movie_name"])
        movie_year.extend(i["movie_year"])
        movie_class.append(i["movie_class"])
        movie_area.extend(i["movie_area"])
        douban_score.append(i["DouBan_score"])
        imdb_score.append(i["IMDb_score"])
        movie_rate.append(i["movie_rate"])
    # context={'movie_name':i["movie_name"]}
    # print(movie_name)
    # return 'ok'
    # print(jsonify(movie_name,movie_year,movie_class,movie_area,douban_score,imdb_score,movie_rate))
    return jsonify(movie_name, movie_year, movie_area, movie_class, douban_score, imdb_score, movie_rate)


@app.route('/getTencetPage/', methods=['POST', 'GET'])
def tencent_get_page():
    pagenum = request.form.get('pagenum')
    print(pagenum)
    tencent_results = coll_ali.find({}).limit(int(pagenum)).skip(int(pagenum) - 5)
    movie_name = []
    movie_year = []
    movie_class = []
    movie_area = []
    douban_score = []
    imdb_score = []
    movie_rate = []
    for i in tencent_results:
        # print(i["movie_name"])
        movie_name.append(i["movie_name"])
        movie_year.extend(i["movie_year"])
        movie_class.append(i["movie_class"])
        movie_area.extend(i["movie_area"])
        douban_score.append(i["DouBan_score"])
        imdb_score.append(i["IMDb_score"])
        movie_rate.append(i["movie_rate"])
    # context={'movie_name':i["movie_name"]}
    # print(movie_name)
    # return 'ok'
    # print(jsonify(movie_name,movie_year,movie_class,movie_area,douban_score,imdb_score,movie_rate))
    return jsonify(movie_name, movie_year, movie_area, movie_class, douban_score, imdb_score, movie_rate)


@app.route('/getWinPage/', methods=['POST', 'GET'])
def win_get_page():
    pagenum = request.form.get('pagenum')
    print(pagenum)
    win_results = coll_ali.find({}).limit(int(pagenum)).skip(int(pagenum) - 5)

    movie_name = []
    movie_year = []
    movie_class = []
    movie_area = []
    douban_score = []
    imdb_score = []
    movie_rate = []
    for i in win_results:
        # print(i["movie_name"])
        movie_name.append(i["movie_name"])
        movie_year.extend(i["movie_year"])
        movie_class.append(i["movie_class"])
        movie_area.extend(i["movie_area"])
        douban_score.append(i["DouBan_score"])
        imdb_score.append(i["IMDb_score"])
        movie_rate.append(i["movie_rate"])
    # context={'movie_name':i["movie_name"]}
    # print(movie_name)
    # return 'ok'
    # print(jsonify(movie_name,movie_year,movie_class,movie_area,douban_score,imdb_score,movie_rate))
    return jsonify(movie_name, movie_year, movie_area, movie_class, douban_score, imdb_score, movie_rate)


@app.route('/deleteOne/', methods=['POST', 'GET'])
def delete_one():
    id = request.form.get('id')
    print(id)
    if id == '1':
        hostname = "腾讯云(Master)"
        coll_tencent.delete_one({"movie_name": "用百度网盘在线观看本站电影"})
        return jsonify({'result': 'ok'})

    if id == '2':
        hostname = "本地(Slave1)"
        coll_win.delete_one({"movie_name": "用百度网盘在线观看本站电影"})
        return jsonify({'result': 'ok'})

    if id == '3':
        hostname = "阿里云(Slave2)"
        coll_ali.delete_one({"movie_name": "用百度网盘在线观看本站电影"})
        return jsonify({'result': 'ok'})


@app.route('/cleanMovieYear/', methods=['POST', 'GET'])
def clean_movie_year():
    id = request.form.get('id')
    print(id)
    if id == '1':
        collection = coll_tencent
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
        return jsonify({'result': 'ok'})

    if id == '2':
        collection = coll_win
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
        return jsonify({'result': 'ok'})

    if id == '3':
        collection = coll_ali
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
        return jsonify({'result': 'ok'})


@app.route('/cleanMovieArea/', methods=['POST', 'GET'])
def clean_movie_area():
    id = request.form.get('id')
    print(id)
    if id == '1':
        collection = coll_tencent
        collection.update_many({'movie_area': []}, {"$set": {'movie_area': ["无"]}})
        print("电影国家清理完成！")
        return jsonify({'result': 'ok'})
    if id == '2':
        collection = coll_win
        collection.update_many({'movie_area': []}, {"$set": {'movie_area': ["无"]}})
        print("电影国家清理完成！")
        return jsonify({'result': 'ok'})
    if id == '3':
        collection = coll_ali
        collection.update_many({'movie_area': []}, {"$set": {'movie_area': ["无"]}})
        print("电影国家清理完成！")
        return jsonify({'result': 'ok'})


@app.route('/cleanMovieClass/', methods=['GET', 'POST'])
def clean_movie_class():
    id = request.form.get('id')
    print(id)
    if id == '1':
        collection = coll_tencent
        collection.update_many({'movie_class': []}, {"$set": {'movie_class': ["无"]}})
        print("电影分类清理完成！")
        return jsonify({'result': 'ok'})
    if id == '2':
        collection = coll_win
        collection.update_many({'movie_class': []}, {"$set": {'movie_class': ["无"]}})
        print("电影分类清理完成！")
        return jsonify({'result': 'ok'})
    if id == '3':
        collection = coll_ali
        collection.update_many({'movie_class': []}, {"$set": {'movie_class': ["无"]}})
        print("电影分类清理完成！")
        return jsonify({'result': 'ok'})


@app.route('/cleanDouBanScore/', methods=['GET', 'POST'])
def clean_douban_socre():
    id = request.form.get('id')
    print(id)
    if id == '1':
        collection = coll_tencent
    if id == '2':
        collection = coll_win
    if id == '3':
        collection = coll_ali
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
    return jsonify({'result': 'ok'})


@app.route('/cleanImdbScore/', methods=['GET', 'POST'])
def clean_imdb_socre():
    id = request.form.get('id')
    print(id)
    if id == '1':
        collection = coll_tencent
    if id == '2':
        collection = coll_win
    if id == '3':
        collection = coll_ali
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
    return jsonify({'result': 'ok'})


@app.route('/allClean/', methods=['POST', 'GET'])
def all_clean():
    id = request.form.get('id')
    print(id)
    if id == '1':
        collection = coll_tencent
    if id == '2':
        collection = coll_win
    if id == '3':
        collection = coll_ali

    collection.delete_one({"movie_name": "用百度网盘在线观看本站电影"})
    print("无效记录,清理成功")
    result = collection.find()
    for i in result:
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

        collection.update_many({'movie_name': i["movie_name"]}, {"$set": {'movie_year': [data]}})

    print("电影年份数据清理成功！")

    collection.update_many({'movie_area': []}, {"$set": {'movie_area': ["无"]}})
    print("电影国家清理完成！")

    collection.update_many({'movie_class': []}, {"$set": {'movie_class': ["无"]}})
    print("电影类别清理完成！")

    for j in result:

        # print(i["DouBan_score"])
        temp = j["DouBan_score"]
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

        collection.update_many({'movie_name': i["movie_name"]}, {"$set": {'DouBan_score': [douban_str]}})

    print("电影豆瓣评分清理完成!")

    for k in result:

        # print(i["DouBan_score"])
        temp = k["IMDb_score"]
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

        collection.update_many({'movie_name': i["movie_name"]}, {"$set": {'IMDb_score': [douban_str]}})

    print("电影IMDB评分清理完成!")
    print('全部清理完成')
    return jsonify({'result': 'ok'})


@app.route('/search/', methods=['GET', 'POST'])
def search():
    id = request.form.get('id')
    context = request.form.get('context')
    if id == '1':
        collection = coll_tencent
    if id == '2':
        collection = coll_win
    if id == '3':
        collection = coll_ali

    result = collection.find({'movie_name': {'$regex': context}})
    movie_name = []
    movie_year = []
    movie_class = []
    movie_area = []
    douban_score = []
    imdb_score = []
    movie_rate = []
    for i in result:
        # print(i["movie_name"])
        movie_name.append(i["movie_name"])
        movie_year.extend(i["movie_year"])
        movie_class.append(i["movie_class"])
        movie_area.extend(i["movie_area"])
        douban_score.append(i["DouBan_score"])
        imdb_score.append(i["IMDb_score"])
        movie_rate.append(i["movie_rate"])
    # context={'movie_name':i["movie_name"]}
    # print(movie_name)
    # return 'ok'
    # print(jsonify(movie_name,movie_year,movie_class,movie_area,douban_score,imdb_score,movie_rate))
    return jsonify(movie_name, movie_year, movie_area, movie_class, douban_score, imdb_score, movie_rate)


@app.route('/stats/', methods=['GET', 'POST'])
def stats():
    tencent_collstats = db_tencent.command('collstats', 'movie4')
    tencent_count = tencent_collstats["count"]

    win_collstats = db_win.command('collstats', 'movie4')
    win_count = win_collstats["count"]

    ali_collstats = db_ali.command('collstats', 'movie4')
    ali_count = ali_collstats["count"]
    all_count = tencent_count + int(win_count) + int(ali_count)

    win_rate_result = coll_win.find()
    # ali_rate_result = coll_ali.find().sort('movie_rate', pymongo.DESCENDING)
    # tencent_rate_result = coll_tencent.find().sort('movie_rate', pymongo.DESCENDING)

    win = []
    win2 = []
    ali = []
    tencent = []

    for i in win_rate_result:
        # print(i["movie_rate"],type(i["movie_rate"]))
        win.append(i["movie_rate"])
        win2.append(i["movie_class"])
        # win.append(i["movie_name"])

        # b = [int(i) for i in win]
        # b.sort(reverse=True)

        # movie_name.append(i["movie_name"])
        # movie_year.extend(i["movie_year"])
        # movie_class.append(i["movie_class"])
        # movie_area.extend(i["movie_area"])
        # douban_score.append(i["DouBan_score"])
        # imdb_score.append(i["IMDb_score"])
        # movie_rate.append(i["movie_rate"])
    # for j in ali_rate_result:
    #     print(j)
    #     ali.append(j["movie_rate"])
    # for k in tencent_rate_result:
    #     tencent.append(k["movie_rate"])

    win.sort(key=lambda x: len(x), reverse=True)
    b = [int(x) for x in win]
    b.sort(reverse=True)

    l = b[0:5]
    # print(b[0:10])
    result = []
    for j in b[0:5]:
        s = coll_win.find({"movie_rate": str(j)})
        for k in s:
            result.append(k["movie_name"])
    # print(result)

    s = []
    for x in win2:
        # print(x,type(x))
        if isinstance(x, list):
            s.append(x[0])
    dict_result = {}

    for item in set(s):
        dict_result.update({item: s.count(item)})
    print(dict_result)
    for key in dict_result.keys():
        print(key)
    # print(set(s))

    return render_template('stats.html', **locals())


if __name__ == '__main__':
    # 设置debug模式热更新
    app.run()
