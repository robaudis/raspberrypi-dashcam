import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.start_recording('/dashcam-videos/my_video.h264')
    camera.wait_recording(30)
    camera.stop_recording()