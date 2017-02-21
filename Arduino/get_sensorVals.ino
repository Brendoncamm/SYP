#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_BMP085_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_10DOF.h>

float sensorVals[]={0};

/* Assign a unique ID to the sensors */
Adafruit_10DOF                dof   = Adafruit_10DOF();
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);
Adafruit_BMP085_Unified       bmp   = Adafruit_BMP085_Unified(18001);

/* Update this with the correct SLP for accurate altitude measurements */
float seaLevelPressure = SENSORS_PRESSURE_SEALEVELHPA;



void setup(void)
{
 
  Serial.begin(115200);
  Serial.println(F("Adafruit 10 DOF Pitch/Roll/Heading Example")); Serial.println("");
  
  /* Initialise the sensors */
  initSensors();
}

void loop(void){

   get_sensorVals(&sensorVals[0]);
   Serial.println(sensorVals[0]);

}

void initSensors()
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

float get_sensorVals(float *sensorVals)
{
  float temperature;
  float altitude;
  float yaw;
  float pitch;
  float roll;
  
  sensors_event_t accel_event;
  sensors_event_t mag_event;
  sensors_event_t bmp_event;
  sensors_vec_t   orientation;

  // Calculate pitch and roll from the raw accelerometer data 
  
  accel.getEvent(&accel_event);
  if (dof.accelGetOrientation(&accel_event, &orientation))
  {
    // 'orientation' should have valid .roll and .pitch fields 
    roll=orientation.roll;
    pitch=orientation.pitch;
    
  }
  
  // Calculate the heading using the magnetometer
  mag.getEvent(&mag_event);
  if (dof.magGetOrientation(SENSOR_AXIS_Z, &mag_event, &orientation))
  {
    // 'orientation' should have valid .heading data now
    yaw=orientation.heading;
    
  }

  // Calculate the altitude using the barometric pressure sensor
  bmp.getEvent(&bmp_event);
  if (bmp_event.pressure)
  {
    // Get ambient temperature in C
    bmp.getTemperature(&temperature);
    
    // Convert atmospheric pressure, SLP and temp to altitude  
    altitude=bmp.pressureToAltitude(seaLevelPressure,bmp_event.pressure,temperature); 
    
  }
 
sensorVals[0]=roll;
sensorVals[1]=pitch;
sensorVals[2]=yaw;
sensorVals[3]=altitude;

}
