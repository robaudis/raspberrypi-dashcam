# Raspberry Pi Dashcam

This is a simple implementation of a car dashcam for a Raspberry Pi.

Features:
* Video annotation with date and time, speed, position
* Rolling file deletion
* UPS support

Main hardware needed:
* Pi (I used a Pi2 Model B) and case
* Pi camera module (I used one of these https://www.tindie.com/products/freto/pi-camera-hdmi-cable-extension/ and a 3m ultra thin HDMI cable http://amzn.eu/i3XP7AO to allow the pi to live in the glove box and have the camera mounted below my rearview mirror)
* Adafruit Ultimate GPS breakout (https://www.modmypi.com/raspberry-pi/breakout-boards/adafruit/adafruit-gps-ultimate-breakout-board) + external antenna
* UPS Pico (http://pimodules.com/) to allow clean shut down when the ignition is turned off and provides hardware RTC
* Drok voltage step down converter (http://amzn.eu/igNtd3K) to connect to the car ignition via the fuse box with a fuse tap.
