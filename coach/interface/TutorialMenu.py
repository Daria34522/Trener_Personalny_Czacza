import sys
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget  # Prawdziwa klasa wideo


class TutorialMenu(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        ui_path = "ui/TutorialMenu.ui"
        loader = QUiLoader()
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Nie można otworzyć pliku: {ui_path}")
            sys.exit(-1)

        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setCentralWidget(self.ui)

        self.real_video_widget = QVideoWidget()
        video_layout = QVBoxLayout(self.ui.video_widget)
        video_layout.setContentsMargins(0, 0, 0, 0)
        video_layout.addWidget(self.real_video_widget)

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.real_video_widget)

        self.setWindowTitle("Film instruktażowy")

        # łączenie przycisków z metodami
        self.ui.btn_play.clicked.connect(self.toggle_play)
        self.ui.Main_menu.clicked.connect(self.backToMainMenu)

        # obsługa wideo
        self.player.positionChanged.connect(lambda p: self.ui.video_slider.setValue(int(p)))
        self.player.durationChanged.connect(lambda d: self.ui.video_slider.setRange(0, int(d)))
        self.ui.video_slider.sliderMoved.connect(self.player.setPosition)

        # obsługa głośności
        self.audio_output.setVolume(0.5)
        self.ui.volume_slider.setValue(50)
        self.ui.volume_slider.valueChanged.connect(self.change_volume)

        self.player.setSource(QUrl.fromLocalFile("tutorial/tut.mp4")) # Ładowanie pliku mp4

        # Czekanie na załadowanie pliku i odpalenie pierwszej klatki
        time.sleep(0.2)
        self.player.play()
        self.player.pause()

    def toggle_play(self):
        # Logika odtwarzania/pauzy dostosowana do PySide6
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def change_volume(self, value):
        float_volume = value / 100.0
        self.audio_output.setVolume(float_volume)

    def backToMainMenu(self):
        self.parent().setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TutorialMenu()
    window.show()
    sys.exit(app.exec())