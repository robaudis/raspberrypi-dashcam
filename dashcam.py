import picamera
import datetime as dt
import time
import os
from multiprocessing import Process, Value
from ctypes import c_bool
import GpsController as gps
import UpsController as ups
import FileMaintenance as file

def RecordVideo(dir, length, gpsc, upsc):
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.vflip = True
        camera.hflip = True
        camera.framerate = 24
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text_size = 24
        
        camera.start_recording(dir + '/%s.h264' % dt.datetime.now().strftime('%Y%m%dT%H%M%S'))
        start = dt.datetime.now()
        
        while True:
            while (dt.datetime.now() - start).seconds < length and upsc.haspower:
                datetime_str = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                camera.annotate_text = 'WG07 HTA : %s : %s' % (gpsc.gpsstring, datetime_str)
                time.sleep(0.25)
                
            if not upsc.haspower:
                break
                
            camera.split_recording(dir + '/%s.h264' % dt.datetime.now().strftime('%Y%m%dT%H%M%S'))
            start = dt.datetime.now()
            
        camera.stop_recording()        
        
def StopThreads(gpsc, upsc, delete_running):
    print 'Setting threads to stop...'
    print 'gps'
    gpsc.running = False
    print 'file'
    delete_running.value = False
    print 'ups'
    upsc.running = False
    
    print 'waiting for threads to stop...'
        
    gpsc.join()
    print 'gps stopped'
    delete.join()
    print 'file stopped'
    upsc.join()
    print 'ups stopped'
    print 'Threads stopped. Exited'
        
if __name__ == '__main__':
    try:
        upsc = ups.UpsController()
        upsc.start()   
        
        gpsc = gps.GpsController()
        gpsc.start()
        
        delete_running = Value(c_bool, True)
        delete = Process(target=file.DeleteOldest, args=('/dashcam-videos', delete_running,))
        delete.start()
        
        RecordVideo('/dashcam-videos', 120, gpsc, upsc)
        
        StopThreads(gpsc, upsc, delete_running)
        time.sleep(5)
        os.system("sudo shutdown -h now") # Send shutdown command to os
    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        StopThreads(gpsc, upsc, delete_running)

