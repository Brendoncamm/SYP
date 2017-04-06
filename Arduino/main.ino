#include <Drone.h>
Drone drone;
Servo esc_1, esc_2, esc_3, esc_4;
int MotorPin1=3, MotorPin2=5, MotorPin3=6, MotorPin4=9;
float Yaw_Setpoint, Pitch_Setpoint, Roll_Setpoint, Altitude_Setpoint;
float Current_Yaw, Current_Pitch, Current_Roll, Current_Altitude;
float initial_pressure;
float kp=17257.712, ki=2752.7, kd=12500;
float AltitudePID;


void setup() {

  esc_1.attach(MotorPin1);  //set up motor connections & Initialize
  esc_2.attach(MotorPin2);
  esc_3.attach(MotorPin3);
  esc_4.attach(MotorPin4);
  drone.initESCs(esc_1, esc_2, esc_3, esc_4);

  //Initialize Serial Bus and IMU Sensors

   Serial.begin(9600);
   drone.initSensors();
   initial_pressure=drone.get_currentPressure();
   
  
}

void loop() {


//Get Control Setpoints
if (Serial.available()==0)
{
  Serial.print('c');
}

while (Serial.available()>0)
  {
    Yaw_Setpoint = drone.read_float();
    Pitch_Setpoint = drone.read_float();
    Altitude_Setpoint = drone.read_float();
    Roll_Setpoint = drone.read_float(); 
  }


//Gather IMU Data
Current_Yaw = drone.get_sensorYaw();
Current_Pitch = drone.get_sensorPitch();
Current_Altitude = drone.get_sensorAltitude(initial_pressure);
Current_Roll = drone.get_sensorRoll();


//Perform PID Loop (Only altitude for testing)
AltitudePID = drone.PID_Calculate(Altitude_Setpoint, Current_Altitude, kp, ki, kd);


//Write Altitude PID Results to motors (Need a function for this future)
 esc_1.writeMicroseconds(AltitudePID);
 esc_2.writeMicroseconds(AltitudePID);
 esc_3.writeMicroseconds(AltitudePID);
 esc_4.writeMicroseconds(AltitudePID);





}
