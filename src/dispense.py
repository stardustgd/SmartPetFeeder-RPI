import sys
import time
from drivers.hx711 import HX711
from step import setup, cleanup, rotate_motor

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <amount>")
    sys.exit(1)

FEEDING_AMOUNT = int(sys.argv[1])

setup()

# Set up hx711
hx = HX711(dout=5, pd_sck=6)
hx.setReferenceUnit(-3410)

for i in range(0, FEEDING_AMOUNT):
    rotate_motor()

    rawBytes = hx.readRawBytes()
    weightValue = hx.rawBytesToWeight(rawBytes)
    print(f"[INFO] POLLING_BASED | weight (grams): {weightValue}")
    time.sleep(1)

hx.powerDown()
cleanup()
