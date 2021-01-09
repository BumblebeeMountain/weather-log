import matplotlib.pyplot as plt
import numpy as np
import math
import datetime

NUM_OF_HOURS = 48
NUM_OF_READINGS = NUM_OF_HOURS * 2

def main(NUM_OF_HOURS):
    f = open("pressure.csv")
    text = f.read()
    text = text.split("\n")
    text.pop()
    text.pop(0)
    text = [reading.split(", ") for reading in text ]

    data = np.array(text)

    fig = plt.figure()
    ax1 = fig.add_subplot(111, label="pressure")
    ax2 = fig.add_subplot(111, label="trend", frame_on=False)

    y = [float(val) for val in data[-NUM_OF_READINGS::,1]]
    x = [int(val) for val in data[-NUM_OF_READINGS::,0]]


    ax1.plot(x, y, "k-", label="pressure", color="C0")
    ax1.set_xlabel("Time", color="C0")
    ax1.set_ylabel("Pressure", color="C0")
    ax1.tick_params(axis="x", colors="C0")
    ax1.tick_params(axis="y", colors="C0")
    ax1.legend(loc="upper left")
    # ax1.set_ylim([980, 1040])

    trend = np.gradient(y)

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

    plt.savefig("plot.png")
    plt.show()

def convert(epoch):
    fmt = "%Y-%m-%d %H:%M"
    t = datetime.datetime.fromtimestamp(epoch)
    return t.strftime(fmt)

def convertToSeaLevel(p, t, h):
    return p*math.pow((1-(0.0065*h/(t+0.0065*h+273.15))), -5.257)

if __name__ == '__main__':
    main(NUM_OF_HOURS)
