import time

from config import (
    STATE_OBSTACLE,
    STATE_CONVERSATION,
    MODE_HOLD_TIME,
    SHOW_PREVIEW,
    EXIT_HOLD_TIME,   # 🔥 ADD THIS
)
from camera_cv import VisionSystem
from motor_control import (
    obstacle_object_feedback,
    obstacle_person_feedback,
    play_morse_left,
    stop_all,
    cleanup,
)
from morse_code import text_to_morse
from speech_io import listen_until_silence, speak_text
from button_input import OneButtonInput


def main() -> None:
    state = STATE_OBSTACLE
    vision = VisionSystem(show_preview=SHOW_PREVIEW)
    button = OneButtonInput()

    last_person_seen = False
    recent_person_time = 0.0

    vision.start()
    print("[SYSTEM] Started.")

    try:
        while True:

            # =========================
            # OBSTACLE MODE
            # =========================
            if state == STATE_OBSTACLE:
                frame = vision.get_frame()
                target = vision.detect_primary_target(frame)

                last_person_seen = False

                if target is not None:
                    print(f"[VISION] {target['label']} | {target['distance']} | area={target['area']}")

                    if target["label"] == "object":
                        obstacle_object_feedback(target["distance"])

                    elif target["label"] == "person":
                        last_person_seen = True
                        recent_person_time = time.time()
                        obstacle_person_feedback(target["distance"])

                # Allow entering conversation mode shortly after a person is seen.
                if last_person_seen or (time.time() - recent_person_time < 3.0):
                    if button.wait_for_long_hold(MODE_HOLD_TIME):
                        state = STATE_CONVERSATION
                        stop_all()
                        print("[STATE] Conversation mode entered.")
                        time.sleep(0.2)

                time.sleep(0.03)

            # =========================
            # CONVERSATION MODE
            # =========================
            elif state == STATE_CONVERSATION:

                # 🔥 GLOBAL FORCE EXIT (4 sec hold)
                if button.wait_for_long_hold(EXIT_HOLD_TIME):
                    state = STATE_OBSTACLE
                    stop_all()
                    print("[STATE] Forced exit → obstacle mode")
                    time.sleep(0.3)
                    continue

                print("[STATE] Listening for incoming speech...")
                incoming_text = listen_until_silence()

                # 🔥 Check again after listening
                if button.wait_for_long_hold(EXIT_HOLD_TIME):
                    state = STATE_OBSTACLE
                    stop_all()
                    print("[STATE] Forced exit → obstacle mode")
                    time.sleep(0.3)
                    continue

                if incoming_text:
                    morse_seq = text_to_morse(incoming_text)
                    print(f"[MORSE IN] {morse_seq}")
                    play_morse_left(morse_seq)
                else:
                    print("[STATE] No incoming speech captured.")

                # 🔥 Collect reply (no exit_requested anymore)
                reply_text, _ = button.collect_reply_until_timeout()

                if reply_text:
                    print(f"[REPLY] {reply_text}")
                    speak_text(reply_text)
                else:
                    print("[REPLY] No reply entered.")

    except KeyboardInterrupt:
        print("\n[SYSTEM] Stopped by user.")
    finally:
        vision.stop()
        cleanup()


if __name__ == "__main__":
    main()