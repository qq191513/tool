# -*- coding: utf-8 -*-
import os
import cv2

def create_new_route(file,size):
    # work:传入一个文件的完整路径，返回新的目标路径和无后缀文件名
    file = file.split('/') #切开
    first_name = file[0]
    first_name = first_name + '_{}x{}'.format(size,size)  #改名
    file[0] =first_name
    file_name = file[-1]  #取最后一个名字
    file_name = file_name.split('.')[0]  # 切开取第0个
    file.pop(-1)  # 删除
    new_route = '/'.join(file) #重连
    if not os.path.exists(new_route):
        cmd = 'mkdir -p ' + new_route
        os.system(cmd)
    return new_route,file_name

def get_files_list(path):
    # work：获取所有文件的完整路径
    files_list = []
    for parent,dirnames,filenames in os.walk(path):
        for filename in filenames:
            files_list.append(os.path.join(parent,filename))
    return files_list

def resize_pic_and_save(file,size= 32):
    new_route, file_name = create_new_route(file,size)
    file_name = file_name + '.jpg'
    pic = cv2.imread(file)
    pic = cv2.resize(pic, (size, size), interpolation=cv2.INTER_CUBIC)
    save_new_route = os.path.join(new_route,file_name)
    cv2.imwrite(save_new_route,pic)
    print(save_new_route)

path = r'asl_dataset'
#获取所有图片文件
files_list = get_files_list(path)
#一个个resize图片
for file in files_list:
    resize_pic_and_save(file,size= 32)
