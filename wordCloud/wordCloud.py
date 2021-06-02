import os
import numpy as np
from PIL import Image
import wordcloud
import jieba

textFile = r'D:\test\wordcloud\wen.txt'
imgFile = r'D:\test\wordcloud\1.jpg'

def getText(textFile):
    with open(textFile,'r',encoding='utf-8') as fb:
        text = fb.read()
        return text

def getCloud(text):
    wordList = jieba.lcut(text)
    mk = np.array(Image.open(imgFile))
    cloud = wordcloud.WordCloud(font_path="msyh.ttc",background_color="white",mask=mk,min_font_size=5)
    cloud.generate(" ".join(wordList))
    cloud.to_file(r'D:\test\wordcloud\2.jpg')


if __name__ == '__main__':
    getCloud(getText(textFile))
