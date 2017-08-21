#!/usr/bin/python3
import time
import importlib
import config
from config import data

while 1:
 importlib.reload(config)
 splited_conf = {key: list(map(int, value.split())) for key, value in config.data.items()}
 print ("\n")
 print (splited_conf['wind_force'])
 time.sleep(10)