from SerialProcessor import SerialProcessor
from multiprocessing import Process
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import pandas as pd

def main():
    sp = SerialProcessor('COM6', 9600, 'test')
    sp.go()

    xdat = pd.read_csv('test_COM6_9600.csv', names=['radx', 'rady', 'radz'])
    pltInterval = 50  # Period at which the plot animation updates [ms]
    xmin = 0
    xmax = 50
    ymin = -(100)
    ymax = 100
    fig = plt.figure()
    ax = plt.axes(xlim=(xmin, xmax), ylim=(float(ymin - (ymax - ymin) / 10), float(ymax + (ymax - ymin) / 10)))
    ax.set_title('Arduino Analog Read')
    ax.set_xlabel("Time")
    ax.set_ylabel("Angle")
    xvals = [len(xdat)]
    for i in range(0, len(xdat) - 2):
        xvals[i] = i
    lineLabel = 'Value'
    timeText = ax.text(0.50, 0.95, '', transform=ax.transAxes)
    lines = ax.plot(xvals, xdat, label=lineLabel)
    lineValueText = ax.text(0.50, 0.90, '', transform=ax.transAxes)
    #anim = animation.FuncAnimation(fig, file[-1], fargs=(lines, lineValueText, lineLabel, timeText),
                                   #interval=pltInterval)  # fargs has to be a tuple
    plt.legend(loc="upper left")
    plt.show()
    plt.close()

if __name__ == "__main__":
    main()