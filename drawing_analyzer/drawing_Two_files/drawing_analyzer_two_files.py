# -*- encoding: utf-8 -*-
# author: mo weilong
import re
import matplotlib.pyplot as plt
from collections import OrderedDict

def get_parameters_list(path,re_dict={}):
	data_dict =OrderedDict()
	for key in re_dict.keys():
		with open(path, 'r') as fo:
			number_list= []
			for line in fo:
				pattern = re.compile(re_dict[key])
				res = pattern.findall(line)
				if res:
					number_list.append(float(res[0]))
		data_dict[key] =number_list
	return data_dict

def curve_smooth(data_list, batch_size=100):
	new_data_list, idx_list = [], []
	for i in range(int(len(data_list) / batch_size)):
		batch = data_list[i*batch_size: (i+1)*batch_size]
		new_data_list.append(1.0 * sum(batch) / len(batch))
		idx_list.append(i*batch_size)

	return new_data_list, idx_list

def plot_curvev_v2(x,y_datas_dict,y_datas_legend_dict = None,setting_dict={}):
    colors=['b','r','y','k','c','m','g',]
    line_styles= ['^','+','x',':','o','*','s','D','.']
    # plt.switch_backend('agg')
    plt.title(setting_dict['title'])
    plt.xlabel(setting_dict['xlabel'])
    plt.ylabel(setting_dict['ylabel'])
    p_legend = []
    p_legend_name = []
    y_datas_keys = y_datas_dict.keys()
    for idx,y_datas_key in enumerate(y_datas_keys):
        y_data_dict = y_datas_dict[y_datas_key]
        p, =plt.plot(x, y_data_dict, line_styles[idx], color=colors[idx])
        p_legend.append(p)
        if y_datas_legend_dict is not None:
            p_legend_name.append(y_datas_legend_dict[y_datas_key])

    if p_legend_name is not None:
        plt.legend(p_legend, p_legend_name, loc='lower right')

    plt.grid()
    plt.savefig(setting_dict['save_name'], dpi=100, format='png')
    plt.show()


if __name__ =='__main__':
    file_path = 'train_log.txt'
    file_path_1 = 'train_N1_log.txt'

    # 从文件中正则re获取全部y轴的值
    #file_path_1
    y_re_dict_1 = OrderedDict()
    y_re_dict_1['net1_list']=r'net1: ([\d\.]+)'
    y_re_dict_1['net2_list']=r'net2: ([\d\.]+)'
    y_re_dict_1['net3_list']=r'net3: ([\d\.]+)'
    y_re_dict_1['decision_prediction_list']=r'decision_prediction: ([\d\.]+)'
    y_datas_dict_1 = get_parameters_list(path = file_path ,re_dict= y_re_dict_1)

    #file_path_2
    y_re_dict_2 = OrderedDict()
    y_re_dict_2['net_N1_list'] = r'net1: ([\d\.]+)'
    y_datas_dict_2 = get_parameters_list(path = file_path_1 ,re_dict= y_re_dict_2)

    #两个顺序字典合并(合并的键值不能一样)
    y_datas_dict = OrderedDict()
    y_datas_dict.update(y_datas_dict_1)
    y_datas_dict.update(y_datas_dict_2)

    #从文件中正则re获取全部x轴的值
    x_re_dict = OrderedDict()
    x_re_dict['epoch_list']=r'epoch: ([\d]+)'
    x_re_dict['global_step_list']=r'global_step: ([\d]+)'
    x_datas_dict = get_parameters_list(path = file_path ,re_dict= x_re_dict)

    #画图显示legend的名字 (下面的写的键值要上面的保持一致)
    y_datas_legend_dict =OrderedDict()
    y_datas_legend_dict['net1_list']="net_N3_net1"
    y_datas_legend_dict['net2_list']="net_N3_net2"
    y_datas_legend_dict['net3_list']="net_N3_net3"
    y_datas_legend_dict['decision_prediction_list']="net_N3_final_predict"
    y_datas_legend_dict['net_N1_list']="net_N1"

    #标题、x轴、y轴显示信息
    setting_dict = OrderedDict()
    setting_dict['title'] = 'cifar10 image classification precision'
    setting_dict['xlabel'] = 'epoch'
    setting_dict['ylabel'] = 'accuracy'
    setting_dict['save_name'] ='cifar10_compare5.png'

    #传入字典参数并画图
    plot_curvev_v2(x_datas_dict['epoch_list'],y_datas_dict,y_datas_legend_dict,setting_dict)


