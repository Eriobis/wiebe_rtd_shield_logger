#! /usr/bin/python

# ---------- IMPORTS ----------

from rtd_board import RTD_Board
import os
import time

# ---------- GLOBAL VARS ----------

CALIB_FILE = "calibration.csv"
rtd = RTD_Board(1,0x08)
rtd.initialize(32, 9, 0.0039083, -0.0000005775)

# ---------- FUNCTIONS ----------

def getChannel():
    channel = raw_input("Enter the channel to calibrate:\n")
    return int(channel)

def getUserTemp():
    value = raw_input("Enter the current calibration temperature ( q to quit ):\n")
    if value == 'q' or value == 'Q':
        exit(0)
    return float(value)

def writeTempDelta(channel, userTemp):
    if os.path.exists(CALIB_FILE) == False:
        fd = open(CALIB_FILE, mode='w')
        fd.write("Channel,SensorTemperature,UserTemperature,Difference\n")
        fd.close()
    fd = open(CALIB_FILE, mode='a')
    sensorTemp = rtd.getTemperatureC(channel)
    diff = sensorTemp - userTemp
    fd.write(str(channel)+","+str(sensorTemp)+","+str(userTemp)+","+str(diff)+"\n")
    print(str(channel)+","+str(sensorTemp)+","+str(userTemp)+","+str(diff)+"\n")
    fd.close()

# ---------- MAIN ROUTINE HERE ----------

print("Board calibration, please enter the channel you want to calibrate")
channel = getChannel()

while True:
    print("Selected channel : "+str(channel)) 
    temp = getUserTemp()
    writeTempDelta(channel, temp)

exit(0)