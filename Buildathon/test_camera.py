from picamera2 import Picamera2
import cv2
import time

picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)
picam2.configure(config)
picam2.start()

time.sleep(1)

try:
    print("Camera preview running... press q to quit")
    while True:
        frame = picam2.capture_array()
        cv2.imshow("Pi Camera Preview", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    pass

finally:
    cv2.destroyAllWindows()
    picam2.stop()