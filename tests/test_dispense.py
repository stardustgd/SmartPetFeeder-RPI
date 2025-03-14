import board
import sys
import time
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <amount>")
    sys.exit(1)

FEEDING_AMOUNT = int(sys.argv[1])

SERVO_CHANNEL = 3
SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 3000
SERVO_ACTUATION_RANGE = 270

# Set up servo
i2c = board.I2C()
pca = PCA9685(i2c)
pca.frequency = 50
servo = servo.Servo(
    pca.channels[SERVO_CHANNEL],
    min_pulse=SERVO_MIN_PULSE,
    max_pulse=SERVO_MAX_PULSE,
    actuation_range=SERVO_ACTUATION_RANGE,
)

servo.angle = 0

steps = [61, 119, 178, 230]

for i in range(0, FEEDING_AMOUNT):
    for step in steps:
        servo.angle = step
        time.sleep(2)

    servo.angle = 0
    time.sleep(3)
