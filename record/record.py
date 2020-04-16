# coding=utf-8
import subprocess, os, sys
import time
import win32api,win32con
import psutil

def loginfo(msg):
    currentTime = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
    msg = '['+currentTime+']'+str(msg)
    # ------------------------------------------TEST-------------------------------------------------------------
    logdir = os.path.join(os.path.dirname(os.path.realpath(sys.executable)),'log')
    # logdir = os.path.join(r'D:\workspace\recordVideo_v1', 'log')
    # ------------------------------------------TEST-------------------------------------------------------------
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
    dirName = os.path.join(avidir,'temp')
    win32api.SetFileAttributes(dirName,win32con.FILE_ATTRIBUTE_HIDDEN)
    return fileName

def judgeprocess(processName):
    loginfo('start judgeprocess ffmpeg-----------------------------------')
    pl = psutil.pids()
    # loginfo(str(pl))
    for pid in pl:
        # loginfo(psutil.Process(pid).name())
        if (processName in psutil.Process(pid).name()) or(psutil.Process(pid).name() == processName ):
            loginfo('ps found')
            return True
    loginfo('ffmepeg not found')
    return False

def startRecord(saveTime,avidir):
    loginfo('start startRecord-----------------------------------')
    # ------------------------------------------TEST-------------------------------------------------------------
    ffmpegPath = os.path.join(os.path.dirname(os.path.realpath(sys.executable)), 'tool', 'fm', 'ffmpeg.exe')
    # ffmpegPath = os.path.join(r'D:\workspace\recordVideo_v1', 'tool', 'fm', 'ffmpeg.exe')
    # ------------------------------------------TEST-------------------------------------------------------------
    while True:
        os.system('taskkill /F /IM ffmpeg.exe')
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
                if judgeprocess('ffmpeg.exe'):
                    loginfo('found ffmpeg on----')
                else:
                    filePath = getSaveFileName(avidir)
                    loginfo(filePath)
                    cmd = ffmpegPath + "  -f gdigrab -framerate 60 -offset_x 0 -offset_y 0 -video_size 1366x768 -i desktop " + filePath
                    subprocess.Popen(cmd, shell=True)
                    loginfo('retry start ffmpeg')
        except Exception as e:
            loginfo(e)
        finally:
            os.system('taskkill /F /IM ffmpeg.exe')

if __name__ == '__main__':
    try:
        loginfo('start main-----------------------------------')
        try:
            saveTime = int(sys.argv[1])
        except:
            saveTime = 1
        loginfo('save Time = %s'%(saveTime))

        #------------------------------------------TEST-------------------------------------------------------------
        cofpath = os.path.join(os.path.dirname(os.path.realpath(sys.executable)),'tool','conf','conf.properties')
        # cofpath = os.path.join(r'D:\workspace\recordVideo_v1','tool','conf','conf.properties')
        # ------------------------------------------TEST-------------------------------------------------------------
        try:
            avidir = getConf(cofpath)
        except:
            avidir = os.path.dirname(os.path.realpath(sys.executable))

        loginfo(avidir)
        startRecord(saveTime,avidir)
    except Exception as e:
        loginfo(e)
