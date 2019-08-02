# coding:utf8
# 抓取特定电影票房数据并储存为 csv 文件
import pandas as pd
import requests
import time
import os

def time_stamp(dt):
    """时间转时间戳"""
    timeArray = time.strptime(dt, "%Y-%m-%d") # 字符串 转 时间数组
    timestamp = int(time.mktime(timeArray)) # 时间数组 转 时间戳
    return timestamp

# 按照绘制九宫格顺序排布
movies = ["西游记之大圣归来", "流浪地球", "白蛇：缘起", "复仇者联盟4：终局之战", "我不是药神", "战狼2", "唐人街探案2", "爱情公寓", "新喜剧之王"]   
headers = {'User-Agent': 'chrome'}
m,mo = {},{}
start = time_stamp('2015-02-13') # 抓取数据的起始时间
end = time_stamp('2019-08-01') # 自定义结束时间
# end = int(time.time()) # 以当前日期为结束时间

while True:
    time_local = time.localtime(start) # 时间数组 转 新的时间格式 20160505(url 所需的格式)
    dt = time.strftime("%Y%m%d",time_local) # 时间
    start += 86400 # 加一天
    print('抓取日期 %s' %dt, end=', ')
    url = 'https://box.maoyan.com/promovie/api/box/second.json?beginDate=' + dt
    r = requests.get(url,headers=headers) # 请求接口
    res = r.json() # 返回 json 文件
    movie_list = res['data']['list'] # 每日电影列表
    qdate = res['data']['queryDate'] # 日期
    if res['success'] and time_stamp(qdate) <= end: # 控制抓取时间
        for movie in movie_list:
            if movie['movieName'] in movies and movie['releaseInfo'] != '点映':
                m[movie['movieName']] = m.get(movie['movieName'], []) 
                m[movie['movieName']].append(movie['boxInfo']) # 存储电影票房
    else:
        print('出问题 或者 结束？')
        break
# 九宫格排序
for r in movies:
    mo[r] = m[r]
# 数据储存      
edf = pd.DataFrame.from_dict(mo, orient='index') 
edf = edf.T # 转置
edf.to_csv(os.path.abspath('.') + r'/boxoffice.csv', sep=',', encoding='utf_8_sig', index=False) # 保存到 csv