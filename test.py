#!/usr/bin/python3
import calculate_azimuth_zenit as caz
import tracker_angles as ta
import wind_force as wf
import light_level as ll
from config import data
import os, signal
import sys


tracker_altitude = ta.get_tracker_altitude_angle()
tracker_azimuth = ta.get_tracker_azimuth_angle()
pid = []

print("Processes")
for line in os.popen("ps ax | grep " + "track_sun_main" + " | grep -v grep"):
  fields = line.split()
  pid.append(fields[0]) 
  #os.kill(int(pid), signal.SIGKILL)

if pid :
	print( "THE SYSTEM IS BUZZY")
	sys.exit()


splited_conf = {key: list(map(int, value.split())) for key, value in data.items()}
print("  <br>  " + "=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+" + "  <br>  ")
print( " Read data from config " + str(data) + "  <br>  ")
print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+" + "  <br>  ")
print(" Pysolar calculated alt = " + str(caz.get_alt()) + "  <br>  " )
print(" Pysolar calculated az = " + str(caz.get_az()) + "  <br>  " )
print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+" + "  <br>  ")
print(" SPI encoder measured ACTUAL ALT = " + str(tracker_altitude) + "  <br>  ")
print(" SPI encoder measured SHIFTED (NORMALIZED) ALT = " + str((90 - (tracker_altitude - splited_conf[ 'shift_alt'][0]))) + "  <br>  ")
print(" SPI encoder measured ACTUAL AZ = " + str(tracker_azimuth) + "  <br>  " )
print(" SPI encoder measured SHIFTED (NORMALIZED) AZ = " + str(tracker_azimuth - splited_conf[ 'shift_az'][0]) + "  <br>  " )
print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+" + "  <br>  ")
print(" Wind force measured = " + str(wf.get_wind_force()) + "  <br>  " )
print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+" + "  <br>  ")
print(" Light level = " + str(ll.readLight()) + "  <br>  " )
print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+" + "  <br>  ")