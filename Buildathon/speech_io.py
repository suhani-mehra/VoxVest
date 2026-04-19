import subprocess
import speech_recognition as sr
import os


from config import (
    SPEECH_PHRASE_TIME_LIMIT,
    SPEECH_SILENCE_TIMEOUT,
    ALLOW_TYPED_SPEECH_FALLBACK,
)

recognizer = sr.Recognizer()


def speak_text(text: str) -> None:
    if not text:
        return
    print(f"[TTS] {text}")
    os.system(f'espeak "{text}"')


def listen_until_silence() -> str:
    try:
        with sr.Microphone(device_index=3) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            recognizer.pause_threshold = 1.4

            print("[MIC] Listening...")

            audio = recognizer.listen(
                source,
                timeout=SPEECH_SILENCE_TIMEOUT,
                phrase_time_limit=SPEECH_PHRASE_TIME_LIMIT,
            )

        text = recognizer.recognize_google(audio).strip()
        print(f"[MIC] Heard: {text}")
        return text

    except Exception as e:
        print(f"[MIC] Error: {e}")
        return ""
    
    except sr.UnknownValueError:
        print("[MIC] Could not understand speech.")
        if ALLOW_TYPED_SPEECH_FALLBACK:
            return input("[FALLBACK] Type incoming text (or blank): ").strip()
        return ""
    except Exception as e:
        print(f"[MIC] Error: {e}")
        if ALLOW_TYPED_SPEECH_FALLBACK:
            return input("[FALLBACK] Type incoming text (or blank): ").strip()
        return ""
