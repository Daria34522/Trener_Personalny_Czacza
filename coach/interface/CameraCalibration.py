from __future__ import annotations

import os
import sys
import threading
import time
import numpy as np
from PySide6.QtMultimedia import (
    QCamera,
    QMediaCaptureSession,
    QMediaDevices,
    QVideoSink,
)
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Slot, Qt, QObject, Signal
from PySide6.QtGui import QImage, QPixmap

from coach.vision.pose import PoseDetector, PoseLandmarkSmoother, PoseDrawer
from coach.vision.constants import Issues
from coach.vision.errors import ErrorDetector
from coach.vision.analysis.quality import QualityReport
from coach.vision.analysis.quality import analyze_front, analyze_side

from coach.interface.VoiceWorker import VoiceWorker


class AtomicBoolean:
    def __init__(self, initial: bool = False):
        self._lock = threading.Lock()
        self.value = initial

    def toggle(self):
        with self._lock:
            self.value = not self.value

    def get(self) -> bool:
        with self._lock:
            return self.value


class PoseWorker(QObject):
    image_processed = Signal(QImage)
    quality_result = Signal(QualityReport)

    def __init__(self, direction: str = "front"):
        super().__init__()
        self.detector = PoseDetector(result_callback=self.on_pose_result)
        self.smoother = PoseLandmarkSmoother(alpha=0.3)
        self.drawer = PoseDrawer()
        self.user_calibration = AtomicBoolean(True)
        self.direction = direction
        self.last_frame = None

    def on_pose_result(self, result, output_image, timestamp_ms):
        if self.last_frame is None:
            return

        if not len(result.pose_landmarks):
            return

        landmarks = self.smoother.smooth(result.pose_landmarks[0])
        if self.direction == "front":
            result = analyze_front(landmarks)
        else:
            result = analyze_side(landmarks)

        self.quality_result.emit(result)

        processed = self.drawer.draw(
            self.last_frame.copy(), landmarks, self.user_calibration.get()
        )
        h, w, ch = processed.shape
        q_img = QImage(processed.data, w, h, ch * w, QImage.Format.Format_RGB888)
        self.image_processed.emit(q_img.copy())

    @Slot(np.ndarray)
    def process_frame(self, frame):
        self.last_frame = frame
        self.detector.detect(frame, int(time.time() * 1000))


class CameraCalibration(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = f"{os.path.dirname(__file__)}/ui/camera_calibration_menu.ui"
        loader = QUiLoader()
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Nie można otworzyć pliku: {ui_path}")
            sys.exit(-1)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Menu kalibracji kamery")
        self.voice = VoiceWorker()

        self.ui.Camera_front.setFixedSize(480, 640)
        self.ui.Camera_side.setFixedSize(480, 640)

        self.worker_front = PoseWorker("front")
        self.worker_front.image_processed.connect(self.update_display_front)
        self.worker_front.quality_result.connect(self.handle_report)

        self.worker_side = PoseWorker("side")
        self.worker_side.image_processed.connect(self.update_display_side)
        self.worker_side.quality_result.connect(self.handle_report)

        self.error_detector = ErrorDetector(
            window_size=60, threshold=20, cooldown_frames=240
        )

        self.label_front = QLabel()
        self.label_side = QLabel()
        self.setup_camera_ui(self.ui.Camera_front, self.label_front)
        self.setup_camera_ui(self.ui.Camera_side, self.label_side)

        cameras = QMediaDevices.videoInputs()
        if len(cameras) < 2:
            msg = "Nie wykryto dwóch kamer. Podłącz dwie kamery i uruchom ponownie."
            self.messageToUser(msg)
            # TODO: nowe komunikaty głosowe dla użytkownika
            # self.voice.say(msg)
            return

        self.camera1 = QCamera(cameras[2])  # obraz z kamerki
        self.session1 = QMediaCaptureSession()
        self.sink1 = QVideoSink()
        self.session1.setCamera(self.camera1)
        self.session1.setVideoSink(self.sink1)
        self.sink1.videoFrameChanged.connect(self.handle_camera_frame_front)

        self.camera2 = QCamera(cameras[1])  # obraz z kamerki
        self.session2 = QMediaCaptureSession()
        self.sink2 = QVideoSink()
        self.session2.setCamera(self.camera2)
        self.session2.setVideoSink(self.sink2)
        self.sink2.videoFrameChanged.connect(self.handle_camera_frame_side)

        self.camera1.start()
        self.camera2.start()

    def setup_camera_ui(self, container, label):
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label)

    def handle_camera_frame_front(self, frame):
        if not frame.isValid():
            return
        img = frame.toImage().convertToFormat(QImage.Format.Format_RGB888)
        ptr = img.bits()
        arr = (
            np.frombuffer(ptr, np.uint8).reshape((img.height(), img.width(), 3)).copy()
        )
        self.worker_front.process_frame(arr)

    def handle_camera_frame_side(self, frame):
        if not frame.isValid():
            return
        img = frame.toImage().convertToFormat(QImage.Format.Format_RGB888)
        ptr = img.bits()
        arr = (
            np.frombuffer(ptr, np.uint8).reshape((img.height(), img.width(), 3)).copy()
        )
        self.worker_side.process_frame(arr)

    def handle_report(self, report: QualityReport):
        self.error_detector.update(report.issues)

        alerts = self.error_detector.show_alerts()
        for issue in alerts:
            ...
            # TODO: Komunikaty głosowe dla użytkownika, 3 kropki do usunięcia jak kod zostanie dodany
            # self.voice.say(Issues.to_polish(issue))

        active = self.error_detector.get_active_errors()
        self.messageToUser("\n".join(Issues.to_polish_list(active)))

    @Slot(QImage)
    def update_display_front(self, q_img):
        pixmap = QPixmap.fromImage(q_img)
        self.label_front.setPixmap(
            pixmap.scaled(self.label_front.size(), Qt.AspectRatioMode.KeepAspectRatio)
        )

    @Slot(QImage)
    def update_display_side(self, q_img):
        pixmap = QPixmap.fromImage(q_img)
        self.label_side.setPixmap(
            pixmap.scaled(self.label_side.size(), Qt.AspectRatioMode.KeepAspectRatio)
        )

    def messageToUser(
        self, message
    ):  # metoda pozwala wyświetlić komunikat dla użytkownika w polu 'Informacje' np. o niepoprawnym ustawieniu kamery
        self.ui.Message_from_app.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraCalibration()
    window.show()
    sys.exit(app.exec())
