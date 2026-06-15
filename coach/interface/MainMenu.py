import os
import sys
from sys import path

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from database.DBHandler import DBHandler

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from VoiceWorker import VoiceWorker

from coach.interface.CalendarMenu import CalendarMenu
from coach.interface.CameraCalibration import CameraCalibration
from coach.interface.ProfileWindow import ProfileWindow
from coach.interface.Settings import Settings
from coach.interface.Stats import Stats
from coach.interface.TutorialMenu import TutorialMenu

db_path = os.path.join(parent_dir, "database/db.sqlite")
db = DBHandler(db_path)

def loadImages(Window):
    menu_button_style = """
        QPushButton {
            background-color: #f8f9fa;
            border: 2px solid #dee2e6;
            border-radius: 20px;
            padding: 50px;
            outline: none;
        }

        QPushButton:hover {
            background-color: #e9ecef;
            border: 2px solid #00ff00;
        }

        QPushButton:pressed {
            background-color: #d1d4d7;
        }
    """

    buttons = {
        Window.ui.Start_training: "assets/icons/dancestart.png",
        Window.ui.Settings: "assets/icons/settings.png",
        Window.ui.Stats: "assets/icons/statistics.png",
        Window.ui.Calendar: "assets/icons/calendar.png",
        Window.ui.Tutorial: "assets/icons/recommendations.png",
        Window.ui.Profile_selection: "assets/icons/profile.png"
    }

    from PySide6.QtGui import QIcon
    from PySide6.QtCore import QSize

    for btn, icon_path in buttons.items():
        btn.setStyleSheet(menu_button_style)
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(128, 128))
        btn.setText("")

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget() # Stackowanie okienek
        self.setCentralWidget(self.stacked_widget)

        ui_path = f"{os.path.dirname(__file__)}/ui/main_menu.ui"
        loader = QUiLoader()
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Nie można otworzyć pliku: {ui_path}")
            sys.exit(-1)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setWindowTitle("Trener")
        loadImages(self) # ładowanie obrazków

        # TODO Dane użytkownika
        self.user_id = -1
        self.song_id = db.get_random_song()

        # Obiekty okienek
        self.stacked_widget.addWidget(self.ui)
        self.settings_window = Settings(self)
        self.calendar_window = CalendarMenu(self)
        self.camera_window = CameraCalibration(self)
        self.profile_window = ProfileWindow(self)
        self.stats_window = Stats(self)
        self.tutorial_window = TutorialMenu(self)

        self.stacked_widget.addWidget(self.settings_window)
        self.stacked_widget.addWidget(self.calendar_window)
        self.stacked_widget.addWidget(self.camera_window)
        self.stacked_widget.addWidget(self.profile_window)
        self.stacked_widget.addWidget(self.stats_window)
        self.stacked_widget.addWidget(self.tutorial_window)

        self.stacked_widget.setCurrentWidget(self.ui)

        self.showMaximized()

        # Łączenie przycisków z metodami
        self.ui.Start_training.clicked.connect(self.startTraining)
        self.ui.Settings.clicked.connect(self.settings)
        self.ui.Stats.clicked.connect(self.stats)
        self.ui.Calendar.clicked.connect(self.calendar)
        self.ui.Tutorial.clicked.connect(self.tutorial)
        self.ui.Profile_selection.clicked.connect(self.profileSelection)
        self.voice = VoiceWorker()
        self.voice.play("Witaj w asystencie czaczy. Wybierz co chcesz zrobić")


    # obsługa przycisków oraz funkcji okienka
    def startTraining(self):
        self.camera_window.refresh_cameras()
        self.stacked_widget.setCurrentWidget(self.camera_window)

    def settings(self):
        self.stacked_widget.setCurrentWidget(self.settings_window)
        self.voice.play("Wybierz piosenkę d której chcesz ćwiczyć")

    def stats(self):
        self.stats_window.setProfile(self.user_id)
        self.stacked_widget.setCurrentWidget(self.stats_window)
        self.voice.play("Oto twoje statystyki")

    def calendar(self):
        self.calendar_window.setProfile(self.user_id)
        self.stacked_widget.setCurrentWidget(self.calendar_window)
        self.voice.play("Witaj w kalendarzu, możesz tu zaplanowć swoje treningi")

    def tutorial(self):
        self.stacked_widget.setCurrentWidget(self.tutorial_window)

    def profileSelection(self):
        self.stacked_widget.setCurrentWidget(self.profile_window)

    def loggedUser(self, user):
        self.user_id = user
        print(self.user_id)

    def selectedSong(self, song):
        self.song_id = song
        print(self.song_id)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainMenu()
    window.show()

    sys.exit(app.exec())
