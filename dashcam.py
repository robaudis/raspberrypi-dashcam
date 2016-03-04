import picamera
import datetime as dt
import os
import time
from multiprocessing import Process, Pipe

def RecordVideo(dir, gpspipe):
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.framerate = 24
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = gpspipe.recv()
        
        camera.start_recording(dir + '/%s.h264' % dt.datetime.now().strftime('%Y%m%dT%H%M%S'))
        start = dt.datetime.now()
        
        while True:
            while (dt.datetime.now() - start).seconds < 10:
                camera.annotate_text = gpspipe.recv()
                
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
    RecordVideo('/dashcam-videos', pipe_a)