#include <cstdlib>
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
using namespace std;
#include <cv.h>
#include <cxcore.h>
#include       <highgui.h>
int main(int argc, char *argv[])
{
	//string dirPath = "F:\\Test\\Cplusplus_test\\myResearch\\train_fist\\tool\\tools\\temp\\negative\\";
	string dirPath = "F:\\datas\\ÊÖÕÆ\\";
	string save_dir = dirPath + "bmp\\";

	string picPath = dirPath + "*.jpg";
	string cmd = "dir /b " + picPath + " > jpglist.txt";
	system(cmd.c_str());
	ifstream jpglist("jpglist.txt");
	vector<string> jpgName;
	string buf;

	string open_dir = dirPath;

	while (jpglist)
	{
		if (getline(jpglist, buf))
		{
			jpgName.push_back(buf);
		}
	}
	jpglist.close();
	for (string::size_type i = 0; i<jpgName.size(); i++)
	{

		string filename = jpgName[i];
		string       file_no_ext = "";
		for (int j = 0; j<jpgName[i].length() - 4; j++)
		{
			file_no_ext += filename[j];
		}
		file_no_ext.append(".bmp");
		IplImage  *src = cvLoadImage((open_dir+jpgName[i]).c_str());
		if (!src)
		{
			cout << "can not load   the image : " << jpgName[i] << endl;
			break;
		}
		cout << "processing   " << jpgName[i] << endl;
		cvSaveImage((save_dir+file_no_ext).c_str(), src);
		cvReleaseImage(&src);
		src = NULL;
	}
	system("PAUSE");
	return  EXIT_SUCCESS;
}