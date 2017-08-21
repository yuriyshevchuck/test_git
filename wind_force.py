#!/usr/bin/python3
import time
import RPi.GPIO as GPIO
import logging

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#wind force sensor should be connected to the 40-th GPIO pin
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def pulses_to_wind_force(pulces_counter):
  #define formula to convert pulces to wind force here
  wind_force = pulces_counter*1
  logging.info(" Measured wind_force value = " + str(wind_force))
  return wind_force

def get_wind_force():
  start_time = time.time()
  #print(start_time)
  pulses_counter = 0
  while True:
    in_40 = GPIO.input(40)
    while in_40:
      in_40 = GPIO.input(40)
      if time.time() > start_time+1: return pulses_to_wind_force(pulses_counter)
    while not in_40:
      in_40 = GPIO.input(40)
      if time.time() > start_time+1: return pulses_to_wind_force(pulses_counter)
    pulses_counter+=1