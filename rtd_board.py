import smbus2
import struct
import ConfigParser

class RTD_Board(object):
    
    DEBUG = 0
    address = 0
    bus = None
    name = ""
    # ----- CLASS INIT ----------
    def __init__(self, port, address, debug = 0):
        self.address = address
        self.bus = smbus2.SMBus(port)
        self.DEBUG = debug
        self.name = "RTD_Board I2C-"+str(port)+" ADDR: 0x"+str(address)
        self.config = ConfigParser.RawConfigParser()
        try:
            self.config.read("calibration.cfg")
        except expression as e:
            print(e)

    # ----- PRIVATE METHODS -----
    
    def __send_cmd_and_byte(self, cmd, data):
        if  self.DEBUG == 1:
                print("Sending cmd:" + str(cmd) + " and bytes :" + str(data))
        self.bus.write_byte_data(self.address, cmd, data)
    
    def __send_cmd_blockData(self, cmd, data):
	    self.bus.write_i2c_block_data(self.address, cmd, data)
    
    # ----- PUBLIC METHODS -----

    #Initialize the board
    def initialize(self, gain, SamplePerSec, a, b):

        self.setGain(gain)
        self.setSPS(SamplePerSec)

        a_bytes = bytearray(struct.pack("f", a))
        b_bytes = bytearray(struct.pack("f", b))

        if  self.DEBUG == 1:
            print([ "A float : 0x%02x" % b for b in a_bytes ])
            print([ "B float : 0x%02x" % b for b in b_bytes ])

        self.__send_cmd_blockData(0x02, a_bytes)
        self.__send_cmd_blockData(0x06, b_bytes)

        #Initialize RTD on the slave side
        #Reading address byte 0x13 will init the RTD on the board
        self.bus.read_byte_data(self.address, 0x13)

        print(self.name + " - Initialize complete")
        
    def sendReset(self)
        self.bus.read_byte_data(self.address, 0x14)
        
    def setGain(self, gain):
        self.__send_cmd_and_byte(0x00,gain)
        
    def setSPS(self, sps):
        self.__send_cmd_and_byte(0x01,sps)

    def getTemperatureC(self, channel):
        #Channel 1 : 0x0A, Channel 2 : 0x0B, Channel3 : 0x0C, Channel4 : 0x0D
        tempBaseAddress = 0x0A
        #Read temp in 4 bytes
        tempByteArray = self.bus.read_i2c_block_data(self.address, tempBaseAddress + channel, 4)
        #Transform 4 bytes to a float value
        tempBytes = struct.pack('BBBB',tempByteArray[0],tempByteArray[1],tempByteArray[2],tempByteArray[3])
        tempFloat = float(struct.unpack('f', tempBytes)[0])

        channelStr = "Channel " + str(channel)
        tempCorrection = self.config.getfloat(channelStr, 'Offset')
        return  tempFloat + tempCorrection

    def getResistance(self, channel):
        #Channel 1 : 0x05, Channel 2 : 0x06, Channel3 : 0x07, Channel4 : 0x08
        resBaseAddress = 0x05
        #Read temp in 4 bytes
        resByteArray = self.bus.read_i2c_block_data(self.address, resBaseAddress + channel, 4)
        #Transform 4 bytes to a float value
        resBytes = struct.pack('BBBB',resByteArray[0],resByteArray[1],resByteArray[2],resByteArray[3])
        resFloat = float(struct.unpack('f', resBytes)[0])

        return  resFloat