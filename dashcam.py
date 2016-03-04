import picamera
import datetime as dt
import os
import time
from multiprocessing import Process

def RecordVideo(dir):
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.framerate = 24
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        camera.start_recording(dir + '/%s.h264' % dt.datetime.now().strftime('%Y%m%dT%H%M%S'))
        start = dt.datetime.now()
        
        while True:
            while (dt.datetime.now() - start).seconds < 10:
                camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                camera.wait_recording(1)
            camera.split_recording(dir + '/%s.h264' % dt.datetime.now().strftime('%Y%m%dT%H%M%S'))
            start = dt.datetime.now()
            
        camera.stop_recording()
        
def DeleteOldest(dir):
    while True:
        time.sleep(5)
        files = os.listdir(dir)
        while DirectorySize(dir + '/', files) > 5242880:
            if len(files) > 1:
                files.sort()
                os.remove(dir + '/' + files.pop(0))
        
def DirectorySize(dir, files):
    return sum(os.path.getsize(dir + f) for f in files)
    
if __name__ == '__main__':
    p = Process(target=DeleteOldest, args=('/dashcam-videos',))
    p.start()
    RecordVideo('/dashcam-videos')