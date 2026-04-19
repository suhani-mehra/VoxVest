import RPi.GPIO as GPIO
import time
from config import BUTTON_PIN

GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    print("Press the button...")
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button Pressed")
            time.sleep(0.3)  # debounce
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()