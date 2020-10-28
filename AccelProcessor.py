import sys
from SerialProcessor import SerialProcessor
from itertools import count
from threading import Thread
from PyQt5 import QtGui, QtCore
import pyqtgraph as pg
import numpy as np


class SerialParser:

    def __init__(self):
        self.data = []
        self.x_vals = np.array((0))
        self.x_angs = np.empty((0))
        self.y_angs = np.empty((0))
        self.z_angs = np.empty((0))
        #self.widget = pg.GraphicsLayoutWidget(show=True)
        #self.widget.setWindowTitle('Accelerometer Visualizer')
        #self.plt = self.widget.addPlot()
        #self.pen = pg.mkPen(color=(0, 255, 0), width=2)
        #self.graph = self.plt.plot(self.x_vals, self.x_angs, self.pen)
        self.sp = SerialProcessor('COM5', 9600, 'test')
        self.index = count()
        self.thread = Thread(target=self.plot_data)


    def go(self):
        self.sp.go()
        self.thread.start()

    #def update(self):
        #self.plt.setXRange(0, len(self.data))
        #self.graph.setData(self.x_vals, self.x_angs)


    def plot_data(self):
        counter = 0
        while self.sp.is_running:
            self.data.append(self.sp.queue.get())
            self.x_vals = np.append(self.x_vals, counter)
            self.data[counter] = self.data[counter].split(',')
            self.x_angs = np.append(self.x_angs, self.data[counter][0])
            self.y_angs = np.append(self.y_angs, self.data[counter][1])
            self.z_angs = np.append(self.z_angs, self.data[counter][2])
            print(self.data[counter])
            #self.update()
            counter += 1

def main():
    plotter = SerialPlotter()
    plotter.go()

if __name__ == "__main__":
    main()
