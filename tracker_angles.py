#!/usr/bin/python3

import time 
import sys 
import spidev
import RPi.GPIO as GPIO
import logging
sys.path.append('/home/sun_tracker/')
from config import data

#logging.basicConfig(filename='/var/log/sun_tracker/SPI_encoders.log', format='%(levelname)s: %(asctime)s %(message)s',level=logging.INFO)

splited_conf = {key: list(map(int, value.split())) for key, value in data.items()}

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#CS pin for encoder #1 ALTITUDE
GPIO.setup(36, GPIO.OUT, initial=GPIO.LOW)

#CS pin for encoder #2 AZIMUTH
GPIO.setup(38, GPIO.OUT, initial=GPIO.LOW)

def check_spi_data(encoder_identificator_for_logging):
  try:
    spi = spidev.SpiDev()
    spi.open(0,0)
    response = spi.readbytes(3)
    spi.close()
  except Exception as e:
    logging.error(" error while reaing data from SPI encoder = " + encoder_identificator_for_logging + str(e.args[0]))
    #here sending enail should be implemented
    #also some alarm lamp on some GPIO pin should be switched on or appropriate message showed on a display
    return (" error " + str(e.args[0]))
  return response

def convert_spi_response(response):
  print(response)
  response[1]&=0b1110000
  response[0]<<=3
  response[1]>>=4
  #return degrees
  return (response[0] | response[1])*(360/1024)

def get_tracker_altitude_angle():
  #select the #1 ALTITUDE encoder
  time.sleep(0.5) # test to check if it helps to avoid getting false data
  GPIO.output(36, True)
  time.sleep(0.03)
  GPIO.output(36, False)
  time.sleep(0.03)
  response = round(convert_spi_response(check_spi_data("alt ")),2)
  logging.info(" Measured alt angle of the tracker (actual value (not shifted))) = " + str(response))
  if(response>360): 
    logging.error("Altitude SPI encoder responded with error, please check it");
    # trigger sending of email about error here
    return (-1)
  return response

def get_tracker_azimuth_angle():
  #select the #2 AZIMUTH encoder
  time.sleep(0.5) # test to check if it helps to avoid getting false data
  GPIO.output(38, True)
  time.sleep(0.03)
  GPIO.output(38, False)
  time.sleep(0.03)
  response = round(convert_spi_response(check_spi_data("az ")),2)
  logging.info(" Measured az angle of the tracker (actual value (not shifted))) = " + str(response))
  if(response>360): 
    logging.error("Azimuth SPI encoder responded with error, please check it");
    # trigger sending of email about error here
    return (-1)
  return response
