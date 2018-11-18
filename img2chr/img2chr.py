# coding: utf8
import cv2 as cv
# 替换字符列表
ascii_char = list(r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
char_len = len(ascii_char)
# 读取图片
frame = cv.imread("img.jpg")
# 转灰度图
img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
# 缩小图片并调整长宽比
img_resize = cv.resize(img_gray, (int(img_gray.shape[0] / 5), int(img_gray.shape[1] / 20)))

text = ''
# 遍历图片中的像素
for row in img_resize:
    for pixel in row:
        # 根据像素值，选取对应的字符
        text += ascii_char[int(pixel / 256 * char_len)]
    text += '\n'
# 输出生成的字符方阵
print(text)


