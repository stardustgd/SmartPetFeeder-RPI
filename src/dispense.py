import sys
import time
from adafruit_servokit import ServoKit
from drivers.hx711 import HX711

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <amount>")
    sys.exit(1)

FEEDING_AMOUNT = int(sys.argv[1]) * 140

kit = ServoKit(channels=16)
kit.servo[7].actuation_range = 270

# Set up hx711
hx = HX711(dout=5, pd_sck=6)
hx.setReferenceUnit(421.03056)


def read_weight(samples=16, delay=0.05):
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


def dispense_food(channel, target_weight, step=1, delay=0.02):
    current_weight = read_weight()

    while current_weight < target_weight:
        for angle in range(0, 270, step):
            kit.servo[channel].angle = angle
            time.sleep(delay)

            current_weight = read_weight()

            if current_weight >= target_weight:
                return

        for angle in range(270, 0, -step):
            kit.servo[channel].angle = angle
            time.sleep(delay)
            current_weight = read_weight()

            if current_weight >= target_weight:
                return


dispense_food(7, FEEDING_AMOUNT)
hx.powerDown()
