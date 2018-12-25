# coding:utf8
# 彩色版
import random
height = 11
for i in range(height):
    print(' ' * (height - i), end='')
    for j in range((2 * i) + 1):
        if random.random() < 0.1:
            color = random.choice(['\033[1;31m', '\033[33m', '\033[1;34m'])
            print(color, end='')  # 彩灯
        else:
            print('\033[32m', end='')  # 绿色
        print('*', end='')
    print()
print((' ' * height) + '|')
