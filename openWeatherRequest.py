#!/usr/bin/python3

import requests
import json

def getApiKey(fileName="apiKey.secret"):
    try:
        f = open(fileName, "r")
        t = f.read()
        f.close()
        t = t.replace("\n", "")
        return t
    except Exception as e:
        raise e

def getLocation(fileName="location.secret"):
    try:
        f = open(fileName, "r")
        t = f.read()
        f.close()
        t = t.replace("\n", "")
        (lat, lon) = t.split(", ")
        return (float(lat), float(lon))
    except Exception as e:
        raise e

def getTemp(api_key, loc):

    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    (lat, lon) = loc

    complete_url = base_url +"lat=" + str(lat) + "&lon=" + str(lon) + "&appid=" + api_key + "&units=metric"

    response = requests.get(complete_url)

    x = response.json()

    if x["cod"] != "404":
        y = x['main']

        t = y['temp']
        return t

    else:
        raise Exception("ERROR WITH API: RESPONSE CODE {}".format(c["cod"]))

if __name__ == '__main__':
    apiKey = getApiKey()
    loc = getLocation()
    print(getTemp(apiKey, loc))
