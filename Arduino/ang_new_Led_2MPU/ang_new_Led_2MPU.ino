/*
Author: Tyler Webster, JMU
Spring 2021
Dual gyroscope readings with realtime light feedback
Recieves serial commands from control software 
*/

#include "I2Cdev.h"
#include "Adafruit_MPU6050.h"
#include "Wire.h"
#include "FastLED.h"
#include <SoftwareSerial.h>
SoftwareSerial XBee(0, 1);

#define DATA_PIN 6
#define NUM_LEDS 16
#define MAX_BRIGHTNESS 20// watch the power!
#define tolerance 5
CRGB leds[NUM_LEDS];
CRGB myColor[] = {CRGB::Green, CRGB::Yellow, CRGB::Red};

Adafruit_MPU6050 mpu;
Adafruit_MPU6050 mpu2;
uint8_t adr2 = 0x69;

sensors_event_t a, g, temp;
sensors_event_t a2, g2, temp2;

int16_t ax, ay, az, gx, gy, gz;
int16_t ax2, ay2, az2, gx2, gy2, gz2;

double timeStep, thistime, timePrev, startTime;
double arx, ary, arz, grx, gry, grz, gsx, gsy, gsz, rx, ry, rz;
double arx2, ary2, arz2, grx2, gry2, grz2, gsx2, gsy2, gsz2, rx2, ry2, rz2;

double gyroScales[] = {131, 65.5, 32.8, 16.4};
double gyroScale = gyroScales[0];
double r2d = (180 / PI);

const int motorPins[] = {10, 9, 2, 3};
const int button1Pin = A4;  // pushbutton 1 pin
const int ledPin =  13;     // LED pin
int buzPin = 4;
int goal = 90;
int i, j;
int pos = 2;
int state = 0;
int curlState = 0;

//default mode is no feedback
int mode = 0;

//headers must be 4 char strings
String headers[] = { "test", "mode", "beep", "rstt", "brtn" };


void getInput(){
  //bool headFound = false;
  if (Serial.available() > 0){
    String msg = String(Serial.readString());
    String key = msg.substring(1, 5);
    int value = msg.substring(6).toInt();
    
    if (key.length() > 0){
      if(key == headers[0]){
        Serial.print(key + "   ");
        Serial.println(value);
      } else if(key == headers[1]){
        mode = value;
      }else if(key == headers[2]){
        beep(value);
      } else if(key == headers[3]){
        reset();
      } else if(key == headers[4]){
        FastLED.setBrightness(value);
      }
    }
  }
}


void reset() {
//Set all angles to 0
    grx = 0;
    gry = 0;
    grz = 0;

    grx2 = 0;
    gry2 = 0;
    grz2 = 0;
}


void clearRing(){
//turn all ring leds off
    for (int j=0; j<NUM_LEDS;j++){
        leds[j] = CRGB::Black;
    }
    //FastLED.show();
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
  beep(10);
  //state = setState;
  pos = setPos;
  //delay(250);
}


void beep(int duration){
  //beep when called
  digitalWrite(buzPin,HIGH);
  delay(duration);
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
  //for (int i = 0; i < NUM_LEDS; i++) leds[i] = CRGB::Black;
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
  pinMode(buzPin,OUTPUT);
  pinMode(button1Pin, INPUT_PULLUP);//set internal pull up for button
  pinMode(ledPin, OUTPUT);
  
  Wire.begin();
  XBee.begin(9600);
  Serial.begin(9600);
  mpu.begin();
  mpu2.begin( adr2 );
  
  startTime = millis();
  thistime = millis();
  i = 1;
  //mpu.setCycleRate(MPU6050_CYCLE_20_HZ);
  
  //Sensitivity
  mpu.setGyroRange(MPU6050_RANGE_2000_DEG);
  mpu2.setGyroRange(MPU6050_RANGE_2000_DEG);
  
  //Live filtering, 260 means filter is off
  mpu.setFilterBandwidth(MPU6050_BAND_260_HZ);
  mpu2.setFilterBandwidth(MPU6050_BAND_260_HZ);
  
  //Setup LED ring
  FastLED.setBrightness(MAX_BRIGHTNESS);
  FastLED.addLeds < WS2812B, DATA_PIN, GRB >( leds, NUM_LEDS);
  clearRing();
  FastLED.show();
  
  Serial.begin(9600);
  Serial.println("x,y,z,x2,y2,z2");

  //delay(100);
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

   mpu2.getEvent(&a2, &g2, &temp2);
   gx2 = -g2.gyro.x;
   gy2 = g2.gyro.y;
   gz2 = g2.gyro.z;

   

  // apply gyro scale from datasheet
  gsx = gx/gyroScale;   gsy = gy/gyroScale;   gsz = gz/gyroScale;
  gsx2 = gx2/gyroScale;   gsy2 = gy2/gyroScale;   gsz2 = gz2/gyroScale;

  // set initial values
  if (i == 1) {
    reset();
  }
  // integrate to find the gyro angle
  else{
    grx += gx*timeStep;
    gry += gy*timeStep;
    grz += gz*timeStep;

    grx2 += gx2*timeStep;
    gry2 += gy2*timeStep;
    grz2 += gz2*timeStep;

  }

  //Do one of these based on what mode variable ='s
  
  switch(mode){
    case 0:
      clearRing();
      FastLED.show();
    break;
    case 1:
      guideCurl();
    break;
  }
  if (XBee.available()){
    XBee.write(grx);
  } else {
    //Serial.println("No XBee");
  }
    Serial.print(grx);   Serial.print(",");
    Serial.print(gry);   Serial.print(",");
    Serial.print(grz);   Serial.print(",");
    Serial.print(grx2);   Serial.print(",");
    Serial.print(gry2);   Serial.print(",");
    Serial.println(grz2);   

  delay(50);
  i++;
}
