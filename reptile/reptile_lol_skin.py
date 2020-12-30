import requests
import os
import shutil
import urllib.request
import urllib

LOG_FILE = r'D:\test\hero.log'
SAVE_PATH = r'D:\test\hero'

def vistUrl(url,isGetJson=True):
    '''
    访问url，默认获取返回Json
    :param url:
    :param isGetHtml:
    :return:默认返回字典，若isGetJson=False，则返回response对象
    '''
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    respose = requests.get(url, headers=headers)
    if isGetJson:
        return respose.json()
    else:
        return respose

def getHeroNumber():
    '''
    获取全英雄Id，组成list返回
    :return: list
    '''
    heroId_list = []
    url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
    respost_json = vistUrl(url)
    
    for hero in respost_json.get('hero'):
        heroId_list.append(hero.get('heroId'))
    
    return heroId_list

def getImgUrl(url):
    '''
    获取单个英雄的名称，皮肤名称，皮肤图片，返回list
    :param url:
    :return:
    '''
    skin_Info = []
    respost_json = vistUrl(url)

    for skin in respost_json.get('skins'):
        if  skin.get('mainImg') != "":
            skin_Info.append([skin.get('name'),skin.get('mainImg')])
    return skin_Info

def initFilePath(path,clear=False):
    '''
    初始化文件目录
    :param save_path:
    :return:
    '''
    if os.path.isfile(path):
        if os.path.exists(path) and clear:
            os.remove(path)
    else:
        if os.path.exists(path) and clear:
            shutil.rmtree(path)
        elif not os.path.exists(path):
            os.makedirs(path)
        else:
            pass
def downloadSkinImg(hero_dict,save_path):
    '''
    下载全英雄皮肤并形成文件管理体系
    :param hero_dict:
    :return:
    '''
    logWrite(str(hero_dict))
    for heroId in hero_dict.keys():
        skin_list = hero_dict.get(heroId)
        hero_name = skin_list[0][0]
        hero_dir = os.path.join(save_path,hero_name)
        
        initFilePath(hero_dir)
        
        logWrite('开始下载【%s】的皮肤图片，请等待...'%(hero_name))
        for skin in skin_list:
            skin_name = skin[0].replace('“',' ').replace('”',' ').replace('？','').replace(':',' ').replace('"',' ').replace('/','-').replace('\\','-')
            skin_Img = skin[1]
            skin_file = os.path.join(hero_dir, skin_name+'.jpg')
            if os.path.exists(skin_file):
                logWrite('【%s】已存在，跳过下载'%(skin_name))
                continue
                
            logWrite('开始从【%s】下载【%s】至文件夹【%s】，请等待...' % (skin_Img,skin_name,skin_file))
            #下载url图片
            request = urllib.request.Request(skin_Img)
            try:
                response = urllib.request.urlopen(request)
                get_img = response.read()
                with open(skin_file, 'wb') as fb:
                    fb.write(get_img)
                    logWrite('下载【%s】至文件夹【%s】，完成' % (skin_name, skin_file))
            except urllib.error.HTTPError as e:
                logWrite(e.reason)
                
            

def logWrite(msg):
    
    with open(LOG_FILE,'a+',encoding='utf-8') as fb:
        print(msg)
        fb.write(msg+'\r')

if __name__ == '__main__':
    initFilePath(LOG_FILE,clear=True)
    hero_dict = {}
    heroId_list = getHeroNumber()
    for heroId in heroId_list:
        logWrite('开始获取id为【%s】的英雄图库地址，请稍等...'%(heroId))
        home_url = 'https://game.gtimg.cn/images/lol/act/img/js/hero/%s.js'%(heroId)
        hero_dict[heroId] = getImgUrl(home_url)
        logWrite('获取【%s】的图库地址，已完成。共获取皮肤【%s】张' % (hero_dict[heroId][0][0],len(hero_dict[heroId])))

    initFilePath(SAVE_PATH)
    
    downloadSkinImg(hero_dict,SAVE_PATH)

    