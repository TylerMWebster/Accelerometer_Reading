#include "I2Cdev.h"
#include "Adafruit_MPU6050.h"
#include "Wire.h"
#include "FastLED.h"
#include "ArdOSC.h"

#define DATA_PIN 6
#define NUM_LEDS 16
#define MAX_BRIGHTNESS 30// watch the power!
#define tolerance 5
CRGB leds[NUM_LEDS];
CRGB myColor[] = {CRGB::Green, CRGB::Yellow, CRGB::Red};

Adafruit_MPU6050 mpu;
sensors_event_t a, g, temp;

int16_t ax, ay, az, gx, gy, gz;
double timeStep, thistime, timePrev, startTime;
double arx, ary, arz, grx, gry, grz, gsx, gsy, gsz, rx, ry, rz;
double gyroScales[] = {131, 65.5, 32.8, 16.4};
double gyroScale = gyroScales[0];
double r2d = (180 / PI);

const int motorPins[] = {10, 9, 2, 3};
const int button1Pin = A4;  // pushbutton 1 pin
const int ledPin =  13;     // LED pin
int buzPin = 3;
int goal = 90;
int i, j;
int pos = 2;
int state = 0;
int curlState = 0;
//default mode is light feedback
int mode = '1';
//int headers[] = {10,20,30};


void getInput(){
  //In Progress
}


void reset() {
//Set all angles to 0
    grx = 0;
    gry = 0;
    grz = 0;
}


void clearRing(){
//turn all ring leds off
    for (int j=0; j<NUM_LEDS;j++){
        leds[j] = CRGB::Black;
    }
    FastLED.show();
}


void updateLeds(int pos1, int ang){
    //Change ring leds color based on how angle is from goal
    int goalDist = (goal - ang);
    int color = 0;
    clearRing();
    if (goalDist>=75){
      color = 2;
      leds[pos1] = myColor[color]; 
      leds[pos1 + 3] = myColor[color]; 
    }
    if (goalDist<75 && goalDist>20){
      color = 1;
      leds[pos1] = myColor[color]; 
      leds[pos1 + 3] = myColor[color]; 
    }
    if (goalDist<20){
      color = 0;
    }
    
    leds[pos1 + 1] = myColor[color];
    leds[pos1 + 2] = myColor[color];
    
    FastLED.show();
}


void turnOn( int setState, int setPos ) {
  //flash whole ring green when goal is reached
  for (int j=0; j<NUM_LEDS;j++)
  {
    leds[j] = CRGB::Green;
  }
  FastLED.show();
  beep();
  //state = setState;
  pos = setPos;
  //delay(250);
}


void beep(){
  //beep when called
  digitalWrite(buzPin,HIGH);
  delay(10);
  digitalWrite(buzPin,LOW);
}


void vibratePin(int pin, int duration){
   //To-Do make it so you can pass an array of pins so you can do more than one at a time
   //set select pin high for select duration
   digitalWrite(ledPin, HIGH); // turn the LED on
   analogWrite(motorPins[pin - 1], 255);  //turn motor (255 is the high)
   delay(duration);
   resetPins();
}


void resetPins() {
   //set all motorPins low
   digitalWrite(ledPin, LOW);  // turn the LED off
   for (int i = 0 ; i < sizeof(motorPins) / sizeof(motorPins[0]); i++){
     analogWrite(motorPins[i], 0);//turn motors off
   }
   //delay(300);
}


void guideCurl(){
  // Illuminate Leds in the direction we want the user to go
  // State 0 is the extension stage of the curl exercise, State 1 is the compression
  for (int i = 0; i < NUM_LEDS; i++) leds[i] = CRGB::Black;
  switch (curlState) {
    case 0:
    goal = 155;
       if (grx < goal - 5 || grx > 0 )
        { pos = 2;} 
       if (grx > goal + 5 && grx < 225)
         { pos = 10 ;}
       if (grx >= goal - 5 && grx <= goal + 5){ 
          turnOn(1,2);
          grx = 0;
          curlState = 1;
       }   
    break;
    case 1:
    goal = -115;
       if (grx > goal + 5 || grx < 90 )
        { pos = 10;}
       if (grx < goal - 5 && grx > -200)
        { pos = 2;}
       if (grx >= goal - 5 && grx <= goal + 5){ 
          turnOn(0,10);
          grx = 0;
          curlState = 0;
        }    
    break;
    }
    //Serial.println(curlState);
    updateLeds(pos, grx);
  }


void setup() {
  pinMode(2, INPUT_PULLUP);
  Wire.begin();
  Serial.begin(9600);
  mpu.begin();
  startTime = millis();
  thistime = millis();
  i = 1;
  //mpu.setCycleRate(MPU6050_CYCLE_20_HZ);
  //Sensitivity
  mpu.setGyroRange(MPU6050_RANGE_2000_DEG);
  //Live filtering, 260 means filter is off
  mpu.setFilterBandwidth(MPU6050_BAND_260_HZ);
  FastLED.setBrightness(MAX_BRIGHTNESS);
  FastLED.addLeds < WS2812B, DATA_PIN, GRB > leds, NUM_LEDS);
  Serial.begin(9600);
  Serial.println("x,y,z");
  pinMode(buzPin,OUTPUT);
  pinMode(button1Pin, INPUT_PULLUP);//set internal pull up for button
  pinMode(ledPin, OUTPUT);
  delay(100);
}


void loop() {

  getInput();
  
  // set up time for integration
  timePrev = thistime;
  thistime = millis();
  timeStep = (thistime - timePrev) / 1000.0; // time-step in s
  // collect readings
   mpu.getEvent(&a, &g, &temp);
   gx = -g.gyro.x;
   gy = g.gyro.y;
   gz = g.gyro.z;

  // apply gyro scale from datasheet
  gsx = gx/gyroScale;   gsy = gy/gyroScale;   gsz = gz/gyroScale;

  // set initial values
  if (i == 1) {
    grx = 90;
    gry = 0;
    grz = 0;
  }
  // integrate to find the gyro angle
  else{
    grx += r2d*gx*timeStep;
    gry += r2d*gy*timeStep;
    grz += r2d*gz*timeStep;

  }

  //Do one of these based on what mode variable ='s
  switch(mode){
    case '0':
      clearRing();
    break;
    case '1':
      guideCurl();
    break;
    case '9':
      reset();
    break;
  }

  Serial.print(grx);   Serial.print(",");
  Serial.print(gry);   Serial.print(",");
  Serial.println(grz);   

  delay(50);
  i++;
}

