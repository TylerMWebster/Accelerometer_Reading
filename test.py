import tkinter as tk
import numpy

HEIGHT = 130
WIDTH = 500
root = tk.Tk()
root.title("Test Name")
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()
frame = tk.Frame(root, bg='#80c1ff')
frame.place(relx=0, rely=0, relwidth=1, relheight=1)
axis = {}


class EntryLine:

    def __init__(self, yPos, labelText):

        def isInt(entry):
            try:
                entry = int(entry)
                self.position = entry
                print(self.position)
            except ValueError:
                print("Bad Input")
                return
            return

        def buttonCommand():
            print("Clicked!")
            isInt(self.entry.get())
            deleteEntity(self.label)
            self.entry.delete(0, 'end')
            render()

        def stepUp():
            print("UP")
            self.position += 1
            print(self.position)
            deleteEntity(self.label)
            render()

        def stepDown():
            print("DOWN")
            self.position -= 1
            print(self.position)
            deleteEntity(self.label)
            render()

        def render():
            self.label = tk.Label(frame, text=labelText + "-Axis, Current Pos:    " + str(self.position))
            self.badInput = tk.Label(frame, text="Expected integer")
            self.label.place(relx=.1, y=20 * yPos, height=20)

        def deleteEntity(entity):
            entity.destroy()

        self.position = 0
        self.goToButton = tk.Button(frame, text="GOTO", bg='white', fg='black', command=buttonCommand)
        self.upButton = tk.Button(frame, text="+", bg='white', fg='black', command=stepUp)
        self.downButton = tk.Button(frame, text="-", bg='white', fg='black', command=stepDown)
        self.entry = tk.Entry(frame)
        self.goToButton.place(relx=.8, y=20 * yPos, height=20, relwidth=.100)
        self.upButton.place(relx=.7, y=20 * yPos, height=10, width=10)
        self.downButton.place(relx=.7, y=10 + 20 * yPos, height=10, width=10)
        self.entry.place(relx=.5, y=20 * yPos, height=20, width=100)

        render()


def main():

    axis[0] = EntryLine(0, "X")
    axis[1] = EntryLine(2, "Y")
    axis[2] = EntryLine(4, "Z")
    updateButton = tk.Button(frame, text="Update All", bg='white', fg='black')
    updateButton.place(relx=.5, y=HEIGHT - 20, height=20, width=100)

    root.mainloop()

main()
