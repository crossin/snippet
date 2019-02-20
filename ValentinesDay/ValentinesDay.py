#-*- coding: utf-8 -*-
####################################
###    99 rose curves for QXT    ###
###    Happy Valentine's Day~    ###
###    by Crossin                ###
####################################
#
# 欢迎关注
# 微信公众号：Crossin的编程教室
# 微信号：crossincode
# 论坛：bbs.crossincode.com
#

import math
rad = 12
heart = u'\u2665'.encode('utf8')
curve = []
for i in range(rad*2+1):
    curve.append([])
    for j in range(rad*2+1):
        curve[i].append(' ')
for n in range(1,100):
    print n
    for k in range(360):
        angle = k * math.pi / 180
        x = int(rad * math.sin(n * angle) * math.sin(angle)) + rad
        y = int(rad * math.sin(n * angle) * math.cos(angle)) + rad
        curve[x][y] = heart
    for i in range(rad*2+1):
        for j in range(rad*2+1):
            print curve[i][j],
            curve[i][j] = ' '
        print
