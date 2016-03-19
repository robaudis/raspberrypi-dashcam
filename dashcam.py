import picamera
import datetime as dt
import os
import time
from multiprocessing import Process, Pipe

def RecordVideo(dir, length, gpspipe):
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.framerate = 24
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = gpspipe.recv()
        
        camera.start_recording(dir + '/%s.h264' % dt.datetime.now().strftime('%Y%m%dT%H%M%S'))
        start = dt.datetime.now()
        
        while True:
            while (dt.datetime.now() - start).seconds < length:
                camera.annotate_text = gpspipe.recv()
                
            camera.split_recording(dir + '/%s.h264' % dt.datetime.now().strftime('%Y%m%dT%H%M%S'))
            start = dt.datetime.now()
            
        camera.stop_recording()
        
def DeleteOldest(dir):
    while True:
        time.sleep(30)
        files = os.listdir(dir)
        while DirectorySize(dir + '/') > 10485760:#2097152000:
            if len(files) > 1:
                files.sort()
                os.remove(dir + '/' + files.pop(0))
            time.sleep(30)
        
def DirectorySize(dir):
    return sum(os.path.getsize(dir + f) for f in os.listdir(dir))
    
def GetGPSData(pipe):
    while True:
        time.sleep(1)
        pipe.send(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
if __name__ == '__main__':
    pipe_a, pipe_b = Pipe()
    delete = Process(target=DeleteOldest, args=('/dashcam-videos',))
    getgps = Process(target=GetGPSData, args=(pipe_b,))
    getgps.start()
    delete.start()
    RecordVideo('/dashcam-videos', 10, pipe_a)