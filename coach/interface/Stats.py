import os
import sys
from sys import path

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from database.DBHandler import DBHandler

from datetime import datetime
from PySide6.QtMultimedia import QCamera, QMediaCaptureSession
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QDate
from PySide6.QtCore import QDateTime, Qt
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtGui import QPainter
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from VoiceWorker import VoiceWorker

db_path = os.path.join(parent_dir, "database/db.sqlite")
db = DBHandler(db_path)

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

        self.user_id = -1

        # Data domyślna
        self.ui.From_date.setDate(QDate.currentDate())
        self.ui.Until_date.setDate(QDate.currentDate())

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
        first_date = first_date[2] + "-" + first_date[1] + "-" + first_date[0]
        second_date = second_date[2] + "-" + second_date[1] + "-" + second_date[0]
        # TODO pobranie danych z bazy oraz narysowanie wykresu
        db.get_a_user(self.user_id)
        info = db.get_statistics_between_dates(self.user_id, first_date, second_date)

        # RYSOWANIE WYKRESU
        seria = QLineSeries()
        seria.setName("Czas treningu (minuty)")
        max_minuty = 0
        for row in info:
            data_str, sekundy = row
            minuty = int(float(sekundy) / 60)
            dt = datetime.strptime(data_str, "%Y-%m-%d")
            q_dt = QDateTime(dt.year, dt.month, dt.day, 0, 0)
            seria.append(q_dt.toMSecsSinceEpoch(), minuty)
            if minuty > max_minuty:
                max_minuty = minuty
        wykres = QChart()
        wykres.addSeries(seria)
        wykres.setTitle("Ilość przećwiczonych minut w danym dniu")

        # 5. Konfiguracja osi X (Oś czasu)
        axis_x = QDateTimeAxis()
        axis_x.setFormat("dd.MM.yyyy")  # Format wyświetlania daty na wykresie
        axis_x.setTitleText("Data")
        axis_x.setTickCount(max(2, min(len(info), 5)))  # Dynamiczna liczba znaczników (od 2 do 5), żeby uniknąć tłoku
        wykres.addAxis(axis_x, Qt.AlignBottom)
        seria.attachAxis(axis_x)

        # 6. Konfiguracja osi Y (Oś wartości - minuty)
        axis_y = QValueAxis()
        axis_y.setTitleText("Minuty")
        axis_y.setLabelFormat("%i")  # Wyświetlanie jako liczby całkowite
        # Ustawiamy zakres od 0 do max_minuty + 10 minut marginesu na górze
        axis_y.setRange(0, max_minuty + 10)
        wykres.addAxis(axis_y, Qt.AlignLeft)
        seria.attachAxis(axis_y)

        # 7. Przygotowanie layoutu wewnątrz Graph_frame
        if not self.ui.Graph_frame.layout():
            layout = QVBoxLayout(self.ui.Graph_frame)
            layout.setContentsMargins(0, 0, 0, 0)  # Wykres idealnie wypełni ramkę
        else:
            layout = self.ui.Graph_frame.layout()

        # 8. Czyszczenie poprzedniego wykresu z layoutu ramki
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 9. Tworzenie nowego widoku wykresu i dodanie go do UI
        widok_wykresu = QChartView(wykres)
        widok_wykresu.setRenderHint(QPainter.Antialiasing)  # Wygładzanie linii wykresu

        layout.addWidget(widok_wykresu)
        pass

    def displayDayStats(self):
        date = self.ui.Selected_date.selectedDate().toString("yyyy-MM-dd")
        # TODO pobranie danych z bazy oraz wyświetlenie danych
        info = db.get_statistics_from_date(self.user_id, date)
        print(info)
        pass

    def userNameAndGeneralStatistic(self):
        username = db.get_a_user(self.user_id)
        self.ui.Logged_user.setText(username)  # Nazwa użytkownika
        total = db.get_exercise_duration(self.user_id) / 60
        self.ui.Exercise_time.setText(str(total) + " min.")  # Czas ćwiczeń

    def setProfile(self, user):
        self.user_id = user
        self.userNameAndGeneralStatistic()

    def backToMainMenu(self):
        self.parent().setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Stats()
    window.show()

    sys.exit(app.exec())
