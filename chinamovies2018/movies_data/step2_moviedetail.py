import requests
import pymongo
import time
from bs4 import BeautifulSoup
import random, re, json

# 通过豆瓣电影详细页面获得每部电影的所有演员
def find_actors():
    count = 0
    for i in collections_detail.find():
        print(count)
        url = i['alt']
        print(url)
        print('fetching')
        person = []
        try:
            req = requests.get(url, headers=headers)
        except Exception as e:
            print(e)
            break

        soup = BeautifulSoup(req.text, 'lxml')
        try:
            actors = soup.find("span", class_="actor").find("span", class_="attrs").find_all("a")
        except Exception as e:
            print(e)
            actors = []
            person = []
        for actor in actors:
            print('actor:', actor)
            name = actor.string
            actor_url = actor['href']
            actor_id = actor_url.split('/')[-2]
            total_url = 'https://movie.douban.com' + actor_url
            person.append({'name':name, 'id':actor_id, 'url':total_url})
        print('person:',person)

        # 更新数据表中数据，增加了演员相关数据
        collections_detail.update({'_id':i['_id']},{'$set':{'actors':person}})
        print('done',i['title'],i['_id'],'====================================')
        count += 1
        time.sleep(2+random.random())


# other_detail 的子函数，获得一部电影在豆瓣的评论人数、短评数，长评数等数据
def one_detail(i):
    url = i['alt']
    title = i['title']
    print('fetching:', title, url)

    try:
        req = requests.get(url, headers=headers)
    except Exception as e:
        print(e)
        return url
    soup = BeautifulSoup(req.text, 'lxml')

    country = soup.find("div", id="info").find(string=re.compile("制片国家/地区:")).parent.next_sibling.split('/')
    country = [i.strip() for i in country]

    error = None

    # 电影时长
    try:
        film_duration = soup.find("div", id="info").find("span", property="v:runtime")["content"]
    except Exception as e:
        print(e)
        film_duration = ''
        error = url

    # IMDB 链接
    try:
        IMDBurl = soup.find("div", id="info").find(string=re.compile("IMDb链接:")).parent.find_next_sibling("a")["href"]
    except Exception as e:
        print(e)
        IMDBurl = ''
        error = url

    # 上映日期
    try:
        releasedate = soup.find("div", id="info").find("span", property="v:initialReleaseDate", content=re.compile("2018.*(中国大陆.*)")).string
    except Exception as e:
        print(e)
        releasedate = ''
        error = url

    print('country:', country, 'film_duration:', film_duration, 'IMDBurl:', IMDBurl,'releasedate:', releasedate)

    # 豆瓣评分
    rate_score = soup.find("div", id="interest_sectl").find("strong", class_="ll rating_num").string

    # 评价人数
    rate_quantity = soup.find("div", id="interest_sectl").find("div", class_="rating_sum").find("a",class_="rating_people")
    if rate_quantity:
        rate_quantity = rate_quantity.span.string
    else:
        rate_quantity = '0'

    # 豆瓣短评数
    comments_num = soup.find("div", id="comments-section").find("div", class_="mod-hd").h2.span.a.string
    comments_num = re.findall(r'\d+', comments_num)[0]

    # 豆瓣长评数
    commentslong_num = soup.find("section", class_="reviews mod movie-content").header.h2.span.a.string
    commentslong_num = re.findall(r'\d+', commentslong_num)[0]

    print('rate_score:', rate_score, 'rate_quantity:', rate_quantity, 'comments_num:', comments_num, 'commentslong_num:', commentslong_num)

    # 更新相关数据到数据表
    collections_detail.update({'_id':i['_id']},{'$set':{
        'country': country, 'film_duration': film_duration,
        'IMDBurl': IMDBurl, 'releasedate': releasedate,
        'rate_score': rate_score, 'rate_quantity': rate_quantity,
        'comments_num': comments_num, 'commentslong_num': commentslong_num
    }})
    print('done', title, '====================================')
    return error


# 通过豆瓣电影详细页面获得每部电影的评论人数、短评数，长评数等数据
def other_detail():
    error_movie = []
    # 遍历数据库，更新豆瓣评分等数据
    for count, i in enumerate(collections_detail.find()):
        print(count)
        error_movie.append(one_detail(i)) # 有问题的电影会返回电影链接，可之后手动处理
        time.sleep(2 + random.random())
        print(error_movie)


# 获得猫眼网电影评分
def get_maoyan_score():
    not_found = []
    for count, i in enumerate(collections_detail.find()):
        print(count,'==================================')
        url = 'https://maoyan.com/ajax/suggest?kw=' + i['title']
        print('fetching:', i['title'])
        try:
            req = requests.get(url, headers=headers)
        except Exception as e:
            print(e)
            not_found.append(i['id'])
            continue
        data = req.json()
        found_it = False

        # type == 0 说明数据正常
        if data['type'] == 0:
            mlist = data['movies']['list']
            for movie in mlist:
                print('searching:', movie['nm'])

                # 必须要名称一致且2018年大陆上映才符合要求
                if movie['nm'] == i['title'] and re.findall(r'2018.*大陆上映', movie['pubDesc']):
                    print('found:', movie['nm'])
                    print({'猫眼':{
                        'title': movie['nm'], 'rank': movie['sc'],
                        'id': movie['id'], 'pubDesc': movie['pubDesc']
                    }})

                    # 更新数据到数据库中
                    collections_detail.update({'_id': i['_id']}, {'$set': {'猫眼':{
                        'title': movie['nm'], 'rank': movie['sc'],
                        'id': movie['id'], 'pubDesc': movie['pubDesc']
                    }}})
                    found_it = True
                    break
        if found_it is False:
            print('not found:', i['title'], '========================================')
            not_found.append(i['id'])
        time.sleep(3 + random.random())


# 获得imdb电影评分
def get_imdb_score():
    not_found = []
    for count, i in enumerate(collections_detail.find()):
        print(count,'==================================')
        if not i['IMDBurl']:
            continue
        url = i['IMDBurl']
        print('fetching:', i['title'])
        try:
            req = requests.get(url, headers=headers)
        except Exception as e:
            print(e)
            not_found.append(i['id'])
            continue
        data = req.text
        soup = BeautifulSoup(data, 'lxml')
        rating = soup.find("div",class_="imdbRating")
        if not rating:
            rate = '0'
            rate_num = '0'
        else:
            rate = rating.find("strong").span.string
            rate_num = rating.a.string

        rate_num = rate_num.replace(',','')
        imdbdata = {'imdb':{'title':i['title'],'rank':rate,'rate_quantity': rate_num}}
        print(imdbdata)
        collections_detail.update({'_id': i['_id']}, {'$set': imdbdata})
        time.sleep(3 + random.random())


# 获得时光网电影评分，时光网比较复杂一些
def get_mtime_score():
    not_found = []
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Host': 'service-channel.mtime.com',
        'Referer': 'http://www.mtime.com/',
    }
    for count, i in enumerate(collections_detail.find()):
        print(count,'==================================')
        url = 'http://service-channel.mtime.com/Search.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Channel.Services&Ajax_CallBackMethod=GetSuggestObjs&Ajax_CrossDomain=1&Ajax_RequestUrl=http%3A%2F%2Fwww.mtime.com%2F&t=1551417777107&Ajax_CallBackArgument0={}&Ajax_CallBackArgument1=627&Ajax_CallBackArgument2=0&_=1551417759329'.format(i['title'])
        print('fetching:', i['title'])
        try:
            req = requests.get(url, headers=headers2)
        except Exception as e:
            print(e)
            not_found.append(i['id'])
            continue
        print(req)

        # 通过电影名称搜索获取到一系列电影，里面只有一部是咱们想要的
        movielists = re.findall(r'= ({ "value":.*});var', req.text)[0]
        moviejson = json.loads(movielists)
        found_it = False

        # 如果没有值，说明没有找到
        if moviejson['value'] is None:
            not_found.append(i['id'])
            continue

        # 对得到的一系列电影进行逐个排查
        for movie in moviejson['value']['objs']:
            print('searching:', movie['titlecn'], movie['id'], movie['moviepage'])

            # 首要满足名称完全一致
            if movie['titlecn'] == i['title']:
                url_movie = r'http://m.mtime.cn/Service/callback.mi/movie/Detail.api?movieId={}&locationId=290&t=20193115171246368'.format(movie['id'])
                req_movie = requests.get(url_movie, headers=headers)
                print(req_movie)
                data = req_movie.json()
                print('data:', data)
                # input('aaaaa')
                try:
                    releasedate = data['release']['date']
                except Exception as e:
                    print(e)
                    continue

                # 接着要满足上映年份在2018年
                if re.findall(r'2018', releasedate):
                    print('found:', movie['titlecn'])
                    updateinf = {'时光': {
                        'title': movie['titlecn'], 'rank': data['rating'], 'rate_quantity': data['scoreCount'],
                        'id': movie['id'], 'pubDesc': data['release']['date']
                    }}
                    print(updateinf)
                    collections_detail.update({'_id': i['_id']}, {'$set': updateinf})
                    found_it = True
                    break
                time.sleep(1 + random.random())
        if found_it is False:
            print('not found:', i['title'], '========================================')
            not_found.append(i['id'])
            print(not_found)
        time.sleep(5 + random.random())
        # input('aaaaaa')


# 获得通过 get_mtime_score 没有找到的时光网电影评分，手工判断电影是否符合，通过一个输入来控制抓取到的电影是否符合要求，可以通过增加一个参数与 get_mtime_score 函数写在一起。。。
def get_mtime_score_not_found():
    not_found = []
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Host': 'service-channel.mtime.com',
        'Referer': 'http://www.mtime.com/',
    }
    for count, i in enumerate(collections_detail.find({'时光':{'$exists':False}})):
        print(count,'==================================')
        url = 'http://service-channel.mtime.com/Search.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Channel.Services&Ajax_CallBackMethod=GetSuggestObjs&Ajax_CrossDomain=1&Ajax_RequestUrl=http%3A%2F%2Fwww.mtime.com%2F&t=1551417777107&Ajax_CallBackArgument0={}&Ajax_CallBackArgument1=627&Ajax_CallBackArgument2=0&_=1551417759329'.format(i['title'])
        print('fetching:', i['title'], i['alt'])
        try:
            req = requests.get(url, headers=headers2)
        except Exception as e:
            print(e)
            not_found.append(i['id'])
            continue
        print(req)
        # print(url)
        # print(req.text)
        # input('aaaaaaaaaa')
        movielists = re.findall(r'= ({ "value":.*});var', req.text)[0]
        moviejson = json.loads(movielists)
        found_it = False
        if moviejson['value'] is None:
            not_found.append(i['id'])
            continue
        for movie in moviejson['value']['objs']:
            print('searching:', movie['titlecn'], movie['id'], movie['moviepage'])
            print('电影名：',i['title'])
            aaa = input('y/n')
            # if movie['titlecn'] == i['title']:
            if aaa == 'y':
                url_movie = r'http://m.mtime.cn/Service/callback.mi/movie/Detail.api?movieId={}&locationId=290&t=20193115171246368'.format(movie['id'])
                req_movie = requests.get(url_movie, headers=headers)
                print(req_movie)
                data = req_movie.json()
                print('data:', data)
                # input('aaaaa')
                try:
                    releasedate = data['release']['date']
                except Exception as e:
                    print(e)
                    releasedate = input('releasedate\n')
                if re.findall(r'2018', releasedate):
                    print('found:', movie['titlecn'])
                    updateinf = {'时光': {'title': movie['titlecn'], 'rank': data['rating'], 'rate_quantity': data['scoreCount'],
                                  'id': movie['id'], 'pubDesc': releasedate}}
                    print(updateinf)
                    collections_detail.update({'_id': i['_id']}, {'$set': updateinf})
                    found_it = True
                    break
                time.sleep(1 + random.random())
        if found_it is False:
            print('not found:', i['title'], '========================================')
            not_found.append(i['id'])
            print(not_found)
        time.sleep(2 + random.random())
        # input('aaaaaa')


# 获得通过 get_maoyan_score 没有找到的猫眼网电影评分，手工判断电影是否符合
def get_maoyan_score_not_found():
    not_found = []
    for count, i in enumerate(collections_detail.find({'猫眼': {'$exists': False}})):
        print(count,'==================================')
        url = 'https://maoyan.com/ajax/suggest?kw=' + i['title']
        print('fetching:', i['title'])
        try:
            req = requests.get(url, headers=headers)
        except Exception as e:
            print(e)
            not_found.append(i['id'])
            continue
        data = req.json()
        found_it = False
        if data['type'] == 0:
            mlist = data['movies']['list']
            for movie in mlist:
                print('searching:', movie['nm'])
                print(movie['nm'], i['title'], re.findall(r'2018.*大陆', movie['pubDesc']), i['alt'], url)
                # if movie['nm'] == i['title'] and re.findall(r'2018.*大陆上映', movie['pubDesc']):
                if input('y/n') == 'y':
                    print('found:', movie['nm'])
                    print({'猫眼':{'title':movie['nm'],'rank':movie['sc'],'id':movie['id'],'pubDesc':movie['pubDesc']}})
                    collections_detail.update({'_id': i['_id']}, {'$set': {'猫眼':{'title':movie['nm'],'rank':movie['sc'],'id':movie['id'],'pubDesc':movie['pubDesc']}}})
                    found_it = True
                    break
        if found_it is False:
            print('not found:', i['title'], '========================================')
            not_found.append(i['id'])
        time.sleep(2 + random.random())


# 没啥用，就是刚开始的票房是在 movies 这个数据表里，把票房数据加到 moviesdetail 数据表里
def addboxofficetodetail():
    for i in collections_detail.find():
        findmovie = collections.find_one({'MovieName': i['title']})
        print(findmovie)
        if findmovie:
            collections_detail.update({'_id': i['_id']}, {'$set': {'boxoffice': findmovie['BoxOffice']}})
            print('done：',findmovie['MovieName'])
        else:
            print('没有找到电影：',i['title'])
        print('========================================')


client = pymongo.MongoClient()
db = client.chinamovies
collections = db.movies
collections_detail = db.moviesdetail

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}

# find_actors()
# other_detail()
# get_imdb_score()
