import board
import sys
import time
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
from drivers.hx711 import HX711

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <amount>")
    sys.exit(1)

FEEDING_AMOUNT = int(sys.argv[1]) * 140
SERVO_CHANNEL = 3
SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 3000
SERVO_ACTUATION_RANGE = 180

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
steps = [0, 42]

# Set up hx711
hx = HX711(dout=5, pd_sck=6)
hx.setReferenceUnit(421.03056)


def read_weight(samples=10, delay=0.05):
    weights = []

    for _ in range(samples):
        rawBytes = hx.readRawBytes()
        weightValue = hx.rawBytesToWeight(rawBytes)
        weights.append(weightValue)
        time.sleep(delay)

    # Remove outliers
    weights.remove(max(weights))
    weights.remove(min(weights))

    return sum(weights) / len(weights)


def dispense_food(target_weight):
    current_weight = read_weight()

    try:
        while current_weight < target_weight:
            for step in steps:
                servo.angle = step
                time.sleep(0.35)

            current_weight = read_weight()

            if current_weight >= target_weight:
                raise StopIteration

            time.sleep(1)
    except (StopIteration, KeyboardInterrupt):
        servo.angle = 0


dispense_food(FEEDING_AMOUNT)
hx.powerDown()
