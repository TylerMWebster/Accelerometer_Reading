from AccelProcessor import SerialParser
import tkinter as tk
import datetime
import math
from threading import Thread

class Window:
    def __init__(self):
        self.HEIGHT = 720
        self.WIDTH = 1080
        self.axis = {}

        self.plotter = SerialParser()
        self.root = tk.Tk()
        self.root.title("Accelerometer Interface")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()
        self.backGround = self.canvas.create_rectangle(0, 0, self.WIDTH, self.HEIGHT, fill='grey', outline='grey')
        self.linelength = 400
        self.link1 = self.canvas.create_line(self.WIDTH/4, self.HEIGHT/4, self.WIDTH/4 + self.linelength, self.HEIGHT/4, width=3)
        self.label = tk.Label(self.canvas, bg='white', fg='red')
        self.label.place(relx=0, rely=.5, height=30, width=800)


    def clock(self):
        if len(self.plotter.x_angs) > 0:
            self.x_ang = self.plotter.x_angs[-1]
            self.canvas.delete(self.link1)
            x_end = self.WIDTH / 4 + self.linelength * math.cos(math.radians(float(self.x_ang)))
            y_end = self.HEIGHT / 4 - self.linelength * math.sin(math.radians(float(self.x_ang)))
            self.link1 = self.canvas.create_line(self.WIDTH / 4, self.HEIGHT / 4, x_end, y_end, width=3)

        time = datetime.datetime.now().strftime("Time: %H:%M:%S")
        self.label.config(text=time)
        self.root.after(1, self.clock)


    def mainloop(self):
        self.clock()
        self.root.mainloop()


if __name__ == '__main__':
    win = Window()
    win.plotter.go()
    win.mainloop()