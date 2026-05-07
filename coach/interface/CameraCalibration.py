import sys
from sys import path
import os

from PySide6.QtMultimedia import QCamera, QMediaCaptureSession
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtCore import QThread

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from voice_control.voice_control import Speaker, Listener


def setup_camera_display(container, video_widget, session, camera): # 'Wrzucenie' obrazu z kamery do ui
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(video_widget)
    session.setCamera(camera)
    session.setVideoOutput(video_widget)

class VoiceWorker(QThread):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.filename = ""

    def say(self, text, filename="example"):
        self.text = text
        self.filename = filename
        if not self.isRunning():
            self.start()
    def run(self):
        speaker = Speaker(voice_filename = self.filename)
        speaker.gen_speak(self.text)
        speaker.speak()
        speaker.delete_file()


class CameraCalibration(QMainWindow):
    def __init__(self):
        # Ładowanie pliku .ui
        super().__init__()
        ui_path = "ui/camera_calibration_menu.ui"
        loader = QUiLoader()
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Nie można otworzyć pliku: {ui_path}")
            sys.exit(-1)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setWindowTitle("Menu kalibracji kamery")

        # Ustawienie stałego rozmiaru okienka
        # TODO Do przetestowania czy chcemy mieć kamerki 16:9 czy 4:3 oraz dopasowanie do tego interfejsu
        self.ui.Camera_front.setFixedSize(640, 480)
        self.ui.Camera_side.setFixedSize(640, 480)

        # TODO Sprawdzene czy mamy podłączone dwie kamerki oraz 'pobranie' obrazu pozwalającego na wyświetlenie w ui LUB przekazanie 'kamer' w konstruktorze do klasy i sprawdzenie czy działają w mainie
        pass

        # TODO Konfiguracja obrazu z kamery przedniej
        self.camera1 = QCamera() # obraz z kamerki
        self.session1 = QMediaCaptureSession()
        self.view1 = QVideoWidget()
        setup_camera_display(self.ui.Camera_front, self.view1, self.session1, self.camera1)

        # TODO Konfiguracja obrazu z kamery z boku
        self.camera2 = QCamera() # obraz z kamerki
        self.session2 = QMediaCaptureSession()
        self.view2 = QVideoWidget()
        setup_camera_display(self.ui.Camera_side, self.view2, self.session2, self.camera2)
        self.voice = VoiceWorker()
        self.voice.say("Ustaw się tak abyś na obu widokach kamery był cały widoczny")


    def messageToUser(self, message): # metoda pozwala wyświetlić komunikat dla użytkownika w polu 'Informacje' np. o niepoprawnym ustawieniu kamery
        self.ui.Message_from_app.setText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = CameraCalibration()
    window.show()
    sys.exit(app.exec())