import cv2

from config import (
    FRAME_WIDTH,
    FRAME_HEIGHT,
    OBJECT_NEAR_AREA,
    OBJECT_MID_AREA,
    PERSON_NEAR_AREA,
    MIN_OBJECT_AREA,
    PERSON_CONFIDENCE_THRESHOLD,
)

try:
    from picamera2 import Picamera2
    PICAMERA2_AVAILABLE = True
except Exception:
    PICAMERA2_AVAILABLE = False


class VisionSystem:
    def __init__(self, show_preview: bool = False):
        self.show_preview = show_preview
        self.picam2 = None
        self.cap = None

        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def start(self) -> None:
        if PICAMERA2_AVAILABLE:
            self.picam2 = Picamera2()
            config = self.picam2.create_preview_configuration(
                main={"size": (FRAME_WIDTH, FRAME_HEIGHT), "format": "RGB888"}
            )
            self.picam2.configure(config)
            self.picam2.start()
        else:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    def stop(self) -> None:
        if self.picam2 is not None:
            self.picam2.stop()
        if self.cap is not None:
            self.cap.release()
        if self.show_preview:
            cv2.destroyAllWindows()

    def get_frame(self):
        if self.picam2 is not None:
            return self.picam2.capture_array()
        if self.cap is not None:
            ok, frame = self.cap.read()
            if ok:
                return frame
        return None

    def detect_primary_target(self, frame):
        if frame is None:
            return None

        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

        person = self._detect_person(frame)
        if person is not None:
            person["distance"] = self._distance_from_area(person["area"], is_person=True)
            if self.show_preview:
                self._draw_box(frame, person["bbox"], "person")
                cv2.imshow("preview", frame)
                cv2.waitKey(1)
            return person

        obj = self._detect_object(frame)
        if obj is not None:
            obj["distance"] = self._distance_from_area(obj["area"], is_person=False)
            if self.show_preview:
                self._draw_box(frame, obj["bbox"], "object")
                cv2.imshow("preview", frame)
                cv2.waitKey(1)
            return obj

        if self.show_preview:
            cv2.imshow("preview", frame)
            cv2.waitKey(1)
        return None

    def _detect_person(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        boxes, weights = self.hog.detectMultiScale(
            gray,
            winStride=(8, 8),
            padding=(8, 8),
            scale=1.05,
        )

        if len(boxes) == 0:
            return None

        best = None
        best_area = 0

        for (x, y, w, h), weight in zip(boxes, weights):
            score = float(weight)
            area = w * h
            if score < PERSON_CONFIDENCE_THRESHOLD:
                continue
            if area > best_area:
                best_area = area
                best = {
                    "label": "person",
                    "bbox": (x, y, w, h),
                    "confidence": score,
                    "area": area,
                }

        return best

    def _detect_object(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        height, width = gray.shape
        best = None
        best_area = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < MIN_OBJECT_AREA:
                continue

            x, y, bw, bh = cv2.boundingRect(cnt)
            box_area = bw * bh

            if box_area < MIN_OBJECT_AREA:
                continue

            # Ignore tiny clutter high in the image.
            if y + bh < int(height * 0.35):
                continue

            if box_area > best_area:
                best_area = box_area
                best = {
                    "label": "object",
                    "bbox": (x, y, bw, bh),
                    "confidence": 1.0,
                    "area": box_area,
                }

        return best

    def _distance_from_area(self, area: int, is_person: bool = False) -> str:
        if is_person:
            if area >= PERSON_NEAR_AREA:
                return "near"
            return "mid"

        if area >= OBJECT_NEAR_AREA:
            return "near"
        if area >= OBJECT_MID_AREA:
            return "mid"
        return "far"

    def _draw_box(self, frame, bbox, label: str) -> None:
        x, y, w, h = bbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            label,
            (x, max(20, y - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )
