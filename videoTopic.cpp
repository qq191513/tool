# -*- encoding: utf-8 -*-
# author: mo weilong
#include <opencv2/opencv.hpp>
#include <sstream>

using namespace std;
using namespace cv;

void int2str(const int &int_temp, string &string_temp);

int main()
{
	Mat frame,transpor;
	int i = 0;
	int j = 0;
	string index;
	stringstream ss;


	VideoCapture video;
	vector<int> compression_params;
	compression_params.push_back(CV_IMWRITE_JPEG_QUALITY);  //选择jpeg

	//要填的参数
	compression_params.push_back(50); //在这个填入你要的图片质量：1到100
	video.open("F:\\datas\\video_test\\video2018_5_15\\palm_video\\palm5.mp4");
	int last_index = 369;  //排序，上个视频第几张了
	string picName = "palm_";
	string save_dir = "F:\\datas\\video_test\\video2018_5_15\\palm_pics\\";
	int scale_of_cols_reduction = 3;//cols缩小比例
	int scale_of_rows_reduction = 2;//rows缩小比例
	int flip_index = 0; //0,1,-1 三个翻转指数
	int transpose_index = 1; //旋转次数
	const int save_frequency = 10;   //每多少帧保存一张

	string tmpName;
	Mat  dstImage;
	void int2str(const int &int_temp, string &string_temp);

	
	while(video.read(frame))
	{




		
		waitKey(5);

		if (i % save_frequency == 0)
		{
			ss << j + last_index + 1 << ".jpg";
			ss >> index;
			tmpName = picName + index;
			cout << " save picture : " << tmpName << endl;

			//尺寸调整
			resize(frame, dstImage, Size(frame.cols / scale_of_cols_reduction, frame.rows / scale_of_rows_reduction), 0, 0, INTER_LINEAR);

			//显示信息
		
			cout << "old cols : " << frame.cols << " old rows : " << frame.rows << endl;
			cout << "new cols : " << dstImage.cols << " new rows : " << dstImage.rows  << endl;
		

			//旋转处理
			for (int k = 0;k< transpose_index;k++)
			{
				Mat dstImage_transpose;
				transpose(dstImage, dstImage_transpose);
				string tmp;
				int2str(k, tmp);
				imwrite(save_dir + "transpose_" + tmp + "_" + tmpName, dstImage_transpose, compression_params);
			}
			
			

			//翻转处理
			//Mat dstImage_flip_1;
			//flip(dstImage, dstImage_flip_1, 0);
			//imshow("dstImage_flip_1", dstImage_flip_1);
			//imwrite(save_dir + "flip_1_" + tmpName  , dstImage, compression_params);


			//Mat dstImage_flip_2;
			//flip(dstImage, dstImage_flip_2, -1);
			//imshow("dstImage_flip_2", dstImage_flip_2);
			//imwrite(save_dir + "flip_2_"  + tmpName, dstImage, compression_params);

			//Mat dstImage_flip_3;
			//flip(dstImage, dstImage_flip_3, 1);
			//imshow("dstImage_flip_3", dstImage_flip_3);
			//imwrite(save_dir + "flip_3_" + tmpName, dstImage, compression_params);


			//保存
			//imshow("dstImage", dstImage);
			//imwrite(save_dir + tmpName, dstImage, compression_params);
			ss.clear();
			j++;
		}

		i++;

	
	}

	cout << " --------------------------" << endl;
	cout << " Work done! press 'q' exit 。" << endl;
	cout << "---------------------------" << endl;

	/*while ((char)waitKey(0) != 27) {
	};*/
	return 0;



}




void int2str(const int &int_temp, string &string_temp)
{
	stringstream stream;
	stream << int_temp;
	string_temp = stream.str();   //此处也可以用 stream>>string_temp  
}







