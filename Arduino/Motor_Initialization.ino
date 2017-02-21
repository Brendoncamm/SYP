//Motor Initialization


#include<Servo.h>



Servo esc_1, esc_2, esc_3, esc_4;
const int MotorPin1 = 6;
const int MotorPin2 = 9;
const int MotorPin3 = 10;
const int MotorPin4 = 11;



void setup() {

  Serial.begin(9600);//begin serial monitor & baud rate
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

void loop() {



}






