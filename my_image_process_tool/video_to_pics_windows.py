# -*- coding: utf-8 -*-
import os
import cv2
# import sys
# sys.path.append('./')
import numpy as np
cwd = os.getcwd()

####################################### 改这里 ##################################
path = r'..\\my_video'
# new_route =r'../my_video_imgs'
save_frequency = 1  #没多少帧保存一次
show_interval_ms = 50  #显示快慢
rot90_number = 1  #视频画面旋转多少次90度
####################################### end ####################################


def create_new_route(file):
    # work:传入一个文件的完整路径(../../../xxx.mp4)，返回新的目标路径
    sep = os.path.sep
    file = file.split(sep) #切开
    first_name = file[0]
    file[0] =first_name
    file_name = file[-1]  #取最后一个名字
    file_name = file_name.split('.')[0]  # 切开取第0个
    file.pop(-1)  # 删除xxx.mp4
    file[-1] = file[-1] + '_new' # 起个新名字
    file.append(file_name)
    new_route = sep.join(file) #重连
    if not os.path.exists(new_route):
        os.makedirs(new_route,exist_ok=True)
    return new_route


def get_files_list(path):
    # work：获取所有文件的完整路径
    files_list = []
    for parent,dirnames,filenames in os.walk(path):
        for filename in filenames:

            files_list.append(os.path.join(cwd,parent,filename))
    return files_list

def mp4_to_image(file,new_route,show_interval_ms,save_frequency):
    # work：MP4转图片
    index = 0
    cap = cv2.VideoCapture(file)

    while cv2.waitKey(show_interval_ms) != ord('q'):
        retval, image = cap.read()
        if retval:
            if index % save_frequency == 0:
                new_pic_name = os.path.join(new_route,'{}.jpg'.format(index))
                # save_pic_name = os.path.join(new_route,new_pic_name)
                image = np.rot90(image,rot90_number)
                cv2.imshow("video", image)
                cv2.imwrite(new_pic_name,image)
                print(new_pic_name)
            index += 1
        else:
            print('No frame')
            return
    cap.release()


#获取所有MP4文件
files_list = get_files_list(path)
#视频转图片
for file in files_list:
    print(file)
    new_route = create_new_route(file)
    os.makedirs(new_route, exist_ok=True)
    mp4_to_image(file,new_route,show_interval_ms = show_interval_ms,save_frequency = save_frequency)