#Requires PySerial

import serial

arduino = serial.Serial('/dev/tty.usbserial', 9600)

ser.write(b'Test')

while True:
    print(ser.readline())
