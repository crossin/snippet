# 为jupyter notebook 中使用 matplotlib 九宫格
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os

# %matplotlib inline # jupyter notebook 中使用
matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文

# 数据读取
data = pd.read_csv(os.path.abspath('.') + r'/boxoffice.csv', sep=',', encoding='utf_8_sig') # 读取数据
title = data.columns.tolist()
data = data.T
box = data.values.tolist()

plt.figure(figsize=(22,12))
for i in range(len(title[:9])):
    plt.subplot(3,3,i+1)
    y = box[i]
    x = [i for i in range(len(y))]
    plt.xticks() # 横坐标
    plt.plot(x,y,"g",linewidth=1.5)   #在当前绘图对象绘图（X轴，Y轴，蓝色，线宽度）
    plt.xlabel("",fontsize=14) #X轴标签
    plt.ylabel("票房（单位/万）",fontsize=14)  #Y轴标签
    plt.title(title[i],fontsize=15) #图标题
plt.savefig(os.path.abspath('.') + r'/boxoffice.png', dpi=300) #指定分辨率保存  
plt.show()