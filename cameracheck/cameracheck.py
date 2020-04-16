import usb.core
import time
import os

if __name__ == '__main__':
    while True:
        if usb.core.find(idVendor=0x046D, idProduct=0xC077) is not None:
            time.sleep(3)
        else:
            os.system('shutdown -r -t 0')




