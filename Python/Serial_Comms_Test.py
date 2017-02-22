#Requires PySerial

import serial

arduino = serial.Serial('/dev/ttyACM0', 9600)

arduino.write(b'Test\r\n')

while True:
    print(arduino.readline())
