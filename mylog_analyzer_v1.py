# -*- encoding: utf-8 -*-
# author: ronniecao
import os
import re
import matplotlib.pyplot as plt
import numpy
# import matplotlib as mpl
# mpl.use('Agg')
from str2float import str2float
# from functools import reduce
# def str2float(s):
#   return reduce(lambda x,y:x+int2dec(y),map(str2int,s.split('.')))
# def char2num(s):
#   return{'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[s]
# def str2int(s):
#   return reduce(lambda x,y:x*10+y,map(char2num,s))
# def intLen(i):
#     return len('%d' % i)
# def int2dec(i):
#   return i/(10** intLen(i))
# def str2float(s):
#     return reduce(lambda x,y: x+int2dec(y),map(str2int,s.split('.')))

def get_number_list(path,re_str=r'example : epoch: ([\d\.]+)'):
	with open(path, 'r') as fo:
		number_list= []
		for line in fo:
			pattern = re.compile(re_str)
			res = pattern.findall(line)
			if res:
				number_list.append(str2float(res[0]))
	return number_list

def curve_smooth(data_list, batch_size=100):
	new_data_list, idx_list = [], []
	for i in range(int(len(data_list) / batch_size)):
		batch = data_list[i*batch_size: (i+1)*batch_size]
		new_data_list.append(1.0 * sum(batch) / len(batch))
		idx_list.append(i*batch_size)

	return new_data_list, idx_list

# def plot_curve(x_axis_list,y1_list,y2_list):
#
# 	fig = plt.figure(figsize=(10, 5))
# 	plt.subplot(121)
# 	p1 = plt.plot(epoch_list, loss_list, '.--', color='#6495ED')
# 	plt.grid(True)
# 	plt.title('cifar10 image classification loss')
# 	plt.xlabel('# of epoch')
# 	plt.ylabel('loss')
# 	plt.subplot(122)
# 	p2 = plt.plot(loss_list,epoch_list, '.--', color='#66CDAA')
# 	p3 = plt.plot(valid_precision_list,epoch_list, '.--', color='#FF6347')
# 	# plt.legend(p2[0], 'valid_precision_list')
# 	plt.grid(True)
# 	plt.title('cifar10 image classification precision')
# 	plt.xlabel('epoch')
# 	plt.ylabel('accuracy')
# 	plt.show()
# 	plt.savefig('cifar10-v1.png', dpi=72, format='png')

def plot_curvev_v1(x,y_1,y_2):
	# plt.ylim((0, 1))  # y参数范围
	# fig = plt.figure(figsize=(10, 5))
	plt.plot(x, y_1, '.--', color='#6495ED')
	plt.plot(x,y_2 ,'.--', color='#FF6347')
	plt.show()
# epoch_list, iter_list, loss_list,valid_precision_list,valid_loss_list = load_log('test_log.txt')
# print(numpy.array(loss_list[-100:]).mean(), numpy.array(iter_list[-100:]).mean())
# loss_list, loss_idxs = curve_smooth(loss_list[0:500], batch_size=1)
# train_precision_list, train_precision_idxs = curve_smooth(iter_list, batch_size=10)
# valid_precision_list, valid_precision_idxs = curve_smooth(valid_precision_list, batch_size=10)
# plot_curve(loss_list, valid_precision_list, epoch_list)
epoch_list = get_number_list(path ='train_log.txt',re_str=r'epoch: ([\d]+)')
global_step_list = get_number_list(path ='train_log.txt',re_str=r'global_step: ([\d]+)')
net1_list = get_number_list(path ='train_log.txt',re_str=r'net1: ([\d\.]+)')
net2_list = get_number_list(path ='train_log.txt',re_str=r'net2: ([\d\.]+)')
net3_list = get_number_list(path ='train_log.txt',re_str=r'net3: ([\d\.]+)')
decision_prediction_list = get_number_list(path ='train_log.txt',re_str=r'decision_prediction: ([\d\.]+)')

plot_curvev_v1(global_step_list,net2_list,net3_list)
# epoch_list, iter_list = load_log('train_log.txt')
# plot_curve(loss_list, valid_precision_list, epoch_list)

