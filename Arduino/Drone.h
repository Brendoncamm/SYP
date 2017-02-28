/*
  Drone.h - Library for Drone Controller.
  Created by Lucas Doucette, February 17, 2017.
*/
#ifndef Drone_h
#define Drone_h

#include "Arduino.h"
#include <Wire.h>
#include <Servo.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_BMP085_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_10DOF.h>

class Drone
{
  public:
    Drone();
    float get_sensorRoll();
    float get_sensorPitch();
    float get_sensorYaw();
    float get_sensorAltitude(float startingPressure);
    float get_currentPressure();
    float PID_Calculate(float Setpoint, float SenseRead, float kp, float kd, float ki );
    void read_PS4Setpoints();
    void initSensors();
    void initESCs(int MotorPin1, int MotorPin2,int MotorPin3,int MotorPin4);
    float read_float();
    void send_float();

};

#endif
