# -*- coding: utf-8 -*-
"""
 Animating multiple objects using a list.
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/Gkhz3FuhGoI

 修改：Crossin
 网址：http://crossincode.com/
 微信公众号：Crossin的编程教室
 知乎：https://zhuanlan.zhihu.com/crossin
"""
 
import pygame
import random
 
# 初始化pygame
pygame.init()
  
# 根据背景图片的大小，设置屏幕长宽
SIZE = (1364, 569)
 
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Snow Animation")
bg = pygame.image.load('snow.jpg')

# 雪花列表
snow_list = []
 
# 初始化雪花：[x坐标, y坐标, x轴速度, y轴速度]
for i in range(200):
    x = random.randrange(0, SIZE[0])
    y = random.randrange(0, SIZE[1])
    sx = random.randint(-1, 1)
    sy = random.randint(3, 6)
    snow_list.append([x, y, sx, sy])
 
clock = pygame.time.Clock()
 
# 游戏主循环
done = False
while not done:
    # 消息事件循环，判断退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    # 黑背景/图片背景
    # screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    # 雪花列表循环
    for i in range(len(snow_list)):
        # 绘制雪花，颜色、位置、大小
        pygame.draw.circle(screen, (255, 255, 255), snow_list[i][:2], snow_list[i][3]-3)
 
        # 移动雪花位置（下一次循环起效）
        snow_list[i][0] += snow_list[i][2]
        snow_list[i][1] += snow_list[i][3]
 
        # 如果雪花落出屏幕，重设位置
        if snow_list[i][1] > SIZE[1]:
            snow_list[i][1] = random.randrange(-50, -10)
            snow_list[i][0] = random.randrange(0, SIZE[0])
 
    # 刷新屏幕
    pygame.display.flip()
    clock.tick(20)

# 退出 
pygame.quit()
