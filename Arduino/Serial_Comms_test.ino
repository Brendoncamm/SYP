void setup() {
  Serial.begin(9600);
}

//from stackoverflow Nils Pipenbrinck
void send_float (float arg) {
  byte * data = (byte *) &arg;
  Serial.write(data, sizeof(arg));
}

float read_float () {
 union{
   float a;
   unsigned char bytes[4];
 } data;
 for (int i=0; i<4; i++) {
   data.bytes[i] = Serial.read();
 } 
 float test = data.a;
 return(test);
}

float recv;
void loop() {
  if (Serial.available() == 4) {
    //Serial.read();
    recv = read_float();
    send_float(recv);
    //Serial.print(sizeof(recv));
  }
}
