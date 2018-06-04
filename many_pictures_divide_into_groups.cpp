// many_pictures_divide_into_groups.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "windows.h"
#include "cstdlib"
#include <opencv2/opencv.hpp>
#include <vector>  
#include <iostream>  
#include <io.h>  
#include <math.h>
#include "iostream"
#include <direct.h>
#include<iostream>
#include<fstream>

void copy(char* src, char* dst);
using namespace cv;
using namespace std;

int Resize(Mat src, Mat& dst, int width, int height);
LPCWSTR stringToLPCWSTR(string orig);
void getFiles(string path, vector<string>& files);

int main()
{

	
	string filePath = "F:\\positive\\";
	vector<string> files;
	getFiles(filePath, files);
	int  filesNmber = files.size();
	float batch = 100.0;
	int groupNumber = ceil(filesNmber * 1.0 / batch);

	stringstream sstream;
	string src, dst;
	string groupName ;
	LPCWSTR wcstring_src, wcstring_dst;
	string newdir;
	int k = 0;
	int i;
	for (i = 0; i < groupNumber-1; i++) {
		sstream << i;
		sstream >> groupName;
		sstream.clear();
		newdir = filePath + groupName +"\\";
		_mkdir(newdir.c_str());
		
		for (int j = 0; j < 100; j++ ) {
			//copy(files[k * 100 + j], groupName)
			dst = newdir + files[k * 100 + j];
			src = filePath + files[k * 100 + j];
			wcstring_src = stringToLPCWSTR(src);
			wcstring_dst = stringToLPCWSTR(dst);
			MoveFile(wcstring_src, wcstring_dst);
		}
		k++;
		
	}

	//最后一组，不够100张
	sstream << i;
	sstream >> groupName;
	sstream.clear();
	newdir = filePath + groupName + "\\";
	_mkdir(newdir.c_str());
	for (int j = 0; j <filesNmber - k * 100; j++) {
		//copy(files[k * 100 + j], groupName)
		dst = newdir + files[k * 100 + j];
		src = filePath + files[k * 100 + j];
		wcstring_src = stringToLPCWSTR(src);
		wcstring_dst = stringToLPCWSTR(dst);
		MoveFile(wcstring_src, wcstring_dst);
	}
	



	waitKey(0);
	return 0;
}

void getFiles(string path, vector<string>& files)
{
	//文件句柄  
	long   hFile = 0;
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
				//files.push_back(p.assign(path).append(fileinfo.name));
				files.push_back(fileinfo.name);
			}
		} while (_findnext(hFile, &fileinfo) == 0);
		//_findclose函数结束查找
		_findclose(hFile);
	}
};
LPCWSTR stringToLPCWSTR(string orig)
{
	size_t origsize = orig.length() + 1;
	const size_t newsize = 100;
	size_t convertedChars = 0;
	wchar_t *wcstring = (wchar_t *)malloc(sizeof(wchar_t) *(orig.length() - 1));
	mbstowcs_s(&convertedChars, wcstring, origsize, orig.c_str(), _TRUNCATE);


	return wcstring;
}


