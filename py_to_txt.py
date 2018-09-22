# -*- coding: utf-8 -*-
"""
Created on 2017年11月11日13:19:20
@author: qcy
"""

import os,shutil
file_list = []

def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print "%s not exist!"%(srcfile)
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print "copy %s -> %s"%(srcfile,dstfile)


def traverse(f, old_suffix='py', new_suffix='txt'):
    fs = os.listdir(f)
    old_suffix ='.'+old_suffix
    for f1 in fs:
        tmp_path = os.path.join(f, f1)
        if not os.path.isdir(tmp_path):
            tmp_path_last= tmp_path.split('/')[-1]
            if old_suffix in tmp_path_last and '.pyc' not in tmp_path_last:
                dirname = os.path.dirname(tmp_path)
                new_name = tmp_path_last.split('.')[0]
                new_name = new_name + '.'+new_suffix
                new_dir = os.path.join(dirname,new_name)
                new_dir = 'new_txt_'+ new_dir
                print('new_dir: %s' % new_dir)
                mycopyfile(tmp_path,new_dir)
                file_list.append(new_dir)
        else:
            traverse(tmp_path,old_suffix='py',new_suffix='txt')
    return file_list




#全部转换并返回转换的列表
path = 'tf-faster-rcnn-master'
file_list = traverse(path,old_suffix='py',new_suffix='txt')

#头说明
for file in file_list:
    with open(file,'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write('路径：' + file + '\n' + content)

