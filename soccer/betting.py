#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import matplotlib.pyplot as plt

# 如果不显示图表，加上这两句
import matplotlib
matplotlib.use('TkAgg')

# In[2]:


profit = 0.05  #预期收益
will_A = 0.8  #投注者的对A队的偏好
prob_A = 0.5  #A队初始预测胜率
amount = [0, 0]  #投注人数记录
amounts = []
prize = [0, 0]  #奖金额记录
prize_A = []
prize_B = []
odds_As = []  #A队赔率记录
odds_Bs = []  #B队赔率记录

odds_A = (1 - profit) / prob_A  #A队赔率
odds_B = (1 - profit) / (1 - prob_A)  #B队赔率

class Player():
    def __init__(self):
        global odds_A, odds_B
        if random.random() < will_A:
            self.bet_A = True
            self.odds = odds_A
            amount[0] += 1
            amounts.append(1)
        else:
            self.bet_A = False
            self.odds = odds_B
            amount[1] += 1
            amounts.append(2)

        if len(amounts) > 1000:
            # 赔率更新
            prob_A = amounts[-1000:].count(1) / len(amounts[-1000:])
            odds_A = (1 - profit) / prob_A
            odds_B = (1 - profit) / (1 - prob_A)


for i in range(100000):
    p = Player()
    if p.bet_A:
        prize[0] += p.odds
    else:
        prize[1] += p.odds
    odds_As.append(odds_A)
    odds_Bs.append(odds_B)
    
    # 每10000人降低A队偏好
#     if i > 0 and i % 10000 == 0:
#         will_A *= 0.9
#         print(will_A)

    # 万分之一概率偏好波动
#     if random.random() < 0.0001:
#         will_A = 0.05 + random.random() * 0.9
#         print(will_A)
        
    prize_A.append(prize[0])
    prize_B.append(prize[1])

# from pylab import mpl
# font = mpl.font_manager.FontProperties(fname='../zhaozi.ttf', size=15)  # 中文乱码问题

fig, ax1 = plt.subplots(figsize=(16, 12))
line1, = ax1.plot(prize_A[::1000], 'b')
line2, = ax1.plot(prize_B[::1000], 'g')
line3, = ax1.plot(range(0,100000,1000), 'r')
# ax1.legend(['A队胜', 'B队胜', '收入'], prop=font)
ax1.legend(['A队胜', 'B队胜', '收入'])

ax2 = ax1.twinx()
line4, = ax2.plot(odds_As[::1000], 'y:')
line5, = ax2.plot(odds_Bs[::1000], 'c:')
# ax2.legend(['A队赔率', 'B队赔率'], prop=font)
ax2.legend(['A队赔率', 'B队赔率'])

# In[1]:


def match(count):
    global odds_A, odds_B
    profit = 0.05
    will_A = 0.5
    prob_A = 0.5
    amount = [0, 0]
    amounts = []
    prize = [0, 0]
    prize_A = []
    prize_B = []
    odds_As = []
    odds_Bs = []

    odds_A = (1 - profit) / prob_A
    odds_B = (1 - profit) / (1 - prob_A)

    class Player():
        def __init__(self):
            global odds_A, odds_B
            if random.random() < will_A:
                self.bet_A = True
                self.odds = odds_A
                amount[0] += 1
                amounts.append(1)
            else:
                self.bet_A = False
                self.odds = odds_B
                amount[1] += 1
                amounts.append(2)
            if len(amounts) > 1000:
                prob_A = amounts[-1000:].count(1) / len(amounts[-1000:])
                odds_A = (1 - profit) / prob_A
                odds_B = (1 - profit) / (1 - prob_A)

    for i in range(count):
        p = Player()
        if p.bet_A:
            prize[0] += p.odds
        else:
            prize[1] += p.odds
        odds_As.append(odds_A)
        odds_Bs.append(odds_B)
        if random.random() < 0.0001:
            will_A = 0.1 + random.random() * 0.8
        prize_A.append(prize[0])
        prize_B.append(prize[1])
    return prize[0] / count, prize[1] / count

result1 = []
result2 = []
# 计算100次收益比例
for i in range(100):
    a, b = match((i+10)*1000)
    result1.append(a)
    result2.append(b)
    print(i, a, b)


# In[ ]:


fig, ax1 = plt.subplots(figsize=(16, 12))
sca1 = ax1.scatter(range(100), result1)
sca2 = ax1.scatter(range(100), result2)
sca3 = ax1.scatter(range(100), [1]*100)

# ax1.legend(['A队胜', 'B队胜', '收入'], prop=font)
ax1.legend(['A队胜', 'B队胜', '收入'])

# In[4]:


def bet(m):
    prob = 0.1 + random.random() * 0.8
    odds = (1 - profit) / prob
    b = 1000  # 每次 1000
#     b = money  # 每次 all-in  
    m -= b
    if random.random() < prob:
        return m + b * odds
    else:
        return m

profit = 0.05
plt.subplots(figsize=(16, 12))
for x in range(100):
    money = 10000
    moneys = [money]

    for i in range(1000):
        # 归零时跳出循环（不许借钱）
        if money < 1:
            break

        money = bet(money)
        moneys.append(money)
    plt.plot(moneys, lw=0.3)
plt.show()

# In[ ]:




