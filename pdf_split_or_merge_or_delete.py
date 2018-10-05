# encoding:utf-8
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
def split_pdf_to_two_part(in_File,outFile_1,outFile_2,split_number):

    pdfFileWriter_1 = PdfFileWriter()
    pdfFileWriter_2 = PdfFileWriter()
    # 获取 PdfFileReader 对象
    pdfFileReader = PdfFileReader(in_File)  # 或者这个方式：pdfFileReader = PdfFileReader(open(readFile, 'rb'))
    # 文档总页数
    numPages = pdfFileReader.getNumPages()


    for index in range(0, split_number ):
        print("part1: %d" % (index +1))
        pageObj = pdfFileReader.getPage(index)
        pdfFileWriter_1.addPage(pageObj)
    pdfFileWriter_1.write(open(outFile_1, 'wb'))

    for index in range(split_number , numPages):
        print("part2: %d" % (index +1))
        pageObj = pdfFileReader.getPage(index)
        pdfFileWriter_2.addPage(pageObj)
    pdfFileWriter_2.write(open(outFile_2, 'wb'))

def delete_pdf(readFile,outFile,delete_start,delete_end):

    pdfFileWriter = PdfFileWriter()

    # 获取 PdfFileReader 对象
    pdfFileReader = PdfFileReader(readFile,strict=False)  # 或者这个方式：pdfFileReader = PdfFileReader(open(readFile, 'rb'))
    # 文档总页数
    numPages = pdfFileReader.getNumPages()

    delete_start = delete_start -1
    for index in range(0, delete_start ):
        print("part1: %d" % (index +1))
        pageObj = pdfFileReader.getPage(index)
        pdfFileWriter.addPage(pageObj)


    for index in range(delete_end , numPages):
        print("part2: %d" % (index +1))
        pageObj = pdfFileReader.getPage(index)
        pdfFileWriter.addPage(pageObj)

    #保存
    pdfFileWriter.write(open(outFile, 'wb'))


def mergePdf(inFileList, outFile):
    '''
    合并文档
    :param inFileList: 要合并的文档的 list
    :param outFile:    合并后的输出文件
    :return:
    '''
    pdfFileWriter = PdfFileWriter()
    for inFile in inFileList:
        # 依次循环打开要合并文件
        pdfReader = PdfFileReader(open(inFile, 'rb'),strict=False)
        numPages = pdfReader.getNumPages()
        for index in range(0, numPages):
            print(inFile ,"merge: %d " % (index +1))
            pageObj = pdfReader.getPage(index)
            pdfFileWriter.addPage(pageObj)

        # 最后,统一写入到输出文件中
        print('save to ',outFile)
        pdfFileWriter.write(open(outFile, 'wb'))

if __name__ == '__main__':

    #1、分割pdf
    # in_File = 'merged_part5.pdf'   #要分割的pdf
    # outFile_1 = 'merged_part3_0_to_200.pdf'   #上部分名字
    # outFile_2 = 'merged_part5_no_0.pdf'   #下部分名字
    # split_number = 1  #分割起始页
    # split_pdf_to_two_part(in_File,outFile_1,outFile_2,split_number)

    #2、合并pdf
    merge_dir = 'mydir' #pdf的目录位置
    save_file = 'fuck.pdf' #合并后的pdf名字
    dirlist = []
    for root,dirs,files in os.walk(merge_dir):
        for file in files:
            full_path = os.path.join(merge_dir, file)
            dirlist.append(full_path)
            print(full_path)
    mergePdf(dirlist,save_file )

    #3、删除pdf
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 35bfba51f6d5db9dd7725de7c342fd200681f7ec
    # in_File = 'merged_part5.pdf'   #输入pdf
    # outFile = 'fuck.pdf'   #输出pdf
    # delete_start = 5  #删除开始的页码
    # delete_end = 5    #删除最后的页码
    # delete_pdf(readFile = in_File, outFile = outFile , delete_start =delete_start, delete_end =delete_end)
<<<<<<< HEAD
=======
    in_File = 'merged_part5.pdf'   #输入pdf
    outFile = 'fuck.pdf'   #输出pdf
    delete_start = 5  #删除开始的页码
    delete_end = 5    #删除最后的页码
    delete_pdf(readFile = in_File, outFile = outFile , delete_start =delete_start, delete_end =delete_end)
>>>>>>> d6753c1493c2cff2ccad8290af745894e1f42b85
=======
>>>>>>> 35bfba51f6d5db9dd7725de7c342fd200681f7ec
