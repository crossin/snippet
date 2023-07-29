
# coding: utf-8

# In[1]:


import tushare as ts
import matplotlib.pyplot as plt

def rebalance(asset, price):
    money = asset * 0.5
    stock = money / price
    return money, stock

asset = 10000
hist_money = []
hist_stock = []
hist_allin_money = []
hist_allin_stock = []
allin_money = 10000
allin_stock = 0
days = 0
interval = 180
df=ts.get_k_data('399300',start='2012-01-01',end='2016-01-01')
# print(df)
for price in df.close:
    days -= 1
    if days < 0:
        money, stock = rebalance(asset, price)
        days = interval
    stock_p = stock * price
    money *= 1.0001
    asset = money + stock_p
    hist_money.append(money)
    hist_stock.append(stock_p)
    # 对比
    allin_money *= 1.0001
    hist_allin_money.append(allin_money)
    if allin_stock == 0:
        allin_stock = 10000 / price
    hist_allin_stock.append(allin_stock * price)

print(asset)
print(allin_money)
print(allin_stock * price)


# In[2]:


# draw
date = list(df.date)

fig, left_axis = plt.subplots()
fig.set_size_inches(16, 10)
right_axis = left_axis.twinx()

p1 = left_axis.plot(date, df.close)
p2 = right_axis.stackplot(date, hist_money, hist_stock, alpha=0.3)
p3 = right_axis.plot(date, hist_allin_money)
p4 = right_axis.plot(date, hist_allin_stock)

xticks = list(range(0, len(date), 90))
xlabels = [date[x] for x in xticks]
left_axis.set_xticks(xticks)
left_axis.set_xticklabels(xlabels, rotation=45)
plt.show()


# In[3]:


# 按比例触发再平衡
def rebalance(asset, price):
    money = asset * 0.5
    stock = money / price
    return money, stock

money = 10000
asset = money
stock = 0
hist_money = []
hist_stock = []
hist_allin_money = []
hist_allin_stock = []
allin_money = 10000
allin_stock = 0
days = 0
interval = 360
df=ts.get_k_data('399300',start='2014-01-01',end='2016-01-01')
# df=ts.get_k_data('601005',start='2007-10-01')
# print(df)
for price in df.close:
    days -= 1
    stock_p = stock * price
    if (money == 0 or stock == 0) or (money / stock_p > 1.2 or stock_p / money > 1.2):
#     if days < 0:
        money, stock = rebalance(asset, price)
        days = interval
    money *= 1.0001
    asset = money + stock_p
    hist_money.append(money)
    hist_stock.append(stock_p)
    # 对比
    allin_money *= 1.0001
    hist_allin_money.append(allin_money)
    if allin_stock == 0:
        allin_stock = 10000 / price
    hist_allin_stock.append(allin_stock * price)

print(asset)
print(allin_money)
print(allin_stock * price)

# draw
date = list(df.date)

fig, left_axis = plt.subplots()
fig.set_size_inches(16, 10)
right_axis = left_axis.twinx()

p1 = left_axis.plot(date, df.close)
p2 = right_axis.stackplot(date, hist_money, hist_stock, alpha=0.3)
p3 = right_axis.plot(date, hist_allin_money)
p4 = right_axis.plot(date, hist_allin_stock)

xticks = list(range(0, len(date), 90))
xlabels = [date[x] for x in xticks]
left_axis.set_xticks(xticks)
left_axis.set_xticklabels(xlabels, rotation=45)
plt.show()


# In[4]:


# 与定投结合
def rebalance(asset, price):
    money = asset * 0.5
    stock = money / price
    return money, stock

money = 10000
cost = money
asset = money
stock = 0
hist_money = []
hist_stock = []
hist_allin_money = []
hist_allin_stock = []
allin_money = 10000
allin_stock = 0
days = 0
interval = 30
df=ts.get_k_data('399300',start='2007-05-01')
# print(df)

for price in df.close:
    days -= 1
    stock_p = stock * price
    if allin_stock == 0:
        allin_stock = 10000 / price
    if days < 0:
        days = interval
        cost += 1000
        money += 1000
        allin_money += 1000
        allin_stock += (1000/price)
        asset = money + stock_p
    if (money == 0 or stock == 0) or (money / stock_p > 1.5 or stock_p / money > 1.5):
#     if days < 0:
        money, stock = rebalance(asset, price)
        stock_p = stock * price
    money *= 1.0001
    asset = money + stock_p
    hist_money.append(money)
    hist_stock.append(stock_p)
    # 对比
    allin_money *= 1.0001
    hist_allin_money.append(allin_money)
    hist_allin_stock.append(allin_stock * price)

print(asset)
print(allin_money)
print(allin_stock * price)
print(cost)

# draw
date = list(df.date)

fig, left_axis = plt.subplots()
fig.set_size_inches(16, 10)
right_axis = left_axis.twinx()

p1 = left_axis.plot(date, df.close)
p2 = right_axis.stackplot(date, hist_money, hist_stock, alpha=0.3)
p3 = right_axis.plot(date, hist_allin_money)
p4 = right_axis.plot(date, hist_allin_stock)

xticks = list(range(0, len(date), 90))
xlabels = [date[x] for x in xticks]
left_axis.set_xticks(xticks)
left_axis.set_xticklabels(xlabels, rotation=45)
plt.show()


# In[79]:


import random
import datetime

def calc_rate(asset, days):
    r = asset / 10000 - 1
    return (r / (days / 240) * 100)

rate1 = []
rate2 = []
rate3 = []
for i in range(1000):
    print(i)
    money = 10000
    asset = money
    stock = 0
    hist_money = []
    hist_stock = []
    hist_allin_money = []
    hist_allin_stock = []
    allin_money = 10000
    allin_stock = 0
    days = 0
    interval = 180
    date_s = datetime.date.today() - datetime.timedelta(days=random.randint(2000,5000))
    date_e = date_s + datetime.timedelta(days=random.randint(1000, 5000))
    date_s = date_s.strftime('%Y-%m-%d')
    date_e = date_e.strftime('%Y-%m-%d')
#     print(date_s,date_e)
    df = ts.get_k_data('399300',start=date_s, end=date_e)
    # print(df)
    for price in df.close:
        days -= 1
        stock_p = stock * price
        if (money == 0 or stock == 0) or (money / stock_p > 1.2 or stock_p / money > 1.2):
    #     if days < 0:
            money, stock = rebalance(asset, price)
            days = interval
        money *= 1.0001
        asset = money + stock_p
        hist_money.append(money)
        hist_stock.append(stock_p)
        # 对比
        allin_money *= 1.0001
        hist_allin_money.append(allin_money)
        if allin_stock == 0:
            allin_stock = 10000 / price
        hist_allin_stock.append(allin_stock * price)

    days = len(df['date'])
    print(df['date'].iloc[0], df['date'].iloc[-1], days)
    print(int(asset), int(allin_money), int(allin_stock * price))
    r1 = calc_rate(asset, days)
    r2 = calc_rate(allin_money, days)
    r3 = calc_rate(allin_stock * price, days)
    rate1.append(r1)
    rate2.append(r2)
    rate3.append(r3)
    print(r1, r2, r3)
    print('=====================')

print(sum(rate1)/len(rate1), sum(rate2)/len(rate2), sum(rate3)/len(rate3))


# In[92]:


import numpy as np
print(np.std(rate1))
print(np.std(rate2))
print(np.std(rate3))

n = range(1000)
plt.scatter(n, rate2, marker='.', c='y' ,alpha=0.5)
plt.scatter(n, rate3, marker='.', c='g' ,alpha=0.5)
plt.scatter(n, rate1, marker='.', c='r' ,alpha=0.5)

fig = plt.gcf()
fig.set_size_inches(16, 30)
plt.yticks(np.arange(-15, 160, 5))
plt.show()

