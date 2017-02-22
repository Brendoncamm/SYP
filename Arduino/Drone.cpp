/*
  Drone.h - Library for Drone Controller.
  Created by Lucas Doucette, February 17, 2017.
*/

#include "Arduino.h"
#include "Drone.h"
#include <Wire.h>
#include <Servo.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_BMP085_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_10DOF.h>


  /* Assign a unique ID to the sensors */
Adafruit_10DOF                dof   = Adafruit_10DOF();
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);
Adafruit_BMP085_Unified       bmp   = Adafruit_BMP085_Unified(18001);

Servo esc_1, esc_2, esc_3, esc_4;
float Error, DError, IError, LastTime, NowTime, LastError, Output;

//Smooting Constant
const int numReadings=10000;
float SmoothingVariable=0;
float NowPressure=0;

float temperature;
float sensorAltitude;
float sensorYaw;
float sensorPitch;
float sensorRoll;
float currentPressure;
  
sensors_event_t accel_event;
sensors_event_t mag_event;
sensors_event_t bmp_event;
sensors_vec_t   orientation;

Drone::Drone()
{

}

float Drone::get_sensorRoll()
{


  // Calculate pitch and roll from the raw accelerometer data 
  
  accel.getEvent(&accel_event);
  if (dof.accelGetOrientation(&accel_event, &orientation))
  {
    // 'orientation' should have valid .roll and .pitch fields 
    sensorRoll=orientation.roll;
    return sensorRoll;  
   
    
  }
}
    
float Drone::get_sensorPitch()
{

  // Calculate pitch and roll from the raw accelerometer data 
  
  accel.getEvent(&accel_event);
  if (dof.accelGetOrientation(&accel_event, &orientation))
  {
    // 'orientation' should have valid .roll and .pitch fields 
   
     sensorPitch=orientation.pitch;
     return sensorPitch;  
    
  }    
}
    
float Drone::get_sensorYaw()
{
  
  // Calculate the heading using the magnetometer
  mag.getEvent(&mag_event);
  if (dof.magGetOrientation(SENSOR_AXIS_Z, &mag_event, &orientation))
  {
    // 'orientation' should have valid .heading data now
    sensorYaw=orientation.heading;
    return sensorYaw;  
    
  }
}
       
float Drone::get_sensorAltitude(float startingPressure)
{
  // Calculate the altitude using the barometric pressure sensor
    
  
  bmp.getEvent(&bmp_event);
 
      
      for(int i=0; i<numReadings; i++)
    {
        SmoothingVariable+=bmp_event.pressure;
    
    }
    
    NowPressure=SmoothingVariable/numReadings;
    SmoothingVariable=0;
    
    Serial.print("Pressure:    ");
    Serial.print(NowPressure);
    Serial.println(" hPa");
      
    // Get ambient temperature in C
    bmp.getTemperature(&temperature);
    Serial.print(temperature);  
    
    // Convert atmospheric pressure, SLP and temp to altitude  
    sensorAltitude=bmp.pressureToAltitude(startingPressure,NowPressure,temperature); 
    return sensorAltitude;  
  
  
}

//must be called after initSensors();

float Drone::get_currentPressure()
{
    bmp.getEvent(&bmp_event);
    for(int i=0; i<numReadings; i++)
    {
        SmoothingVariable+=bmp_event.pressure;
    
    }
    currentPressure = SmoothingVariable/numReadings;
    SmoothingVariable=0;
    
    Serial.print("CurrentPressure:    ");
    Serial.print(bmp_event.pressure);
    return currentPressure;
    
    
}

float Drone::PID_Calculate(float Setpoint, float SenseRead, float kp, float kd, float ki )
{
    //unsigned long NowTime = millis();
//if(NowTime-LastTime >= SampleTime)
//{
  //calculate error
  Error = Setpoint-SenseRead;
  DError = (Error-LastError)/(NowTime-LastTime);
  IError += (Error*(NowTime-LastTime));

  Output = kp*Error+ki*IError+kd*DError;
//Save LastTime and LastError

  LastTime=NowTime;
  LastError=Error;

  return Output;
}

void Drone::initSensors()
{

  if(!accel.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println(F("Ooops, no LSM303 detected ... Check your wiring!"));
    while(1);
  }
  if(!mag.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println("Ooops, no LSM303 detected ... Check your wiring!");
    while(1);
  }
  if(!bmp.begin())
  {
    /* There was a problem detecting the BMP180 ... check your connections */
    Serial.println("Ooops, no BMP180 detected ... Check your wiring!");
    while(1);
  }

}

void Drone::initESCs(int MotorPin1, int MotorPin2,int MotorPin3,int MotorPin4)
{

  esc_1.attach(MotorPin1);  //set up motor connections
  esc_2.attach(MotorPin2);
  esc_3.attach(MotorPin3);
  esc_4.attach(MotorPin4);

  //Initialization of the ESCs
  esc_1.writeMicroseconds(1860);
  esc_2.writeMicroseconds(1860);
  esc_3.writeMicroseconds(1860);
  esc_4.writeMicroseconds(1860);
  delay(3000);
  esc_1.writeMicroseconds(1060);
  esc_2.writeMicroseconds(1060);
  esc_3.writeMicroseconds(1060);
  esc_4.writeMicroseconds(1060);
  delay(3000);


}
