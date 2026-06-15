import os
import sys
from sys import path

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from database.DBHandler import DBHandler


from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QBarSet,
    QBarSeries,
    QBarCategoryAxis,
    QValueAxis,
)
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QDate
from PySide6.QtWidgets import QFormLayout, QLabel, QVBoxLayout, QWidget

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
        self.ui.Main_menu.clicked.connect(self.backToMainMenu)  # Menu główne

    def check_user(self):
        if self.user_id == -1:
            QMessageBox.warning(
                self, "Nie wybrane konto", "Wybierz konto aby zobaczzyć statystyki"
            )
            return False
        return True

    # Daty pobrane z ui zapisane są w tablicy posiadającej 3 elementy typu String tj. dzień, miesiąc, rok
    def drawGraph(self):
        if not self.check_user():
            return
        first_date = self.ui.From_date.text().split(".")
        second_date = self.ui.Until_date.text().split(".")
        first_date = first_date[2] + "-" + first_date[1] + "-" + first_date[0]
        second_date = second_date[2] + "-" + second_date[1] + "-" + second_date[0]

        db.get_a_user(self.user_id)
        info = db.get_statistics_between_dates(self.user_id, first_date, second_date)

        bar_set = QBarSet("Czas treningu")

        kategorie_dat = []
        max_minuty = 0

        for row in info:
            data_str, sekundy = row
            minuty = int(float(sekundy) / 60)
            bar_set.append(minuty)

            try:
                from datetime import datetime

                dt = datetime.strptime(data_str, "%Y-%m-%d")
                ladna_data = dt.strftime("%d.%m.%Y")
            except:
                ladna_data = data_str

            kategorie_dat.append(ladna_data)

            if minuty > max_minuty:
                max_minuty = minuty

        seria = QBarSeries()
        seria.append(bar_set)

        wykres = QChart()
        wykres.addSeries(seria)
        wykres.setTitle("Ilość przećwiczonych minut w danym dniu")
        wykres.setAnimationOptions(QChart.SeriesAnimations)

        axis_x = QBarCategoryAxis()
        axis_x.append(kategorie_dat)
        axis_x.setTitleText("Data")
        wykres.addAxis(axis_x, Qt.AlignBottom)
        seria.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setTitleText("Minuty")
        axis_y.setLabelFormat("%i")
        axis_y.setRange(0, max_minuty + 10)  # Margines na górze
        wykres.addAxis(axis_y, Qt.AlignLeft)
        seria.attachAxis(axis_y)

        if not self.ui.Graph_frame.layout():
            layout = QVBoxLayout(self.ui.Graph_frame)
            layout.setContentsMargins(0, 0, 0, 0)
        else:
            layout = self.ui.Graph_frame.layout()

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        widok_wykresu = QChartView(wykres)
        widok_wykresu.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(widok_wykresu)
        pass

    def displayDayStats(self):
        date = self.ui.Selected_date.selectedDate().toString("yyyy-MM-dd")
        # TODO pobranie danych z bazy oraz wyświetlenie danych
        info = db.get_statistics_from_date(self.user_id, date)
        old_layout = self.ui.Day_stats.layout()
        if old_layout is not None:
            while old_layout.count():
                item = old_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            QWidget().setLayout(old_layout)

        if not info:
            layout = QVBoxLayout()
            if self.user_id == -1:
                no_data_lbl = QLabel("Wybierz konto aby zobaczyć statystyki")
            else:
                no_data_lbl = QLabel("Brak statystyk dla wybranego dnia.")
            no_data_lbl.setStyleSheet("font-style: italic; color: #7f8c8d;")
            layout.addWidget(no_data_lbl)
            self.ui.Day_stats.setLayout(layout)
            return

        (
            repetitions,
            duration_seconds,
            comment,
            tempo,
            step_accuracy,
            posture,
        ) = info[0]

        minutes = duration_seconds // 60
        seconds = duration_seconds % 60
        time_str = f"{minutes}m {seconds:02d}s"

        layout = QFormLayout()
        layout.setSpacing(10)

        label_style = "font-weight: bold; color: #2c3e50; font-size: 15px;"
        value_style = "color: #34495e; font-size: 15px;"

        def add_stat_row(label_text, value_text):
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            val = QLabel(str(value_text))
            val.setStyleSheet(value_style)
            val.setWordWrap(True)
            layout.addRow(lbl, val)

        add_stat_row("Liczba powtórzeń:", repetitions)
        add_stat_row("Czas trwania:", time_str)
        add_stat_row("Tempo:", tempo)
        add_stat_row("Precyzja kroków:", step_accuracy)
        add_stat_row("Postawa:", posture)

        comment_lbl = QLabel(f"*{comment}*")
        comment_lbl.setStyleSheet(
            "color: #0096FF; font-weight: bold; font-size: 17px; margin-top: 12px;"
        )
        comment_lbl.setWordWrap(True)
        layout.addRow(comment_lbl)
        self.ui.Day_stats.setLayout(layout)

    def userNameAndGeneralStatistic(self):
        if self.user_id == -1:
            self.ui.Logged_user.setText("Nie wybrano konta")
            self.ui.Exercise_time.setText("Wybierz konto aby zobaczyć czas")
            return
        username = db.get_a_user(self.user_id)
        self.ui.Logged_user.setText(username)  # Nazwa użytkownika
        total = db.get_exercise_duration(self.user_id) / 60
        self.ui.Exercise_time.setText(str(total) + " min.")  # Czas ćwiczeń

    def setProfile(self, user):
        self.user_id = user
        self.userNameAndGeneralStatistic()
        self.displayDayStats()

    def backToMainMenu(self):
        self.parent().setCurrentIndex(0)
        self.main_window.voice.stop_playing()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Stats()
    window.show()

    sys.exit(app.exec())
