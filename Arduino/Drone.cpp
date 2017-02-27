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
#include <Adafruit_LSM303.h>
#include <Adafruit_BMP085_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_10DOF.h>


  /* Assign a unique ID to the sensors */
Adafruit_10DOF dof   = Adafruit_10DOF();
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);
Adafruit_BMP085_Unified       bmp   = Adafruit_BMP085_Unified(18001);



//Define Motors for Initialization
Servo esc_1, esc_2, esc_3, esc_4;

//Define PID Variables
float Error, DError, IError, LastTime, NowTime, LastError, Output;

//Smooting Constant
const int numReadings=100;
float SmoothingVariable=0;
float NowPressure=0;

//PS4 Receive Variables
int buffer[16];
float PS4Yaw, PS4Pitch, PS4Roll, PS4Altitude;
int YawBuffer[4], PitchBuffer[4], RollBuffer[4], AltitudeBuffer[4];


// kalman filtering variables

float Variance=0.4;
float varProcess = 1e-1;
float Pc = 0.0;
float G = 0.0;
float P = 1.0;
float Xp = 0.0;
float Zp = 0.0;
float Xe = 0.0;

/*unsigned long Time=0, prevTime=0, TimeBetween=0;
float Displacement=0, TotalDisplacement, Acceleration=0, InitialAcceleration=0;
*/

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
    NowPressure=bmp_event.pressure;
    
    // Get ambient temperature in C
    bmp.getTemperature(&temperature);
    
    
    // Convert atmospheric pressure, SLP and temp to altitude
    sensorAltitude=bmp.pressureToAltitude(startingPressure,NowPressure,temperature);
    
    
    // kalman filter;
    Pc=P+varProcess;
    G=Pc/(Pc+Variance);
    P=(1-G)*Pc;
    Xp=Xe;
    Zp=Xp;
    Xe=G*(sensorAltitude-Zp)+Xp;
    
    
    //Cutoff useless info (Less than ground level)
    
      if(Xe<0)
    {
        Xe=0;
    }
    
    return Xe;
    
  
}

//must be called after initSensors();

float Drone::get_currentPressure()
{
   //Initializing Pressure, Filtered for accuracy
    
    bmp.getEvent(&bmp_event);
    for(int i=0; i<numReadings; i++)
    {
        SmoothingVariable+=bmp_event.pressure;
        //delay(1);
    
    }
    
    currentPressure = SmoothingVariable/numReadings;    
    SmoothingVariable=0;
    
    return currentPressure;
    
}

float Drone::PID_Calculate(float Setpoint, float SenseRead, float kp, float kd, float ki )
{
    
    //find current time
    unsigned long NowTime = millis();
    
    //calculate PID Error values
    Error = Setpoint-SenseRead;
    DError = (Error-LastError)/(NowTime-LastTime);
    IError += (Error*(NowTime-LastTime));

    //Calculate Output
    Output = kp*Error+ki*IError+kd*DError;
   
    //Save LastTime and LastError
    LastTime=NowTime;
    LastError=Error;

    return Output;
}


void Drone::read_PS4Setpoints()
    
{
    
    //Write serially to Pi to begin transmission.
    if (Serial.available()) {
        for (int i=0; i<15; i++) {
            buffer[i] = Serial.read();
        }
    }

}

float Drone::get_PS4Yaw()
{
    for(int i=0; i<4; i++)
    {
        YawBuffer[i]=buffer[i];
        PS4Yaw = *((float*)(YawBuffer));
    }
    
    return YawBuffer[1];
}

float Drone::get_PS4Pitch()
{
    for(int i=4; i<8; i++)
    {
        PitchBuffer[i]=buffer[i];
        PS4Pitch = *((float*)(PitchBuffer));
    }
    
    return PS4Pitch;
}

float Drone::get_PS4Roll()
{
    for(int i=8; i<12; i++)
    {
        RollBuffer[i]=buffer[i];
        PS4Roll = *((float*)(RollBuffer));
    }
    
    return PS4Roll;
}

float Drone::get_PS4Altitude()
{
    for(int i=12; i<16; i++)
    {
        AltitudeBuffer[i]=buffer[i];
        PS4Altitude = *((float*)(AltitudeBuffer));
    }
    
    return PS4Altitude;
    
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


