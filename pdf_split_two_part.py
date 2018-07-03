# encoding:utf-8
from PyPDF2 import PdfFileReader, PdfFileWriter

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
        pageObj = pdfFileReader.getPage(index)
        pdfFileWriter_1.addPage(pageObj)
        pdfFileWriter_1.write(open(outFile_1, 'wb'))

    for index in range(split_number , numPages):
        pageObj = pdfFileReader.getPage(index)
        pdfFileWriter_2.addPage(pageObj)
        pdfFileWriter_2.write(open(outFile_2, 'wb'))


splitPdf()