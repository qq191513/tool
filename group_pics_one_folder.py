from PIL import Image, ImageDraw
import os
import re
####################################### 改这里 ###################################################################
image_path = os.path.join('F:/Test/Py_test/py35_windows/predict_tensor_feature_map_merge' )# 图片集目录地址
image_size_h = 512    #将要把每张小图片resize成的大小
image_size_w = image_size_h*8   # 将要把每张小图片resize成的大小
image_row = 15  # 图片间隔，也就是合并成一张图后，一共有几行
image_column = 1  # 图片间隔，也就是合并成一张图后，一共有几列
image_save_path =os.path.join(image_path,'../','merge.jpg')  # 图片转换后的图片
####################################### end ######################################################################

####################################### 改这里 ###################################################################
# image_path_1='4_2'  #让最终保存的图片名字为文件夹的名字
# image_path = os.path.join('F:/Test/Py_test/py35_windows/predict_tensor_feature_map/u_cap3_5', image_path_1 )# 图片集目录地址
# image_size_w = 256   # 将要把每张小图片resize成的大小
# image_size_h = 256    #将要把每张小图片resize成的大小
# image_row = 4  # 图片间隔，也就是合并成一张图后，一共有几行
# image_column = 4  # 图片间隔，也就是合并成一张图后，一共有几列
# image_save_path =os.path.join(image_path,'../',image_path_1+'.jpg')  # 图片转换后的图片
# ####################################### end ######################################################################

image_format = ['.jpg', '.JPG', '.png']  # 图片格式
# 获取图片集地址下的所有图片名称
image_names = [name for name in os.listdir(image_path) for item in image_format if
               os.path.splitext(name)[1] == item]



re_digits = re.compile(r'(\d+)')


def embedded_numbers(s):
    pieces = re_digits.split(s)  # 切成数字和非数字
    pieces[1::2] = map(int, pieces[1::2])  # 将数字部分转成整数
    return pieces


def sort_string(lst):
    return sorted(lst, key=embedded_numbers)  # 将前面的函数作为key来排序

# Python根据内嵌的数字将字符串来排序，如"file2.txt file11.txt file8.txt file5.txt"
# 排列成"file2.txt file5.txt file8.txt file11.txt"
# 因为Python默认的字符串排序是基于字符ASCII来排序的
image_names= sort_string(image_names)
print(' '.join(image_names))


# .sort()

# 简单的对于参数的设定和实际图片集的大小进行数量判断
if len(image_names) != image_row * image_column:
    raise ValueError("合成图片的参数和要求的数量不能匹配！")


# 给左上角写标注
def write_label_in_left():
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, image_row + 1):
        for x in range(1, image_column + 1):
            img = Image.open(os.path.join(image_path, image_names[image_column * (y - 1) + x - 1])).resize(
                (image_size_w, image_size_h), Image.ANTIALIAS)

            # 给图片左上角写个标注
            label = image_names[image_column * (y - 1) + x - 1].split('.')[0]  #把label作为要写的文字
            from_image = ImageDraw.Draw(img)  # 修改图片
            from_image.text((2, 2), label,fill=(255,255,255))  # 利用ImageDraw的内置函数，在图片上写入文字
            img.show()
            save_new_path =image_path+'_new'
            img.save(os.path.join(save_new_path,label+'.jpg'))
    return save_new_path

# 生成格子
def generate_grid(rows_cell,cols_cell):
    line_list = []
    # 横线
    for line in range(1,rows_cell):

        x_start = 0
        y_start = line*image_size_h

        x_end = rows_cell*image_size_h
        y_end = line*image_size_h

        line_list.append((x_start,y_start,x_end,y_end))

    #竖线
    for line in range(1,cols_cell):
        x_start = line*image_size_w
        y_start = 0

        x_end = line*image_size_w
        y_end = cols_cell*image_size_w

        line_list.append((x_start, y_start, x_end, y_end))

    return line_list

# 画格子函数
def image_draw_line(img,rows_cell, cols_cell):
    from_image = ImageDraw.Draw(img)  # 修改图片

    # 返回生成的线条
    line_list = generate_grid(rows_cell, cols_cell)

    # 一条条画出来
    for line in line_list:
        from_image.line(line, fill = 128)
    return img

# 定义图像拼接函数
def image_concact(image_path):
    to_image = Image.new('RGB', (image_column * image_size_w, image_row * image_size_h))  # 创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, image_row + 1):
        for x in range(1, image_column + 1):

            img = Image.open(os.path.join(image_path,image_names[image_column * (y - 1) + x - 1])).resize(
                (image_size_w, image_size_h), Image.ANTIALIAS)
            to_image.paste(img, ((x - 1) * image_size_w, (y - 1) * image_size_h))

    # 把拼接好的图进行划线
    to_image = image_draw_line(to_image, rows_cell = image_row, cols_cell = image_column)

    to_image.show()  #远程Image的显示像cv2一样要打开Xming才行
    to_image.save(image_save_path)  # 保存新图
    # time.sleep(3)

# 给左上角写标注
# save_new_path = write_label_in_left()
# image_path =save_new_path
# 调用函数
image_concact(image_path)