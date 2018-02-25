# Wiebie RTD Shield Interface
A python class for the Wiebe RTD Shield 

I wanted to make a python class and application for the Wiebe Brewing RTD shield, since originaly it's been made for an arduino.
The RTD shield act like an I2C slave device, so basicaly any device with I2C capabality shoudl be able to use it.

I am planning to run an OrangePi Zero with MySQL server to logg the temperature of this board. 

The project is based on Python 2.7
The python script obviously needs smbus2 to be installed


This is where I got the board and schematic :
http://wiebebrewing.com/rtdshield/
