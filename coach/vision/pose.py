import os
import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks import python

MODEL_PATH = os.path.join(os.path.dirname(__file__), "pose_landmarker_heavy.task")


class PoseDetector:
    def __init__(self):
        self._base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
        self._options = vision.PoseLandmarkerOptions(
            base_options=self._base_options,
            running_mode=vision.RunningMode.VIDEO,
            output_segmentation_masks=True,
        )
        self.detector = vision.PoseLandmarker.create_from_options(self._options)

    def detect(self, frame: cv2.typing.MatLike, timestamp: int):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        result = self.detector.detect_for_video(mp_image, timestamp)
        return result


class PoseDrawer:
    def __init__(self, draw_indices: bool = True):
        self.draw_indices = draw_indices

        self.connections = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 7),
            (0, 4),
            (4, 5),
            (5, 6),
            (6, 8),
            (9, 10),
            (11, 12),
            (11, 13),
            (13, 15),
            (12, 14),
            (14, 16),
            (11, 23),
            (12, 24),
            (23, 24),
            (23, 25),
            (25, 27),
            (27, 29),
            (29, 31),
            (24, 26),
            (26, 28),
            (28, 30),
            (30, 32),
        ]

        self.important_points = {
            # fmt: off
            23, 24,  # biodra
            25, 26,  # kolana
            27, 28,  # kostki
            31, 32,  # stopy
        }  # fmt: on

    def draw(self, frame: cv2.typing.MatLike, result):
        if not result.pose_landmarks:
            return frame

        h, w, _ = frame.shape
        landmarks = result.pose_landmarks[0]

        for idx, lm in enumerate(landmarks):
            x, y = int(lm.x * w), int(lm.y * h)

            if idx in self.important_points:
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)

            cv2.circle(frame, (x, y), 4, color, -1)

        for start_idx, end_idx in self.connections:
            s = landmarks[start_idx]
            e = landmarks[end_idx]

            x1, y1 = int(s.x * w), int(s.y * h)
            x2, y2 = int(e.x * w), int(e.y * h)

            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        return frame
