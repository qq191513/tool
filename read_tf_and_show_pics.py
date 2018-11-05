import tensorflow as tf
import cv2

##########################要改的东西#######################################
#tfrecords文件的路径
train_record = 'asl_tf/asl_train_00000-of-00001.tfrecord'

# 填入解码键值
example_name = {}
example_name['image'] = 'image/encoded'  #主要是这个(原图)p
example_name['label'] = 'image/class/label' #主要是这个(标签)
reshape_size =(32,32,1)
###########################################################################

def ReadTFRecord(tfrecords,example_name):
    # 可以把多个tfrecords排成一个queue,这样可以方便的使用多个tfrecords文件
    record_queue = tf.train.string_input_producer([tfrecords])
    # 读取TFRecords器
    reader = tf.TFRecordReader()
    # 一个数据一个数据的读返回key-value值,都保存在serialized_ex中
    # 注意: 这里面keys是序列化的副产物,命名为tfrecords+random(),表示唯一的ID,没有作用,可以设置为_
    #keys, serialized_ex = reader.read(record_queue)
    _, serialized_ex = reader.read(record_queue)
    # 直接解析出features数据,并且使用固定特征长度,及每个Example中一定会存在一个image和一个label
    # 并不是输入的图片大小不同就使用VarLenFeature.
    # parse_single_example意思是，后面每次sess.run就是输出一张图片，而不是一个batch_size
    features = tf.parse_single_example(serialized_ex,
            features={
                # 取出key为img_raw和label的数据,尤其是int位数一定不能错!!!
                example_name['image']: tf.FixedLenFeature([],tf.string),
                example_name['label']: tf.FixedLenFeature([], tf.int64)
            })
    img = tf.decode_raw(features[example_name['image']], tf.uint8)

    # 注意定义的为int多少位就转换成多少位,否则容易出错!!
    label = tf.cast(features[example_name['label']], tf.int64)
    return img, label

imgs,labels = ReadTFRecord(train_record,example_name)
if len(reshape_size) == 2:
    w,h = reshape_size
else:
    w,h,c = reshape_size
# with tf.Session() as sess:  # 开始一个会话
sess = tf.Session()
coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)
# 输出100个样本
for i in range(100):
    image,label = sess.run([imgs,labels])
    if len(reshape_size) == 2:
        image = image.reshape(w, h)
    else:
        image = image.reshape(w, h, c)
    print(image.shape,'label:', label)
    cv2.namedWindow('label:{}'.format(label),0)
    cv2.startWindowThread()
    cv2.imshow('label:{}'.format(label),image)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()

coord.request_stop()
coord.join(threads)
