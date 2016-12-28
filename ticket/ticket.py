# coding: utf-8
#
# 定时访问12306网站上某天某条线路上的车次信息
# 需要手动停止（一般系统是 ctrl+c 中断）
#
# 欢迎关注
# 微信公众号：Crossin的编程教室
# 微信号：crossincode
# 论坛：bbs.crossincode.com

import urllib2
import ssl
import json
import time

# 忽略 ssl 证书验证
ssl._create_default_https_context = ssl._create_unverified_context

TRAIN = 'G7028'
DELAY = 300
DATE = '2016-12-31'
FROM = 'SHH'
TO = 'NJH'


def get_resp():
    # 设置网页请求地址
    req_url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT' % (
        DATE, FROM, TO)
    # 打开网页
    resp = urllib2.urlopen(req_url)
    if resp:
        print ('请求成功')
    # 读取网页内容
    return resp.read()


def get_data(resp_info):
    # 转换 json 数据
    info_json = json.loads(resp_info)
    info = info_json['data']
    # 遍历每车次信息
    for train_data in info:
        # 判断并获取需要查询的车次信息
        train = train_data['queryLeftNewDTO']
        if train['station_train_code'] == TRAIN:
            print '商务座：', train['swz_num']
            print '特等座', train['tz_num']
            print '一等座', train['zy_num']
            print '二等座', train['ze_num']
            print '高级软卧', train['gr_num']
            print '软卧', train['rw_num']
            print '硬卧', train['yw_num']
            print '软座', train['rz_num']
            print '硬座', train['yz_num']
            print '无座', train['wz_num']
            print '其它', train['qt_num']


# 循环查询
while True:
    html_info = get_resp()
    get_data(html_info)
    print('------------------------------')
    # 延时设定
    time.sleep(DELAY)
