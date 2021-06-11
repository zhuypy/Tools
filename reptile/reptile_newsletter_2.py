import requests
import re, os
from bs4 import BeautifulSoup
import time

# 此脚本为获取秦楚网-小学教育板块的通讯报道
URL = 'http://www.10yan.com/jiaoyu/xxjy/.shtml'
FILENAME = r'D:\test\newsletter\news.txt'


def getHomeHtml(url, isGetStatusCode=False):
    '''
    请求页面
    :param url:
    :param isGetStatusCode:
    :return:
    '''
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    try:
        respose = requests.get(url, headers=headers,timeout=0.1)
    except:
        print('请求超时')
    
    if isGetStatusCode:
        return respose.status_code
    
    # homeHtml = respose.content.decode('gbk', 'ignore')
    homeHtml = respose.content.decode()
    return homeHtml


def getNewsDict(homeHtml):
    '''
    获取当前页的小说
    :param homeHtml:
    :return:
    '''
    newsDict = {}
    bf = BeautifulSoup(homeHtml)
    for news in bf.find_all('a', attrs={'target': '_blank','style':'color:'}):
        newsDict[news.string] = news.attrs['href']
    return newsDict


def reptileNews(url, dir):
    '''
    提供向外接口函数
    :param url:
    :param dir:
    :return:
    '''
    if not os.path.exists(dir):
        os.makedirs(dir)
    homeHtml = getHomeHtml(url)
    newsDict = getNewsDict(homeHtml)
    return newsDict


def findByKeywordFromDict(keyword, urlDict):
    result_dict = {}
    for title in urlDict.keys():
        print(title, urlDict[title])
        if findByKeywordFromHtml(keyword, urlDict[title]):
            result_dict[title] = urlDict[title]
            print('----------命中关键字--------------')
            # time.sleep(3)
        else:
            print('未命中关键字')
    return result_dict


def findByKeywordFromHtml(keyword, url):
    try:
        homeHtml = getHomeHtml(url)
    except:
        return False
    pattern = r'[\u4E00-\u9FFF]+'
    for part in re.findall(pattern, homeHtml):
        if keyword in part:
            return True
    return False

def writeDown(result_dict):
    for news in result_dict.keys():
        homeHtml = getHomeHtml(result_dict[news])
        bs = BeautifulSoup(homeHtml)
        partList = bs.find('div',attrs={'class':'article-content fontSizeSmall BSHARE_POP'}).find_all('p')
        for p in partList:
            if '报道：' in str(p):
                writeInText(FILENAME,re.findall(r'报道：(.*)</p>',str(p))[0])
            elif p.string == None:
                continue
            else:
                writeInText(FILENAME,p.string)
    
        
def writeInText(fileName,text):
    '''
    文件操作
    :param name:
    :param text:
    :return:
    '''
    with open(fileName, 'a+', encoding='utf-8') as fb:
        fb.write(text)

if __name__ == '__main__':
    urlList = []
    urlDict = {}
    print('获取文章列表---------')
    for i in range(1, 83):
        urlList.append(URL.replace('.shtml', '%s.shtml' % (i)))
    for url in urlList:
        newsDict = reptileNews(url, FILENAME)
        urlDict.update(newsDict)
    print('检索目标文章-------------')
    # urlDict = {'1':'http://www.10yan.com/2021/0419/710158.shtml'}
    result_dict = findByKeywordFromDict('朱林海', urlDict)
    print('[结果集]：', result_dict)
    writeDown(result_dict)
