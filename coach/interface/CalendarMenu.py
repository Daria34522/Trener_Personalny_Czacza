from __future__ import annotations

import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from database.DBHandler import DBHandler

from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QFrame,
    QHBoxLayout,
    QMessageBox,
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QDate

db_path = os.path.join(parent_dir, "database/db.sqlite")
db = DBHandler(db_path)


class CalendarMenu(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        ui_path = f"{os.path.dirname(__file__)}/ui/Calendar_menu.ui"
        loader = QUiLoader()
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Nie można otworzyć pliku: {ui_path}")
            sys.exit(-1)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.user_id = -1  # ID użytkownika

        self.setWindowTitle("Plan treningowy")

        # Podpinanie metod pod przyciski
        self.ui.Add_entry.clicked.connect(self.addEntry)
        self.ui.Calendar1.clicked.connect(self.selectedDate)
        self.ui.Main_menu.clicked.connect(self.backToMainMenu)  # Menu główne

    def loadTrainingList(self):  # Pokazanie całej listy treningowej
        layout = self.ui.scrollAreaWidgetContents.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Zabezpieczenie przed brakiem konta na liście
        if self.user_id == -1:
            row_widget = QFrame()
            row_layout = QHBoxLayout(row_widget)
            lbl = QLabel("Wybierz konto, aby zobaczyć listę planów.")
            lbl.setStyleSheet(
                "font-style: italic; color: #e74c3c; font-weight: bold; border: none;",
            )
            row_layout.addWidget(lbl)
            layout.addWidget(row_widget)
            return

        rows = db.get_training_plans(self.user_id)

        for row in rows:
            data, opis, czas = row

            row_widget = QFrame()
            row_widget.setStyleSheet("""
                QFrame {
                    background-color: #ffffff;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                }
            """)
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(15, 10, 15, 10)

            label_opis = QLabel(str(opis))
            label_opis.setStyleSheet(
                "font-size: 14px; color: #222222; font-weight: bold; border: none; background: transparent;",
            )
            label_data = QLabel(str(data))
            label_data.setStyleSheet(
                "font-size: 13px; color: #888888; border: none; background: transparent;",
            )
            label_data.setAlignment(Qt.AlignCenter)
            Hours = czas // 3600
            Minutes = (czas % 3600) // 60
            Time = f"{Hours:02d}:{Minutes:02d}"
            label_czas = QLabel(Time)
            label_czas.setStyleSheet(
                "font-size: 13px; color: #2b8a3e; font-weight: bold; border: none; background: transparent;",
            )
            label_czas.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            row_layout.addWidget(label_opis, stretch=4)
            row_layout.addWidget(label_data, stretch=2)
            row_layout.addWidget(label_czas, stretch=2)

            layout.addWidget(row_widget)

    def addEntry(self):  # Dodanie planu na konkretny dzień
        if self.user_id == -1:
            QMessageBox.warning(
                self,
                "Nie wybrane konto",
                "Wybierz konto aby dodać trening",
            )
        Time = self.ui.Time.time()
        Date = self.ui.Calendar2.selectedDate()

        # Cel i długość treningu
        Target = self.ui.Target.text().strip()
        hours = Time.hour()
        minutes = Time.minute()
        seconds = Time.second()
        # Wybrany dzień
        datestr = Date.toString("yyyy-MM-dd")

        if Target == "":
            self.ui.Message.setText("Cel jest pusty")
            return
        if Date < QDate.currentDate():
            self.ui.Message.setText("Wybrano date z przeszłości")
            return

        Total = 3600 * hours + 60 * minutes + seconds
        db.add_training_plan(self.user_id, datestr, Target, Total)

        self.ui.Message.setText("Wpis został dodany")
        self.loadTrainingList()

    def selectedDate(self):  # Wypisanie planu na wybrany dzień
        Date = self.ui.Calendar1.selectedDate()
        # Wybrany dzień
        datestr = Date.toString("yyyy-MM-dd")

        trening = db.get_training_plan_from_date(self.user_id, datestr)
        Target = ""
        for t in trening:
            Target, Seconds = t

        if Target == "":
            self.ui.Target_2.setText("Brak treningu na dany dzień")
            self.ui.Time_2.setText("")
        else:
            self.ui.Target_2.setText(Target)
            Hours = Seconds // 3600
            Minutes = (Seconds % 3600) // 60
            Time = f"{Hours:02d}:{Minutes:02d}"
            self.ui.Time_2.setText(Time)

    def setProfile(self, user):
        self.user_id = user
        self.loadTrainingList()
        self.selectedDate()
        self.ui.User_name.setText(db.get_a_user(self.user_id))

    def backToMainMenu(self):
        self.parent().setCurrentIndex(0)
        self.main_window.voice.stop_playing()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = CalendarMenu()
    window.show()

    sys.exit(app.exec())
