#include <Wire.h>


const int IntPin =  2;
int byteArray[]={0};
int count=0;

void setup() {

  pinMode(IntPin, OUTPUT);
  Serial.begin(115200);
  Wire.begin(8);
  Wire.onReceive(receiveData); //Call I2C data handler
}

void loop()
{


  digitalWrite(IntPin, HIGH); //Creating a delay for I2C receive, mapped to an RPi input
  delay(2000);
  digitalWrite(IntPin, LOW);
  delay(2000);
  
}

void receiveData(int numByte){

    while(Wire.available()){
      for(int i=0; i<numByte; i++){
        byteArray[i] = Wire.read();
        Serial.print(byteArray[i]);
        
      }
      
    }
}  
