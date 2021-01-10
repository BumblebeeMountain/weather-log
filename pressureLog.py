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

    # dataFile.write("{}, {:.1f}, {}\n".format(now(), p, temp))
    # dataFile.flush()

def getDbSecrets(fileName="db.secret"):
    try:
        secrets = {}
        f = open(fileName)
        text = f.read()
        f.close()

        text = text.split("\n")
        text.pop()

        for line in text:
            (key, value) = line.split(": ")
            secrets[key] = value
        return secrets

    except Exception as e:
        raise e



def main():
    try:
        apiKey = wth.getApiKey("/home/pi/weather-log/apiKey.secret")
        loc = wth.getLocation("/home/pi/weather-log/location.secret")
        dbSecrets = getDbSecrets("/home/pi/weather-log/db.secret")
        con = db.createConnection(dbSecrets["hostname"], dbSecrets["username"], dbSecrets["dbname"], dbSecrets["password"]) # createConnection(hostName, userName, dbName, password):

        takeRecord(apiKey, loc, con)

    except Exception as e:
        print("something went wrong:\n{}".format(e))
        sense.clear()
    #finally:
        #dataFile.close()

if __name__ == '__main__':
    # data = open("/home/pi/weather-log/pressure.csv", "a+")
    main()
