import time
import RPi.GPIO as GPIO

from config import (
    BUTTON_PIN,
    BUTTON_ACTIVE_STATE,
    MORSE_DASH_THRESHOLD,
    LETTER_TIMEOUT,
    WORD_TIMEOUT,
    MESSAGE_TIMEOUT,
    EXIT_HOLD_TIME,
)

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class OneButtonInput:
    def __init__(self):
        pass

    def is_pressed(self) -> bool:
        return GPIO.input(BUTTON_PIN) == BUTTON_ACTIVE_STATE

    def wait_for_long_hold(self, hold_time: float) -> bool:
        # Non-blocking-ish check used in obstacle mode.
        if not self.is_pressed():
            return False

        start = time.time()
        while self.is_pressed():
            if time.time() - start >= hold_time:
                while self.is_pressed():
                    time.sleep(0.01)
                return True
            time.sleep(0.01)
        return False

    def collect_reply_until_timeout(self):
        current_letter = ""
        decoded_parts = []
        last_input_time = None
        word_gap_added = False

        print("[BUTTON] Morse reply mode. Short=dot, Long=dash, Pause=send.")
        print("[BUTTON] Hold very long to exit conversation mode.")

        while True:
            if self.is_pressed():
                start = time.time()

                while self.is_pressed():
                    time.sleep(0.01)

                duration = time.time() - start
                symbol = "." if duration < MORSE_DASH_THRESHOLD else "-"
                current_letter += symbol
                print(f"[BUTTON] {symbol}")

                last_input_time = time.time()
                word_gap_added = False
                time.sleep(0.15)

            now = time.time()

            # End of letter
            if current_letter and last_input_time and (now - last_input_time >= LETTER_TIMEOUT):
                from morse_code import decode_letter
                letter = decode_letter(current_letter)
                decoded_parts.append(letter)
                print(f"[BUTTON] Letter: {letter}")
                current_letter = ""

            # End of word
            if (
                not current_letter
                and decoded_parts
                and last_input_time
                and (now - last_input_time >= WORD_TIMEOUT)
                and not word_gap_added
            ):
                if decoded_parts[-1] != " ":
                    decoded_parts.append(" ")
                    print("[BUTTON] Word gap")
                word_gap_added = True

            # End of full message
            if decoded_parts and last_input_time and (now - last_input_time >= MESSAGE_TIMEOUT):
                return "".join(decoded_parts).strip(), False
            time.sleep(0.01)