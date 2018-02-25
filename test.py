#! /usr/bin/python

import smbus2
import time
import struct
import os

clear = lambda: os.system('clear')

bus = smbus2.SMBus(1)

DEVICE_ADDR = 0x08
DEBUG = 1

def send_one_byte(data):
	if  DEBUG == 1:
		print("Sending " + str(data))
	bus.write_byte(DEVICE_ADDR, data)

def send_cmd_and_byte(cmd, data):
        if  DEBUG == 1:
                print("Sending cmd:" + str(cmd) + " and bytes :" + str(data))
        bus.write_byte_data(DEVICE_ADDR, cmd, data)

def send_cmd_and_16bytes(cmd, data):
	if  DEBUG == 1:
		print("Sending cmd:" + str(cmd) + " and 16 bytes :" + str(data))
	bus.write_word_data(DEVICE_ADDR, cmd, data)

def send_cmd_blockData(cmd, data):
	bus.write_i2c_block_data(DEVICE_ADDR, cmd, data)

def initialize(gain, SamplePerSec, a, b):

	send_cmd_and_byte(0x00,gain)
	send_cmd_and_byte(0x01,SamplePerSec)

	a_bytes = bytearray(struct.pack("f", a))
	b_bytes = bytearray(struct.pack("f", b))

        if  DEBUG == 1:
		print([ "A float : 0x%02x" % b for b in a_bytes ])
		print([ "B float : 0x%02x" % b for b in b_bytes ])

	send_cmd_blockData(0x02, a_bytes)
	send_cmd_blockData(0x06, b_bytes)

	#Initialize RTD
	bus.read_byte_data(DEVICE_ADDR, 0x13)

	print("Initialize complete")

initialize(32, 9, 0.0039083, -0.0000005775)

# READ AND PRINT
while 1:
	temp = bus.read_i2c_block_data(DEVICE_ADDR, 0x0A, 4)
	temp_fl = struct.pack('BBBB',temp[0],temp[1],temp[2],temp[3])
	ch1_temp = struct.unpack('f',temp_fl)

        temp = bus.read_i2c_block_data(DEVICE_ADDR, 0x0B, 4)
        temp_fl = struct.pack('BBBB',temp[0],temp[1],temp[2],temp[3])
        ch2_temp = struct.unpack('f',temp_fl)

        temp = bus.read_i2c_block_data(DEVICE_ADDR, 0x0C, 4)
        temp_fl = struct.pack('BBBB',temp[0],temp[1],temp[2],temp[3])
        ch3_temp = struct.unpack('f',temp_fl)

        temp = bus.read_i2c_block_data(DEVICE_ADDR, 0x0D, 4)
        temp_fl = struct.pack('BBBB',temp[0],temp[1],temp[2],temp[3])
        ch4_temp = struct.unpack('f',temp_fl)

	print("Channel 1: " + str(ch1_temp))
        print("Channel 2: " + str(ch2_temp))
        print("Channel 3: " + str(ch3_temp))
        print("Channel 4: " + str(ch4_temp))
	time.sleep(1)
	clear()
