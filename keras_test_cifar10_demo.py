'''
###################     说明    ###############################
这里安装的是关于GPU版本的TensorFlow，如果安装CPU版本，
那么就不需要关系安装顺序和方法了，
这里主要考虑到cuda和cudnn以及后面Keras和TensorFlow匹配的问题，
这里在安装TensorFlow-GPU时，会安装指定版本的cuda和cudnn，
一定要注意下这两个的安装版本是否适配当前的nvidia驱动，
否则在后面调用TensorFlow时会出现问题
这里需要使用pip来安装Keras，如果使用conda来安装的话，
conda可能会给你安装一个新的TensorFlow版本，所以需要使用pip来进行安装，
这样keras就会使用上面安装的TensorFlow来作为backend
搜索conda能够安装对应包的哪些版本  conda search cudnn
###################     end    ##############################

运行前安装以下库
conda create -n keras_test python=3.5
vim ~/.bashrc
source activate keras_testy
conda tensorflow-gpu==1.5
pip install keras==2.2.2
conda install pydot
conda install graphviz
sudo apt-get install graphviz
windows端打开Xming
远程pycharm的environment variables填写DISPLAY和localhost:10.0
'''


import sys
import time
from keras.datasets import cifar10
from keras.layers import Convolution2D, MaxPooling2D, AveragePooling2D
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.models import Sequential
from keras.optimizers import SGD
from keras.utils import np_utils
from keras.utils.vis_utils import plot_model
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session


#########################   使用GPU  动态申请显存占用 ####################
# 1、使用allow_growth option，刚一开始分配少量的GPU容量，然后按需慢慢的增加，由于不会释放内存，所以会导致碎片
# 2、visible_device_list指定使用的GPU设备号；
# 3、allow_soft_placement如果指定的设备不存在，允许TF自动分配设备（这个设置必须有，否则无论如何都会报cudnn不匹配的错误）
# 4、per_process_gpu_memory_fraction  指定每个可用GPU上的显存分配比
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
session_config = tf.ConfigProto(
            device_count={'GPU': 0},
            gpu_options={'allow_growth': 1,
                # 'per_process_gpu_memory_fraction': 0.1,
                'visible_device_list': '0'},
                allow_soft_placement=True) #这个设置必须有，否则无论如何都会报cudnn不匹配的错误

sess = tf.Session(config=session_config)
KTF.set_session(sess)

#########################   END   ####################################

#########################   使用GPU  固定显存 ########################

# import tensorflow as tf
# from keras.backend.tensorflow_backend import set_session
# config = tf.ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0.4
# set_session(tf.Session(config=config))

#########################   END   ####################################


#########################   CPU 充分使用  ##############################

# num_cores = 4
# config = tf.ConfigProto(intra_op_parallelism_threads=num_cores, inter_op_parallelism_threads=num_cores,
#                         allow_soft_placement=True, device_count={'CPU': 4})
# session = tf.Session(config=config)
# KTF.set_session(session)

#########################   END   ####################################

# 开始下载数据集
t0 = time.time()  # 打开深度学习计时器
# CIFAR10 图片数据集
(X_train, Y_train), (X_test, Y_test) = cifar10.load_data()  # 32×32

X_train = X_train.astype('float32')  # uint8-->float32
X_test = X_test.astype('float32')
X_train /= 255  # 归一化到0~1区间
X_test /= 255
print('训练样例:', X_train.shape, Y_train.shape,
      ', 测试样例:', X_test.shape, Y_test.shape)


nb_classes = 10  # label为0~9共10个类别
# Convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(Y_train, nb_classes)
Y_test = np_utils.to_categorical(Y_test, nb_classes)
print("取数据耗时: %.2f seconds ..." % (time.time() - t0))


###################
# 1. 建立CNN模型
###################
print("开始建模CNN ...")
model = Sequential()  # 生成一个model
model.add(Convolution2D(
    32, 3, 3, border_mode='valid', input_shape=X_train.shape[1:]))  # C1 卷积层
model.add(Activation('relu'))  # 激活函数：relu, tanh, sigmoid

model.add(Convolution2D(32, 3, 3))  # C2 卷积层
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))  # S3 池化
model.add(Dropout(0.25))  # 


model.add(Convolution2D(64, 3, 3, border_mode='valid')) # C4
model.add(Activation('relu'))


model.add(Convolution2D(64, 3, 3)) # C5
model.add(Activation('relu'))
model.add(AveragePooling2D(pool_size=(2, 2)))  # S6
model.add(Dropout(0.25))


model.add(Flatten())  # bottleneck 瓶颈
model.add(Dense(512))  # F7 全连接层, 512个神经元
model.add(Activation('relu'))  # 
model.add(Dropout(0.5))


model.add(Dense(nb_classes))  # label为0~9共10个类别
model.add(Activation('softmax'))  # softmax 分类器
model.summary() # 模型小节
print("建模CNN完成 ...")

###################
# 2. 训练CNN模型
###################
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(
    loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
plot_model(model, to_file='model1.png', show_shapes=True)  # 画模型图


model.fit(X_train, Y_train, batch_size=100, nb_epoch=50,
          validation_data=(X_test, Y_test))  # 81.34%, 224.08s
Y_pred = model.predict_proba(X_test, verbose=0)  # Keras预测概率Y_pred
print(Y_pred[:3, ])  # 取前三张图片的十类预测概率看看
score = model.evaluate(X_test, Y_test, verbose=0) # 评估测试集loss损失和精度acc
print('测试集 score(val_loss): %.4f' % score[0])  # loss损失
print('测试集 accuracy: %.4f' % score[1]) # 精度acc
print("耗时: %.2f seconds ..." % (time.time() - t0))