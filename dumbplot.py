import time
from itertools import count
import serial

sr = serial.Serial(port='COM5', baudrate=9600)
sr.flushInput()
index = index = count()
csvname = 'dumbcsv'
startTime = time.time()

while time.time() - startTime < 10:
    # time.sleep(1.0/240)
    file = open(csvname + '.csv', 'a')
    data_line = sr.readline().decode('utf-8')
    sr_bytes = sr.readline()
    decoded_bytes = sr_bytes[0:len(sr_bytes) - 2].decode("utf-8")
    data_line.strip('\n')
    print(decoded_bytes)
    line = str(next(index)) + ',' + str(decoded_bytes)
    file.write(line + '\n')
    file.close()