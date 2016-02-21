import picamera
import datetime as dt

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 24
    camera.annotate_background = picamera.Color('black')
    camera.annotate_text = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    camera.start_recording("/dashcam-videos/%s.h264" % dt.datetime.now().strftime("%Y%m%dT%H%M%S"))
    start = dt.datetime.now()
    for i in range(0,10):
        while (dt.datetime.now() - start).seconds < 5:
            camera.annotate_text = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            camera.wait_recording(0.2)
        camera.split_recording("/dashcam-videos/%s.h264" % dt.datetime.now().strftime("%Y%m%dT%H%M%S"))
        start = dt.datetime.now()
        
    camera.stop_recording()