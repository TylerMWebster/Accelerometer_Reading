void calibrate(double samples){

  double xslope;
  double yslope;
  double zslope;
  double initx = 0;
  double inity = 0;
  double initz = 0;
  Serial.println("Calibrating, Please Wait");

  timePrev = thistime;
  thistime = millis();
  timeStep = (thistime - timePrev) / 1000.0;

  // collect readings
  mpu.getEvent(&a, &g, &temp);
  gx = -g.gyro.x;
  gy = g.gyro.y;
  gz = g.gyro.z;
  // apply gyro scale from datasheet
  gsx = gx/gyroScale;   gsy = gy/gyroScale;   gsz = gz/gyroScale;

  initx += r2d*(gx*timeStep);
  inity += r2d*(gy*timeStep);
  initz += r2d*(gz*timeStep);
  delay(50);
  
  for(int j = 0; j < samples - 1; j++){
    timePrev = thistime;
    thistime = millis();
    timeStep = (thistime - timePrev) / 1000.0;
    // collect readings
    //accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    mpu.getEvent(&a, &g, &temp);
    gx = -g.gyro.x;
    gy = g.gyro.y;
    gz = g.gyro.z;
    // apply gyro scale from datasheet
    gsx = gx/gyroScale;   gsy = gy/gyroScale;   gsz = gz/gyroScale;
    grx += (gx*timeStep);
    gry += (gy*timeStep);
    grz += (gz*timeStep);
    delay(50);
  }

}
