
# coding: utf-8

# In[17]:


import datetime
import time
import requests
from bs4 import BeautifulSoup
day = datetime.date(year=2019, month=3, day=8)
url = 'http://www.chinaclear.cn/cms-search/view.action?action=china'
accounts = []
for i in range(200):
    print(i)
    time.sleep(0.15)
    day -= datetime.timedelta(weeks=1)
    day_str = day.strftime('%Y.%m.%d')
    data = {
        'dateStr': day_str
    }
    text = requests.post(url, data, headers={'user-agent':'BDSpider'}).text
#     print(text)
    if '没有找到相关信息' in text:
        continue
    soup = BeautifulSoup(text, 'lxml')
    acc_new = soup.find(class_='Stock2').find_all('td')
    acc = (day, float(acc_new[4].text), float(acc_new[10].text.replace(',','')))
    accounts.append(acc)
#     print(acc)
accounts.reverse()
accounts


# In[45]:


import pandas
import matplotlib.pyplot as plt
import tushare as ts

df = pandas.DataFrame(accounts)
# print(df)
# draw
date = list(df[0])

# print(date)
fig, left_axis = plt.subplots()
fig.set_size_inches(32, 10)
right_axis = left_axis.twinx()
right_axis2 = left_axis.twinx()

p1 = left_axis.bar(date, df[1], width=5)

df2 = ts.get_k_data('sh', start='2015-05-01')
date.append(datetime.date(year=2019,month=3,day=1))
date.append(datetime.date(year=2019,month=3,day=8))
price = []
change = []
last = []
c = 0
for day in date:
    while True:
        try:
            p = float(df2.loc[df2.date==day.strftime('%Y-%m-%d')]['close'])
#             print(p)
            price.append(p)
            if len(last) == 4:
                avg = sum(last)/4
                c = p/avg - 1
                last.pop(0)
            last.append(p)
            change.append(c)
            break
        except:
            print('ERROR: no price in', day)
            day += datetime.timedelta(days=1)
p2 = right_axis.plot(date, price, color='r')
p3 = right_axis2.plot(date, change, color='g')
p4 = right_axis2.plot(date, [0]*196, color='g', ls='--')

plt.show()

