import time
import requests
import re


def vistUrl(url):
    
    
    # payload = {}
    # headers = {
    #     'Cookie': 'uuid_tt_dd=10_37481401500-1606373606501-221963; dc_session_id=10_1606373606501.576673; dc_sid=614c4943949a47bab63329e8244a0fa3'
    # }
    #
    # response = requests.request("GET", url, headers=headers, data=payload)
    response = requests.request("GET", url)
    # print(response.json())
    print(response)

def getBlogList(html_str):
    pattern = r'<a href="(https://blog.csdn.net/zy1007531447/article/details/[0-9]{9})"'
    blog_list = re.findall(pattern, html_str)
    print(blog_list)
    return list(set(blog_list))


def vist(url_list):
    for blog_url in url_list:
        print(blog_url)
    while True:
        for blog_url in url_list:
            print(blog_url)
            print(vistUrl(blog_url), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))


def updateCSDNListFile(url_list):
    print(len(url_list))
    file = r'D:\work\jmeter\test\data.txt'
    with open(file, 'w+', encoding='utf-8') as fb:
        for blog_url in url_list:
            blog_number = blog_url.split('/')[-1]
            fb.write(blog_number + '\r')
    
    with open(file, 'r', encoding='utf-8') as fb:
        for line in fb.readlines():
            print(line)


if __name__ == '__main__':
    home_url = 'https://blog.csdn.net/community/home-api/v1/get-business-list?page=1&size=100&businessType=blog&orderby=&noMore=false&username=zy1007531447'
    # html_str = vistUrl(home_url)
    # blog_url_list = getBlogList(html_str)
    # updateCSDNListFile(blog_url_list)

    import requests

    # url = "http://blog.csdn.net/community/home-api/v1/get-business-list"
    # params ={'page':'1','size':'100','businessType':'blog','orderby':'','noMore':'false','username':'zy1007531447'}

    response = requests.post(home_url)

    print(response.text)
    print(response.content.decode())