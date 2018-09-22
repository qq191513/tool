# -*- coding: utf-8 -*-

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


def traverse(f, old_suffix=None, new_suffix=None,head_show = None):
    fs = os.listdir(f)
    old_suffix_1 ='.'+old_suffix
    for f1 in fs:
        tmp_path = os.path.join(f, f1)
        if not os.path.isdir(tmp_path):
            tmp_path_list= tmp_path.split('/')
            tmp_path_last= tmp_path_list[-1]   #取最后一个名字
            tmp_path_first= tmp_path_list[0]  #取第一个名字
            if old_suffix_1 in tmp_path_last and '.pyc' not in tmp_path_last:

                #改最后一个名字
                dirname = os.path.dirname(tmp_path)
                new_name_last_1 = tmp_path_last.split('.')[0]
                new_name_last_2 = new_name_last_1 + '.'+new_suffix

                #改第一个名字
                new_name_first_1 = tmp_path_first + '_new'+'_'+new_suffix

                #放回列表
                tmp_path_list[0] = new_name_first_1
                tmp_path_list[-1] = new_name_last_2

                #重新合并得new_dir
                new_dir= '/'.join(tmp_path_list)

                #复制到new_dir
                mycopyfile(tmp_path,new_dir)

                # 头说明
                if head_show:
                    with open(new_dir, 'r+') as open_f:
                        content = open_f.read()
                        open_f.seek(0, 0)
                        message = '路径：' + tmp_path + '\n'
                        print('message: %s' % tmp_path)
                        open_f.write(message + content)
                file_list.append(new_dir)
        else:
            traverse(tmp_path,old_suffix=old_suffix,new_suffix=new_suffix,head_show=head_show)
    return file_list




#全部转换并返回转换的列表
path = 'tf-faster-rcnn-master'
file_list = traverse(path,old_suffix='py',new_suffix='txt',head_show=True)



