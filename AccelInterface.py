#THIS IS WHAT YOU RUN TO GET A GUI

from AccelProcessor import SerialParser
import tkinter as tk
import datetime
import math
import time
from threading import Thread

class Window:
    def __init__(self):
        self.HEIGHT = 720
        self.WIDTH = 1080
        self.axis = {}

        #Will need to change Com port based on what computer you are using
        self.parser = SerialParser('COM4')
        self.root = tk.Tk()
        self.root.title("Accelerometer Interface")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()
        self.backGround = self.canvas.create_rectangle(0, 0, self.WIDTH, self.HEIGHT, fill='grey', outline='grey')
        self.linelength = 400
        self.link1 = self.canvas.create_line(self.WIDTH/4, self.HEIGHT/4, self.WIDTH/4 + self.linelength, self.HEIGHT/4, width=3)
        self.label = tk.Label(self.canvas, bg='grey', fg='black')
        self.label.place(x=2, y=self.HEIGHT - 29, height=30, width=100)
        self.stopButton = tk.Button(self.canvas, text="Stop Light", bg='white', fg='black', command=self.stopLight)
        self.stopButton.place(x=400, rely=.6, height=30, width=80)
        self.startButton = tk.Button(self.canvas, text="Start Light", bg='white', fg='black', command=self.startLight)
        self.startButton.place(x=485, rely=.6, height=30, width=80)
        self.resetButton = tk.Button(self.canvas, text="Reset Unit", bg='white', fg='black', command=self.resetUnit)
        self.resetButton.place(x=570, rely=.6, height=30, width=80)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def stopLight(self):
        self.parser.sp.sr.write(b'0')
        time.sleep(.5)

    def startLight(self):
        self.parser.sp.sr.write(b'1')
        time.sleep(.5)

    def resetUnit(self):
        self.parser.sp.sr.write(b'9')
        time.sleep(.1)
        self.stopLight()
        time.sleep(.5)

    def clock(self):
        if len(self.parser.x_angs) > 0:
            self.x_ang = self.parser.x_angs[-1]
            self.canvas.delete(self.link1)
            x_end = self.WIDTH / 4 + self.linelength * math.cos(math.radians(float(self.x_ang)))
            y_end = self.HEIGHT / 4 - self.linelength * math.sin(math.radians(float(self.x_ang)))
            self.link1 = self.canvas.create_line(self.WIDTH / 4, self.HEIGHT / 4, x_end, y_end, width=3)

        time = datetime.datetime.now().strftime("Time: %H:%M:%S")
        self.label.config(text=time)
        self.root.after(1, self.clock)

    def on_closing(self):
        self.parser.sp.is_running = False
        self.root.destroy()

    def mainloop(self):
        self.clock()
        self.root.mainloop()


if __name__ == '__main__':
    win = Window()
    win.parser.go()
    win.mainloop()