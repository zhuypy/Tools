import os,subprocess
from shutil import copy,rmtree
dir_path = r'D:\build\recordVideo_v2_build'
version = 'v3'
try:
    rmtree(os.path.join(dir_path,version))
except:
    pass
try:
    rmtree(os.path.join(dir_path,'log'))
except:
    pass
try:
    rmtree(os.path.join(dir_path,'temp'))
except:
    pass
try:
    os.remove(os.path.join(dir_path,'record.exe'))
except:
    pass
os.mkdir(os.path.join(dir_path,version))
os.chdir(os.path.join(dir_path,version))
os.system(r'pyinstaller --onefile --nowindowed --icon="D:\build\recordVideo_v2_build\tool\ico\1.ico" D:\ku\Tools\record\recordv2.py')
copy(r'%s\dist\recordv2.exe'%(os.path.join(dir_path,version)),r'D:\build\recordVideo_v2_build')

