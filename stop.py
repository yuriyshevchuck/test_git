#!/usr/bin/python3
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#(ZENIT) stop
GPIO.setup(31, GPIO.OUT)
GPIO.output(31,False)
GPIO.setup(33, GPIO.OUT)
GPIO.output(33,False)

#(AZIMUTH) stop
GPIO.setup(35, GPIO.OUT)
GPIO.output(35,False)
GPIO.setup(37, GPIO.OUT)
GPIO.output(37,False)