import os
import sys
from sys import path

from PySide6.QtMultimedia import QCamera, QMediaCaptureSession
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QDate
from VoiceWorker import VoiceWorker

class Stats(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        ui_path = f"{os.path.dirname(__file__)}/ui/Stats_menu.ui"
        loader = QUiLoader()
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Nie można otworzyć pliku: {ui_path}")
            sys.exit(-1)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setWindowTitle("Statystyki")

        # Data domyślna
        self.ui.From_date.setDate(QDate.currentDate())
        self.ui.Until_date.setDate(QDate.currentDate())

        self.userNameAndGeneralStatistic()

        # Łączenie przycisków z metodami
        self.ui.Draw_graph.clicked.connect(self.drawGraph)
        self.ui.Selected_date.selectionChanged.connect(self.displayDayStats)
        self.ui.Main_menu.clicked.connect(self.backToMainMenu) # Menu główne
        self.voice = VoiceWorker()
        self.voice.play("Oto twoje statystyki")

    # Daty pobrane z ui zapisane są w tablicy posiadającej 3 elementy typu String tj. dzień, miesiąc, rok
    def drawGraph(self):
        first_date = self.ui.From_date.text().split(".")
        second_date = self.ui.Until_date.text().split(".")
        # TODO pobranie danych z bazy oraz narysowanie wykresu
        pass

    def displayDayStats(self):
        date = self.ui.Selected_date.selectedDate().toString("dd-MM-yyyy").split("-")
        print(date)
        # TODO pobranie danych z bazy oraz wyświetlenie danych
        pass

    def userNameAndGeneralStatistic(self):
        # TODO Pobranie z bazy danych
        self.ui.Logged_user.setText("xyz")  # Nazwa użytkownika
        self.ui.Exercise_time.setText("xyz")  # Czas ćwiczeń

    def setProfile(self, user):
        self.user_id = user

    def backToMainMenu(self):
        self.parent().setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Stats()
    window.show()

    sys.exit(app.exec())
