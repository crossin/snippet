#-*- coding: utf-8 -*-
#
# 访问12306网站上某天某条线路上的车次信息
# 如果有自己关注的票，就发邮件通知
# 该程序只访问一次，实际使用时可通过 crontab 或计划任务定时执行
#
# 欢迎关注
# 微信公众号：Crossin的编程教室
# 微信号：crossincode
# 论坛：bbs.crossincode.com

import urllib2
import json
import smtplib
import time
import codecs
from email.mime.text import MIMEText  

# 记录日志
def log(content):
    t = time.strftime('%Y-%m-%d %H:%M:%S')
    f = codecs.open('watcher.log', 'a', 'utf-8')
    f.write('[%s]%s\n' % (t, content))
    f.close()

# 发送邮件
def send_mail(content): 
    to_list=['xxx@gmail.com'] # 接收通知的邮箱
    mail_host = 'smtp.163.com' #, 587  #设置服务器
    mail_user = 'username' #替换为发件邮箱用户名
    mail_pass = 'password'   #替换为发件邮箱口令 
    mail_postfix = '163.com'  #发件箱的后缀
    me = "TicketsWatcher"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
    msg['Subject'] = 'There are some tickets you need.'  
    msg['From'] = me
    msg['To'] = ";".join(to_list)  
    server = smtplib.SMTP()  
    server.connect(mail_host)
    server.ehlo()
    server.starttls()
    server.login(mail_user,mail_pass)  
    server.sendmail(me, to_list, msg.as_string())  
    server.close()
    log('sent mail successfully')


try:
    # 请求地址根据实际要抓取的页面修改，参数包括日期、出发站、到达站
    resp = urllib2.urlopen("https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate=2016-06-03&from_station=NJH&to_station=SHH")
    result = resp.read()
    data = json.loads(result)
    datas = data['data']['datas']
    for d in datas:
        if d['station_train_code'] == 'Z39':  # 设置关注的车次
            content = 'tickes for hard seat of %s: %s' % (d['station_train_code'], d['yz_num'])
            log(content)
            if unicode(d['yz_num']) != u"无":
                send_mail(content)  # 如果不是“无”就发邮件通知
            break
except Exception, e:
    content = 'somethings wrong with the program:\n' + str(e)
    log(content)
    send_mail(content)  # 出错时也发邮件
