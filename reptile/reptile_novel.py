import requests
import re,os
from bs4 import BeautifulSoup

#红楼梦
# URL = 'https://www.xyyuedu.com/wgmz/dongyeguiwu/baiyexingxs/'
# DIR = r'D:\test\0602\baiyexing'

#白夜行
# URL = 'https://www.xyyuedu.com/gdmz/sidamingzhu/hlmeng/index.html'
# DIR = r'D:\test\0602\hongloumeng'

#过去我死去的家
# URL = 'https://www.xyyuedu.com/wgmz/dongyeguiwu/guoquwosiqudejia/index.html'
# DIR = r'D:\test\0602\gqwsqdj'

#壮丽的奥力诺克河
URL = 'https://www.xyyuedu.com/gdmz/yingliechuan/index.html'
DIR = r'D:\test\mingzhu\中国古典文学\英烈传'


def getHomeHtml(url,isGetStatusCode=False):
    '''
    请求页面
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

def getChapterUrlList(homeHtml):
    '''
    获取各章节url
    :param homeHtml:
    :return:
    '''
    dict_chapter = {}
    pattern = r'<a href="(/[A-Za-z]+/[A-Za-z]+/[A-Za-z]+/[0-9]+.html)"'
    urlList = re.findall(pattern, homeHtml)
    if(len(urlList) == 0):
        pattern = r'<a href="(/[A-Za-z]+/[A-Za-z]+/[0-9]+.html)"'
        urlList = re.findall(pattern, homeHtml)
    urlList_re = []
    for url in urlList:
        urlList_sub = []
        url = 'https://www.xyyuedu.com' + url
        urlList_sub.append(url)
        for i in range(2,10):
            url_next = url.replace('.html','')+'_%s'%(i)+'.html'
            statusCode = getHomeHtml(url_next,isGetStatusCode=True)
            print('%s   %s'%(url_next,statusCode))
            if statusCode !=(200):
                break
            else:
                urlList_sub.append(url_next)
        urlList_re.append(urlList_sub)
        
    pattern_chapter = r'title="(.+?)"   target="_blank"'
    chapterList = re.findall(pattern_chapter, homeHtml)
    
    for i in range(len(chapterList)):
        dict_chapter[str(i+1)+chapterList[i].replace('?','')] = urlList_re[i]
    
    return dict_chapter


def saveChapterText(name,urlList):
    '''
    将各章节文本记录在txt文件中
    :param name:
    :param urlList:
    :return:
    '''
    for url in urlList:
        chapterHtml = getHomeHtml(url)
        bf = BeautifulSoup(chapterHtml)
        
        isDown = False
        if writeDown(name,bf.find_all('p')) or writeDown_mode2(name,bf.find_all('div',id="onearcxsbd")):
            print('下载%s成功'%(name))
            isDown = True
        else:
            print('未获得文本,切换模式下载')
    if not isDown:
        print('失败，未获得文本')

def writeDown_mode2(name,chapterTextList):
    '''
    第二种文本解析方式
    该模式下，章节文本存储在整个<div>中
    :param name:
    :param chapterTextList:
    :return:
    '''
    isMatch = False
    for text in chapterTextList:
        text = \
        str(text).replace('<p>', '').replace('</p>', '').replace('<br/>', '').replace('&lt', '').replace(' ', '').split(
            '<!--分页-->')[0].replace('<divclass="onearcxsbd"id="onearcxsbd">','')
        if len(text) != 0:
            writeInText(name, text + '\r\n')
            isMatch = True
    return isMatch

def writeDown(name,chapterTextList):
    '''
    第一种文本解析方式
    该模式下，章节文本存储在整个<p>中
    :param name:
    :param chapterTextList:
    :return:
    '''
    isMatch = False
    for text in chapterTextList:
        text = str(text).replace('<p>', '').replace('</p>', '').replace('<br/>', '').replace('&lt', '').replace(' ', '').split('<!--分页-->')[0]
        if ('微信扫码关注' not in text) and ('互联网信息管理办法' not in text) and ('声明' not in text) and ('分页' not in text) and (
                '开始' not in text) and ('回目录' not in text) and ('轩宇阅读网' not in text) and (len(text) != 0) :
            writeInText(name, text + '\r\n')
            isMatch = True
    return isMatch

def writeInText(name,text):
    '''
    文件操作
    :param name:
    :param text:
    :return:
    '''
    fileName = r'%s\%s.txt'%(DIR,name)
    # print('写入文件%s'%(fileName))
    with open(fileName, 'a+', encoding='utf-8') as fb:
        fb.write(text)

def reptileNovel(url,dir):
    '''
    提供向外接口函数
    :param url:
    :param dir:
    :return:
    '''
    global URL
    global DIR
    DIR = dir
    URL = url
    if not os.path.exists(dir):
        os.makedirs(dir)
    homeHtml = getHomeHtml(url)
    dict_chapter = getChapterUrlList(homeHtml)
    for chapterName in dict_chapter.keys():
        # print(chapterName, dict_chapter[chapterName])
        saveChapterText(chapterName, dict_chapter[chapterName])


if __name__ == '__main__':

    reptileNovel(URL,DIR)







