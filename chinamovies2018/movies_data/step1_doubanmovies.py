import pymongo
import requests
from bs4 import BeautifulSoup
import time
import re
import random


# 进入豆瓣每一部电影的页面，通过其上映日期和名称判断是否是所要的电影
def douban_detail(url_detail):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    req = requests.get(url_detail,headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')

    releasedate = soup.find("div",id="info").find("span",property="v:initialReleaseDate",content=re.compile("2018.*(中国大陆)"))
    name = soup.find("div", id="content").h1.find("span", property=True).string
    time.sleep(1.5+random.random())

    # 电影上映时间必须要为 2018 年，中国大陆上映，如果满足条件，返回TRUE，不然没有返回信息
    if releasedate:
        print(name, ': ', releasedate.string)
        return True
    print(name, ': 没有信息')


# 从豆瓣api中搜索输入的电影名称，通过 douban_detail 函数判断是否符合条件
def douban_api(moviename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Host': 'api.douban.com',
    }
    url_api = 'https://api.douban.com/v2/movie/search?q={}'.format(moviename)
    print(url_api)
    req = requests.get(url_api, headers=headers)

    # search 以后可能会有很多结果，data_total 为通过影片名搜索到的所有相关电影
    data_total = req.json()['subjects']
    time.sleep(4+random.random())
    # print(data_total)
    if not data_total:
        print('你搜索的不存在：', moviename)
        return

    # 对于搜索结果依次进行判断，先判断影片名是否完全一致，接着通过 douban_detail 函数判断上映年份和国家是否一致
    for data in data_total:
        if data['title'] != moviename:
            print(data['title'], ': 没有信息')
        else:
            url_detail = data['alt']
            if douban_detail(url_detail):
                print('搜索到结果:', moviename)
                return data
    print('搜索结果中没有符合的条件：', moviename)


# 根据中国票房网得到的电影数据，从豆瓣 api 接口中获得更详细的数据并存入数据库
def douban_movies(movie_now):
    client = pymongo.MongoClient()
    db = client.chinamovies
    collections = db.movies
    collections_detail = db.moviesdetail # 豆瓣数据都放入了moviesdetail中
    # db.drop_collection('movies')

    for count, i in enumerate(collections.find()[movie_now:]):

        # 由于电影较多，随时可能因为异常而中断，因此，用 movieid.txt 记录已经保存仅数据库的豆瓣电影id，防止重复保存数据
        # 如果重新运行程序，可删除 movieid.txt 中的所有数据
        with open('movieid.txt', 'r') as f:
            movieid = f.read().split()

        print(count) # 计数，看目前是第几部电影了
        print(i['MovieName'])
        moviename = i['MovieName']
        datadetail = douban_api(moviename) # 通过douban api，获取电影详细信息
        # print(datadetail)

        # 如果存在这部电影数据，写入数据库
        if datadetail:
            # 如果这个电影还没有被写入数据库，那么就写入
            if str(datadetail['id']) not in movieid:
                movieid.append(datadetail['id'])
                print('已存数据库：', datadetail['id'], datadetail['title'])
                collections_detail.insert_one(datadetail)

                # 写入完成后在 movieid.txt 新增一个 id 数据
                with open('movieid.txt', 'a') as f2:
                    f2.write(' '+datadetail['id'])
            else:
                print('该电影已存在，id：', datadetail['id'], datadetail['title'])

        # 如果没有抓取到这部电影的数据，就把电影名保存进 notexistmovie.txt，之后处理
        else:
            with open('notexistmovie.txt', 'a', encoding='utf-8') as f3:
                f3.write(' '+i['MovieName'])
        print('========================================')


# 考虑到抓取过程可能中断，因此 douban_movies 函数中增加了一个参数
# 参数刚开始时是0，后面可以根据已经抓取的电影数量修改参数，便于从抓取被打断的地方重新开始
# douban_movies(0)