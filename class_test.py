from rtd_board import RTD_Board
import os
import time

clear = lambda: os.system('clear')

rtd = RTD_Board(1,0x08)
# Using Callendar-Van Dusen typical values
rtd.initialize(32, 9, 0.0039083, -0.0000005775)

# READ AND PRINT
while 1:
    channel = 1
    print("Ch "+str(channel)+"\tTemp: " + str(rtd.getTemperatureC(channel -1)) +"\n\tResistance: " + str(rtd.getResistance(channel -1)))
    channel = 2
    print("Ch "+str(channel)+"\tTemp: " + str(rtd.getTemperatureC(channel -1)) +"\n\tResistance: " + str(rtd.getResistance(channel -1)))
    channel = 3
    print("Ch "+str(channel)+"\tTemp: " + str(rtd.getTemperatureC(channel -1)) +"\n\tResistance: " + str(rtd.getResistance(channel -1)))
    channel = 4
    print("Ch "+str(channel)+"\tTemp: " + str(rtd.getTemperatureC(channel -1)) +"\n\tResistance: " + str(rtd.getResistance(channel -1)))
    print("")
    time.sleep(1)
    #clear()

