#!/usr/bin/python

import config
import importlib
import random
import calculate_azimuth_zenit as caz
import wind_force as wf
import light_level as ll
import logging
from sys import exit


splited_conf = {key: list(map(int, value.split())) for key, value in config.data.items()}

wind_force_critical = 0
wind_force_sum = 0

min_alowed_light_level = 1
light_level_sum = 0

wind_force = int(round(wf.get_wind_force()))
logging.info("wind_force " + str(wind_force))

#here config data should be created
if len(splited_conf['wind_force']) < 180: # NEW VALUE EVERY 5 SECONDS (will allow to have data for 15 minutes) 
  #logging.info(splited_conf['wind_force'])
  splited_conf['wind_force'].append(wind_force)
  #logging.info(splited_conf['wind_force'])
else:
  #logging.info(splited_conf['wind_force'])
  splited_conf['wind_force'][-1] = wind_force # эквивалентно a[len(a) - 1] = a[0]
  i = 0
  while i < len(splited_conf['wind_force']) - 1:
    splited_conf['wind_force'][i] = splited_conf['wind_force'][i + 1]
    i += 1

light_level = int(round(ll.readLight()))
logging.info("light_level " + str(light_level))

if len(splited_conf['light_level']) < 180: # NEW VALUE EVERY 5 SECONDS (will allow to have data for 15 minutes) 
  #logging.info(splited_conf['light_level'])
  splited_conf['light_level'].append(light_level)
  #logging.info(splited_conf['light_level'])
else:
  #logging.info(splited_conf['light_level'])
  splited_conf['light_level'][-1] = light_level # эквивалентно a[len(a) - 1] = a[0]
  i = 0
  while i < len(splited_conf['light_level']) - 1:
    splited_conf['light_level'][i] = splited_conf['light_level'][i + 1]
    i += 1

#check if there are 10 points with value > then 40 then wind_force_critical = 1 if there are less then corresponding 5 point then wind_force_critical = 0 
critical_points_counter = 0
for i in range(1, 101):
  if splited_conf['wind_force'][-i] > 40 :
    critical_points_counter+=1
    if critical_points_counter >= 10:
      wind_force_critical = 1
    elif critical_points_counter < 5:
      wind_force_critical = 0

#check last 100 points of light data if average value is bigger then min allow tracking
for i in range(1, 101):
  light_level_sum += splited_conf['light_level'][-i]
  #print(splited_conf['light_level'][-i])
if (light_level_sum/100) <= 2000:
  min_alowed_light_level = 0
splited_conf['min_alowed_light_level'][0] = min_alowed_light_level

# if there is a point with 0 value check last one and if there is anough light allow tracking
for i in range(1, 101):
  if splited_conf['light_level'][-i] == 0 and splited_conf['light_level'][-1] > 2000:
    min_alowed_light_level = 1
    break

#unsplit config before wriring to a file
conf = {key: ' '.join(map(str, value)) for key, value in splited_conf.items()}
#print(conf)
#logging.info(conf)
try:
  file = open("config.py","w")
  file.write("data = " + str(conf)) 
  file.close() 
except Exception as e:
  logging.error(" error while writting data to config file " + str(e.args[0]))
  #here an email with error should be sent to the predefined destinations
exit()