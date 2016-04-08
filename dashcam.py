import picamera
import datetime as dt
import time

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
                
            if not upsc.haspower:
                break
                
            camera.split_recording(dir + '/%s.h264' % dt.datetime.now().strftime('%Y%m%dT%H%M%S'))
            start = dt.datetime.now()
            
        camera.stop_recording()        
        
if __name__ == '__main__':
    try:
        upsc = ups.UpsController()
        upsc.start()   
        
        gpsc = gps.GpsController()
        gpsc.start()
        
        delete = file.FileMaintenance('/dashcam-videos')
        delete.start()
        
        RecordVideo('/dashcam-videos', 120, gpsc, upsc)
    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        print 'Setting threads to stop...'
        print 'gps'
        gpsc.running = False
        print 'file'
        delete.running = False
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
