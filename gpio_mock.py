# gpio_mock.py

class GPIO:
    BCM = OUT = IN = HIGH = LOW = None

    @staticmethod
    def setmode(mode):
        print(f"[MOCK] GPIO setmode({mode})")

    @staticmethod
    def setup(pin, mode):
        print(f"[MOCK] GPIO setup(pin={pin}, mode={mode})")

    @staticmethod
    def output(pin, state):
        print(f"[MOCK] GPIO output(pin={pin}, state={state})")

    @staticmethod
    def cleanup():
        print("[MOCK] GPIO cleanup()")
