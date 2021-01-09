#!/bin/bash

scp -C pi@piserver:/home/pi/weather-log/pressure.csv .;
wait
python3 displayPressure.py
