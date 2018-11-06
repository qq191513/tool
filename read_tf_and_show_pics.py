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
    # [tfrecords]为文件列表
    record_queue = tf.train.string_input_producer([tfrecords],
        shuffle=False, num_epochs=5)
    # eg :  tf.train.string_input_producer(['a.txt','b.txt'])
    # 如果仅有一个文件名，其实就没必要使用此函数了，
    # shuffle = False意味着让文件名洗乱，num_epochs=5让每个文件被使用5次
    # 返回：文件队列queue
    # 后面配合tf.TFRecordReader()函数使用

    # 区别：输入队列tf.train.slice_input_producer
    # 功能：分割和读取输入的数据集,传入图片路径，函数返回张量队列queue
    # 使用前需要将features和labels包装成tensorflow的tensor对象
    # imgpath=tf.convert_to_tensor(imgpath)），其中input_data为'*.jpg'、'*.bmp'等路径的图片
    # tf.train.slice_input_producer([imgpath, label_tensor], num_epochs, shuffle, capacity)
    # 后面配合函数tf.read_file和tf.train.batch使用
    # 如：
    # reader = tf.read_file(queues[0][0])
    # image = tf.image.decode_jpeg(reader)
    # label = queues[0][1]
    # image_batch, label_batch = tf.train.batch([image, label], batch_size=100, capacity=100, num_threads=1)




    reader = tf.TFRecordReader()
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

# 使用tf.train.start_queue_runners之后，
# 才会启动填充队列的线程，这时系统就不再“停滞”。
# 此后计算单元就可以拿到数据并进行计算，
# 整个程序也就跑起来了，这就是函数tf.train.start_queue_runners的用处。
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
