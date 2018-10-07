#encoding:utf-8
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

dir = './'
# 1.Import data
mnist = input_data.read_data_sets(dir, one_hot=True)
# print data information
print (mnist.train.images.shape, mnist.train.labels.shape)
print(mnist.test.images.shape, mnist.train.labels.shape)
print(mnist.validation.images.shape, mnist.validation.labels.shape)

# 2.Create the model
x = tf.placeholder(tf.float32, [None, 784])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
y = tf.matmul(x, W) + b  # y=wx+b

# Define loss and optimizer
y_ = tf.placeholder(tf.float32, [None, 10])

cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

# Init model
sess = tf.InteractiveSession()
tf.global_variables_initializer().run()
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
# Train
for i in range(10000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
    if (i % 100 == 0):
        print(i,sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

# Test trained model
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
