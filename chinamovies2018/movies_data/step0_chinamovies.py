import requests
import pymongo
import time
from bs4 import BeautifulSoup
import random
import csv


# 获取中国票房网各个国家的代号，用于之后得到各个国家2018年在中国上映的电影
def get_area():
    urlmovie = 'http://www.cbooo.cn/movies'
    req = requests.get(urlmovie, headers=headers)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    arealist = soup.find("select",id="selArea")
    # print(arealist)
    arealist = arealist.find_all("option")
    area_dic = {}
    # area_dic = []
    for i in arealist:
        # area_dic.append(i["value"])
        area_dic[i.get_text()] = i["value"]

    print(area_dic)

    # 将代号保存到 arealist.csv 中
    with open('arealist.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for key, val in area_dic.items():
            print(repr(key), ':', repr(val))
            writer.writerow([key, val])


# 获取中国票房网中一个国家的电影及电影票房数据并保存到 mongodb 中
def get_data(area):
    client = pymongo.MongoClient()
    db = client.chinamovies # 获取或新建名为 chinamovies 的 database
    collections = db.movies # 获取或者新建了一个表

    url_origin = 'http://www.cbooo.cn/Mdata/getMdata_movie?area={area}&type=0&year=2018&initial=%E5%85%A8%E9%83%A8&pIndex={page}'
    page = 1

    while True:
        url = url_origin.format(area=area[1], page=page)
        try:
            req = requests.get(url, headers=headers)
            data = req.json()
        except Exception as e:
            print(e)
            page += 1
            error_url.append(url)
            continue

        if data['tCount'] == 0:
            break
        time.sleep(2)
        print(url)
        collections.insert_many(data['pData'])
        page += 1
        if page > data['tPage']:
            print('page:',page)
            print("data['tPage']:",data['tPage'])
            print('area:',area)
            print('==========================================================================')
            break


# 获取中国票房网所有电影及票房
def get_cbooomovies():
    areadata = []
    with open('arealist.csv', 'r', encoding='utf-8') as areafile: # 打开 arealist.csv，把国家代号写入 areadata
        reader = csv.reader(areafile)
        for item in reader:
            areadata.append(item)

    print(areadata)

    for area in areadata: # 对于每一个国家，调用函数 get_data 获得电影票房数据
        print(area)
        get_data(area)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Host': 'www.cbooo.cn',
    'Referer': 'http://www.cbooo.cn/movies',
}

error_url = [] # 把所有没有成功获取电影数据的链接都放在这里

# get_area() # step 0_0，获得地区代号

# get_cbooomovies() # step 0_1，获取中国票房网所有电影及票房

print(error_url) # 输出不成功的操作，可自行对没有成功获取的数据再重新抓取一遍
