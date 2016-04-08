import time
import os
import threading

def DeleteOldest(dir, keep_running):
    while keep_running.value:
        for i in range(59):
            time.sleep(1)
            if not keep_running.value:
                break
                
        while keep_running.value and DirectorySize(dir + '/') > 4194304000:            
            files = os.listdir(dir)
            files.sort()
            if len(files) > 1:               
                os.remove(dir + '/' + files.pop(0))
            time.sleep(5)
        
def DirectorySize(dir):
    return sum(os.path.getsize(dir + f) for f in os.listdir(dir))