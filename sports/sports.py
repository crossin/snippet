#!/usr/bin/env python
# coding: utf-8

# In[47]:


import pandas as pd
is_change = True
count = 12
all_data = []     # 记录历届成绩
data = []         # 记录一届成绩
writer = pd.ExcelWriter('history.xls')
watches = set()
with open('history.txt') as f:    
    for line in f:
        if line.strip():
            # 非空行
            if is_change:
                is_change = False
            # 读取、清理空格、记录数据
            data.append([l.strip() for l in line.split('┃')])
        else:
            # 遇到空行，结束一届的记录
            if not is_change:
                # 记录数据
                df = pd.DataFrame(data)
                all_data.append(df)
                # 写入文件
                df.to_excel(writer, sheet_name=f'No.{count}', index=False)
                # 把前3名加入集合
                top3 = list(df[1][:3])
                watches.update(top3)
                # 重置参数
                is_change = True
                count -= 1
                data = []
writer.save()
watches


# In[55]:


gold = {}
all_data.reverse()
# 遍历队伍
for team in watches:
    gold[team] = []
    # 遍历每一届数据
    for data in all_data:
        gold[team].append(float(data[data[1]==team][2]))

# 输出
for team in gold:
    print(team, gold[team])


# In[56]:


import matplotlib.pyplot as plt
from pylab import mpl

plt.rcParams['figure.figsize'] = (16, 12)
# 中文乱码问题（自行下载）
font = mpl.font_manager.FontProperties(fname='../simhei.ttf', size=15)

for team in gold:
    plt.plot(gold[team], linewidth=4, label=team)
plt.legend(prop=font)


# In[57]:


from pyecharts.charts import Line

line = Line()
line.add_xaxis(xaxis_data=range(1, 13))
for team in gold:
    line.add_yaxis(team, gold[team])
line.render_notebook()


# In[ ]:




