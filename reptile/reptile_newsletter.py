import requests
import re,os
from bs4 import BeautifulSoup


#此脚本为获取十堰市人民政府网-郧阳区板块的通讯报道
URL = 'http://www.shiyan.gov.cn/ywdt/xqsm/yyq/index.shtml'
DIR = r'D:\test\newsletter'

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
    respose = requests.get(url, headers=headers)
    
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
    for news in bf.find_all('a',attrs={'class':'text-decoration-none'}):
        newsDict[news.find_all('h5')[0].string] = news.attrs['href']
    return newsDict
    
def reptileNews(url,dir):
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

def findByKeywordFromDict(keyword,urlDict):
    result_dict = {}
    for title in urlDict.keys():
        print(title,urlDict[title])
        if findByKeywordFromHtml(keyword,urlDict[title]):
            result_dict[title] = urlDict[title]
            print('命中关键字')
        else:
            print('未命中关键字')
    return result_dict

def findByKeywordFromHtml(keyword,url):
    homeHtml = getHomeHtml(url)
    pattern = r'[\u4E00-\u9FFF]+'
    for part in re.findall(pattern,homeHtml):
        if keyword in part:
            return True
    return False
    
if __name__ == '__main__':
    urlList = [URL]
    urlDict = {}
    print('获取文章列表---------')
    for i in range(1,100):
        urlList.append(URL.replace('.shtml','_%s.shtml'%(i)))
    for url in urlList:
        newsDict = reptileNews(url,DIR)
        urlDict.update(newsDict)
    print(urlDict)
    print('检索目标文章-------------')
    result_dict = findByKeywordFromDict('香菇',urlDict)
    print('[结果集]：',result_dict)

