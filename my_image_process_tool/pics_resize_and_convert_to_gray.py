# -*- coding: utf-8 -*-
import os
import cv2

##########################要改的东西#######################################
path = r'..\\my_video_new'
reshape_size =(224,224,3)
resize_pic = True
convert_to_gray = False
###########################################################################


def create_new_route(file,reshape_size,resize_pic,convert_to_gray):
    # work:传入一个文件的完整路径，返回新的目标路径和无后缀文件名
    sep = os.path.sep
    file = file.split(sep) #切开
    index = 0

    # 循环，找出file的头名字，用来等下起个新的名字
    while True:
        first_name = file[index]
        if '..' in first_name or first_name == '':
            index += 1
            continue
        first_name = file.pop(index)  #弹出file的头名字，避免等下重复起名字
        break


    if len(reshape_size) == 2:
        w, h = reshape_size
    else:
        w, h, c = reshape_size

    if convert_to_gray:
        first_name = first_name + '_gray'
    if resize_pic:
        first_name = first_name + '_{}x{}'.format(w, h)  #改名
    file[0] =first_name
    file_name = file[-1]  #取最后一个名字
    file_name = file_name.split('.')[0]  # 切开取第0个
    file.pop(-1)  # 删除
    new_route = sep.join(file) #重连
    if not os.path.exists(new_route):
        os.makedirs(new_route,exist_ok=True)
    return new_route,file_name

def get_files_list(path):
    # work：获取所有文件的完整路径
    files_list = []
    for parent,dirnames,filenames in os.walk(path):
        for filename in filenames:
            files_list.append(os.path.join(parent,filename))
    return files_list

def resize_pic_and_save(file,reshape_size= (32,32,1),resize_pic = True,convert_to_gray =True):
    if len(reshape_size) == 2:
        w, h = reshape_size
    else:
        w, h, c = reshape_size
    new_route, file_name = create_new_route(file,reshape_size,resize_pic,convert_to_gray)
    file_name = file_name + '.jpg'
    pic = cv2.imread(file)
    if resize_pic:  #是否resize图片
        pic = cv2.resize(pic, (w, h), interpolation=cv2.INTER_CUBIC)
    if convert_to_gray: #是否转成灰度图
        pic = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    save_new_route = os.path.join(new_route,file_name)
    cv2.imwrite(save_new_route,pic)
    print(save_new_route)



#获取所有图片文件
files_list = get_files_list(path)
#一个个resize图片和转成灰度图
for file in files_list:
    resize_pic_and_save(file,reshape_size= reshape_size,resize_pic = resize_pic,convert_to_gray = convert_to_gray)
