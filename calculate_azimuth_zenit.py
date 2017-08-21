#!/usr/bin/python3

import datetime
import logging
from pysolar.solar import *
from datetime import timedelta

logging.basicConfig(filename='/var/log/sun_tracker.log', format='%(levelname)s: %(asctime)s %(message)s',level=logging.INFO)
#logging.debug('This message should go to the log file')
#logging.info('So should this')
#logging.warning('And this, too')
#logging.error('Something bad caused')
#logging.critical('Something very bad caused')

now = datetime.datetime.utcnow();
#print(now)
timestamp_string_for_log = now.strftime("%Y-%m-%d %H:%M:%S")

#Here we can do automatic switch to winter/summer time
kiev_datetime = now + timedelta(hours=3)
kiev_timestamp_string_for_log = kiev_datetime.strftime("%Y-%m-%d %H:%M:%S")

#Vinnitsa coordinates in degrees
lat = 48.62
longt = 27.8

#print(kiev_timestamp_string_for_log )

def get_alt(lat = lat, longt = longt):
  try:
    alt = round(get_altitude(lat, longt, datetime.datetime.utcnow()), 2)
    #alt = round(get_altitude(lat, longt, (datetime.datetime.utcnow() + timedelta(hours=3))), 2)
    if (alt>=0) and (alt<=68):
      logging.info(' Got altitude successfuly, alt = ' + str(alt))
      return alt
    else:
      logging.info("Alt is outside of the allowed sector (0-68 deg) (return -1). Actual value is = " + str(alt))
      return (-1)
  except Exception as e:
    logging.error(" get_altitude error " + str(e.args[0]))
    #here sending email should be implemented
    #also some alarm lamp on some GPIO pin should be switched on or appropriate message showed on a display
    return (" error " + str(e.args[0]))

def get_az(lat = lat, longt = longt):
  try:
    az = round(get_azimuth(lat, longt, datetime.datetime.utcnow()),2)
    #az = round(get_azimuth(lat, longt, (datetime.datetime.utcnow() + timedelta(hours=3))),2)
    actual_az = az
    if (((az <= -250) and (az >= -360)) or ((az <= 0) and (az >= -110))): # sector within !(-110 and -270) (THIS IS DEFAUL SECTOR)
    #if (((az <= -225) and (az >= -360)) or ((az <= 0) and (az >= -90))): # (THIS SECTOR IS LIMITED BY END SWITCHES)
      if (az <= 0) and (az >= -110):
        az = az*(-1) + 110
      if (az <= -250) and (az >= -360):
        az = az*(-1) - 250
      logging.info(' Got azimuth successfuly, az = ' + str(az) + ' - actual value = ' + str(actual_az) + ' / ' + str(datetime.datetime.utcnow())  )
      return az
    else:
      logging.info("Az is outside of the allowed sector (+/-110 deg) (return -1). Actual value is = " + str(az))
      return (-1)
  except Exception as e:
    logging.error(" get_azimuth error " + str(e.args[0]))
    #here sending email should be implemented
    #also some alarm lamp on some GPIO pin should be switched on or appropriate message showed on a display
    return (" error " + str(e.args[0]))
