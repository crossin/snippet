# coding: utf-8
import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image,ImageFont,ImageDraw

# 获取前景方法
def get_fore(img):
    shape = img.shape[:]
    # 缩小图片
    img = cv2.resize(img,(int(img.shape[1] / 8), int(img.shape[0] / 8)), interpolation=cv2.INTER_CUBIC)
    # 创建空的蒙版
    mask = np.zeros(img.shape[:2],np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    # 判断范围限定
    rect = (10, 10, img.shape[1]-10, img.shape[0]-10)
    try:
        # 前景提取，结果保存在 mask 中
        cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    except:
        pass
    # 对蒙版进行着色、放大处理
    mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    mask = cv2.resize(mask,(shape[1], shape[0]))
    return mask

img = cv2.imread('jljt.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

font = ImageFont.truetype('../zhaozi.ttf', 60)
im = Image.fromarray(img)

draw = ImageDraw.Draw(im)
draw.text((300, 200), '你尽管写代码', '#600', font=font)
draw.text((300, 300), '运行的起来算我输', '#060', font=font)
draw.text((300, 400), 'Crossin的编程教室', '#006', font=font)
draw.text((300, 500), '每天5分钟，轻松学编程', '#606', font=font)

# 添加了弹幕的图像
# chrimg = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
plt.figure(figsize=(16,9))
plt.subplot(2, 2, 1)
plt.imshow(im)
plt.axis('off')
plt.title('barrage')

# 前景蒙版
mask = get_fore(img)
plt.subplot(2, 2, 2)
plt.imshow(mask)
plt.axis('off')
plt.title('mask')

# 前景
img_fore = img * mask[:,:,np.newaxis]
plt.subplot(2, 2, 3)
plt.imshow(img_fore)
plt.axis('off')
plt.title('foreground')

# 合成
img = im * (1-mask)[:,:,np.newaxis] + img * mask[:,:,np.newaxis]
plt.subplot(2, 2, 4)
plt.imshow(img)
plt.axis('off')
plt.title('result')

plt.show()
