#!/usr/bin/python3

import matplotlib.pyplot as plt
import databaseController as db
import numpy as np
import math
import datetime
import time
import sys

global NUM_OF_HOURS
NUM_OF_HOURS = 24

TIME_AGO = NUM_OF_HOURS * 60 * 60
MIN_TIME = int(time.time()) - TIME_AGO

global HEIGHT
HEIGHT = 191

def getData(dbSecret, MIN_TIME=0):
    s = db.getDbSecrets(dbSecret)

    CMD = """
        SELECT * FROM measure WHERE time >= {};
    """.format(MIN_TIME)
    host = s["hostname"]
    user = s["username"]
    passwd = s["password"]
    dbname = s["dbname"]
    ca = PATH + s["ca"]
    cert = PATH + s["cert"]
    key = PATH + s["key"]

    con = db.createConnectionSSL(host, dbname, user, passwd, ca, cert, key)

    data = db.executeQuery(con, CMD)
    con.close()

    return np.array(data)

def main(MIN_TIME):

    global PATH
    PATH = "".join([route + "/" for route in sys.argv[0].split("/")[:-1]])

    data = getData(PATH+"secrets/db.secret", MIN_TIME=MIN_TIME)

    fig = plt.figure()
    ax1 = fig.add_subplot(111, label="pressure")
    ax2 = fig.add_subplot(111, label="trend", frame_on=False)

    fig.suptitle("Change in pressure for the past {} hrs".format(NUM_OF_HOURS))

    y = data[:, 1]
    seaPressure = [
                convertToSeaLevel(float(p), float(t), HEIGHT) for [p, t] in data[:, 1:3]
            ]

    x = data[:, 0]

    ax1.plot(x, seaPressure, "k-", label="sea level pressure", color="C0")
    # ax1.plot(x, y, "-", label="absolute pressure", color="C1", alpha=0.4)
    ax1.set_xlabel("Time", color="C0")
    ax1.set_ylabel("Pressure", color="C0")
    ax1.tick_params(axis="x", colors="C0")
    ax1.tick_params(axis="y", colors="C0")
    ax1.legend(loc="upper left")
    ax1.set_ylim([980, 1040])

    try:
        trend = np.gradient(y)
    except ValueError:
        trend = np.zeros((len(x)))

    flat = np.array(x) * 0
    ax2.plot(x, trend, label="trend", color="skyblue", alpha=0.4)
    ax2.plot(x, flat, color="black")
    # ax2.set_xticks([])
    # ax2.xaxis.tick_top()
    ax2.yaxis.tick_right()
    # ax2.xaxis.set_label_position('top')
    ax2.yaxis.set_label_position('right')
    ax2.tick_params(axis="y", colors="black")

    ax2.grid(color='lightgray', which='both', axis='both')

    print("Latest reading: {} : {}".format(convert(float(data[-1, 0])), data[-1, 1]))

    plt.savefig(PATH + "plot.png")
    plt.show()

def convert(epoch):
    fmt = "%Y-%m-%d %H:%M"
    t = datetime.datetime.fromtimestamp(epoch)
    return t.strftime(fmt)

def convertToSeaLevel(p, t, h):
    return p*math.pow((1-(0.0065*h/(t+0.0065*h+273.15))), -5.257)

if __name__ == '__main__':
    main(MIN_TIME)
