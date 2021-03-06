#THIS IS WHAT YOU RUN TO GET A GUI

from AccelProcessor import SerialParser
import tkinter as tk
import datetime
import math
from PIL import ImageTk, Image  

class Window:
    def __init__(self):
        self.HEIGHT = 720
        self.WIDTH = 1080
        self.axis = {}
        self.ring_x = 200
        self.ring_y = 300

        #Will need to change Com port based on what computer you are using
        self.parser = SerialParser('COM12')

        self.root = tk.Tk()
        self.root.title("Accelerometer Interface")
        self.root.resizable(False, False)
        #self.root.wm_attributes('-alpha', 0.9)

        self.canvas = tk.Canvas(self.root, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()
        self.backGround = self.canvas.create_rectangle(0, 0, self.WIDTH, self.HEIGHT, fill='grey', outline='grey')

        self.linelength = 200
        self.link1 = self.canvas.create_line(self.WIDTH/2, self.HEIGHT/4, self.WIDTH/2 + self.linelength, self.HEIGHT/4, width=3)

        self.label = tk.Label(self.canvas, bg='grey', fg='black')
        self.label.place(x=2, y=self.HEIGHT - 29, height=30, width=100)

        self.stopButton = tk.Button(self.canvas, text="Stop Light", bg='white', fg='black', command=self.stopLight)
        self.stopButton.place(x=400, rely=.6, height=30, width=80)

        self.startButton = tk.Button(self.canvas, text="Start Light", bg='white', fg='black', command=self.startLight)
        self.startButton.place(x=485, rely=.6, height=30, width=80)
        self.resetButton = tk.Button(self.canvas, text="Reset Unit", bg='white', fg='black', command=self.resetUnit)
        self.resetButton.place(x=570, rely=.6, height=30, width=80)

        self.beepButton = tk.Button(self.canvas, text="Beep", bg='white', fg='black', command=self.makeBeep)
        self.beepButton.place(x=20, rely=.8, height=30, width=80)
        self.beepDuration = tk.Scale(self.canvas, from_=500, to=1000, tickinterval=50, orient='horizontal')
        self.beepDuration.place(x=20, rely=.835, width=350)
        self.beepDuration.set(600)

        self.brightnessButton = tk.Button(self.canvas, text="Brightness", bg='white', fg='black', command=self.setBrightness)
        self.brightnessButton.place(x=500, rely=.8, height=30, width=80)
        self.brightness = tk.Scale(self.canvas, from_=0, to=50, tickinterval=5, orient='horizontal')
        self.brightness.place(x=500, rely=.835, width=350)
        self.brightness.set(100)

        self.followButton = tk.Button(self.canvas, text="Follow", bg='white', fg='black', command=self.follow)
        self.followButton.place(x=self.ring_x - 40 , y=self.ring_y + 100, height=30, width=80)

        self.clearButton = tk.Button(self.canvas, text="Clear", bg='white', fg='black', command=self.clear)
        self.clearButton.place(x=self.ring_x - 40 , y=self.ring_y + 140, height=30, width=80)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind('<Motion>', self.motion)
        self.root.bind("<Button-1>", self.leftclick)
        self.root.bind("<Button-3>", self.rightclick)
        self.root.bind_all("<MouseWheel>", self.scroll)


    #Messages take a command and value argument. command must be a 4 character string.
    def stopLight(self):
        self.parser.sp.sendMessage('mode', 0)

    def startLight(self):
        self.parser.sp.sendMessage('mode', 1)
    
    def follow(self):
        self.parser.sp.sendMessage('mode', 2)

    def makeBeep(self):
        self.parser.sp.sendMessage('beep', self.beepDuration.get())

    def setBrightness(self):
        self.parser.sp.sendMessage('brtn', self.brightness.get())

    def resetUnit(self):
        self.parser.sp.sendMessage('rstt', 0)

    def setLed(self, led):
        self.parser.sp.sendMessage('lite', led)
    
    def clear(self):
        self.parser.sp.sendMessage('cler', 0)

    def clock(self):
        if len(self.parser.x_angs) > 0:
            self.x_ang = self.parser.x_angs[-1]
            self.canvas.delete(self.link1)
            x_end = self.WIDTH / 2 + self.linelength * math.cos(math.radians(float(self.x_ang-90)))
            y_end = self.HEIGHT / 4 - self.linelength * math.sin(math.radians(float(self.x_ang-90)))
            self.link1 = self.canvas.create_line(self.WIDTH / 2, self.HEIGHT / 4, x_end, y_end, width=3)

        time = datetime.datetime.now().strftime("Time: %H:%M:%S")
        self.label.config(text=time)
        self.root.after(1, self.clock)

    def on_closing(self):
        self.parser.stop()
        self.root.destroy()
    
    def ring(self):
        self.color = 0
        led_increment = 22.5
        self.led_angles = []
        self.led_span = 1
        for i in range(0,16):
            self.led_angles.append(tuple((i*led_increment - led_increment / 2, i*led_increment + led_increment / 2 )))
            #print(self.led_angles)
        self.img = ImageTk.PhotoImage(Image.open("Accelerometer_Reading\imgs\pixelring.png").resize((200, 200), Image.ANTIALIAS))  
        self.canvas.create_image(self.ring_x, self.ring_y, image=self.img) 

    def mainloop(self):
        self.clock()
        self.ring()
        self.root.mainloop()

    def motion(self, event):
        x, y = event.x, event.y
        self.angle = -math.atan2(self.ring_y - y,self.ring_x - x) * (180 / math.pi)
        if self.angle < 0 and self.angle < self.led_angles[0][0]:
            self.angle = -math.atan2( (self.ring_y - y) * -1, (self.ring_x - x) * -1 ) * ( 180 / math.pi ) + 180
        circle = (x-self.ring_x)**2 + (y-self.ring_y)**2
        self.on_led = False
        for i in range(0, 16):
            if self.angle > self.led_angles[i][0] and self.angle < self.led_angles[i][1]:
                self.led_num = i 
                self.on_led = True

        inner_bound = 4900
        outer_bound = 10000
        if (circle < outer_bound) and (circle > inner_bound) :
            self.on_circle = True
        else:
            self.on_circle = False
    
    def leftclick( self, event ):
        if self.on_circle and self.on_led:
            print( 'left click on circle at ' + str(round(self.angle, 1)) + ' degrees' + ', LED: ' + str(self.led_num))
            self.setLed(self.led_num) 
            #print( 'left click on circle at LED: ' + str(self.led_num))

    def rightclick( self, event ):
        #TODO
        if self.on_circle:
            print('rightclick')
            if self.color < 2:
                self.color += 1
            else:
                self.color = 0
            print(self.color)
            self.parser.sp.sendMessage('colr', self.color)


    def scroll( self, event ):
        span_min = 1
        span_max = 17

        delta = int(event.delta / 120)
        if self.on_circle:
            if self.led_span + 2 * delta < span_max and self.led_span + 2 * delta >= span_min:
                self.led_span += 2 * delta
                self.parser.sp.sendMessage('span', self.led_span)
            print(self.led_span)


if __name__ == '__main__':
    win = Window()
    win.parser.go()
    if(win.parser.sp.is_running):
        win.mainloop()