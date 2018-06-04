// skin_detect_RGB.cpp : 定义控制台应用程序的入口点。
//

//Author: samylee
//Contact email: ahuljx@126.com
#include "stdafx.h"
#include "stdlib.h"
#include "stdio.h"
#include "cv.h"
#include "highgui.h"

using namespace cv;
using namespace std;

void SkinRG(IplImage* rgb, IplImage* gray);
void SkinRGB(Mat& rgb);
void cvSkinOtsu(IplImage* src, IplImage* dst);
void cvThresholdOtsu(IplImage* src, IplImage* dst);
int main()
{
	double time,stop,start;

	//读图
	string  picture = "F:\\datas\\skin6.jpg";
	Mat img_RGB = imread(picture);
	Mat img_RG = imread(picture);
	Mat img_SkinOtsu = imread(picture);

	imshow("原图", img_RGB);


	//RGB算法
	start = cvGetTickCount();   //开始计时
	SkinRGB(img_RGB);
	stop = cvGetTickCount();     //终止计时
	time  = (stop - start) * 1000 / getTickFrequency();
	cout <<"RGB : use "<< time << " ms\r\n";
	imshow("img_RGB", img_RGB);

	//RG算法
	Mat gray;
	start = cvGetTickCount();     //开始计时
	cvtColor(img_RG, gray,CV_RGB2GRAY);
	SkinRG(&IplImage(img_RG), &IplImage(gray));
	stop = cvGetTickCount();      //终止计时
	time = (stop - start) * 1000 / getTickFrequency();
	cout << "RG : use " << time << " ms\r\n";
	imshow("img_RG", gray);



	//otsu+cr算法
	 Mat dst_Otsu;
	start = cvGetTickCount();     //开始计时
	cvtColor(img_SkinOtsu, dst_Otsu, CV_RGB2GRAY);
	cvSkinOtsu(&IplImage(img_SkinOtsu), &IplImage(dst_Otsu));
	stop = cvGetTickCount();      //终止计时
	time = (stop - start) * 1000 / getTickFrequency();
	cout << "otsu+cr : use " << time << " ms\r\n";
	imshow("otsu+cr", dst_Otsu);

	waitKey(0);
	return 0;
}


// skin detection in rg space
void SkinRG(IplImage* rgb, IplImage* gray)
{
	assert(rgb->nChannels == 3 && gray->nChannels == 1);

	const int R = 2;
	const int G = 1;
	const int B = 0;

	double Aup = -1.8423;
	double Bup = 1.5294;
	double Cup = 0.0422;
	double Adown = -0.7279;
	double Bdown = 0.6066;
	double Cdown = 0.1766;
	for (int h = 0; h<rgb->height; h++) {
		unsigned char* pGray = (unsigned char*)gray->imageData + h*gray->widthStep;
		unsigned char* pRGB = (unsigned char*)rgb->imageData + h*rgb->widthStep;
		for (int w = 0; w<rgb->width; w++) {
			int s = pRGB[R] + pRGB[G] + pRGB[B];
			double r = (double)pRGB[R] / s;
			double g = (double)pRGB[G] / s;
			double Gup = Aup*r*r + Bup*r + Cup;
			double Gdown = Adown*r*r + Bdown*r + Cdown;
			double Wr = (r - 0.33)*(r - 0.33) + (g - 0.33)*(g - 0.33);
			if (g<Gup && g>Gdown && Wr>0.004) {
				*pGray = 255;
			}
			else {
				*pGray = 0;
			}
			pGray++;
			pRGB += 3;
		}
	}

}


void SkinRGB(Mat& rgb)
{

	Size size;
	size.width = rgb.cols;
	size.height = rgb.rows;
	Mat dst = Mat::ones(size, CV_8UC3);
	for (int row = 0; row < size.height; row++)
	{
		for (int col = 0; col < size.width; col++)
		{
			int B = rgb.at<Vec3b>(row, col)[0];
			int G = rgb.at<Vec3b>(row, col)[1];
			int R = rgb.at<Vec3b>(row, col)[2];
			////principle////
			if ((R > 95 &&
				G > 40 &&
				B > 20 &&
				R - B > 15 &&
				R - G > 15)
				||
				(R > 200 &&
					G > 210 &&
					B > 170 &&
					abs(R - B) <= 15 &&
					R > B &&
					G > B))
			{
				dst.at<Vec3b>(row, col)[0] = B;
				dst.at<Vec3b>(row, col)[1] = G;
				dst.at<Vec3b>(row, col)[2] = R;
			}
			////principle////
		}
	}

	rgb = dst;
}

// implementation of otsu algorithm
// author: onezeros#yahoo.cn
// reference: Rafael C. Gonzalez. Digital Image Processing Using MATLAB
void cvThresholdOtsu(IplImage* src, IplImage* dst)
{
	int height = src->height;
	int width = src->width;

	//histogram
	float histogram[256] = { 0 };
	for (int i = 0; i<height; i++) {
		unsigned char* p = (unsigned char*)src->imageData + src->widthStep*i;
		for (int j = 0; j<width; j++) {
			histogram[*p++]++;
		}
	}
	//normalize histogram
	int size = height*width;
	for (int i = 0; i<256; i++) {
		histogram[i] = histogram[i] / size;
	}

	//average pixel value
	float avgValue = 0;
	for (int i = 0; i<256; i++) {
		avgValue += i*histogram[i];
	}

	int threshold;
	float maxVariance = 0;
	float w = 0, u = 0;
	for (int i = 0; i<256; i++) {
		w += histogram[i];
		u += i*histogram[i];

		float t = avgValue*w - u;
		float variance = t*t / (w*(1 - w));
		if (variance>maxVariance) {
			maxVariance = variance;
			threshold = i;
		}
	}

	cvThreshold(src, dst, threshold, 255, CV_THRESH_BINARY);
}

void cvSkinOtsu(IplImage* src, IplImage* dst)
{
	assert(dst->nChannels == 1 && src->nChannels == 3);

	IplImage* ycrcb = cvCreateImage(cvGetSize(src), 8, 3);
	IplImage* cr = cvCreateImage(cvGetSize(src), 8, 1);
	cvCvtColor(src, ycrcb, CV_BGR2YCrCb);
	cvSplit(ycrcb, 0, cr, 0, 0);

	cvThresholdOtsu(cr, cr);
	cvCopyImage(cr, dst);
	cvReleaseImage(&cr);
	cvReleaseImage(&ycrcb);
}
