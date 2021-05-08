# coding=utf-8
import subprocess, os, sys
import time
import psutil

#------------------------------------------TEST-------------------------------------------------------------
# BASE_PATH = os.path.dirname(os.path.realpath(sys.executable))
BASE_PATH = r'D:\ku\Tools\record'
# ------------------------------------------TEST------------------------------------------------------------

def loginfo(msg):
    currentTime = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
    msg = '['+currentTime+']'+str(msg)

    logdir = os.path.join(BASE_PATH, 'log')
    if not os.path.isdir(logdir):
        os.makedirs(logdir)

    logfile = os.path.join(logdir,'record.log')
    with open(logfile,'a+')as fb:
        fb.write(msg+'\r\n')
        print(msg)

def getConf(filePath):
    with open(filePath,'r',encoding='utf8') as fb:
        return fb.read()


def getSaveFileName(avidir):
    loginfo('start getSaveFileName-----------------------------------')
    currentTime = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime())
    time_sub=currentTime.split('_')
    fileName = os.path.join(avidir,'temp',time_sub[0],time_sub[1],time_sub[2],currentTime+'.avi')
    if not os.path.isdir(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))
    return fileName

def judgeprocess(processName):
    loginfo('start judgeprocess %s-----------------------------------'%(processName))
    pl = psutil.pids()
    # loginfo(str(pl))
    for pid in pl:
        # loginfo(psutil.Process(pid).name())
        processName = processName.lower()
        psName = psutil.Process(pid).name().lower()
        if ((processName in psName) or (processName == psName) ):
            # loginfo(psutil.Process(pid).name())
            loginfo('ps found')
            return True
    loginfo('%s not found'%(processName))
    return False

def startRecord(saveTime,avidir):
    loginfo('start startRecord-----------------------------------')
    ffmpegPath = os.path.join(BASE_PATH, 'tool', 'fm', 'ffmpeg.exe')
    while True:
        os.system('taskkill /F /IM ffmpeg.exe')
        if  not findExeStart():
            time.sleep(5)
            continue
        try:
            filePath = getSaveFileName(avidir)
            loginfo(filePath)
            cmd=ffmpegPath + "  -f gdigrab -framerate 60 -offset_x 0 -offset_y 0 -video_size 1366x768 -i desktop " + filePath
            loginfo(cmd)
            subprocess.Popen(cmd ,shell=True)
            loginfo('excute cmd suc')
            for i in range(saveTime*6):
                time.sleep(10)
                loginfo('check ffmpeg ----%s---'%(i))
                if judgeprocess('ffmpeg.exe') and findExeStart():
                    loginfo('found ffmpeg on----')
                elif (not judgeprocess('ffmpeg.exe')) and findExeStart():
                    filePath = getSaveFileName(avidir)
                    loginfo(filePath)
                    cmd = ffmpegPath + "  -f gdigrab -framerate 60 -offset_x 0 -offset_y 0 -video_size 1366x768 -i desktop " + filePath
                    subprocess.Popen(cmd, shell=True)
                    loginfo('retry start ffmpeg')
                elif not findExeStart():
                    loginfo('stop recoed')
                    break
        except Exception as e:
            loginfo(e)
        finally:
            os.system('taskkill /F /IM ffmpeg.exe')
            
def findExeStart():
    cofpath_exe = os.path.join(BASE_PATH, 'tool', 'conf', 'exe.properties')
    cofpath_mode = os.path.join(BASE_PATH, 'tool', 'conf', 'mode.properties')
    
    exe_list = getConf(cofpath_exe).split('=')
    mode  = getConf(cofpath_mode)
    
    if mode == 'all':
        return judgeprocess(exe_list[0]) and judgeprocess(exe_list[1]) and judgeprocess(exe_list[2])
        
    elif mode == 'any':
        return judgeprocess(exe_list[0]) or judgeprocess(exe_list[1]) or judgeprocess(exe_list[2])
    else:
        loginfo('Wrong mode configuration, please configure "all" or "any" in the mode.properties file')
        return False


if __name__ == '__main__':
    try:
        loginfo('start main-----------------------------------')
        try:
            saveTime = int(sys.argv[1])
        except:
            saveTime = 1
        loginfo('save Time = %s'%(saveTime))
        cofpath_avidir = os.path.join(BASE_PATH, 'tool', 'conf', 'conf.properties')
        try:
            avidir = getConf(cofpath_avidir)
        except:
            avidir = os.path.dirname(os.path.realpath(sys.executable))

        loginfo(avidir)
        startRecord(saveTime,avidir)
    except Exception as e:
        loginfo(e)
    
    
    