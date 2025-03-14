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


def move_servo(servo, target_angle, step=1, delay=0.02):
    if servo.angle is None:
        servo.angle = 0

    current_angle = int(servo.angle)

    step = step if target_angle > current_angle else -step

    for angle in range(current_angle, target_angle, step):
        servo.angle = angle
        time.sleep(delay)

    servo.angle = target_angle


try:
    while True:
        angle = int(input("Enter angle:"))

        move_servo(servo, angle, delay=0.1)
except KeyboardInterrupt:
    print("Exiting")
    move_servo(servo, 0)
