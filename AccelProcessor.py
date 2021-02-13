import sys
from SerialProcessor import SerialProcessor
from itertools import count
from threading import Thread
import numpy as np
import math

class SerialParser:

    def __init__(self, comPort):
        self.data = []
        self.x_vals = np.array((0))
        self.x_angs = np.empty((0))
        self.y_angs = np.empty((0))
        self.z_angs = np.empty((0))
        self.sp = SerialProcessor(comPort, 9600, 'test')
        self.index = count()
        self.thread = Thread(target=self.plot_data)


    def go(self):
        self.sp.go()
        try:
            print('Attempting to initialize writing thread')
            self.thread.start()
            print('Thread initialized successfully')
        except:
            rint('Failed to initialize process')


    def stop(self):
        self.sp.is_running = False


    def plot_data(self):
        counter = 0
        #while data is actively being read form serial pull it from the queue and append it to the list.
        #Then append the axis angles to their own lists.
        while self.sp.is_running:
            self.data.append(self.sp.queue.get())
            self.x_vals = np.append(self.x_vals, counter)
            self.data[counter] = self.data[counter].split(',')
            self.x_angs = np.append(self.x_angs, round(math.degrees(float(self.data[counter][0])), 2))
            self.y_angs = np.append(self.y_angs, round(math.degrees(float(self.data[counter][1])), 2))
            self.z_angs = np.append(self.z_angs, round(math.degrees(float(self.data[counter][2])), 2))
            print(self.x_angs[counter], end=', ')
            print(self.y_angs[counter], end=', ')
            print(self.z_angs[counter])
            counter += 1


def main():
    plotter = SerialParser()
    plotter.go()


if __name__ == "__main__":
    main()
