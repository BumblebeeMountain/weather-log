#!/bin/bash

scp -C pi@piserver:/home/pi/pressure.csv .;
wait
python3 displayPressure.py
