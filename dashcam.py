import picamera
import datetime as dt
import os
import time
import gps
import socket
from multiprocessing import Process, Pipe, Value, Array
from ctypes import c_bool, c_char
import RPi.GPIO as GPIO

def RecordVideo(dir, length, gpstext, haspower):
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
            while (dt.datetime.now() - start).seconds < length and haspower.value:
                datetime_str = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                camera.annotate_text = 'WG07 HTA : %s : %s' % (gpstext.value, datetime_str)
                
            if not haspower.value:
                break
                
            camera.split_recording(dir + '/%s.h264' % dt.datetime.now().strftime('%Y%m%dT%H%M%S'))
            start = dt.datetime.now()
            
        print "UPS Sent power signal, stopping"
        camera.stop_recording()
        
def DeleteOldest(dir):
    while True:
        time.sleep(60)
        while DirectorySize(dir + '/') > 2097152000:            
            files = os.listdir(dir)
            files.sort()
            if len(files) > 1:               
                os.remove(dir + '/' + files.pop(0))
            time.sleep(1)
        
def DirectorySize(dir):
    return sum(os.path.getsize(dir + f) for f in os.listdir(dir))
    
def GetGPSData(gpstext, haspower):
    session = None
    connected = False
    
    while haspower.value:
        while not connected:
            try:
                session = gps.gps("localhost", "19000")
                connected = True
            except socket.error:
                print 'GPSD not available, trying again'
                time.sleep(2)
            
        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

        for report in session:            
            if session.fix.mode > 2:            
                text = 'lat %.5f, lon %.5f %.1fmph' % (session.fix.latitude, session.fix.longitude, session.fix.speed * 2.23694)                
                gpstext.value = text       
            else:
                gpstext.value = 'No GPS Fix'
                
        connected = False
        gpstext.value = 'No GPS Fix'        
        print 'GPSD connection lost - trying to reconnect'
        time.sleep(2)
        
def MonitorUPS(haspower):
    GPIO.setmode(GPIO.BCM) # Set pin numbering to board numbering
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Setup pin 27 as an input
    GPIO.setup(22, GPIO.OUT) # Setup pin 22 as an output

    while True: # Setup a while loop to wait for a button press
        GPIO.output(22,True)
        time.sleep(0.25) # Allow a sleep time of 0.25 second to reduce CPU usage
        GPIO.output(22,False)
        if(GPIO.input(27)==0): # Setup an if loop to run a shutdown command when button press sensed
            haspower.value = False
            time.sleep(5)
            os.system("sudo shutdown -h now") # Send shutdown command to os
            break

        time.sleep(0.25) # Allow a sleep time of 0.25 second to reduce CPU usage

if __name__ == '__main__':
    haspower = Value(c_bool, True)
    ups = Process(target=MonitorUPS, args=(haspower,))
    ups.start()
      
    delete = Process(target=DeleteOldest, args=('/dashcam-videos',))
    
    gpstext = Array('c', 'No GPS Fix')
    getgps = Process(target=GetGPSData, args=(gpstext, haspower))
    getgps.start()
    delete.start()
    RecordVideo('/dashcam-videos', 120, gpstext, haspower,)
    
    getgps.join()
    delete.join()
    ups.join()
