#preprocess_data_tf.py 这种tensorflow版本的预处理方式也只能一张张图片处理，不能同时预处理图像分割的image和Mask


##########################   要改的东西   #######################################
#预处理方式
# to_random_brightness = True
# to_random_contrast = True
# to_resize_images = True
# resize_size =[1280,1918]
# to_random_crop = False
# crop_size = [28, 28, 1]
#######################     end     #############################################
import tensorflow as tf
import numpy as np


def distort_color(image, color_ordering=0):
    if color_ordering == 0:
        image = tf.image.random_brightness(image, max_delta=32. / 255.)  # 亮度
        image = tf.image.random_saturation(image, lower=0.5, upper=1.5)  # 饱和度
        image = tf.image.random_hue(image, max_delta=0.2)               # 色相
        image = tf.image.random_contrast(image, lower=0.5, upper=1.5)  # 对比度
    if color_ordering == 1:
        image = tf.image.random_saturation(image, lower=0.5, upper=1.5)# 饱和度
        image = tf.image.random_hue(image, max_delta=0.2)               # 色相
        image = tf.image.random_contrast(image, lower=0.5, upper=1.5)   # 对比度
        image = tf.image.random_brightness(image, max_delta=32. / 255.)  # 亮度
    if color_ordering == 2:
        image = tf.image.random_hue(image, max_delta=0.2)                 # 色相
        image = tf.image.random_contrast(image, lower=0.5, upper=1.5)   # 对比度
        image = tf.image.random_brightness(image, max_delta=32. / 255.)  # 亮度
        image = tf.image.random_saturation(image, lower=0.5, upper=1.5)  # 饱和度
    if color_ordering == 3:
        image = tf.image.random_contrast(image, lower=0.5, upper=1.5)    # 对比度
        image = tf.image.random_brightness(image, max_delta=32. / 255.)   # 亮度
        image = tf.image.random_saturation(image, lower=0.5, upper=1.5)   # 饱和度
        image = tf.image.random_hue(image, max_delta=0.2)                   # 色相
    return tf.clip_by_value(image, 0.0, 1.0)


def preprocess_for_train(image, height, width):
    image = tf.image.convert_image_dtype(image, dtype=tf.float32)    #归一化
    image = tf.image.resize_images(image, [width,height], method=np.random.randint(4))
    distorted_image = tf.image.random_flip_left_right(image)       #随机左右
    distorted_image = distort_color(distorted_image, np.random.randint(4))  #处理颜色
    return distorted_image
