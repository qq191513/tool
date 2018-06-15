# coding=utf-8
#本代码用于保存csdn文章，然后自己手工打开浏览器Ctrl + P 打印成 pdf

from bs4 import BeautifulSoup
import urllib.request as request
import os,requests

import urllib


#选择1：本地保存好的网页
# page_name= 'ccc.html'
# page_name_prettify= 'ccc_prettify.html'


#选择2：网址
page_name = 'test.html'   #下载保存的网页名字
url = 'https://www.cnblogs.com/zyly/p/9146787.html' #csdn博客地址
tmp= url.split('/')
page_name_prettify = tmp[-1]+'_'+page_name  #修改后的保存网页名



def save_html(url,page_name):
    # 反爬虫，要设置头
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36')
    response = urllib.request.urlopen(req)
    html = response.read()
    f = open(page_name, 'wb')
    f.write(html)  # save to page.html
    f.close()
    # r_page = requests.get(url)
    # f = open(page_name,'wb')
    # f.write(r_page.content)#save to page.html
    # f.close()
    #return f

def save_csdn():
    #先下载网站并且网站
    save_html(url, page_name)
    #打开
    f = open(page_name, encoding='UTF-8')
    soup = BeautifulSoup(f,"html.parser")

    #下面是删除不用的标签，包含各个广告，侧栏，评论栏,脚本等等

    #要删除的东西
    remove_structs = ['aside', 'header','']
    remove_classes = ['txt-row-box','tool-box','edu-promotion',
                      'comment-box','recommend-box','pulllog-box',
                      'hide-article-box text-center csdn-tracking-statistics tracking-click',
                      'csdn-toolbar tb_disnone ','meau-gotop-box','']
    remove_ids = ['commentBox','toolbar','btn-readmore','toolbar-tpl-scriptId','']
    remove_scripts = ['commen','']


    #删除所有不用的script
    for script in soup.find_all('script'):
        text = script.get_text()
        for remove_script in remove_scripts:
            if remove_script is not '':
                if text.find(remove_script) != -1:
                    print(script)
                    script.extract()
    #删除所有不用的struct
    for remove_struct in remove_structs:
        if remove_struct is not '':
            soup_structs = soup.find(remove_struct)
            if  soup_structs is not None:
                soup_structs.extract()

    # 删除所有不用的class
    for remove_classe in remove_classes:
        if remove_classe is not '':
            soup_classe = soup.find(class_ = remove_classe)
            if soup_classe is not None:
                soup_classe.extract()

    # 删除所有不用的id
    for remove_id in remove_ids:
        if remove_id is not '':
            soup_id = soup.find(id = remove_id)
            if soup_id is not None:
                soup_id.extract()

    #保存
    with open(page_name_prettify,"wb") as file:
        file.write(bytes(soup.prettify(formatter="html"),encoding ='utf-8'))
        file.close()

    f.close();


def save_cnblogs():
    #先下载网站并且网站
    save_html(url, page_name)
    #打开
    f = open(page_name, encoding='UTF-8')
    soup = BeautifulSoup(f,"html.parser")

    #下面是删除不用的标签，包含各个广告，侧栏，评论栏,脚本等等

    #要删除的东西
    remove_structs = ['', '','']
    remove_classes = ['',]
    remove_ids = ['sideBar','header','blog_post_info_block','comment_form_container',
                  'under_post_news','under_post_kb','footer']
    remove_scripts = ['','']


    #删除所有不用的script
    for script in soup.find_all('script'):
        text = script.get_text()
        for remove_script in remove_scripts:
            if remove_script is not '':
                if text.find(remove_script) != -1:
                    print(script)
                    script.extract()
    #删除所有不用的struct
    for remove_struct in remove_structs:
        if remove_struct is not '':
            soup_structs = soup.find(remove_struct)
            if  soup_structs is not None:
                soup_structs.extract()

    # 删除所有不用的class
    for remove_classe in remove_classes:
        if remove_classe is not '':
            soup_classe = soup.find(class_ = remove_classe)
            if soup_classe is not None:
                soup_classe.extract()

    # 删除所有不用的id
    for remove_id in remove_ids:
        if remove_id is not '':
            soup_id = soup.find(id = remove_id)
            if soup_id is not None:
                soup_id.extract()

    #保存
    with open(page_name_prettify,"wb") as file:
        file.write(bytes(soup.prettify(formatter="html"),encoding ='utf-8'))
        file.close()

    f.close();

if __name__ == '__main__':
    #保存csdn的文章
    if url.find('csdn.net') != -1:
        save_csdn()


    if url.find('cnblogs.com') != -1:
        save_cnblogs()
    #之后自己手工用火狐或google浏览器打开然后按A3类型纸张打印成pdf，
    # 然后打印成纸张的时候就用A4纸模式