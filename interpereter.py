
# info source = https://arduino.stackexchange.com/questions/55941/serial-communication-between-python-and-arduino
import serial
import time  # Required to use delay functions
import sys

#Read from Arduino

ser = serial.Serial(
   port = 'COM4',
   baudrate = 9600,
   timeout = 10
)

while True:
   print(ser.readline().decode())#.strip().split(','))

#write to csv

"""
Initializes a file for writing and returns the file object
"""
def csv_init():

    print("Enter output file name (e.g. data.csv):")
    filename = input()

    return open(filename, "w")

<<<<<<< HEAD
def csv_teardown(filename):
    filename.close()
=======

def csv_teardown(file_obj):
    file_obj.close()


>>>>>>> 30d70cd75f0eb994069bf04243a6bfc430e9bc3f
