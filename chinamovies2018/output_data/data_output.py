import pymongo, csv

client = pymongo.MongoClient()
db = client.chinamovies
collections = db.movies
collections_detail = db.moviesdetail
col_casts = db.casts
col_directors = db.directors

# 将每个影人2018年参演电影的票房总和导出数据库，存入 cast_data.csv
with open('cast_data.csv','w',newline='',encoding='utf-8') as file:
    cast_list = ['演员', '演员id', '参演电影总票房(亿)', '参演电影']
    f_csv = csv.writer(file)
    f_csv.writerow(cast_list)
    # 对影人参演电影票房总和排了个序
    for i in col_casts.find().sort('total_box',-1):
        print(i)
        data = [i['name'], i['id'], i['total_box']/10000, ' '.join(i['movie'])]
        print(data)
        print()
        f_csv.writerow(data)

# 将2018年电影数据从数据库导出至 movie_data.csv
with open('movie_data.csv','w',newline='',encoding='utf-8') as file:
    movie_list = [
        '电影名', '类型', '上映日期', '时长（分）', '导演', '主要演员', '全部演员', '票房', '豆瓣链接',
        '豆瓣评分', '豆瓣评分人数', '豆瓣短评数', '豆瓣长评数', '猫眼评分', '时光网评分', 'imdb评分'
    ]
    f_csv = csv.writer(file)
    f_csv.writerow(movie_list)
    for i in collections_detail.find():
        # print(i, '==============================')
        genres = ' '.join(i['genres'])
        directors = ' '.join([dir['name'] for dir in i['directors']])
        casts = ' '.join([onecast['name'] for onecast in i['casts']]) if i['casts'] else ''
        actors = ' '.join([oneactor['name'] for oneactor in i['actors']]) if i['actors'] else ''

        maoyan = str(i.get('猫眼')['rank']) if i.get('猫眼') else ''

        if i.get('时光'):
            # 时光网中，没有评分的默认为-1，需要转一下
            mtimeorigin = i.get('时光')['rank']
            mtime = '' if float(mtimeorigin) == -1.0 else mtimeorigin
        else:
            mtime = ''

        imdb = i.get('imdb')['rank'] if i.get('imdb') else ''

        data = [i['title'], genres, i['releasedate'], i['film_duration'], directors, casts, actors,
              str(i.get('boxoffice_num')), i['alt'], i['rate_score'], i['rate_quantity'], i['comments_num'],
              i['commentslong_num'], maoyan, mtime, imdb]
        print(data)
        print()
        f_csv.writerow(data)
