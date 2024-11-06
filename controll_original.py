from adafruit_servokit import ServoKit
import board
import busio
import adafruit_pca9685
import socket
import time
import struct

# Get local machine name
host = '192.168.243.7'
port = 8081

# Connect to the server
while True:
 try:
  # Create a socket object
  print("Try to connect", host, " and ", port)
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect((host, port))
  break
 except ConnectionRefusedError:
  print("Could not connect to server, on ",host," and " , port )
  time.sleep(5)



# Initialize the I2C bus and the PCA9685 PWM driver
print(board.SCL, board.SDA)
#i2c = busio.I2C('GEN1_I2C_SCL', 'GEN1_I2C_SDA')
i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)


# Set the PWM frequency to 250 Hz (standard for ESCs)
pca.frequency = 250

myKit=ServoKit(channels=16)
a=0
angle=0
speed=0.0
myKit.servo[4].actuation_range = 180
szervo_1=pca.channels[0]

myKit.servo[4].set_pulse_width_range(400,2000)

client_socket.send('ready'.encode())
print("Ready to go!")
try:
 while True:
    try:
       data=client_socket.recv(1024)
       print(data)
    except socket.error:
       print("Connection lost")
       myKit.servo[4].angle=50
       myKit.continuous_servo[8].throttle=0.1
       break
    if not data:
        print("Connection lost")
        myKit.servo[4].angle=50
        myKit.continuous_servo[8].throttle=0.1
        break
    decoded=data.decode('utf8').split()
    if(len(decoded[1].split('-'))>1):
      print("Data value error")
    else:
    #if True:
     speed = float(decoded[0])
     angle = float(decoded[1])
     print(speed,angle)
    if(angle<-0.5 or angle>100.5):
        angle=50
    if (speed>0.5 or speed<-0.5):
        speed=0.1

    myKit.servo[4].angle=angle
    myKit.continuous_servo[8].throttle=speed
finally:
 myKit.servo[4].angle=50
 myKit.continuous_servo[8].throttle=0.1
