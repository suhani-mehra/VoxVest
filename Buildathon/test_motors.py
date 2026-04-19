import RPi.GPIO as GPIO
import time
from config import LEFT_MOTOR_PIN, RIGHT_MOTOR_PIN

GPIO.setmode(GPIO.BCM)

GPIO.setup(LEFT_MOTOR_PIN, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_PIN, GPIO.OUT)

def cleanup():
    GPIO.output(LEFT_MOTOR_PIN, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_PIN, GPIO.LOW)
    GPIO.cleanup()

try:
    print("Testing LEFT motor...")
    GPIO.output(LEFT_MOTOR_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(LEFT_MOTOR_PIN, GPIO.LOW)

    time.sleep(1)

    print("Testing RIGHT motor...")
    GPIO.output(RIGHT_MOTOR_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(RIGHT_MOTOR_PIN, GPIO.LOW)

    time.sleep(1)

    print("Testing BOTH motors...")
    GPIO.output(LEFT_MOTOR_PIN, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(LEFT_MOTOR_PIN, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_PIN, GPIO.LOW)
finally:
     cleanup()