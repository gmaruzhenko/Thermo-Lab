
# info source = https://arduino.stackexchange.com/questions/55941/serial-communication-between-python-and-arduino
import serial
from datetime import datetime
import csv
#Read from Arduino

ser = serial.Serial(
   port = '../../../dev/ttyACM0',
   baudrate = 9600,
   timeout = 10
)
filename = datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S.csv")
while True:
   with open(str(filename), "a", newline='') as csv_file:
      writer = csv.writer(csv_file, delimiter=',')
      count = 0
      while count < 1000:
         data = ser.readline().decode().strip().split(',')
         print (data)
         writer.writerow(data)
         count += 1
   

   