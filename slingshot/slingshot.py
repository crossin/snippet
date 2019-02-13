# coding: utf-8

import pygame
import math
import sys

# 取符号函数
def sign(a):
   return (a > 0) - (a < 0)

# 定义颜色
black = 0, 0, 0
white = 255, 255, 255

k = 1e7            # 距离缩放参数
m = 5.9742e24      # 地球质量
M = 1898.7e27      # 木星质量
G = 6.67259e-17    # 万有引力常量
t = 1e5            # 时间缩放参数

pos_x= 0           # 地球坐标
pos_y= 400
earth = pos_x, pos_y
vel_x= 80          # 地球速度
vel_y= 60
jupiter = 700, 300 # 木星坐标
v_j = 3            # 木星速度

pygame.init()  # 初始化
screen= pygame.display.set_mode((800, 600))  # 创建窗口
font = pygame.font.Font('../zhaozi.ttf', 30)  # 显示中文需要字体，否则可略过
text = font.render("木星引力弹弓 - Crossin的编程教室", 1, white)
pygame.display.set_caption("引力弹弓模拟")

e = pygame.image.load("earth.png").convert_alpha()  # 地球图片
j = pygame.image.load("jupiter.png").convert_alpha()  # 木星图片

while True:  # 主循环
    for event in pygame.event.get():
        if event.type in (pygame.QUIT, pygame.KEYDOWN):
            sys.exit()  # 按键响应，按键后退出
    
    screen.fill(black)  # 刷新背景
    
    jupiter = jupiter[0] - v_j, jupiter[1]  # 木星位移
    screen.blit(j, jupiter)  # 画木星

    # 地木坐标差
    delta_x = (jupiter[0] - earth[0]) * k
    delta_y = (jupiter[1] - earth[1]) * k
    # 地木距离平方
    r2 = delta_x ** 2 + delta_y ** 2
    # 地木间引力，万有引力定律
    F = G * m * M / r2
    # 地木夹角
    theta = math.acos(delta_x / r2 ** 0.5)
    # x、y 轴引力分量
    fx = abs(F * math.cos(theta)) * sign(delta_x)
    fy = abs(F * math.sin(theta)) * sign(delta_y)
    # x、y 轴加速度，牛顿第二定律
    ax = fx / m
    ay = fy / m
    # 速度变化，vt = v0 + at
    vel_x += ax * t
    vel_y += ay * t
    # 位移变化，st = s0 + vt
    pos_x += vel_x * t / k
    pos_y += vel_y * t / k
    earth = int(pos_x), int(pos_y)
    screen.blit(e, earth)  # 画地球

    v = '地球速度 %.2f km/s' % ((vel_x ** 2 + vel_y ** 2) ** 0.5)  # 速度大小
    speed = font.render(v, 1, white)
    screen.blit(text, (150, 100))
    screen.blit(speed, (200, 50))
    pygame.display.update()  # 刷新
