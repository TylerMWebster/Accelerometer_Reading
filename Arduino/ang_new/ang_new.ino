#include "I2Cdev.h"
#include "Adafruit_MPU6050.h"
#include "Wire.h"

Adafruit_MPU6050 mpu;

int16_t ax, ay, az, gx, gy, gz;
sensors_event_t a, g, temp;
double timeStep, thistime, timePrev, startTime;
double arx, ary, arz, grx, gry, grz, gsx, gsy, gsz, rx, ry, rz;

int i, j;
double gyroScales[] = {131, 65.5, 32.8, 16.4};
double gyroScale = gyroScales[0];

double prevgsx = 0;
double prevgsy = 0;
double prevgsz = 0;
double slopes[3];

double r2d = (180 / PI);

void reset() {
    grx = 0;
    gry = 0;
    grz = 0;
}

void setup() {

  pinMode(2, INPUT_PULLUP);
  Wire.begin();
  Serial.begin(9600);
  mpu.begin();
  startTime = millis();
  thistime = millis();
  i = 1;
  mpu.setCycleRate(MPU6050_CYCLE_20_HZ);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);  
  //Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    //Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    //Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    //Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    //Serial.println("+- 2000 deg/s");
    break;
  }
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  //Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    //Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    //Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    //Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    //Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    //Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    //Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    //Serial.println("5 Hz");
    break;
  }
  Serial.println("");
  delay(100);
}

void loop() {
  
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

  // set initial values to 0
  if (i == 1) {
    //calibrate(100.0);
    grx = 0;
    gry = 0;
    grz = 0;
    //Serial.println("grx,gry,grz");
  }
  // integrate to find the gyro angle
  else{
    grx += r2d*gx*timeStep;
    gry += r2d*gy*timeStep;
    grz += r2d*gz*timeStep;
  }  

  Serial.print(grx);   Serial.print(",");
  Serial.print(gry);   Serial.print(",");
  Serial.println(grz);   

  delay(50);
  i++;
}
