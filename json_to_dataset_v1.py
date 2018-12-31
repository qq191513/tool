import argparse
import base64
import json
import os
import os.path as osp
import warnings

import PIL.Image
import yaml

from labelme import utils
###############################################增加的语句,改下路径即可##############################
import glob
json_list = glob.glob(os.path.join('F:\\Test\\Py_test\\py35_windows\\had_labled','*.json'))
# out_dir ='F:\\Test\\Py_test\\py35_windows\\had_labled_out'
out_dir_img ='F:\\Test\\Py_test\\py35_windows\\had_labled_out_img'
out_dir_label ='F:\\Test\\Py_test\\py35_windows\\had_labled_out_label'

###############################################   end    ##########################################


def main():
    # warnings.warn("This script is aimed to demonstrate how to convert the\n"
    #               "JSON file to a single image dataset, and not to handle\n"
    #               "multiple JSON files to generate a real-use dataset.")


    ###############################################  删除的语句  ##################################
    # parser = argparse.ArgumentParser()
    # parser.add_argument('json_file')
    # json_file = args.json_file

    # parser.add_argument('-o', '--out', default=None)
    # args = parser.parse_args()
    ###############################################    end       ##################################

    ###############################################增加的语句######################################
    for json_file in json_list:
        file_name =json_file.split('\\')[-1].split('.')[0]
    ###############################################    end       ##################################

    ###############################################  删除的语句  ##################################
        # if args.out is None:
        #     out_dir = osp.basename(json_file).replace('.', '_')
        #     out_dir = osp.join(osp.dirname(json_file), out_dir)
        # else:
        #     out_dir = args.out
        # if not osp.exists(out_dir):
        #     os.mkdir(out_dir)
    ###############################################    end       ##################################



        if not osp.exists(out_dir_img):
            os.mkdir(out_dir_img)
        if not osp.exists(out_dir_label):
            os.mkdir(out_dir_label)

        data = json.load(open(json_file))

        if data['imageData']:
            imageData = data['imageData']
        else:
            imagePath = os.path.join(os.path.dirname(json_file), data['imagePath'])
            with open(imagePath, 'rb') as f:
                imageData = f.read()
                imageData = base64.b64encode(imageData).decode('utf-8')
        img = utils.img_b64_to_arr(imageData)

        label_name_to_value = {'_background_': 0}
        for shape in sorted(data['shapes'], key=lambda x: x['label']):
            label_name = shape['label']
            if label_name in label_name_to_value:
                label_value = label_name_to_value[label_name]
            else:
                label_value = len(label_name_to_value)
                label_name_to_value[label_name] = label_value
        lbl = utils.shapes_to_label(img.shape, data['shapes'], label_name_to_value)

        label_names = [None] * (max(label_name_to_value.values()) + 1)


        PIL.Image.fromarray(img).save(osp.join(out_dir_img, file_name+'.png'))
        utils.lblsave(osp.join(out_dir_label, file_name+'.png'), lbl)
        ###############################################  删除的语句  ##################################
        # for name, value in label_name_to_value.items():
        #     label_names[value] = name
        # lbl_viz = utils.draw_label(lbl, img, label_names)
        # PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir,file_name+'label_viz.png'))
        # with open(osp.join(out_dir, file_name+'label_names.txt'), 'w') as f:
        #     for lbl_name in label_names:
        #         f.write(lbl_name + '\n')

        # warnings.warn('info.yaml is being replaced by label_names.txt')
        # info = dict(label_names=label_names)
        # with open(osp.join(out_dir, file_name+'info.yaml'), 'w') as f:
        #     yaml.safe_dump(info, f, default_flow_style=False)
        # print('Saved to: %s' % out_dir)
        ###############################################  end  ##################################
        print('Saved to: %s  ,  %s ' % (out_dir_img,out_dir_label))


if __name__ == '__main__':
    main()
