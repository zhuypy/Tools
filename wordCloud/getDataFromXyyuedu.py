import requests
import re

def getHomeHtml(url):
    
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    respose = requests.get(url, headers=headers)
    homeHtml  = respose.content.decode('gbk', 'ignore')
    return homeHtml

def getChapterUrlList(homeHtml):
    dict_chapter = {}
    pattern = r'<a href="(/[A-Za-z]+/[A-Za-z]+/[A-Za-z]+/[0-9]{5}.html)"'
    urlList = re.findall(pattern,homeHtml)
    
    pattern_chapter = r'title="(.+?)"   target="_blank"'
    chapterList = re.findall(pattern_chapter,homeHtml)
    
    for i in range(len(urlList)):
        dict_chapter[urlList[i]] = chapterList[i]
    
    return dict_chapter

def getChapterText(url):
    pattern = r'.*?([\u4E00-\u9FA5]+).*?'
    chapterHtml = getHomeHtml(url)
    writeInText(re.findall(pattern,chapterHtml))
    
def writeInText(textList):
    
    textFile = r'D:\test\wordcloud\wen.txt'
    with open(textFile,'a',encoding='utf-8') as fb:
        for text in textList:
            fb.write(str(text))
        

if __name__ == '__main__':
    # url = 'https://www.xyyuedu.com/wgmz/dongyeguiwu/baiyexingxs/'
    url = 'https://www.xyyuedu.com/gdmz/sidamingzhu/hlmeng/index.html'
    
    
    homeHtml = getHomeHtml(url)
    dict_chapter = getChapterUrlList(homeHtml)
    for chapterUrl in dict_chapter.keys():
        print(chapterUrl,dict_chapter[chapterUrl])
        getChapterText('https://www.xyyuedu.com'+chapterUrl)

    
    
    
    
    
    
    