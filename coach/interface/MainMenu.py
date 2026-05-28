import os
import sys
from sys import path

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from VoiceWorker import VoiceWorker

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

    # Konfiguracja przycisków
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
        # Ładowanie pliku .ui
        super().__init__()
        ui_path = f"{os.path.dirname(__file__)}/ui/main_menu.ui"
        loader = QUiLoader()
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Nie można otworzyć pliku: {ui_path}")
            sys.exit(-1)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setWindowTitle("Menu główne")
        loadImages(self) # ładowanie obrazków
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


    # TODO Obsługa przycisków otwierających poszczególne okienka oraz realizująca ich funkcje w mainie
    pass

    # obsługa przycisków oraz funkcji okienka
    def startTraining(self):
        pass

    def settings(self):
        pass

    def stats(self):
        pass

    def calendar(self):
        pass

    def tutorial(self):
        pass

    def profileSelection(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainMenu()
    window.show()

    sys.exit(app.exec())
