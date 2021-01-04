import requests
import os
import shutil
import urllib.request
import urllib
import re


def vistUrl(url,isGetJson=True):
    '''
    访问url，默认获取返回Json
    :param url:
    :param isGetHtml:
    :return:默认返回字典，若isGetJson=False，则返回response对象
    '''
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'cookie':'_ga=GA1.1.314232902.1609310189; picHost=http%3A//www-mipengine-org.mipcdn.com/i/p3.manhuapan.com; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1609310206,1609310240; _ga_1FZE0C2L80=GS1.1.1609314430.2.1.1609314677.0; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1609314684'
    }
    respose = requests.get(url, headers=headers)
    if isGetJson:
        return respose.json()
    else:
        return respose

def initFilePath(path,isFile=False,clear=False):
    '''
    初始化文件目录
    :param save_path:
    :return:
    '''
    if isFile:
        if os.path.exists(path) and clear:
            os.remove(path)
    else:
        if os.path.exists(path) and clear:
            shutil.rmtree(path)
        elif not os.path.exists(path):
            os.makedirs(path)
        else:
            pass

def logWrite(msg,log_file):
    with open(log_file, 'a+', encoding='utf-8') as fb:
        print(msg)
        fb.write(msg + '\r')
        
def saveImg(img_url,img_name,img_file):
    try:
        response = urllib.request.urlopen(img_url)
        get_img = response.read()
        with open(img_file, 'wb') as fb:
            fb.write(get_img)
            print('下载【%s】至文件夹【%s】，完成' % (img_name, img_file))
    except urllib.error.HTTPError as e:
        logWrite(e.reason)


def getUrlList(pattern,html_str):
    # pattern = r'<a href="(https.*?/[0-9]{9})".*'
    url_list = re.findall(pattern, html_str)
    return list(set(url_list))