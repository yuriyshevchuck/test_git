#!/usr/bin/python3
import time
import RPi.GPIO as GPIO
import logging
import sys
sys.path.append('/home/sun_tracker/')
import tracker_angles as ta
from config import data

splited_conf = {key: list(map(int, value.split())) for key, value in data.items()}

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#(AZIMUTH) motor rotation "-"" pin should be connected to 35 board GPIO
GPIO.setup(35, GPIO.OUT)
GPIO.output(35,False)

GPIO.output(35,True)
try:
	while True :
		print("Azimuth position :" + str(ta.get_tracker_azimuth_angle()) + " | actual (shifted value) is :" + str(ta.get_tracker_azimuth_angle() - splited_conf[ 'shift_az'][0]))
except KeyboardInterrupt:
    GPIO.output(35,False)                  
finally:
	GPIO.output(35,False)