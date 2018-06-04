
#include <io.h>  
#include <iostream>  
#include <vector>  
#include <opencv2/opencv.hpp>
using namespace std;
using namespace cv;

void int2str(const int &int_temp, string &string_temp);
void getFiles(string path, vector<string>& files);
string oldName, newName,index;

int main() {

	//char * filePath = "F:\\datas\\范冰冰\\test\\";//自己设置目录
	char * filePath = "F:\\datas\\video_test\\video2018_5_15\\palm_pics\\";//自己设置目录
	vector<string> files;

	string string_temp;
	//获取该路径下的所有文件  
	getFiles(filePath, files);

	char str[100];
	int size = files.size();
	for (int i = 0; i < size; i++)
	{
		int2str(i, index);
		newName = "myPalm_train_" + index + ".jpg";
		//newName = "palm_" + newName + ".jpg";
		//newName = "arm" + newName + ".bmp";
		newName = filePath + newName;
		cout << files[i].c_str() << endl;
		oldName = files[i].c_str();
		if (!rename(oldName.c_str(), newName.c_str()))
		{
			std::cout << "rename success " << std::endl;
		}
		else
		{
			std::cout << "error !!!!!!!可能名字重复？" << std::endl;
		}
	}


	//cout << "work done!! Press 'q' exit! \r\n";
	while (1) {
		if (char(waitKey(50)) == 'q')
			break;
	};
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
				files.push_back(p.assign(path).append(fileinfo.name));
				//files.push_back(fileinfo.name);
			}
		} while (_findnext(hFile, &fileinfo) == 0);
		//_findclose函数结束查找
		_findclose(hFile);
	}
}
void int2str(const int &int_temp, string &string_temp)
{
	stringstream stream;
	stream << int_temp;
	string_temp = stream.str();   //此处也可以用 stream>>string_temp  
}
