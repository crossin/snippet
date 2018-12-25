# coding:utf8
# 极简版
height = 7
for i in range(height):
    print((' ' * (height - i)) + ('*' * ((2 * i) + 1)))
print((' ' * height) + '|')