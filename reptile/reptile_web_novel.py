import requests
import re,os
from bs4 import BeautifulSoup
from reptile.reptile_novel import reptileNovel
import time

URL = 'https://www.xyyuedu.com/mingzhu'
DIR = r'D:\test\mingzhu'


def getHomeHtml(url, isGetStatusCode=False):
    '''
    请求主页
    :param url:
    :param isGetStatusCode:
    :return:
    '''
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    respose = requests.get(url, headers=headers)
    
    if isGetStatusCode:
        return respose.status_code
    
    homeHtml = respose.content.decode('gbk', 'ignore')
    return homeHtml

def getCategoryList(homeHtml):
    '''
    获取类别列表
    :param homeHtml:
    :return:
    '''
    pattern_url = r'<a href="(/[A-Za-z]+/index.html)" class="more"'
    pattern_category = r'<a href="/[A-Za-z]+/index.html">(.+)</a></h2>'
    urlList = re.findall(pattern_url,homeHtml)
    categoryList = re.findall(pattern_category,homeHtml)
    
    dict_category_url = {}
    for i in range(len(categoryList)):
        dict_category_url[categoryList[i]] = URL.replace(URL.split('/')[-1],'') + urlList[i]
    
    return dict_category_url
    
def getNovelDict(homeHtml):
    '''
    获取小说列表
    :param homeHtml:
    :return:
    '''
    dict_novel = {}
    
    pattern_url = r'<a href="(/[A-Za-z]+/[A-Za-z]+/index.html)" title="'
    pattern_novel = r'<a href="/[A-Za-z]+/[A-Za-z]+/index.html" title="(.+)" class="[A-Za-z]+" target="_[A-Za-z]+" ><img src="'
    
    urlList = re.findall(pattern_url,homeHtml)
    novelList = re.findall(pattern_novel,homeHtml)

    for i in range(len(novelList)):
        dict_novel[novelList[i]] = URL.replace('/'+URL.split('/')[-1],'') + urlList[i]
    return dict_novel

def mkdirForDict(dict_all_url):
    '''
    创建目录
    :param dict_all_url:
    :return:
    '''
    category_name_list = dict_all_url.keys()
    for category_name in category_name_list:
        novel_dict = dict_all_url.get(category_name)
        for novel_name in novel_dict.keys():
            dir_path = os.path.join(DIR,category_name,novel_name)
            try:
                os.makedirs(dir_path)
                print('新建目录%s成功'%(dir_path))
            except:
                print('目录已存在:%s'%(dir_path))
                
            try:
                print('开始下载%s,目标地址为%s,下载路径为%s'%(novel_name,novel_dict.get(novel_name),dir_path))
                #此处调用单册下载函数
                reptileNovel(novel_dict.get(novel_name),dir_path)
                # time.sleep(10)
                print('下载完成')
            except:
                print('下载%s失败，或许这不是一本小说'%(novel_name))
             
if __name__ == '__main__':
    
    homeHtml = getHomeHtml(URL)
    dict_category_url = getCategoryList(homeHtml)
    dict_all_url = {}
    for category_name in dict_category_url.keys():
        category_home_html = getHomeHtml(dict_category_url[category_name])
        dict_novel_url = {}
        dict_novel = getNovelDict(category_home_html)
        dict_all_url[category_name] = dict_novel
    mkdirForDict(dict_all_url)
    
    
    
    
    
    