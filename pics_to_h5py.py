import numpy as np
import matplotlib.pyplot as plt
import h5py
import random
import os

def get_pics_labels_file_list(where):
    pics_list = []
    dirs =os.listdir(where)  #列出路径where下的每个文件夹
    for dir in dirs:
        dir_path = os.path.join(where, dir)
        pics = os.listdir(dir_path)  #列出该文件夹下的所有图片
        for pic in pics:
            file_path = os.path.join(dir_path, pic)
            label = dir   #dir的名称即为标签
            pics_list.append(file_path +' '+ label) #都放入列表pics_list中，用空格隔开图片和label

    #疯狂洗乱列表所有图片
    random.shuffle(pics_list)
    random.shuffle(pics_list)
    random.shuffle(pics_list)
    return pics_list


def get_pics_labels_array(pics_list):
    fist_flag = True
    for index,pic_and_label in enumerate(pics_list):
        pic,lable = pic_and_label.split(' ')   #按空格分开图片和label
        pic_array = np.array(plt.imread(pic))  #读图并变成np格式
        pic_array = pic_array[np.newaxis,:]    #插入一个新维度，用来合并，即由（64，64，3）变（1，64，64，3）
        lable_array = np.array([int(lable)])

        if fist_flag == True:   #if里面仅仅是为了方便后面np.concatenate
            pics_array = pic_array    #数组pics_np作为存放所有图片的array
            lables_array = lable_array  #数组lables_array作为存放所有图片的label
            fist_flag = False
            continue
        pics_array = np.concatenate((pics_array, pic_array), axis=0)    #全部放到pics_array中
        lables_array = np.concatenate((lables_array, lable_array), axis=0)  #全部放到lables_array中
        print(index)
    return pics_array,lables_array

def save_h5py(pics_array,lables_array,output_h5py_file):
    h5py_file = h5py.File(output_h5py_file, 'w')
    h5py_file.create_dataset('train_data', data=pics_array)
    h5py_file.create_dataset('train_label', data=lables_array)
    h5py_file.close()



output_h5py_file = 'fuck.h5'
pics_list =get_pics_labels_file_list('out_imgs')
pics_array,lables_array = get_pics_labels_array(pics_list)
save_h5py(pics_array,lables_array,output_h5py_file)

