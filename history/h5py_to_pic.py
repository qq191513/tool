import h5py
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

import matplotlib



import os
def encode_one_hot(labels, c):
    c = tf.constant(c, name='c')

    # print(labels.shape)
    one_hot = tf.one_hot(labels, c, axis=-1)

    with tf.Session() as sess:
        encode = sess.run(one_hot)

    # print(encode.shape)
    return encode.reshape(encode.shape[1], encode.shape[2])

def look_keys(h5py_file):
    #查看h5文件到底有哪些键值
    for key in h5py_file.keys():
        print('#################################')
        print('key: ',h5py_file[key].name)
        print('key shape : ',h5py_file[key].shape)
        # print('key value : ',train_dataset[key].value)
        print('#################################')

def load_h5_dataset(train_dataset):



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


#1、取h5文件对象
train_dataset = h5py.File('dataset/train_signs.h5', 'r')

#2、查看h5文件到底有哪些键值
look_keys(train_dataset)

#3、取值
train_imgs, test_imgs, train_labels, test_labels, classes = load_h5_dataset(train_dataset)

print('###')

# matplotlib.image.imsave('name.png', array)

output_dir = 'out_imgs'
fig = plt.gcf()
for each in range(train_imgs.shape[0]):
    img = train_imgs[each,:]
    label = train_labels[:,each]
    # print('img',img)
    print('label',label)

    save_dir = os.path.join(output_dir,str(label[0]))
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_dir = os.path.join(save_dir,'{}.png'.format(each))

    # plt.image.imsave(save_dir, img)
    matplotlib.image.imsave(save_dir, img)








