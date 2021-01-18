from util import *
import socket
# socket.setdefaulttimeout(20)

LOG_FILE = r'D:\test\cartoon.log'
SAVE_PATH = r'D:\test\cartoon'

def logWrite_cartoon(msg):
    logWrite(msg,LOG_FILE)

def getChapterList(url_home):
    resp = vistUrl(url_home, False)
    pattern = r'<a href="(.{0,10}[0-9]{3}/)"'
    chapterList = getUrlList(pattern,resp.text)
    resp.close()
    return [url_home+i for i in chapterList]

def getIndexHtmlList(url_chapter):
    resp = vistUrl(url_chapter, False)
    pattern = r'<a href="(index_[0-9]{1,3}.html)"'
    chapterList = getUrlList(pattern, resp.text)
    resp.close()
    return [url_chapter + i for i in chapterList]

def getImgList(url_html):
    resp = vistUrl(url_html, False)
    pattern = r'<img src="(https:.*?.jpg)"'
    url_img = getUrlList(pattern, resp.text)
    print('-------------------------------------------------------------------------------------------')
    print(resp.text)
    print('-------------------------------------------------------------------------------------------')
    print(url_img)

def test():
    url_home = 'https://www.fzdm.com/manhua/74/'
    chapterList = getChapterList(url_home)
    # for url_charpter in chapterList:
    #     getIndex(url_charpter)
    index_html_list = getIndexHtmlList(chapterList[0])
    getImgList(index_html_list[0])
    

if __name__ == '__main__':
    initFilePath(LOG_FILE,isFile=True,clear=True)
    initFilePath(SAVE_PATH)
    test()
    











