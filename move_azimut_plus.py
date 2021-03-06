#!/usr/bin/python3
import time
import RPi.GPIO as GPIO
import logging
import sys
sys.path.append('/home/sun_tracker/')
import tracker_angles as ta
from config import data

splited_conf = {key: list(map(int, value.split())) for key, value in data.items()}

#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#(AZIMUTH) motor rotation "+"" pin should be connected to 37 board GPIO
GPIO.setup(37, GPIO.OUT)
GPIO.output(37,False)

GPIO.output(37,True)
try:
	while True :
		GPIO.output(37,True)
		print("Azimuth position :" + str(ta.get_tracker_azimuth_angle()) + " | actual (shifted value) is :" + str(ta.get_tracker_azimuth_angle() - splited_conf[ 'shift_az'][0]))
except KeyboardInterrupt:
    GPIO.output(37,False)
except Exception as e:
	print(" error : " + str(e.args[0]))
finally:
	GPIO.output(37,False)