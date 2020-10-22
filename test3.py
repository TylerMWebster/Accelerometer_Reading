import tkinter as tk
import time
import numpy

track = False
HEIGHT = 720
WIDTH = 1080
axis = {}
posData = ""

root = tk.Tk()
root.title("Window")
root.resizable(False, False)

#frame = tk.Frame(root, bg='#9c9c9c')
#frame.place(relx=0, rely=0, relwidth=1, relheight=1)

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()
canvas.old_coords = None

backGround = canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill='grey', outline='grey')

cornerLabel = tk.Label(canvas, text="0, 0", bg='white', fg='red')
cornerLabel.place(x=20, y=HEIGHT - 20, height=20, width=100)

lX = canvas.create_line(0, 0, 0, 0)
lY = canvas.create_line(0, 0, 0, 0)

startTime = time.time()

def toggle(event):
    global track
    track = not track
    print(track)

def clearScreen(exent):
    canvas.delete("all")
    backGround = canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill='grey', outline='grey')

def updateLabelText(label, text):
    label.destroy()
    label = tk.Label(canvas, text=text, bg='white', fg='red')
    label.place(x=20, y=HEIGHT - 20, height=20, width=100)

def motion(event):
    if track:
        tempx = root.winfo_pointerx() - root.winfo_rootx()
        tempy = root.winfo_pointery() - root.winfo_rooty()
        if tempx >= 0 and tempx <= WIDTH:
            global x
            x = tempx
        if tempy >= 0 and tempy <= HEIGHT:
            global y
            y = tempy

        posData = str(x) + ", " + str(y)
        updateLabelText(cornerLabel, posData)
        if canvas.old_coords:
            global lX
            global lY
            canvas.delete(lX, lY)
            lX = canvas.create_line(0, y, WIDTH, y)
            lY = canvas.create_line(x, 0, x, HEIGHT)
            oval = canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill="red", outline="red", width=0)

        canvas.old_coords = x, y
        print(posData)

root.bind('<Motion>', motion)
root.bind('<Button-1>', toggle)
root.bind('<Button-3>', clearScreen)

def mainloop():
    root.mainloop()

mainloop()
