import tkinter as tk
from tkinter.ttk import *
import numpy
import RPi.GPIO as GPIO
import time
import csv

initpos = open('posdata.csv', "r")
lastLine = initpos.readlines()[-1]
initX = int(lastLine)
initpos.close

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

controlPins = [7, 11, 13, 15]

def setlow():
    for pin in controlPins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
setlow()

forward_seq = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]
backward_seq = forward_seq[::-1]
step_seq = [backward_seq, forward_seq]
current_dir = ["Backward", "Forward"]


HEIGHT = 60
WIDTH = 560
root = tk.Tk()
root.title("Stepper Control")
root.resizable(False, False)
root.geometry('{}x{}+{}+{}'.format(WIDTH, HEIGHT, 0, 0))
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()
frame = tk.Frame(root, bg='#9c9c9c')
frame.place(relx=0, rely=0, relwidth=1, relheight=1)
axis = {}

def step(steps):
    print(int(steps / abs(steps)))
    dir = int(steps / abs(steps))
    if (dir == 1):
        dir = 0
    print(current_dir[dir + 1])
    for i in range(steps * int(steps / abs(steps))):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(controlPins[pin], step_seq[dir + 1][halfstep][pin])
            time.sleep(0.001)
    setlow()
    
class EntryLine:

    def isInt(self, entry):
        try:
            entry = int(entry)
            self.position = entry
        except ValueError:
            print("\nBad Input at " + self.labelText)
            return
        return
    
    def buttonCommand(self):
        currentpos = self.position
        self.isInt(self.entry.get())
        self.label.destroy()
        if ( self.position - currentpos != 0):
            step(self.position - currentpos)
        self.entry.delete(0, 'end')
        self.render()
        renderCorner()
        
    def setHome(self):
        self.position = 0
        self.label.destroy()
        self.render()
        renderCorner()

    def stepUp(self):
        inc = 5
        self.position += inc
        self.label.destroy()
        self.render()
        renderCorner()
        step(inc)

    def stepDown(self):
        inc = 5
        self.position -= inc
        self.label.destroy()
        self.render()
        renderCorner()
        step(-inc)

    def render(self):
        self.label = tk.Label(frame, text=self.labelText + "-Axis, Current Pos:    " + str(self.position), bg='#9c9c9c')
        self.label.place(x=20, y=20 * self.yPos, height=20)

    position = initX

    def __init__(self, yPos, labelText):
        self.yPos = yPos
        self.labelText = labelText
        self.entry = tk.Entry(frame)
        self.goToButton = tk.Button(frame, text="GOTO", bg='white', fg='black', command=self.buttonCommand)
        self.upButton = tk.Button(frame, text="+", bg='white', fg='black', command=self.stepUp)
        self.downButton = tk.Button(frame, text="-", bg='white', fg='black', command=self.stepDown)
        self.setHomeButton = tk.Button(frame, text='Set Home', bg='white', fg='black', command=self.setHome)
        self.goToButton.place(x=360, y=20 * self.yPos, height=20, width=100)
        self.upButton.place(x=350, y=20 * self.yPos, height=10, width=10)
        self.downButton.place(x=350, y=10 + 20 * self.yPos, height=10, width=10)
        self.setHomeButton.place(x=460, y=20*self.yPos, height=20, width=100)
        self.entry.place(x=250, y=20 * self.yPos, height=20, width=100)
        self.render()

def updateAll():
    for ax in axis:
        axis[ax].buttonCommand()


def renderCorner():
    cords = ""
    file = open('posdata.csv', 'a')
    file.write('\n')
    for ax in axis:
        cords += str(axis[ax].position)
        if ax < len(axis) - 1:
            cords += ", "
        file.write('{}'.format(axis[ax].position))
    file.close()
    cornerLabel = tk.Label(frame, text=cords, bg='#9c9c9c', fg='red')
    cornerLabel.place(x=20, y=HEIGHT - 20, height=20, width=120)

def mainloop():

    axis[0] = EntryLine(0, "X")
    cornerLabel = tk.Label(frame, text=initX, bg='#9c9c9c', fg='red')
    cornerLabel.place(x=20, y=HEIGHT - 20, height=20, width=100)
    updateButton = tk.Button(frame, text="Update All", bg='white', fg='black', command=updateAll)
    updateButton.place(x=200, y=HEIGHT - 20, height=20, width=100)
    root.mainloop()


mainloop()