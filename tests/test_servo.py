import time
import board
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

i2c = board.I2C()

pca = PCA9685(i2c)

pca.frequency = 50

channel = int(input("Enter channel: "))

test_servo = servo.Servo(pca.channels[channel], min_pulse=500, max_pulse=3000)

test_servo.angle = 0
time.sleep(1)

try:
    while True:
        angle = input("Enter angle:")

        test_servo.angle = int(angle)
except KeyboardInterrupt:
    print("Exiting")
    test_servo.angle = 0
