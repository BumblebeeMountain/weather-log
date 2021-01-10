#!/usr/bin/python3

from sense_hat import SenseHat
import openWeatherRequest as wth
import databaseController as db

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

def takeRecord(apiKey, loc, con):
    p = 0
    tries = 0
    while p==0:
        p = getPressure()
        tries += 1

        if tries > MAX_TRY:
            raise Exception("MAX TRIES REACHED FOR PRESSURE READING")

        time.sleep(2)

    temp = wth.getTemp(apiKey, loc)

    p = "{:.1f}".format(p)
    cmd = db.INSERT_COMMAND.format(now(), p, temp)
    db.executeUpdate(con, cmd)

def main():
    try:
        apiKey = wth.getApiKey("/home/pi/weather-log/apiKey.secret")
        loc = wth.getLocation("/home/pi/weather-log/location.secret")
        dbSecrets = db.getDbSecrets("/home/pi/weather-log/db.secret")
        con = db.createConnection(dbSecrets["hostname"], dbSecrets["username"], dbSecrets["dbname"], dbSecrets["password"]) # createConnection(hostName, userName, dbName, password):

        takeRecord(apiKey, loc, con)

    except Exception as e:
        print("something went wrong:\n{}".format(e))
        sense.clear()

if __name__ == '__main__':
    main()
