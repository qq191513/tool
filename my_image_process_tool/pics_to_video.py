import cv2
import os
import glob
####################################### 改这里 ##################################
# pics_path = r'..\\my_video_new_224x224\\video_20190301_201739'
# save_video = os.path.join(r'..\\my_video_new_224x224\\','video_20190301_201739.mp4')
####################################### end ####################################
####################################### 改这里 ##################################
pics_path = r'..\\my_video_new_224x224\\video_20190301_201915'
save_video = os.path.join(r'..\\my_video_new_224x224\\','video_20190301_201915.mp4')
####################################### end ####################################

#取出其中的一张观察大小
img = cv2.imread(os.path.join(pics_path,'0.jpg'))
imgInfo = img.shape
size = (imgInfo[1], imgInfo[0])

fourcc = cv2.VideoWriter_fourcc('M','J','P','G') #opencv3.0
frame_frequency = 48  #手机是48帧每秒
videoWrite = cv2.VideoWriter(save_video , fourcc, 48, size ) # 写入对象 1 file name 2 编码器 3 帧率 4 尺寸大小

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