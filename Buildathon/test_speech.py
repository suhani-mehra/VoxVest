from speech_io import listen_until_silence, speak_text

print("Say something...")
text = listen_until_silence()

print("You said:", text)

if text:
    speak_text(text)
