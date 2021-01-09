#!/usr/bin/python3

from sense_hat import SenseHat
import openWeatherRequest as wth

import numpy as np
import time
import datetime

sense = SenseHat()

def now():
    return int(time.time())

def main(dataFile):
    try:
        apiKey = wth.getApiKey()
        loc = wth.getLocation()

        while True:
            p = sense.get_pressure()
            temperature = wth.getTemp(apiKey, loc)

            dataFile.write("{}, {:.1f}, {}\n".format(now(), p, temperature))
            dataFile.flush()
            time.sleep(1800)
    except Exception as e:
        print("something went wrong:\n{}".format(e))
        sense.clear()
    finally:
        print("closing")
        dataFile.close()

if __name__ == '__main__':
    data = open("pressure.csv", "a+")
    main(data)
