from button_input import OneButtonInput
from speech_io import speak_text

button = OneButtonInput()

print("Morse to speech test")
print("Use the button to enter Morse.")
print("Pause to end letters/words, longer pause to send.")

try:
    while True:
        reply_text, _ = button.collect_reply_until_timeout()

        if reply_text:
            print(f"Decoded: {repr(reply_text)}")
            speak_text(reply_text)
        else:
            print("No reply entered.")

except KeyboardInterrupt:
    print("\nStopped.")