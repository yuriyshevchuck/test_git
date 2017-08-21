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

#(ZENIT) motor rotation "+"" pin should be connected to 31 board GPIO
GPIO.setup(31, GPIO.OUT)
GPIO.output(31,False)

GPIO.output(31,True)
try:
	while True :
		print("Altitude position :" + str(ta.get_tracker_altitude_angle()) + " | actual (shifted value) is :" + str(ta.get_tracker_altitude_angle() - splited_conf[ 'shift_alt'][0]))
except KeyboardInterrupt:
    GPIO.output(31,False)
except Exception as e:
	print(" error : " + str(e.args[0]))
finally:
	GPIO.output(31,False)
