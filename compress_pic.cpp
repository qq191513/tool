#include <opencv2\opencv.hpp>   
#include <opencv2\highgui\highgui.hpp>
#include <io.h>  
#include <iostream>  
#include <vector>  

using namespace std;
using namespace cv;

void getFiles(string path, vector<string>& files,char* fileType);

int main(int argc, char** argv)
{
	char * dir_Path = "F:\\datas\\61人_3种_train_tfrecord\\tmp\\";//图片目录
	char * save_Path = "F:\\datas\\61人_3种_train_tfrecord\\tmp1\\";
	char * fileType = "jpg";

	vector<string> files;
	Mat img;

	vector<int> compression_params;
	compression_params.push_back(CV_IMWRITE_JPEG_QUALITY);  //选择jpeg
	compression_params.push_back(10); //在这个填入你要的图片质量：1到100

	getFiles(dir_Path, files, fileType);


	/*Mat img = imread("F:\\datas\\61人\\fist\\fist_0.jpg");*/
	int size = files.size();
	for (int i = 0; i < size; i++)
	{

	    img = imread(dir_Path+ files[i]);

		cout << "compress output :" << save_Path + files[i] <<endl;
		imwrite(save_Path+ files[i], img, compression_params);
		
	}

	cout << " --------------------------" << endl;
	cout << " Work done! press 'q' exit 。" << endl;
	cout << "---------------------------" << endl;

	while (1) {
		if (char(waitKey(0)) == 'q')
			break;
	};
	return 0;

}

void getFiles(string path, vector<string>& files ,char* fileType)
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
					getFiles(p.assign(path).append(fileinfo.name), files , fileType);
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
