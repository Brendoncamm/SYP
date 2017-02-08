
float Error, DError, IError, LastError;
float SenseRead, Output, Setpoint;
float kp, ki, kd;
//unsigned long LastTime = 0;
//int SampleTime=1000; //one second sampling initially



void setup() {
  // put your setup code here, to run once:

  //Initializations of ESC's, Busses Etc.

}

void loop() {
  // put your main code here, to run repeatedly:

  //read controller data, sensor data, perform PID control
  //write pulse to ESC

}



float PID_Calculate(float Setpoint, float SenseRead, float kp, float kd, float ki ) {

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
//}


}
