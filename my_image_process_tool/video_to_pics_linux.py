# -*- coding: utf-8 -*-
import os
import cv2

def create_new_route(file):
    # work:传入一个文件的完整路径，返回新的目标路径和无后缀文件名
    file = file.split('/') #切开
    first_name = file[0]
    first_name = first_name + '_imgs'  #改名
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

def mp4_to_image(file,show_interval_ms,save_frequency):
    # work：MP4转图片
    index = 0
    cap = cv2.VideoCapture(file)
    new_route, file_name = create_new_route(file)
    while cv2.waitKey(show_interval_ms) != ord('q'):
        retval, image = cap.read()
        if retval:
            if index % save_frequency == 0:
                new_pic_name = file_name + '_{}.jpg'.format(index)
                save_pic_name = os.path.join(new_route,new_pic_name)
                cv2.imshow("video", image)
                cv2.imwrite(save_pic_name,image)
                print(save_pic_name)
            index += 1
        else:
            break
    cap.release()

path = r'test_vedio'
#获取所有MP4文件
files_list = get_files_list(path)
#视频转图片
for file in files_list:
    print(file)
    mp4_to_image(file,show_interval_ms = 30,save_frequency = 10)
