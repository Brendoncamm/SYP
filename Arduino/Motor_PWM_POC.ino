
const int Var_Resistor = A0;
const int MotorPin = 9;
int Resistor_Value = 0;



void setup() {




  //Begin Serial Monitor
  
  Serial.begin(9600);
  
  //Initiate Motor Pin and Variable Resistor Input
  
  pinMode(MotorPin,OUTPUT); 
  pinMode(Var_Resistor,INPUT); 
  

}

void loop() {

  //Read value from the variable resistor, output PWM based on value returned.

   Resistor_Value=analogRead(Var_Resistor)/4; //Divided by 4 to reduce the input from 0-1023 to 0-255
   analogWrite(MotorPin,Resistor_Value); // Apply resistors input as a pwm to the motor pin

   Serial.print("PWM Value is: ");
   Serial.println(Resistor_Value); //Send Value to the Serial Monitor
   
  
   
  
}
