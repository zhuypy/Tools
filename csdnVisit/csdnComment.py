import time
import requests
import re


def vistUrl(url, isGetHtml=False):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    respose = requests.get(url, headers=headers)
    if isGetHtml:
        return respose.content.decode()
    else:
        return respose.status_code


def getBlogList(html_str):
    pattern = r'<a href="(https.*?/[0-9]{9})".*'
    blog_list = re.findall(pattern, html_str)
    return list(set(blog_list))


def vist(url_list):
    for blog_url in url_list:
        print(blog_url)
    while True:
        for blog_url in url_list:
            print(blog_url)
            print(vistUrl(blog_url), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))


if __name__ == '__main__':
    home_url = 'https://blog.csdn.net/zy1007531447'
    html_str = vistUrl(home_url, isGetHtml=True)
    blog_url_list = getBlogList(html_str)
    
