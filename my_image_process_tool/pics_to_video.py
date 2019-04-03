import cv2
import os
import glob

####################################### 改这里 ##################################
pics_path = r'..\\output\\output_224x224\\my_video_new\\video_20190403_004212'
save_video_path = r'..\\output\\my_video_new_224x224\\'
save_video_name = 'video_20190403_004212.mp4'
####################################### end ####################################

save_video_name = os.path.join(save_video_path,save_video_name)
os.makedirs(save_video_path,exist_ok=True)
#取出其中的一张观察大小
pics_list = os.listdir(pics_path)
img = cv2.imread(os.path.join(pics_path,pics_list[0]))
imgInfo = img.shape
size = (imgInfo[1], imgInfo[0])

fourcc = cv2.VideoWriter_fourcc('M','J','P','G') #opencv3.0
frame_frequency = 48  #手机是48帧每秒
print(save_video_name)
videoWrite = cv2.VideoWriter(save_video_name , fourcc, 48, size ) # 写入对象 1 file name 2 编码器 3 帧率 4 尺寸大小

pics_number_list = glob.glob(os.path.join(pics_path,'*.jpg'))
pics_number = len(pics_number_list)
for i in range(0, pics_number, 1):
    fileName =os.path.join(pics_path,str(i)+'.jpg')
    # fileName = './image_target/image'+str(i)+'.jpg'
    img = cv2.imread(fileName)
    videoWrite.write(img) # 写入方法 1 jpg data

print('################################')
print('work done!!!')
print('################################')