
/************************************************************************/
/*
OpenCV图像缩放使用的函数是：resize
void resize(InputArray src, OutputArray dst, Size dsize, double fx=0, double fy=0, int interpolation=INTER_LINEAR )
参数含义：
InputArray src     -原图像
OutputArray dst    -输出图像
Size dsize         -目标图像的大小
double fx=0        -在x轴上的缩放比例
double fy=0        -在y轴上的缩放比例
int interpolation  -插值方式，有以下四种方式

INTER_NN      -最近邻插值
INTER_LINEAR  -双线性插值 (缺省使用)
INTER_AREA    -使用象素关系重采样，当图像缩小时候，该方法可以避免波纹出现。当图像放大时，类似于 INTER_NN 方法。
INTER_CUBIC   -立方插值。

说明：dsize与fx和fy必须不能同时为零
*/
/************************************************************************/
#include <opencv2\opencv.hpp>
#include <opencv2\imgproc\imgproc.hpp>
#include <io.h>  
#include <iostream>  
#include <vector>  

using namespace std;
using namespace cv;

void getFiles(string path, vector<string>& files, char* fileType);

int main()
{
	//读入图像
	char * dir_Path = "F:\\datas\\61人_3种_train_tfrecord\\fist\\";//图片目录
	char * save_Path = "F:\\datas\\61人_3种_train_tfrecord\\tmp\\";
	char * fileType = "jpg";

	vector<string> files;
	Mat srcImage, dstImage;

	getFiles(dir_Path, files, fileType);

	int size = files.size();
	for (int i = 0; i < size; i++)
	{
		srcImage = imread(dir_Path + files[i]);

		//尺寸调整
		resize(srcImage, dstImage, Size(srcImage.cols / 11, srcImage.rows / 11), 0, 0, INTER_LINEAR);


		//显示信息
		cout << "compress output :" << save_Path + files[i] << endl;
		cout << "old cols : " << srcImage.cols  << " old rows : " << srcImage.rows  << endl;
		cout << "new cols : " << dstImage.cols << " new rows : " << dstImage.rows  << endl;
		imwrite(save_Path + files[i], dstImage);

	}


	cout << " --------------------------" << endl;
	cout << " Work done! press 'q' exit 。" << endl;
	cout << "---------------------------" << endl;

	while ((char)waitKey(0) != 27) {
	};
	return 0;

}



void getFiles(string path, vector<string>& files, char* fileType)
{
	//文件句柄  
	long   hFile = 0;
	//文件信息，声明一个存储文件信息的结构体  
	struct _finddata_t fileinfo;
	int fuck;
	string p;//字符串，存放路径+
			 //string d = p.assign(path);
			 //string h = p.assign(path).append("\\*");
			 //string dj = p.assign(path).append("\\*").c_str();
	if ((hFile = _findfirst(p.assign(path).append("*").c_str(), &fileinfo)) != -1)//若查找成功，则进入
	{
		do
		{
			//如果是目录,迭代之（即文件夹内还有文件夹）  
			if ((fileinfo.attrib &  _A_SUBDIR))
			{
				//文件名不等于"."&&文件名不等于".."
				//.表示当前目录
				//..表示当前目录的父目录
				//判断时，两者都要忽略，不然就无限递归跳不出去了！
				if (strcmp(fileinfo.name, ".") != 0 && strcmp(fileinfo.name, "..") != 0)
					getFiles(p.assign(path).append(fileinfo.name), files, fileType);
			}
			//如果不是,加入列表  
			else
			{
				//files.push_back(p.assign(path).append(fileinfo.name));
				if (fileType != "0")
				{
					string filename = fileinfo.name;
					string filename_type = filename.substr(filename.find_last_of('.') + 1);
					fuck = strcmp(filename_type.c_str(), fileType);
					if (fuck == 0)
					{
						files.push_back(fileinfo.name);
					}

				}
				else
				{
					files.push_back(fileinfo.name);
				}



			}
		} while (_findnext(hFile, &fileinfo) == 0);
		//_findclose函数结束查找
		_findclose(hFile);
	}
}
