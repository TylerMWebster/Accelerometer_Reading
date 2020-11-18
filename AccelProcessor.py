import sys
from SerialProcessor import SerialProcessor
from itertools import count
from threading import Thread
from PyQt5 import QtGui, QtCore
import pyqtgraph as pg
import numpy as np


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
        self.thread.start()


    def plot_data(self):
        counter = 0
        while self.sp.is_running:
            self.data.append(self.sp.queue.get())
            self.x_vals = np.append(self.x_vals, counter)
            self.data[counter] = self.data[counter].split(',')
            self.x_angs = np.append(self.x_angs, float(self.data[counter][0]))
            self.y_angs = np.append(self.y_angs, float(self.data[counter][1]))
            self.z_angs = np.append(self.z_angs, float(self.data[counter][2]))
            print(self.data[counter])
            counter += 1

def main():
    plotter = SerialParser()
    plotter.go()

if __name__ == "__main__":
    main()
