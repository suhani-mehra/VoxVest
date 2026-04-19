import time
import RPi.GPIO as GPIO

from config import (
    LEFT_MOTOR_PIN,
    RIGHT_MOTOR_PIN,
    OBJECT_PULSE,
    PERSON_PULSE,
    DOT_TIME,
    DASH_TIME,
    SYMBOL_GAP,
    LETTER_GAP,
    WORD_GAP,
)

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_MOTOR_PIN, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_PIN, GPIO.OUT)

GPIO.output(LEFT_MOTOR_PIN, GPIO.LOW)
GPIO.output(RIGHT_MOTOR_PIN, GPIO.LOW)


def pulse(pin: int, duration: float) -> None:
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(pin, GPIO.LOW)


def pulse_left(duration: float) -> None:
    pulse(LEFT_MOTOR_PIN, duration)


def pulse_right(duration: float) -> None:
    pulse(RIGHT_MOTOR_PIN, duration)


def stop_all() -> None:
    GPIO.output(LEFT_MOTOR_PIN, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_PIN, GPIO.LOW)


def obstacle_object_feedback(distance_level: str) -> None:
    # Short pulses for general objects. Faster repeat when closer.
    if distance_level == "far":
        pulse_right(OBJECT_PULSE)
        time.sleep(0.9)
    elif distance_level == "mid":
        for _ in range(2):
            pulse_right(OBJECT_PULSE)
            time.sleep(0.35)
    else:
        for _ in range(4):
            pulse_right(OBJECT_PULSE)
            time.sleep(0.15)


def obstacle_person_feedback(distance_level: str) -> None:
    # Longer pulse pattern for people so it feels distinct.
    if distance_level == "near":
        pulse_right(PERSON_PULSE)
        time.sleep(0.2)
        pulse_right(0.25)
    else:
        pulse_right(PERSON_PULSE)


def play_morse_left(sequence: str) -> None:
    # Morse plays on the left motor during conversation mode.
    for ch in sequence:
        if ch == ".":
            pulse_left(DOT_TIME)
            time.sleep(SYMBOL_GAP)
        elif ch == "-":
            pulse_left(DASH_TIME)
            time.sleep(SYMBOL_GAP)
        elif ch == " ":
            time.sleep(LETTER_GAP)
        elif ch == "/":
            time.sleep(WORD_GAP)


def cleanup() -> None:
    stop_all()
    GPIO.cleanup()
