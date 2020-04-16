
__author__ = 'zhuy'

'''
    该方法自动生成20000用户，名称以per开头，生成文件可直接导入loadrunner配置项
'''

dataFile =""
username = "per"

with open(dataFile,'w',encoding='utf-8') as fb:
    fb.truncate()
    fb.write('username\r\n')
    for i in range(1,20001):
        j = str(i)
        fb.write(username+j.zfill(5)+'\n')

