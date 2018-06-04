// get_batch_pictures_ROI.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
//
//#include <io.h>  
//#include <iostream>  
//#include <vector>  
//#include <opencv2/opencv.hpp>
//#include <algorithm>
//#include <opencv2/highgui/highgui.hpp>
//
//
//using namespace std;
//using namespace cv;
//Point origin;
//bool flag = false;
//Rect selection;
//bool selectObject = false;
//bool pause = false;
//Mat img;
//Mat roi;
//bool g_bDrawingBox = false;
//Rect g_rectangle;
//RNG g_rng(123456);
//
//static void onMouse(int event, int x, int y, int, void*)
//{
//	if (!flag&&pause)
//	{
//		if (selectObject)
//		{
//			selection.x = MIN(x, origin.x);
//			selection.y = MIN(y, origin.y);
//			selection.width = std::abs(x - origin.x);
//			selection.height = std::abs(y - origin.y);
//			selection &= Rect(0, 0, img.cols, img.rows);
//		}
//
//		switch (event)
//		{
//		case CV_EVENT_LBUTTONDOWN:
//			origin = Point(x, y);
//			selection = Rect(x, y, 0, 0);
//			selectObject = true;
//			break;
//		case CV_EVENT_LBUTTONUP:
//			selectObject = false;
//			if (selection.width > 0 && selection.height > 0)
//				rectangle(img, selection, Scalar(0, 255, 255));
//			 imshow("ccav", img);
//			flag = true;
//			break;
//		}
//	}
//}
//
//void getFiles(string path, vector<string>& files)
//{
//	//文件句柄  
//	long   hFile = 0;
//	//文件信息，声明一个存储文件信息的结构体  
//	struct _finddata_t fileinfo;
//	string p;//字符串，存放路径+
//			 //string d = p.assign(path);
//			 //string h = p.assign(path).append("\\*");
//			 //string dj = p.assign(path).append("\\*").c_str();
//	if ((hFile = _findfirst(p.assign(path).append("*").c_str(), &fileinfo)) != -1)//若查找成功，则进入
//	{
//		do
//		{
//			//如果是目录,迭代之（即文件夹内还有文件夹）  
//			if ((fileinfo.attrib &  _A_SUBDIR))
//			{
//				//文件名不等于"."&&文件名不等于".."
//				//.表示当前目录
//				//..表示当前目录的父目录
//				//判断时，两者都要忽略，不然就无限递归跳不出去了！
//				if (strcmp(fileinfo.name, ".") != 0 && strcmp(fileinfo.name, "..") != 0)
//					getFiles(p.assign(path).append(fileinfo.name), files);
//			}
//			//如果不是,加入列表  
//			else
//			{
//				files.push_back(p.assign(path).append(fileinfo.name));
//				//files.push_back(fileinfo.name);
//			}
//		} while (_findnext(hFile, &fileinfo) == 0);
//		//_findclose函数结束查找
//		_findclose(hFile);
//	}
//}
//void int2str(const int &int_temp, string &string_temp)
//{
//	stringstream stream;
//	stream << int_temp;
//	string_temp = stream.str();   //此处也可以用 stream>>string_temp  
//}
//void DrawRectangle(Mat &img,Rect box)
//{
//	rectangle(img,box.tl,box.br(),Scalar(g_rng.uniform(0,255), g_rng.uniform(0, 255), g_rng.uniform(0, 255)));
//}
//int main() {
//	char * filePath = "F:\\Test\\Cplusplus_test\\leran_51cto\\train_51cto_face\\positive\\img\\01\\";
//	vector<string> files;
//
//	////获取该路径下的所有文件  
//	getFiles(filePath, files);
//	namedWindow("ccav",WINDOW_AUTOSIZE);
//	setMouseCallback("ccav", onMouse);
//
//	int size = files.size();
//	for (int i = 0; i < size; i++)
//	{
//		img = imread(files[i]);
//		if (!img.data) {
//			continue;
//		}
//		imshow("ccav", img);
//
//		while (char(waitKey(0)) != 'n') {
//			if (g_bDrawingBox) {
//				DrawRectangle(img,g_rectangle);
//			}
//		
//		
//		};
//
//
//
//	}
//	cout << "screenshot done !!!! \r\n";
//	getchar();
//	waitKey(0);
//}


//#include <opencv2/opencv.hpp>
//#include <opencv2/tracking.hpp>
//#include <io.h>  
//#include <iostream>  
//#include <vector>  
//#include <opencv2/opencv.hpp>
//using namespace std;
//using namespace cv;
//bool fromCenter = false;
//bool showCross = false;
#include <io.h>  
#include <iostream>  
#include <vector>  
#include <opencv2/opencv.hpp>
#include <opencv2/tracking.hpp>
using namespace std;
using namespace cv;

bool fromCenter = false;
bool showCross = false;
string GetPathOrURLShortName(std::string strFullName);
void string_replace(std::string &strBig, const std::string &strsrc, const std::string &strdst);
void getFiles(string path, vector<string>& files);
#define MIN_ROI 24
int main(int argc, char **arv)
{
	// Read image
	vector<string> files;
	//string filePath = "F:\\datas\\拳头\\";//自己设置目录  
	//string filePath = "F:\\datas\\手掌\\bmp\\";
	string filePath = "F:\\datas\\人脸\\";
	string save_dir = filePath + "ROI\\";
	string strFileName;

	getFiles(filePath, files);
	int size = files.size();
	Mat img,temp;
	namedWindow("img",WINDOW_AUTOSIZE);
	//namedWindow("temp", WINDOW_AUTOSIZE);
	Rect2d r, r_modidy, r_last;
	for (int i = 0; i < size; i++)
	{
		img = imread(files[i]);
		imshow("img", img);
		if (!img.data)
		{
			continue;
		}

		
		while(1)
		{

			r = selectROI("img", img, fromCenter, showCross);

			//如果没有做出ROI选择，则被破迫重新选择
			if (r != r_last)
				if (r.width > MIN_ROI)
					if (r.height > MIN_ROI)
						break;
		}

		r_last = r;//上一个没有做出修改的ROI
		
		if (r.x + r.width > img.cols)
			r.width = img.cols - r.x-1;
		if (r.y + r.height > img.rows)
			r.height = img.rows - r.y -1;

		if (r.x < 0)
		{
			r.width = r.width + r.x;
			r.x = 0;
			
		}
			

		if (r.y < 0)
		{
			r.height = r.height + r.y;
			r.y = 0;
			
		}
		r_modidy = r;//修正不合格的ROI（超出范围）



		temp = img(r_modidy);
		strFileName = GetPathOrURLShortName(files[i]);

		imwrite(save_dir + strFileName,temp);
		//imshow("temp", temp);

	}




}


void getFiles(string path, vector<string>& files)
{
	//文件句柄  
	intptr_t   hFile = 0;
	//文件信息，声明一个存储文件信息的结构体  
	struct _finddata_t fileinfo;
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
					getFiles(p.assign(path).append(fileinfo.name), files);
			}
			//如果不是,加入列表  
			else
			{
				files.push_back(p.assign(path).append(fileinfo.name));
				//files.push_back(fileinfo.name);
			}
		} while (_findnext(hFile, &fileinfo) == 0);
		//_findclose函数结束查找
		_findclose(hFile);
	}
}



void string_replace(std::string &strBig, const std::string &strsrc, const std::string &strdst)
{
	std::string::size_type pos = 0;
	std::string::size_type srclen = strsrc.size();
	std::string::size_type dstlen = strdst.size();

	while ((pos = strBig.find(strsrc, pos)) != std::string::npos)
	{
		strBig.replace(pos, srclen, strdst);
		pos += dstlen;
	}
}

//************************************
// Method:    GetFileOrURLShortName
// FullName:  GetFileOrURLShortName
// Access:    public 
// Returns:   std::string
// Qualifier: 获取路径或URL的文件名（包括后缀，如 C:\Test\abc.xyz --> abc.xyz）
// Parameter: std::string strFullName
//************************************
std::string GetPathOrURLShortName(std::string strFullName)
{
	if (strFullName.empty())
	{
		return "";
	}

	string_replace(strFullName, "/", "\\");

	std::string::size_type iPos = strFullName.find_last_of('\\') + 1;

	return strFullName.substr(iPos, strFullName.length() - iPos);
}

