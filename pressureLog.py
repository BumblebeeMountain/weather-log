#!/usr/bin/python3

from sense_hat import SenseHat
import openWeatherRequest as wth
import databaseController as db

import numpy as np
import time
import datetime
import sys

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
    con = None
    path = "".join([route + "/" for route in sys.argv[0].split("/")[:-1]])
    try:
        apiKey = wth.getApiKey(path+"secrets/apiKey.secret")
        loc = wth.getLocation(path+"secrets/location.secret")
        dbSecrets = db.getDbSecrets(path+"secrets/db-pi.secret")

        host = dbSecrets["hostname"]
        user = dbSecrets["username"]
        passwd = dbSecrets["password"]
        dbname = dbSecrets["dbname"]
        ca = path + dbSecrets["ca"]
        cert = path + dbSecrets["cert"]
        key = path + dbSecrets["key"]

        con = db.createConnectionSSL(host, dbname, user, passwd, ca, cert, key)

        takeRecord(apiKey, loc, con)

    except Exception as e:
        print("something went wrong:\n{}".format(e))
        sense.clear()

    finally:
        if con is not None:
            con.close()

if __name__ == '__main__':
    main()
