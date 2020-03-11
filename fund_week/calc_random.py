import requests
import re
import random
import json
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',}
url = 'http://fund.eastmoney.com/js/fundcode_search.js?v=20200301111634'
response=requests.get(url, header)
result=response.text.replace('var r = ', '').replace(';', '')
pattern=re.compile(r'\["(.*?)"\,', re.S)
item=re.findall(pattern,result)
codes=random.sample(item[:200], 20)
codes=['001210', '519670', '002207', '001618', '519670', '590008', '001071', '257040', '590005', '080012']
month=['01','02','03','04','05','06','07','08','09','10','11','12']
day=range(1, 32)
#startDate = '2018-{0}-{1}'.format(random.sample(month,1)[0],random.sample(day,1)[0])  #起始时间
#endDate = '2019-{0}-{1}'.format(random.sample(month,1)[0],random.sample(day,1)[0])   #截止时间
startDate = '2018-01-21'  #起始时间
#startDate = '2018-04-17'  #起始时间
endDate = '2020-01-28'   #截止时间

allpro=[]
name_list = ['周一', '周二', '周三', '周四', '周五']
money = 100  #定投金额
n = 0
while n < 10:
    n += 1
    startDate = '2018-{0}-{1}'.format(random.sample(month, 1)[0], random.sample(day, 1)[0])  # 起始时间
    endDate = '2019-{0}-{1}'.format(random.sample(month,1)[0],random.sample(day,1)[0])   #截止时间
    print(startDate, endDate)
    for i, j in enumerate(codes):
        total = [0] * 5   # 到期后总份额
        count = [0] * 5   # 每日定投次数
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
            'Referer': 'http://fundf10.eastmoney.com/jjjz_{0}.html'.format(j)
        }
        url = 'http://api.fund.eastmoney.com/f10/lsjz?fundCode={0}&pageIndex={1}&pageSize=5000&startDate={2}&endDate={3}&_=1555586870418?'.format(
            j, 1, startDate, endDate)
        response = requests.get(url, headers=header)
        result = json.loads(response.text)
        for j in result['Data']['LSJZList'][::-1]:
            if j['JZZZL']=='':
                pass
            else:
                weekday = int(datetime.strptime(j['FSRQ'], '%Y-%m-%d').weekday())
                DWJZ = float(j['DWJZ'])   # 净值
                total[weekday] += money/DWJZ
                count[weekday] += 1
        total_money = []  # 根据份额算出总金额
        for t, k in enumerate(total):
            total_money.append(k * DWJZ)
            print("周{0}定投最终金额{1}".format(t + 1, k * DWJZ), "定投{0}次".format(count[t]))
        profit_list = [round((i-100*j)/(100*j), 4) for i, j in zip(total_money, count)]  # 到期后总收益率
        allpro.append(profit_list)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams["font.family"] = 'Arial Unicode MS'  # mac 用来正常显示中文标签
matplotlib.rcParams['axes.unicode_minus'] =False  #显示负号
plt.figure(figsize=(15, 10), dpi=80)
plt.title('随机基金模拟定投收益散点图', color='blue', fontweight=800, size=40)
x = range(len(name_list))
for t, i in enumerate(allpro):
    plt.scatter(x, i, c='b', s=0.5)  #画每个基金的散点图
average=[]
for i in range(5):
    eve_average = 0
    for j in allpro:
        eve_average=eve_average+j[i]
    average.append(eve_average/100)
for a, b in zip(x, average):
    plt.text(a+0.4, b, '%.5f' % b, ha='center', va='bottom', fontsize=20)
plt.scatter(x, average, s=50, c='r', label='平均值')
plt.legend(loc="upper left")  # 防止label和图像重合显示不出来
plt.xticks(x, name_list, size=20, color='r')   # x坐标
plt.ylabel('收益率', color='r', size=20)
plt.grid(axis="y")  #生成网格'''
plt.show()

