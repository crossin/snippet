import requests
import pymongo
import time
from bs4 import BeautifulSoup
import random

client = pymongo.MongoClient()
db = client.chinamovies
collections = db.movies
collections_detail = db.moviesdetail
col_casts = db.casts
col_directors = db.directors
# db.drop_collection('casts')


# 新建一个影人条目的数据表
def createcelebrity():
    movie_id = {}
    movie_name = {}
    movie_cele = {}
    for i in collections_detail.find({'boxoffice': {'$exists': True}}):
        print(i['title'])
        for j in i['actors']:
            if j['id']:
                print(j)
                print(type(j['id']), j['name'])
                movie_id.setdefault(j['id'], []).append(i['id'])
                movie_name.setdefault(j['id'], []).append(i['title'])
                movie_cele[j['id']] = j['name']

    for k in movie_id:
        print(k, movie_id[k])
        col_casts.update_one({'id': k}, {'$set': {'movie_id': movie_id[k], 'movie': movie_name[k], 'name': movie_cele[k]}}, upsert=True)
        print('新建一个影人条目')


# 计算每个影人2018年参演电影的票房总和
def cal_boxoffice():
    for i in col_casts.find():
        total_box = 0
        for j in i['movie_id']:
            movie = collections_detail.find_one({'id': j})
            print(movie['title'], movie['boxoffice'])
            if movie['boxoffice']:
                total_box += int(movie['boxoffice'])
        print('total_box:', total_box)
        col_casts.update_one({'_id': i['_id']}, {'$set': {'total_box': total_box}}, upsert=True)


# 新建一个导演条目的数据表
def createdirector():
    movie_id = {}
    movie_name = {}
    movie_cele = {}
    for i in collections_detail.find({'boxoffice': {'$exists': True}}):
        print(i['title'])
        for j in i['directors']:
            if j['id']:
                print(j)
                print(type(j['id']), j['name'])
                movie_id.setdefault(j['id'], []).append(i['id'])
                movie_name.setdefault(j['id'], []).append(i['title'])
                movie_cele[j['id']] = j['name']

    for k in movie_id:
        print(k, movie_id[k])
        col_directors.update_one({'id': k}, {'$set': {'movie_id': movie_id[k], 'movie': movie_name[k], 'name': movie_cele[k]}}, upsert=True)
        print('新建一个导演条目')


# 计算每个导演2018年导演电影的票房总和
def cal_dir_boxoffice():
    for i in col_directors.find():
        total_box = 0
        for j in i['movie_id']:
            movie = collections_detail.find_one({'id': j})
            print(movie['title'], movie['boxoffice'])
            if movie['boxoffice']:
                total_box += int(movie['boxoffice'])
        print('total_box:', total_box)
        col_directors.update_one({'_id': i['_id']}, {'$set': {'total_box': total_box}}, upsert=True)


# createcelebrity()
# cal_boxoffice()
# createdirector()
# cal_dir_boxoffice()

# # 对影人参演电影票房总和排了个序
# for i in col_casts.find().sort('total_box',1):
#     print(i)
