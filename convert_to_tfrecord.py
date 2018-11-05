import math
import os
import random
import sys

import tensorflow as tf

LABELS_FILENAME = 'labels.txt'
paramenmt_set = {}
example_name = {}

def int64_feature(values):
  if not isinstance(values, (tuple, list)):
    values = [values]
  return tf.train.Feature(int64_list=tf.train.Int64List(value=values))

def bytes_feature(values):
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[values]))

def float_feature(values):
  if not isinstance(values, (tuple, list)):
    values = [values]
  return tf.train.Feature(float_list=tf.train.FloatList(value=values))

def image_to_tfexample(example_name,image_data, image_format, height, width, class_id):
  return tf.train.Example(features=tf.train.Features(feature={
      example_name['encoded']: bytes_feature(image_data),
      example_name['format']: bytes_feature(image_format),
      example_name['label']: int64_feature(class_id),
      example_name['height']: int64_feature(height),
      example_name['width']: int64_feature(width),
  }))


def write_label_file(labels_to_class_names, dataset_dir,
                     filename=LABELS_FILENAME):
  labels_filename = os.path.join(dataset_dir, filename)
  with tf.gfile.Open(labels_filename, 'w') as f:
    for label in labels_to_class_names:
      class_name = labels_to_class_names[label]
      f.write('%d:%s\n' % (label, class_name))

def has_labels(dataset_dir, filename=LABELS_FILENAME):
  return tf.gfile.Exists(os.path.join(dataset_dir, filename))

def read_label_file(dataset_dir, filename=LABELS_FILENAME):
  labels_filename = os.path.join(dataset_dir, filename)
  with tf.gfile.Open(labels_filename, 'rb') as f:
    lines = f.read().decode()
  lines = lines.split('\n')
  lines = filter(None, lines)

  labels_to_class_names = {}
  for line in lines:
    index = line.index(':')
    labels_to_class_names[int(line[:index])] = line[index+1:]
  return labels_to_class_names

class ImageReader(object):
  def __init__(self):
    # Initializes function that decodes RGB JPEG data.
    self._decode_jpeg_data = tf.placeholder(dtype=tf.string)
    self._decode_jpeg = tf.image.decode_jpeg(self._decode_jpeg_data, channels=3)

  def read_image_dims(self, sess, image_data):
    image = self.decode_jpeg(sess, image_data)
    return image.shape[0], image.shape[1]

  def decode_jpeg(self, sess, image_data):
    image = sess.run(self._decode_jpeg,
                     feed_dict={self._decode_jpeg_data: image_data})
    assert len(image.shape) == 3
    assert image.shape[2] == 3
    return image

def _get_filenames_and_classes(dataset_dir):
  # flower_root = os.path.join(dataset_dir, 'flower_photos')
  directories = []
  class_names = []
  for filename in os.listdir(dataset_dir):
    path = os.path.join(dataset_dir, filename)
    if os.path.isdir(path):
      directories.append(path)
      class_names.append(filename)

  photo_filenames = []
  for directory in directories:
    for filename in os.listdir(directory):
      path = os.path.join(directory, filename)
      photo_filenames.append(path)

  return photo_filenames, sorted(class_names)


def _get_dataset_filename(paramenmt_set, split_name, shard_id):
  output_filename = paramenmt_set['dst_file']+ '_%s_%05d-of-%05d.tfrecord' % (
      split_name, shard_id, paramenmt_set['_NUM_SHARDS'])
  return os.path.join(paramenmt_set['dst_folder'], output_filename)

def _convert_dataset(example_name,split_name, filenames, class_names_to_ids, paramenmt_set):
  assert split_name in ['train', 'validation']

  num_per_shard = int(math.ceil(len(filenames) / float(paramenmt_set['_NUM_SHARDS'])))

  with tf.Graph().as_default():
    image_reader = ImageReader()

    with tf.Session() as sess:
      for shard_id in range(paramenmt_set['_NUM_SHARDS']):
        output_filename = _get_dataset_filename(
            paramenmt_set, split_name, shard_id)

        with tf.python_io.TFRecordWriter(output_filename) as tfrecord_writer:
          start_ndx = shard_id * num_per_shard
          end_ndx = min((shard_id+1) * num_per_shard, len(filenames))
          for i in range(start_ndx, end_ndx):
            sys.stdout.write('\r>> Converting image %d/%d shard %d' % (
                i+1, len(filenames), shard_id))
            sys.stdout.flush()

            # Read the filename:
            image_data = tf.gfile.FastGFile(filenames[i], 'rb').read()
            height, width = image_reader.read_image_dims(sess, image_data)

            class_name = os.path.basename(os.path.dirname(filenames[i]))
            class_id = class_names_to_ids[class_name]

            example = image_to_tfexample(
                example_name,image_data, b'jpg', height, width, class_id)
            tfrecord_writer.write(example.SerializeToString())

  sys.stdout.write('\n')
  sys.stdout.flush()

def _dataset_exists(dataset_dir):
  for split_name in ['train', 'validation']:
    for shard_id in range(paramenmt_set['_NUM_SHARDS']):
      output_filename = _get_dataset_filename(
          dataset_dir, split_name, shard_id)
      if not tf.gfile.Exists(output_filename):
        return False
  return True

def convert_pics_to_tfrecord(example_name,paramenmt_set):
  if not tf.gfile.Exists(paramenmt_set['dst_folder']):
    tf.gfile.MakeDirs(paramenmt_set['dst_folder'])

  # if _dataset_exists(paramenmt_set['dst']):
  #   print('Dataset files already exist. Exiting without re-creating them.')
  #   return

  photo_filenames, class_names = _get_filenames_and_classes(paramenmt_set['src'])
  class_names_to_ids = dict(zip(class_names, range(len(class_names))))

  # Divide into train and test:
  random.seed(paramenmt_set['_RANDOM_SEED'])
  random.shuffle(photo_filenames)
  random.shuffle(photo_filenames)
  random.shuffle(photo_filenames)
  training_filenames = photo_filenames[paramenmt_set['_NUM_VALIDATION']:]
  validation_filenames = photo_filenames[:paramenmt_set['_NUM_VALIDATION']]


  # First, convert the training and validation sets.
  _convert_dataset(example_name,'train', training_filenames, class_names_to_ids,
                   paramenmt_set)
  _convert_dataset(example_name,'validation', validation_filenames, class_names_to_ids,
                   paramenmt_set)

  # # Finally, write the labels file:
  labels_to_class_names = dict(zip(range(len(class_names)), class_names))
  write_label_file(labels_to_class_names, paramenmt_set['dst_folder'] )

  print('\nFinished converting the dataset!')


paramenmt_set['src'] = 'asl_dataset_gray_32x32'  #源图片集（双层文件夹）
paramenmt_set['dst_folder'] = 'asl_dataset_gray_32x32_tfrecord' #生成的目录
paramenmt_set['dst_file'] = 'asl' #生成的文件名

paramenmt_set['_NUM_VALIDATION'] = 350 #测试张数
paramenmt_set['_RANDOM_SEED'] = 33  #随机洗乱种子
paramenmt_set['_NUM_SHARDS'] = 1 #tfrecord分割块数

# example_name的名字，解码的时候要知道名字
example_name['encoded'] = 'image/encoded'  #主要是这个
example_name['format'] = 'image/format'  #这个一般不用理
example_name['label'] = 'image/class/label' #主要是这个
example_name['height'] = 'image/height' #这个一般不用理
example_name['width'] = 'image/width'  #这个一般不用理

# 开始转换
convert_pics_to_tfrecord(example_name,paramenmt_set)
