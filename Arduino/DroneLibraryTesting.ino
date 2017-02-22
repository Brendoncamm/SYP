#include <Drone.h>
//float sensorRoll;
Drone drone;
float roll, pitch, yaw, altitude, initial_pressure;



void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);
  drone.initSensors();
  initial_pressure=drone.get_currentPressure();
 

}

void loop() {
 /* roll=drone.get_sensorRoll();
  Serial.print("Roll: ");
  Serial.print(roll);

  pitch=drone.get_sensorPitch();
  Serial.print("Pitch: ");
  Serial.print(pitch);
  
  yaw=drone.get_sensorYaw();
  Serial.print("Yaw: ");
  Serial.print(yaw);
  */
  altitude=drone.get_sensorAltitude(initial_pressure);
  Serial.print("Altitude: ");
  Serial.println(altitude);


}
