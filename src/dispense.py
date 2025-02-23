import sys
import time
from step import setup, cleanup, rotate_motor

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <amount>")
    sys.exit(1)

FEEDING_AMOUNT = int(sys.argv[1])

setup()

for i in range(0, FEEDING_AMOUNT):
    rotate_motor()
    time.sleep(1)

cleanup()
