# 抓取哪吒数据并储存
import pandas as pd
import requests
import time
import os

def time_stamp(dt):
    """时间转时间戳"""
    timeArray = time.strptime(dt, "%Y-%m-%d") # 字符串 转 时间数组
    timestamp = int(time.mktime(timeArray)) # 时间数组 转 时间戳
    return timestamp
  
headers = {'User-Agent': 'chrome'}
m = {}
start = time_stamp('2019-07-26') # 哪吒上映时间
# end = time_stamp('2019-08-01') # 结束时间，可以自定义
end = int(time.time()) # 以当前日期为结束时间

while True:
    time_local = time.localtime(start) # 时间数组 转 新的时间格式 20160505(url 所需的格式)
    start += 86400 # 加一天
    dt = time.strftime("%Y%m%d",time_local) # 时间
    print('抓取日期 %s' %dt, end=', ')
    url = 'https://box.maoyan.com/promovie/api/box/second.json?beginDate=' + dt
    r = requests.get(url,headers=headers) # 请求接口
    res = r.json() # 返回 json 文件
    movie_list = res['data']['list'] # 每日电影列表
    qdate = res['data']['queryDate'] # 日期
    if res['success'] and time_stamp(qdate) <= end: # 控制抓取时间
        for movie in movie_list:
            if movie['movieName'] == '哪吒之魔童降世' and movie['releaseInfo'] != '点映':
                m[movie['movieName']] = m.get(movie['movieName'], [])
                m[movie['movieName']].append(movie['boxInfo'])
    else:
        print('结束')
        break
# 数据储存      
edf = pd.DataFrame.from_dict(m, orient='index')
edf = edf.T
edf.to_csv(os.path.abspath('.') + r'/nezha.csv', sep=',', encoding='utf_8_sig', index=False)