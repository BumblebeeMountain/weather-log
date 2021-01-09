#!/usr/bin/python3

from sense_hat import SenseHat
import openWeatherRequest as wth

import numpy as np
import time
import datetime

sense = SenseHat()
global MAX_TRY
MAX_TRY = 4

def now():
    return int(time.time())

def getPressure():
    return sense.get_pressure()

def takeRecord(apiKey, loc, dataFile):
    p = 0
    tries = 0
    while p==0:
        p = getPressure()
        tries += 1

        if tries > MAX_TRY:
            raise Exception("MAX TRIES REACHED FOR PRESSURE READING")

        time.sleep(2)

    temp = wth.getTemp(apiKey, loc)

    dataFile.write("{}, {:.1f}, {}\n".format(now(), p, temp))
    dataFile.flush()

def main(dataFile):
    try:
        apiKey = wth.getApiKey("/home/pi/weather-log/apiKey.secret")
        loc = wth.getLocation("/home/pi/weather-log/location.secret")

        takeRecord(apiKey, loc, dataFile)

    except Exception as e:
        print("something went wrong:\n{}".format(e))
        sense.clear()
    finally:
        dataFile.close()

if __name__ == '__main__':
    data = open("/home/pi/weather-log/pressure.csv", "a+")
    main(data)
