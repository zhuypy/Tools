from bs4 import BeautifulSoup
import requests
import re

url = 'https://www.xyyuedu.com/wgmz/dongyeguiwu/baiyexingxs/47448_2.html'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}
respose = requests.get(url, headers=headers)
htmlText = respose.content.decode('gbk', 'ignore')


bf =BeautifulSoup(htmlText)
subList = bf.find_all('div',id="onearcxsbd")
for sub in subList:
    print('---------------------------------------------------------------------')
    print(str(sub).split('<!--分页-->')[0].replace('<br/>',''))
# print(subList)
# print(str(subList).replace('<p>','').replace('</p>','').replace(s1,'').replace(s2,'').replace(s3,''))




