import RPi.GPIO as GPIO
import time
from enum import Enum


class Direction(Enum):
    COUNTER_CLOCKWISE = 0
    CLOCKWISE = 1


# https://ben.akrin.com/driving-a-28byj-48-stepper-motor-uln2003-driver-with-a-raspberry-pi/
PIN1 = 17
PIN2 = 18
PIN3 = 27
PIN4 = 22

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
STEP_SLEEP = 0.002

STEP_COUNT = 4096  # 5.625*(1/64) per step, 4096 steps is 360°

rotate_direction = Direction.COUNTER_CLOCKWISE

# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
STEP_SEQUENCE = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
]

MOTOR_PINS = [PIN1, PIN2, PIN3, PIN4]
motor_step_counter = 0


def setup():
    # setting up
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN1, GPIO.OUT)
    GPIO.setup(PIN2, GPIO.OUT)
    GPIO.setup(PIN3, GPIO.OUT)
    GPIO.setup(PIN4, GPIO.OUT)

    # initializing
    GPIO.output(PIN1, GPIO.LOW)
    GPIO.output(PIN2, GPIO.LOW)
    GPIO.output(PIN3, GPIO.LOW)
    GPIO.output(PIN4, GPIO.LOW)


def cleanup():
    GPIO.output(PIN1, GPIO.LOW)
    GPIO.output(PIN2, GPIO.LOW)
    GPIO.output(PIN3, GPIO.LOW)
    GPIO.output(PIN4, GPIO.LOW)
    GPIO.cleanup()


def rotate_motor(direction=Direction.COUNTER_CLOCKWISE):
    for i in range(STEP_COUNT):
        for pin in range(0, len(MOTOR_PINS)):
            GPIO.output(MOTOR_PINS[pin], STEP_SEQUENCE[motor_step_counter][pin])

        if direction == Direction.CLOCKWISE:
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction == Direction.COUNTER_CLOCKWISE:
            motor_step_counter = (motor_step_counter + 1) % 8
        else:
            print("error")
            break

        time.sleep(STEP_SLEEP)
