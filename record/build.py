import os,subprocess
from shutil import copy,rmtree
try:
    rmtree(r'D:\build\recordVideo_build\v1')
except:
    pass
try:
    rmtree(r'D:\build\recordVideo_build\log')
except:
    pass
try:
    rmtree(r'D:\build\recordVideo_build\temp')
except:
    pass
os.remove(r'D:\build\recordVideo_build\record.exe')
os.mkdir(r'D:\build\recordVideo_build\v1')
os.chdir(r'D:\build\recordVideo_build\v1')
os.system(r'pyinstaller --onefile --nowindowed --icon="D:\build\recordVideo_build\tool\ico\1.ico" D:\workspace\recordVideo_v1\record.py')
copy(r'D:\build\recordVideo_build\v1\dist\record.exe',r'D:\build\recordVideo_build')

