from __future__ import annotations

from dataclasses import dataclass

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from coach.vision.constants import MODEL_PATH


class PoseDetector:
    def __init__(self, result_callback):
        self._base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
        self._options = vision.PoseLandmarkerOptions(
            base_options=self._base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=result_callback,
            num_poses=1,
            min_pose_detection_confidence=0.55,
            min_pose_presence_confidence=0.55,
            min_tracking_confidence=0.55,
        )
        self.detector = vision.PoseLandmarker.create_from_options(self._options)

    def detect(self, frame: cv2.typing.MatLike, timestamp: int):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        try:
            result = self.detector.detect_async(mp_image, timestamp)
        except Exception:
            result = None
        return result


@dataclass
class SmoothedPoseResult:
    x: float
    y: float
    z: float
    visibility: float


class PoseLandmarkSmoother:
    def __init__(self, alpha: float = 0.5):
        self.alpha = alpha  # 0.1=bardzo gładko, 0.9=prawie surowo
        self._prev = None

    def smooth(self, landmarks) -> list[SmoothedPoseResult]:
        if landmarks is None:
            self._prev = None
            return []

        if self._prev is None:
            self._prev = [(lm.x, lm.y, lm.z, lm.visibility) for lm in landmarks]
            return [
                SmoothedPoseResult(x, y, z, visibility)
                for x, y, z, visibility in self._prev
            ]

        smoothed = []
        for i, lm in enumerate(landmarks):
            px, py, pz, p_visibility = self._prev[i]
            sx = self.alpha * lm.x + (1 - self.alpha) * px
            sy = self.alpha * lm.y + (1 - self.alpha) * py
            sz = self.alpha * lm.z + (1 - self.alpha) * pz
            self._prev[i] = (sx, sy, sz, p_visibility)
            smoothed.append(SmoothedPoseResult(sx, sy, sz, p_visibility))

        return smoothed


class PoseDrawer:
    def __init__(self):
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
        self.important_points = frozenset({23, 24, 25, 26, 27, 28, 31, 32})

    def draw(self, frame, landmarks, pose_frame: bool = False):
        if landmarks is None:
            return frame

        h, w, _ = frame.shape

        # Liczenie współrzędnych.
        pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

        # Rysowanie połączeń
        for s, e in self.connections:
            cv2.line(frame, pts[s], pts[e], (255, 0, 0), 2)

        # Rysowanie punktów.
        for idx, pt in enumerate(pts):
            color = (0, 0, 255) if idx in self.important_points else (0, 255, 0)
            cv2.circle(frame, pt, 4, color, -1)

        if pose_frame:
            # Rysowanie ramki w srodku kamery gdzie użytkownik powinien się mieścić, takie 80% szerokości i 100% wysokości
            cv2.rectangle(
                frame,
                (int(w * 0.1), int(h * 0.1)),
                (int(w * 0.9), int(h * 0.9)),
                (255, 255, 255),
                2,
            )

        return frame
