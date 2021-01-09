#!/usr/bin/python3

from sense_hat import SenseHat
import numpy as np
import time
import datetime

sense = SenseHat()

def now():
    return int(time.time())

def main(dataFile):
    try:
        while True:
            p = sense.get_pressure()
            dataFile.write("{}, {:.1f}\n".format(now(), p))
            dataFile.flush()
            time.sleep(1800)
    except Exception as e:
        sense.clear()
    finally:
        print("closing")
        dataFile.close()

if __name__ == '__main__':
    data = open("pressure.csv", "a+")
    main(data)
