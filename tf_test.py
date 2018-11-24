# coding:utf-8
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import os
from six.moves import urllib

#文件名
dir = 'mnist_data'
TRAIN_IMAGES = 'train-images-idx3-ubyte.gz'
TRAIN_LABELS = 'train-labels-idx1-ubyte.gz'
TEST_IMAGES = 't10k-images-idx3-ubyte.gz'
TEST_LABELS = 't10k-labels-idx1-ubyte.gz'

#路径
if not os.path.exists(dir):
    os.system('mkdir mnist_data')

#下载数据集
def maybe_download(filename, work_directory):
    SOURCE_URL = 'http://yann.lecun.com/exdb/mnist/'
    if not os.path.exists(work_directory):
        os.mkdir(work_directory)
    filepath = os.path.join(work_directory, filename)
    if not os.path.exists(filepath):
        filepath, _ = urllib.request.urlretrieve(SOURCE_URL + filename, filepath)
        statinfo = os.stat(filepath)
        print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')
    return filepath
local_file = maybe_download(TRAIN_IMAGES, dir)
local_file = maybe_download(TRAIN_LABELS, dir)
local_file = maybe_download(TEST_IMAGES, dir)
local_file = maybe_download(TEST_LABELS, dir)

#读取数据集
mnist = input_data.read_data_sets(dir, one_hot=True)

print(mnist.train.images.shape, mnist.train.labels.shape)
print(mnist.test.images.shape, mnist.train.labels.shape)
print(mnist.validation.images.shape, mnist.validation.labels.shape)

# Create the model
x = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, [None, 10])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
pred = tf.matmul(x, W) + b  # y=wx+b

# Define loss and optimizer
cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=pred))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)


# 1、使用allow_growth option，刚一开始分配少量的GPU容量，然后按需慢慢的增加，由于不会释放内存，所以会导致碎片
# 2、visible_device_list指定使用的GPU设备号；
# 3、allow_soft_placement如果指定的设备不存在，允许TF自动分配设备（这个设置必须有，否则无论如何都会报cudnn不匹配的错误）
# 4、per_process_gpu_memory_fraction  指定每个可用GPU上的显存分配比
session_config = tf.ConfigProto(
            device_count={'GPU': 0},
            gpu_options={'allow_growth': 1,
                # 'per_process_gpu_memory_fraction': 0.1,
                'visible_device_list': '0'},
                allow_soft_placement=True)  ##这个设置必须有，否则无论如何都会报cudnn不匹配的错误,BUG十分隐蔽，真是智障
sess = tf.Session(config=session_config)
sess.run(tf.global_variables_initializer())
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(pred, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Train loop
for i in range(100000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y: batch_ys})
    if (i % 100 == 0):
        print(i, sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels}))

# Test trained model
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels}))