import RPi.GPIO as GPIO
import time
import os
import threading

class UpsController(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.haspower = True
    self.running = True 

  def run(self):
    GPIO.setmode(GPIO.BCM) # Set pin numbering to board numbering
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Setup pin 27 as an input
    #GPIO.setup(22, GPIO.OUT) # Setup pin 22 as an output

    while self.running: # Setup a while loop to wait for a button press
        #GPIO.output(22,True)
        time.sleep(0.25) # Allow a sleep time of 0.25 second to reduce CPU usage
        #GPIO.output(22,False)
        if(GPIO.input(27)==0): # Setup an if loop to run a shutdown command when button press sensed
            self.haspower = False            
            break

        time.sleep(0.25) # Allow a sleep time of 0.25 second to reduce CPU usage
    GPIO.cleanup()
        
