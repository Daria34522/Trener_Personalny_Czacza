import sys
from sys import path

from PySide6.QtMultimedia import QCamera, QMediaCaptureSession
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QDate


class Stats(QMainWindow):
    def __init__(self):
        # Ładowanie pliku .ui
        super().__init__()
        ui_path = "ui/Stats_menu.ui"
        loader = QUiLoader()
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Nie można otworzyć pliku: {ui_path}")
            sys.exit(-1)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setWindowTitle("Statystyki")
        self.showMaximized()

        # Data domyślna
        self.ui.From_date.setDate(QDate.currentDate())
        self.ui.Until_date.setDate(QDate.currentDate())

        # TODO Wpisanie nazwy użytkownika w pole 'Zalogowany użytkownik:' oraz statystyk ogólnych
        self.userNameAndGeneralStatistic()

        # Łączenie przycisków z metodami
        self.ui.Draw_graph.clicked.connect(self.drawGraph)
        self.ui.Selected_date.selectionChanged.connect(self.displayDayStats)
        self.ui.Main_menu.clicked.connect(self.backToMainMenu) # Menu główne

    # Daty pobrane z ui zapisane są w tablicy posiadającej 3 elementy typu String tj. dzień, miesiąc, rok
    def drawGraph(self):
        first_date = self.ui.From_date.text().split(".")
        second_date = self.ui.Until_date.text().split(".")
        # TODO pobranie danych z bazy oraz narysowanie wykresu
        pass

    def displayDayStats(self):
        date = self.ui.Selected_date.selectedDate().toString("dd-MM-yyyy").split("-")
        # TODO pobranie danych z bazy oraz wyświetlenie danych
        pass

    def userNameAndGeneralStatistic(self):
        self.ui.Logged_user.setText("xyz") # Nazwa użytkownika
        self.ui.Exercise_time.setText("xyz") # Czas ćwiczeń

    def backToMainMenu(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Stats()
    window.show()

    sys.exit(app.exec())