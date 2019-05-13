# info source = https://arduino.stackexchange.com/questions/55941/serial-communication-between-python-and-arduino
import serial
import time  # Required to use delay functions

arduinoSerialData = serial.Serial('com8', 9600)  # Create Serial port object called arduinoSerialData
time.sleep(10)  # wait for 2 secounds for the communication to get established

print arduinoSerialData.readline()  # read the serial data and print it as line
print ("Enter 1 to turn ON LED and 0 to turn OFF LED")

