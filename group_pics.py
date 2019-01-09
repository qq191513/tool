from PIL import Image, ImageDraw, ImageFont

import os
import cv2
IMAGES_PATH = '/home/mo/work/caps_face/Matrix-Capsules-EM-Tensorflow-master/data/group'  # 图片集地址
IMAGES_FORMAT = ['.jpg', '.JPG']  # 图片格式
IMAGE_SIZE = 32  # 每张小图片的大小
IMAGE_ROW = 6  # 图片间隔，也就是合并成一张图后，一共有几行
IMAGE_COLUMN = 6  # 图片间隔，也就是合并成一张图后，一共有几列
IMAGE_SAVE_PATH = 'final.jpg'  # 图片转换后的地址
# ttfont = ImageFont.truetype('simhei.ttf', 10)  # 字体大小
# font = cv2.FONT_HERSHEY_SIMPLEX  # 使用默认字体

import numpy as np
# 获取图片集地址下的所有图片名称
image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
               os.path.splitext(name)[1] == item]

# 简单的对于参数的设定和实际图片集的大小进行数量判断
if len(image_names) != IMAGE_ROW * IMAGE_COLUMN:
    raise ValueError("合成图片的参数和要求的数量不能匹配！")


# 定义图像拼接函数
def image_compose():
    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE))  # 创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            img = Image.open(os.path.join(IMAGES_PATH,image_names[IMAGE_COLUMN * (y - 1) + x - 1])).resize(
                (IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
            label = image_names[IMAGE_COLUMN * (y - 1) + x - 1].split('.')[0]
            # 1、 先让图片左上角写个标注
            from_image = ImageDraw.Draw(img)  # 修改图片
            from_image.text((2, 2), label,fill=(255,255,255))  # 利用ImageDraw的内置函数，在图片上写入文字
            # img.show()
            # img.save(os.path.join('new',label+'.jpg'))
            # 2、 保存成一张大图
            to_image.paste(img, ((x - 1) * IMAGE_SIZE, (y - 1) * IMAGE_SIZE))

    to_image.show()
    return to_image.save(IMAGE_SAVE_PATH)  # 保存新图


image_compose()  # 调用函数
