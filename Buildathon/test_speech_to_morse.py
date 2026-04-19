from speech_io import listen_until_silence
from morse_code import text_to_morse
from motor_control import play_morse_left, cleanup

try:
    print("Say something...")
    text = listen_until_silence()

    print("Heard:", text)

    if text:
        morse = text_to_morse(text)
        print("Morse:", morse)
        print("Playing on left motor...")
        play_morse_left(morse)

finally:
    cleanup()