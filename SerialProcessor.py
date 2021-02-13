from multiprocessing import Process, Queue
from threading import Thread
from itertools import count
import serial
import time


class SerialProcessor:

    def __init__(self, com, baud, csvname):
        self.polling_rate = 240
        self.com = com
        self.baud = baud
        self.csvname = csvname + '_' + str(self.com) + '_' + str(self.baud)
        try:
            self.sr = serial.Serial(port=self.com, baudrate=self.baud)
            self.sr.flushInput()
            self.queue = Queue()
            print("Connected to: " + self.sr.portstr)
        except:
            print('Cannot reach this serial port')

        try:
            print('Attempting to initialize reading thread')
            self.read = Thread(target=self.readData)
            print('Thread initialized successfully')
        except:
            print('Failed to initialize process')

    def go(self):
        self.read.start()

    def quit(self):
        self.is_running = False
        self.sr.close()

    def sendMessage(self, command, value):
        message = '/' + command + '/' + str(value)
        try:
            self.sr.write(message.encode('ascii'))
            time.sleep(.05)
        except:
            print('Failed to Send Command and Value')

    def readData(self):
        self.is_running = True
        self.sr.reset_input_buffer()
        print('Reading Data')
        index = count()
        startTime = time.time()
        self.sr.readline()
        while self.is_running:
            file = open(self.csvname + '.csv', 'a')
            # data_line = self.sr.readline().decode('utf-8')
            sr_bytes = self.sr.readline()
            decoded_bytes = sr_bytes[0:len(sr_bytes) - 2].decode('utf-8')
            line = str(next(index)) + ',' + str(decoded_bytes)

            # if line looks like accelerometer data, add it to the queue. if not, just print it out.
            if len(decoded_bytes) > 10:
                self.queue.put(str(decoded_bytes))
            else:
                print(str(decoded_bytes))
            file.close()

        self.quit()
