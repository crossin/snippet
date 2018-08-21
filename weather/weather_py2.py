# -*- coding: utf-8 -*-
# windows 下如果出现编码问题，将 utf-8 改为 gbk

import urllib
import urllib2
import gzip
import json
from StringIO import StringIO
from city import city


def get_weather_1(cityname):
    print '\n接口 1：'
    citycode = city.get(cityname)
    if not citycode:
        print '未找到该城市'
        return
    url = 'http://www.weather.com.cn/data/cityinfo/%s.html' % citycode
    print url
    resp = urllib2.urlopen(url).read()
    # print resp
    # 将 json 格式的结果转为字典对象
    result = json.loads(resp)
    # print result
    result_data = result.get('weatherinfo')
    # print result_data
    if result_data:
        print '天气：', result_data.get('weather')
        print '最低温度：', result_data.get('temp1')
        print '最高温度：', result_data.get('temp2')
    else:
        print '未能获取此城市的天气情况。'


def get_weather_2(cityname):
    print '\n接口 2：'
    citycode = city.get(cityname)
    if not citycode:
        print '未找到该城市'
        return
    url = 'http://wthrcdn.etouch.cn/weather_mini?citykey=%s' % citycode
    print url
    resp = urllib2.urlopen(url).read()
    # print resp
    # 因网页内容做了 gzip 压缩，所以要对其解压
    try:
        buf = StringIO(resp)
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    except:
        data = resp
    # print data
    # 将 json 格式的结果转为字典对象
    result = json.loads(data)
    # print result
    result_data = result.get('data')
    # print result_data
    if result_data:
        print '当前温度：', result_data.get('wendu'), '℃'
        print '空气质量：', result_data.get('aqi')
        print result_data.get('ganmao')
        # print result_data.get('ganmao').decode('utf-8')  # windows 编码参考
        print '天气预报：'
        forecast = result_data.get('forecast')
        for fc in forecast:
            print fc.get('date'), '：', fc.get('type'), '，', fc.get('low'), '，', fc.get('high')
    else:
        print '未能获取此城市的天气情况。'


def get_weather_3(cityname):
    print '\n接口 3：'
    cityurl = urllib.quote(cityname)
    # cityurl = urllib.quote(cityname.decode('gbk').encode('utf8'))  # windows 编码参考
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=%s' % cityurl
    print url
    resp = urllib2.urlopen(url).read()
    # print resp
    # 因网页内容做了 gzip 压缩，所以要对其解压
    try:
        buf = StringIO(resp)
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    except:
        data = resp
    # print data
    # 将 json 格式的结果转为字典对象
    result = json.loads(data)
    # print result
    result_data = result.get('data')
    # print result_data
    if result_data:
        print '当前温度：', result_data.get('wendu'), '℃'
        print '空气质量：', result_data.get('aqi')
        print result_data.get('ganmao')
        # print result_data.get('ganmao').decode('utf-8')  # windows 编码参考
        print '天气预报：'
        forecast = result_data.get('forecast')
        for fc in forecast:
            print fc.get('date'), '：', fc.get('type'), '，', fc.get('low'), '，', fc.get('high')
    else:
        print '未能获取此城市的天气情况。'


while True:
    # 获取网页返回
    cityname = raw_input('请输入要查询的城市（直接回车退出）：\n')
    if not cityname:
        break
    get_weather_1(cityname)
    get_weather_2(cityname)
    get_weather_3(cityname)
