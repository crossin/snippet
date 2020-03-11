import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt

money = 100
fundCode = '160135'  #基金代码
pageIndex = 1
startDate = '2018-08-21'  #起始时间
endDate = '2020-03-03'   #截止时间
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
    'Referer': 'http://fundf10.eastmoney.com/jjjz_{0}.html'.format(fundCode)
}
url = 'http://api.fund.eastmoney.com/f10/lsjz?fundCode={0}&pageIndex={1}&pageSize=5000&startDate={2}&endDate={3}&_=1555586870418?'.format(fundCode, pageIndex, startDate, endDate)
response = requests.get(url, headers=header)
result=json.loads(response.text)
print(result)
total = [0] * 5   # 到期后总份额
count = [0] * 5   # 每日定投次数
for j in result['Data']['LSJZList'][::-1]:
    if j['JZZZL']=='':
        pass
    else:
        weekday = int(datetime.strptime(j['FSRQ'], '%Y-%m-%d').weekday())
        DWJZ = float(j['DWJZ'])   # 净值
        total[weekday] += money/DWJZ
        count[weekday] += 1
total_money=[]   #根据份额算出总金额
for t, i in enumerate(total):
    total_money.append(i*DWJZ)
    print("周{0}定投最终金额{1}".format(t+1, i*DWJZ), "定投{0}次".format(count[t]))
plt.rcParams['font.sans-serif'] = ['SimHei']  # windows 用来正常显示中文标签
# plt.rcParams["font.family"] = 'Arial Unicode MS'  # mac 用来正常显示中文标签
plt.figure(figsize=(15, 10), dpi=80)
plt.title('{0}基金模拟定投收益图'.format(fundCode), color='blue', fontweight=800, size=50)

profit_list = [round((i-100*j)/(100*j), 4) for i, j in zip(total_money, count)]  # 到期后总收益率
print(profit_list)
# 生成画布
name_list = ['周一', '周二', '周三', '周四', '周五']
x = range(len(name_list))
minytick=int(min(total_money))-1000
maxytick=int(max(total_money))+1000
plt.bar(x, [i for i in total_money], label='该日定投最终收益', width=0.4, color='y')
# 参数 m、m2、r 用来调整高度比例
m = sum(total_money) / 5
m2 = min(profit_list)
r = 50000
plt.bar([i+0.4 for i in x], [(i-m2)*r + m for i in profit_list], label='该日定投收益率', width=0.4, color='r')
plt.legend(loc="upper left")  # 防止label和图像重合显示不出来
plt.xticks(x, name_list, size=20)   # x坐标
plt.ylim(minytick, maxytick)
plt.yticks(range(minytick, maxytick, 200), size=20) # y坐标
ax = plt.gca();#获得坐标轴的句柄
ax.spines['left'].set_linewidth(3) ; ####设置左边坐标轴的粗细
ax.spines['bottom'].set_linewidth(3) ; ###设置底部坐标轴的粗细

for a, b, c in zip(x, total_money, count):
    plt.text(a, b+0.05, '%.1f' % b, ha='center', va='bottom', fontsize=15)
    plt.text(a, b+100, '定投{}次'.format(c), ha='center', va='bottom', fontsize=15, color='r')
for a, b in zip(x, profit_list):
    plt.text(a+0.4, (b-m2)*r + m, '%.4f' % b, ha='center', va='bottom', fontsize=15)

plt.text(2, maxytick+300, '时间：{0}至{1}'.format(startDate, endDate), fontsize=20)
plt.grid(axis="y")  #生成网格'''
plt.show()