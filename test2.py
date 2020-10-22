from tkinter import PhotoImage
import tkinter as tk
from tkinter.ttk import *
import numpy

HEIGHT = 150
WIDTH = 460
root = tk.Tk()
root.title("Window")
root.resizable(False, False)
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()
frame = tk.Frame(root, bg='#9c9c9c')
frame.place(relx=0, rely=0, relwidth=1, relheight=1)
#buttonImg = PhotoImage(file="C:/Users/Tyler/Desktop/button.png")
axis = {}

class EntryLine:

    def isInt(self, entry):
        try:
            entry = int(entry)
            self.position = entry
            #print(self.position)
        except ValueError:
            print("\nBad Input at " + self.labelText)
            return
        return

    def buttonCommand(self):
        #print("Clicked!")
        self.isInt(self.entry.get())
        self.label.destroy()
        self.entry.delete(0, 'end')
        self.render()
        renderCorner()

    def stepUp(self):
        #print("UP")
        self.position += 1
        self.label.destroy()
        #print(self.position)
        self.render()
        renderCorner()

    def stepDown(self):
        #print("DOWN")
        self.position -= 1
        self.label.destroy()
        #print(self.position)
        self.render()
        renderCorner()

    def render(self):
        self.label = tk.Label(frame, text=self.labelText + "-Axis, Current Pos:    " + str(self.position), bg='#9c9c9c')
        self.label.place(x=40, y=20 * self.yPos, height=20)

    position = 0

    def __init__(self, yPos, labelText):
        self.yPos = yPos
        self.labelText = labelText
        self.entry = tk.Entry(frame)
        self.goToButton = tk.Button(frame, text="GOTO", bg='white', fg='black', command=self.buttonCommand)
        self.upButton = tk.Button(frame, text="+", bg='white', fg='black', command=self.stepUp)
        self.downButton = tk.Button(frame, text="-", bg='white', fg='black', command=self.stepDown)
        self.goToButton.place(x=310, y=20 * self.yPos, height=20, width=100)
        self.upButton.place(x=300, y=20 * self.yPos, height=10, width=10)
        self.downButton.place(x=300, y=10 + 20 * self.yPos, height=10, width=10)
        self.entry.place(x=200, y=20 * self.yPos, height=20, width=100)
        self.render()

def updateAll():
    for ax in axis:
        axis[ax].buttonCommand()


def renderCorner():
    cords = ""
    for ax in axis:
        cords += str(axis[ax].position)
        if ax < len(axis) - 1:
            cords += ", "

    cornerLabel = tk.Label(frame, text=cords, bg='#9c9c9c', fg='red')
    cornerLabel.place(x=20, y=HEIGHT - 20, height=20, width=100)

def mainloop():

    axis[0] = EntryLine(0, "X")
    axis[1] = EntryLine(1.5, "Y")
    axis[2] = EntryLine(3, "Z")
    axis[3] = EntryLine(4.5, "I ")

    cornerLabel = tk.Label(frame, text="0, 0, 0, 0", bg='#9c9c9c', fg='red')
    cornerLabel.place(x=20, y=HEIGHT - 20, height=20, width=100)
    updateButton = tk.Button(frame, text="Update All", bg='white', fg='black', command=updateAll)
    updateButton.place(x=200, y=HEIGHT - 20, height=20, width=100)
    root.mainloop()


mainloop()