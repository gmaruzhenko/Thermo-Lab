import serial

ser = serial.Serial(

   port = 'COM8',

   baudrate = 9600,

   timeout = 10

)

while True:
   print(ser.readline())
