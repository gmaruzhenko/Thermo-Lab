
# info source = https://arduino.stackexchange.com/questions/55941/serial-communication-between-python-and-arduino
import serial
import time  # Required to use delay functions
import sys
import csv
#Read from Arduino

ser = serial.Serial(
   port = 'COM4',
   baudrate = 9600,
   timeout = 10
)
with open("test.csv", "a", newline='') as csv_file:
   writer = csv.writer(csv_file, delimiter=',')
   while True:
      data = ser.readline().decode().strip().split(',')
      print (data)
      writer.writerow(data)