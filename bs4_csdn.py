# coding=utf-8
#本代码用于保存csdn文章，然后自己手工打开浏览器Ctrl + P 打印成 pdf

from bs4 import BeautifulSoup
import urllib.request as request
import os,requests


#选择1：本地保存好的网叶
# page_name= 'ccc.html'
# page_name_prettify= 'ccc_prettify.html'

#选择2：网址
def save_html(url,page_name):
    r_page = requests.get(url)
    f = open(page_name,'wb')
    f.write(r_page.content)#save to page.html
    f.close()
    return f


page_name = 'test.html'   #下载保存的网页名字
url = 'https://blog.csdn.net/bhneo/article/details/79419361'  #csdn博客地址
f = save_html(url,page_name)

page_name_prettify = 'ch_'+page_name  #修改后的网页名字





def save_file_to_local():


    #打开
    f = open(page_name, encoding='UTF-8')
    soup = BeautifulSoup(f,"html.parser")

    #删除不用的标签，包含各个广告，侧栏，评论栏等等

    for toolbar in soup.find_all(id='csdn-toolbar'):
        toolbar.extract()

    soup.find('aside').extract()
    soup.find('header').extract()

    soup.find( class_ ="tool-box").extract()

    # soup.find(class_="csdn-toolbar tb_disnone ").extract()

    soup.find(class_="txt-row-box").extract()
    # soup.find(class_="meau-gotop-box").extract()
    soup.find( class_ ="edu-promotion").extract()
    soup.find(class_="comment-box").extract()
    soup.find(class_="recommend-box").extract()


    #保存
    with open(page_name_prettify,"wb") as file:
        print(soup.prettify)
        print(soup.original_encoding)
        # print(word_soup.prettify(word_soup.original_encoding))
        file.write(bytes(soup.prettify(formatter="html"),encoding ='utf-8'))

        # file.write(bytes("hello\n",encoding ='utf-8'))
        file.close()

    f.close();




if __name__ == '__main__':

    save_file_to_local()

    #之后自己手工用火狐或google浏览器打开然后按A3类型纸张打印成pdf