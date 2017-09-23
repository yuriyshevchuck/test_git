#!/usr/bin/python3
import calculate_azimuth_zenit as caz
import tracker_angles as ta
import wind_force as wf
import light_level as ll
from config import data
import time
import RPi.GPIO as GPIO
import logging
from config import data
import sys

splited_conf = {key: list(map(int, value.split())) for key, value in data.items()}

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#(ZENIT) motor rotation "-"" pin should be connected to 31 board GPIO
GPIO.setup(31, GPIO.OUT)
GPIO.output(31,False)
#(ZENIT) motor rotation "+" pin should be connected to 32 board GPIO
GPIO.setup(33, GPIO.OUT)
GPIO.output(33,False)

#(AZIMUTH) motor rotation "-"" pin should be connected to 35 board GPIO
GPIO.setup(35, GPIO.OUT)
GPIO.output(35,False)
#(ZENIT) motor rotation "+"" pin should be connected to 37 board GPIO
GPIO.setup(37, GPIO.OUT)
GPIO.output(37,False)

#get curent sun position
altitude = caz.get_alt()
azimuth = caz.get_az()

#read data from config
min_alowed_light_level = splited_conf['min_alowed_light_level'][0] # equal 1 if light level i enough 
wind_force_critical = splited_conf['wind_force_critical'][0] # equal to 0 if wind force is not higher then allowed
shift_alt =  splited_conf['shift_alt'][0]# 0deg (horizontal) position is shifted ~ 33 (measured = 33 shifted = 0) 
shift_az =  splited_conf['shift_az'][0]# 0deg possition of the encoder is oriented to Notrh ~ 60deg (will set it once )
alt_delta = 30 # isensitivity zone (if sun ALT is less than delta we should position tracker altitude to alt_delta)

#log BEGIN
logging.info("START MAIN TRACK HANDLER")
logging.info("Calculated altitude = " + str(altitude))
logging.info("Calculated azimuth = " + str(azimuth))
logging.info("Delta= " + str(alt_delta))
logging.info("wind_force_critical " + str(wind_force_critical));
logging.info("min_alowed_light_level " + str(min_alowed_light_level));

#DELETE ME
#this constant ovirrides the parameter from config (once positioning to south alt 45 degrees is implemented DELETE IT)
#min_alowed_light_level = 1 #DELETE ME

#altitude =-1
#azimuth = -1

#track AZIMUTH/ZENIT
#check if ZENIT and AZIMUTH tracking is allowed (condition key from config)
if ( (altitude != (-1)) and (azimuth != (-1)) and (ta.get_tracker_azimuth_angle() != (-1)) and (ta.get_tracker_altitude_angle() != (-1)) and (not wind_force_critical) ) :
	
	if not min_alowed_light_level: # override altitude/azimuth if there is no anough light
	   altitude = 85				# override altitude/azimuth if there is no anough light
	   azimuth = -10				# override altitude/azimuth if there is no anough light
    
	tracker_altitude = ta.get_tracker_altitude_angle()
	#SUN ALTITUDE IS LESS THEN ALT DELTA (isensitive zone)
	logging.info(" HERE IT IS ALTITUDE ")
	logging.info(" altitude " + str(altitude))
	logging.info(" alt_delta " + str(alt_delta))
	logging.info(" (90 - (tracker_altitude - shift_alt)) " + str((90 - (tracker_altitude - shift_alt))))
	if altitude <= alt_delta:
		#move it to alt_delta
		GPIO.output(33,True)
		while True:
			time.sleep(0.5)
			tracker_altitude = ta.get_tracker_altitude_angle()
			logging.info(" Debug conditions in main script (alt correction) | tracker_altitude (normalized) = " + str((90 - (tracker_altitude - shift_alt))) + " | calculated azimuth = " + str(altitude));
			if (90 - (tracker_altitude - shift_alt)) <= alt_delta: # 90 is there to noralize altitude encoder (it has 0 at the end and 65 at the begining)
				GPIO.output(33,False)
				logging.info(" Altitude position of the tracker was corrected to: " + str(altitude))
				break
	#ALTITUDE PLUS
	#logging.info("ALTITUDE PLUS= " + str(90 - (tracker_altitude - shift_alt)))
	elif (90 - (tracker_altitude - shift_alt)) < altitude:
		#move it up
		GPIO.output(31,True)
		while True:
			time.sleep(0.5)
			tracker_altitude = ta.get_tracker_altitude_angle() 
			logging.info(" Debug conditions (alt plus) | tracker_altitude (normalized) = " + str((90 - (tracker_altitude - shift_alt))) + " | calculated altitude = " + str(altitude));
			if (90 - (tracker_altitude - shift_alt)) >= altitude: # 90 is there to noralize altitude encoder (it has 0 at the end and 65 at the begining)
				GPIO.output(31,False)
				logging.info(" Altitude position of the tracker was corrected to: " + str(altitude))
				break
	#ALTITUDE MINUS
	elif ((90 - (tracker_altitude - shift_alt)) > altitude) and (altitude > alt_delta):
		#move it down
		GPIO.output(33,True)
		while True:
			time.sleep(0.5)
			tracker_altitude = ta.get_tracker_altitude_angle() 
			logging.info(" Debug conditions (alt minus) | tracker_altitude (normalized) = " + str((90 - (tracker_altitude - shift_alt))) + " | calculated azimuth = " + str(altitude));
			if (90 - (tracker_altitude - shift_alt)) <= altitude: # 90 is there to noralize altitude encoder (it has 0 at the end and 65 at the begining)
				GPIO.output(33,False)
				logging.info(" Altitude position of the tracker was corrected to: " + str(altitude))
				break

	tracker_azimuth = ta.get_tracker_azimuth_angle()
	logging.info(" HERE IT IS AZIMUTH ")
	logging.info(" (tracker_azimuth - shift_az) = " + str((tracker_azimuth - shift_az)));
	logging.info(" (azimuth) = " + str(azimuth));
	#AZIMUTH PLUS
	if ((tracker_azimuth - shift_az) < 195) and ((tracker_azimuth - shift_az) < azimuth) and (azimuth != (-10)) : # 195 is west end_switch limit / if -10 skip tracking due to small light level
		GPIO.output(37,True)
		while True:
			time.sleep(0.5)
			tracker_azimuth = ta.get_tracker_azimuth_angle()
			logging.info(" Debug conditions (az plus) | (tracker_azimuth - shift_az)) = " + str((tracker_azimuth - shift_az)) + " | calculated azimuth = " + str(azimuth));
			if ((tracker_azimuth - shift_az) >= 195) or ((tracker_azimuth - shift_az) >= azimuth):
				GPIO.output(37,False)
				logging.info(" Azimuth position of the tracker was corrected to: " + str(azimuth))
				break
		#sys.exit()
	#AZIMUTH MINUS (-1 is there to avoid false switching)
	if (tracker_azimuth - shift_az > 20) and ((tracker_azimuth - shift_az - 1) > azimuth) and (azimuth != (-10)) : #20 is east end_switch limit / if -10 skip tracking due to small light level
		GPIO.output(35,True)
		while True:
			time.sleep(0.5)
			tracker_azimuth = ta.get_tracker_azimuth_angle()
			logging.info(" Debug conditions (az minus) | (tracker_azimuth - shift_az)) = " + str((tracker_azimuth - shift_az)) + " | calclated azimuth = " + str(azimuth));
			if ((tracker_azimuth - shift_az) <= 20) or ((tracker_azimuth - shift_az) <= azimuth):
				GPIO.output(35,False)
				logging.info(" Azimuth position of the tracker was corrected to: " + str(azimuth))
				break
		#sys.exit()
elif altitude == (-1) :
	# move zenit to the initial position
	time.sleep(1)
	tracker_altitude = ta.get_tracker_altitude_angle()
	logging.info(" Tracker alt " + str(tracker_altitude))
	logging.info(" tracker_altitude - shift_alt " + str(tracker_altitude - shift_alt))
	logging.info("HERE to initiall position")
	if (tracker_altitude - shift_alt) > 13: # horizont is 3.3
		GPIO.output(31,True)
		while True:
			time.sleep(1)
			tracker_altitude = ta.get_tracker_altitude_angle()
			logging.info(" (tracker_altitude - shift_alt)) = " + str((tracker_altitude - shift_alt)))
			logging.info(" (90 - (tracker_altitude - shift_alt)) = " + str((90 - (tracker_altitude - shift_alt))))
			if (tracker_altitude - shift_alt) <= 13: # horizont is 3.3
				GPIO.output(31,False)
				logging.info(" Altitude was moved to the initial position " + str(tracker_altitude))
				break
	# move azimuth to the initial position
	time.sleep(1)
	tracker_azimuth = ta.get_tracker_azimuth_angle()
	logging.info(" tracker_azimuth " + str(tracker_azimuth - shift_az))
	logging.info(" tracker_azimuth - splited_conf['shift_az'][0] " + str(tracker_azimuth - splited_conf['shift_az'][0]))
	if tracker_azimuth > splited_conf['shift_az'][0] + 20: # 24 limitet by endswitch
		GPIO.output(35,True)
		while True:
			time.sleep(1)
			tracker_azimuth = ta.get_tracker_azimuth_angle()
			logging.info(" (tracker_azimuth - shift_az) = " + str((tracker_azimuth - shift_az)))
			if tracker_azimuth <= splited_conf['shift_az'][0] + 20: # 24 limitet by east endswitch
				#time.sleep(30) # sleep some time to allow tracker reach the endd switch (DUE TO DIFFERENCE BETWEN MAIN AND SLAVE TRACKERS)
				GPIO.output(35,False)
				logging.info(" Azimuth was moved to the initial position " + str(tracker_azimuth - splited_conf['shift_az'][0]))
				break
elif wind_force_critical : # if wind is more then allowedleved
	# move zenit to the initial position
	time.sleep(1)
	tracker_altitude = ta.get_tracker_altitude_angle()
	logging.info(" Tracker alt " + str(tracker_altitude))
	logging.info(" tracker_altitude - shift_alt " + str(tracker_altitude - shift_alt))
	logging.info("HERE wind_force_critical")
	if (tracker_altitude - shift_alt) > 13: # horizont is 3.3
		GPIO.output(31,True)
		while True:
			time.sleep(1)
			tracker_altitude = ta.get_tracker_altitude_angle()
			logging.info(" (90 - (tracker_altitude - shift_alt)) = " + str((90 - (tracker_altitude - shift_alt))))
			if (tracker_altitude - shift_alt) <= 13: # horizont is 3.3
				GPIO.output(31,False)
				logging.info(" Altitude was moved to the initial position " + str(tracker_altitude - splited_conf['shift_alt'][0]))
				break