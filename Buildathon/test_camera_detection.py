import time
from camera_cv import VisionSystem

# Use headless mode (no preview window)
vision = VisionSystem(show_preview=True)
vision.start()

try:
    print("Starting camera detection test... (Ctrl+C to stop)")

    while True:
        start_time = time.time()
        label = "nothing"

        # Sample frames for ~1 second to stabilize detection
        while time.time() - start_time < 1.0:
            frame = vision.get_frame()
            target = vision.detect_primary_target(frame)

            if target is not None:
                label = target["label"]  # "person" or "object"

        print(f"[DETECTION] {label}")

        # Wait so it prints every 5 seconds total
        time.sleep(4)

except KeyboardInterrupt:
    print("\nStopping camera test...")

finally:
    vision.stop()