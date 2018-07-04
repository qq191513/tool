# encoding:utf-8
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
def splitPdf():

    readFile = 'merged_part3.pdf'
    outFile_1 = 'merged_part3_0_to_200.pdf'
    outFile_2 = 'merged_part3_200_to_end.pdf'
    split_number = 214


    pdfFileWriter_1 = PdfFileWriter()
    pdfFileWriter_2 = PdfFileWriter()
    # 获取 PdfFileReader 对象
    pdfFileReader = PdfFileReader(readFile)  # 或者这个方式：pdfFileReader = PdfFileReader(open(readFile, 'rb'))
    # 文档总页数
    numPages = pdfFileReader.getNumPages()


    for index in range(0, split_number ):
        print("part1: %d" % index)
        pageObj = pdfFileReader.getPage(index)
        pdfFileWriter_1.addPage(pageObj)
        pdfFileWriter_1.write(open(outFile_1, 'wb'))

    for index in range(split_number , numPages):
        print("part2: %d" % index)
        pageObj = pdfFileReader.getPage(index)
        pdfFileWriter_2.addPage(pageObj)
        pdfFileWriter_2.write(open(outFile_2, 'wb'))

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
        pdfReader = PdfFileReader(open(inFile, 'rb'))
        numPages = pdfReader.getNumPages()
        for index in range(0, numPages):
            print(inFile ,"merge: %d " % index)
            pageObj = pdfReader.getPage(index)
            pdfFileWriter.addPage(pageObj)

        # 最后,统一写入到输出文件中
        print('save to ',outFile)
        pdfFileWriter.write(open(outFile, 'wb'))

if __name__ == '__main__':

    #分割pdf
    # splitPdf()

    #合并pdf
    merge_dir = 'mydir' #pdf的目录位置
    save_file = 'fuck.pdf' #合并的pdf
    dirlist = []
    for root,dirs,files in os.walk(merge_dir):
        for  file in files:
            dirlist.append(os.path.join(merge_dir,file))
    mergePdf(dirlist,save_file )
