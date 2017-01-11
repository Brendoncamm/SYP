#include<Servo.h>

//Define Constants

Servo esc;
const int MotorPin = 9;
const int Var_Resistor = A0;
int Resistor_Value = 0;
int time_value = 0;


void setup() {

  Serial.begin(9600);//begin serial monitor & baud rate
  esc.attach(MotorPin);  //set up motor connection
  pinMode(Var_Resistor,INPUT); //Enable Variable Resistor Input

  //Initialization of the ESC
  esc.writeMicroseconds(1860);
  delay(3000);
  esc.writeMicroseconds(1060);
  delay(3000);
  
}

void loop() {

  //Read the resistor value 
  Resistor_Value=analogRead(Var_Resistor);
  
  //Var_Resistor will be between 1-1024, need to convert to 1060-1860
  //1060-1860 is a range of 800, 800/1023=0.78201
  time_value=(Resistor_Value*0.78201)+1060;//Conversion into req'd time range

  //write the time signal to the servo motor
  esc.writeMicroseconds(time_value);
  Serial.println(time_value);
  

}
