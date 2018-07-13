import h5py
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib

def look_keys(h5py_file):
    #查看h5文件到底有哪些键值
    for key in h5py_file.keys():
        print('#################################')
        print('key: ',h5py_file[key].name)
        print('key shape : ',h5py_file[key].shape)
        # print('key value : ',train_dataset[key].value)
        print('#################################')

def h5py_to_numpy(train_dataset):
    hh = train_dataset['train_set_x'][:]
    hhd = train_dataset['train_set_x']
    train_imgs = np.array(train_dataset['train_set_x'][:])
    train_labels = np.array(train_dataset['train_set_y'][:])
    train_labels = train_labels.reshape((1, train_labels.shape[0]))


    test_dataset = h5py.File('dataset/test_signs.h5', 'r')
    test_imgs = np.array(test_dataset['test_set_x'][:])
    test_labels = np.array(test_dataset['test_set_y'][:])
    test_labels = test_labels.reshape((1, test_labels.shape[0]))

    classes = np.array(test_dataset['list_classes'][:])
    # train_labels = encode_one_hot(train_labels, len(classes))
    # test_labels = encode_one_hot(test_labels, len(classes))

    return train_imgs, test_imgs, train_labels, test_labels, classes


def numpy_to_pics(train_imgs, train_labels, output_dir):
    for each in range(train_imgs.shape[0]):
        img = train_imgs[each, :]
        label = train_labels[:, each]
        # print('img',img)
        print('label', label)

        save_dir = os.path.join(output_dir, str(label[0]))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_dir = os.path.join(save_dir, '{}.jpg'.format(each))

        # plt.image.imsave(save_dir, img)
        matplotlib.image.imsave(save_dir, img)


#1、取h5文件对象
train_dataset = h5py.File('dataset/train_signs.h5', 'r')

#2、如果不知道键值，查看h5文件到底有哪些键值
look_keys(train_dataset)

#3、h5py转numpy的array
train_imgs, test_imgs, train_labels, test_labels, classes = h5py_to_numpy(train_dataset)

#4、输出路径
output_dir_train = 'out_imgs_train'
output_dir_test = 'out_imgs_test'

#5、array转图片，文件全部输出到文件夹output_dir中，train_labels作为中不同种类的文件夹
numpy_to_pics(train_imgs,train_labels,output_dir_train)
numpy_to_pics(test_imgs,test_labels,output_dir_test)




