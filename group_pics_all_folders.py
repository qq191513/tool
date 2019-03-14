from PIL import Image, ImageDraw
import os
from random import shuffle
##### read me #####
#step 1、取所有层生成的各个文件夹，依次对每个文件随机取image_column张图片
#合成image_row行image_column列的图片，输出到新目录mage_path+'_merge'中
#step 2、将上一步新目录的图片再次合成大图
##### end #########

####################################### 改这里 ###################################################################
image_total_path = os.path.join('F:/Test/Py_test/py35_windows/predict_tensor_feature_map' )# 图片集总目录地址
image_size = 256  # 将要把每张小图片resize成的大小
image_row = 1  # 图片间隔，也就是合并成一张图后，一共有几行
image_column = 8  # 图片间隔，也就是合并成一张图后，一共有几列
image_save_path =os.path.join(image_total_path+'_merge_1')  # 图片转换后的图片
image_save_path_big_image =os.path.join(image_total_path+'_merge_2')  # 图片转换后的图片
# exclude_folder = ['L15_predict'] #不想生成的文件夹
exclude_folder = [''] #不想生成的文件夹
####################################### end ######################################################################
os.makedirs(image_save_path,exist_ok=True)

allpath = []
allname = []


def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)

def get_folder_pic_list(image_total_path,folder_need_to_merge,shuffle_pic):

    image_format = ['.jpg', '.JPG', '.png']  # 图片格式
    image_names_list = []
    # 获取图片集地址下的所有图片名称
    folder_need_to_merge_1 = os.path.join(image_total_path,folder_need_to_merge)
    list_name = []
    listdir(path=folder_need_to_merge_1, list_name=list_name)


    for pic in list_name:
        for item in image_format:
            if os.path.splitext(pic)[1] == item:
                image_names_list.append(pic)
    #打乱顺序
    if shuffle_pic == True:
        shuffle(image_names_list)
        shuffle(image_names_list)
        shuffle(image_names_list)
        shuffle(image_names_list)
    else:
        image_names_list.sort()
    #只要image_column*image_row张
    image_names_list = image_names_list[0:image_column*image_row]
    if len(image_names_list) != image_row * image_column:

        raise ValueError("文件夹{}只有{}张图片，合成图片的参数和要求的image_row * image_column数量不能匹配！".
                         format(folder_need_to_merge,len(image_names_list)))
    return image_names_list


# 给左上角写标注
def write_label_in_left(image_path,image_names):
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, image_row + 1):
        for x in range(1, image_column + 1):
            img = Image.open(os.path.join(image_path, image_names[image_column * (y - 1) + x - 1])).resize(
                (image_size, image_size), Image.ANTIALIAS)

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
        y_start = line*image_size

        x_end = rows_cell*image_size
        y_end = line*image_size

        line_list.append((x_start,y_start,x_end,y_end))

    #竖线
    for line in range(1,cols_cell):
        x_start = line*image_size
        y_start = 0

        x_end = line*image_size
        y_end = cols_cell*image_size

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
def image_concact(image_dir,image_names,image_save_path):
    to_image = Image.new('RGB', (image_column * image_size, image_row * image_size))  # 创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, image_row + 1):
        for x in range(1, image_column + 1):
            img = Image.open(os.path.join(image_names[image_column * (y - 1) + x - 1])).resize(
                (image_size, image_size), Image.ANTIALIAS)
            to_image.paste(img, ((x - 1) * image_size, (y - 1) * image_size))

    # 把拼接好的图进行划线
    to_image = image_draw_line(to_image, rows_cell = image_row, cols_cell = image_column)

    # to_image.show()  #远程Image的显示像cv2一样要打开Xming才行

    image_save_path = os.path.join(image_save_path,image_dir+'.jpg')
    to_image.save(image_save_path)  # 保存新图
    # time.sleep(3)

# 给左上角写标注
# save_new_path = write_label_in_left()
# image_path =save_new_path
# 调用函数
# image_concact(image_path)

#获取所有文件夹
image_dir_list = os.listdir(image_total_path)

# step 1
for image_dir in image_dir_list:
    for exclude in exclude_folder:
        if exclude == image_dir:
            continue
    #获取某个文件夹所有图片（每个图片是完整路径）
    image_names_list = get_folder_pic_list(image_total_path,image_dir,shuffle_pic=True)
    #拼接图片
    image_concact(image_dir=image_dir,image_names=image_names_list,image_save_path=image_save_path)

# step 2

image_names_list = get_folder_pic_list(image_save_path,image_dir,shuffle_pic=True)
image_concact(image_dir=image_dir,image_names=image_names_list,image_save_path=image_save_path_big_image)






