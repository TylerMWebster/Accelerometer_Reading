import math
from threading import Thread
import serial
import csv
import time

class SerialProcessor:

    def __init__(self, com, baud, csvname):
        try:
            print("attempting to initialize reading thread")
            self.thread = Thread(target=self.readData)
            print('thread initialized successfully')
        except:
            print('failed to initialize thread')
        self.com = com
        self.baud = baud
        self.csvname = csvname + '_' + str(com) + '_' + str(baud)
        self.sr = serial.Serial(port=self.com, baudrate=self.baud)
        self.sr.flushInput()
        print("connected to: " + self.sr.portstr)


    def go(self):
        self.thread.start()
        #self.readData()

    def readData(self):
        startTime = time.time()
        print('started')
        self.sr.readline()
        while time.time() - startTime < 10 :
            file = open(self.csvname + '.csv', 'a')
            data_line = self.sr.readline().decode('utf-8')
            sr_bytes = self.sr.readline()
            decoded_bytes = sr_bytes[0:len(sr_bytes) - 2].decode("utf-8")
            data_line.strip('\n')
            print(decoded_bytes)
            file.write(str(decoded_bytes) + '\n')
            file.close()