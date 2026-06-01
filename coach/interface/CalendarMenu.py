import sys
from sys import path

from PIL import Image
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QLabel, QPushButton, QFrame, QHBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QSize, QDate

class CalendarMenu(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        ui_path = "ui/Calendar_menu.ui"
        loader = QUiLoader()
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Nie można otworzyć pliku: {ui_path}")
            sys.exit(-1)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setWindowTitle("Plan treningowy")
        self.showMaximized()
        self.loadTrainingList()
        self.selectedDate()

        user_id = -1 # ID użytkownika

        # Podpinanie metod pod przyciski
        self.ui.Add_entry.clicked.connect(self.addEntry)
        self.ui.Calendar1.clicked.connect(self.selectedDate)
        self.ui.Main_menu.clicked.connect(self.backToMainMenu) # Menu główne

    def loadTrainingList(self):  # Pokazanie całej listy treningowej
        # TODO połączenie z bazą danych oraz pobranie wszystkich planów treningowych które odbędą się w przyszłości
        rows = [
            ("Cardio Interwały na bieżni", "2026-05-16", "00:45"),
            ("Trening siłowy - Klatka + Triceps", "2026-05-17", "01:00"),
            ("Rozciąganie i Joga regeneracyjna", "2026-05-20", "00:30"),
            ("Trening obwodowy FBW (Full Body)", "2026-05-22", "00:55"),
            ("Spacer regeneracyjny w terenie", "2026-05-24", "01:15")
        ]  # Przykładowe dane

        layout = self.ui.scrollAreaWidgetContents.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for row in rows:
            opis, data, czas = row

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
                "font-size: 14px; color: #222222; font-weight: bold; border: none; background: transparent;")
            label_data = QLabel(str(data))
            label_data.setStyleSheet("font-size: 13px; color: #888888; border: none; background: transparent;")
            label_data.setAlignment(Qt.AlignCenter)
            label_czas = QLabel(f"⏱️ {czas}")
            label_czas.setStyleSheet(
                "font-size: 13px; color: #2b8a3e; font-weight: bold; border: none; background: transparent;")
            label_czas.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            row_layout.addWidget(label_opis, stretch=4)
            row_layout.addWidget(label_data, stretch=2)
            row_layout.addWidget(label_czas, stretch=2)

            layout.addWidget(row_widget)

    def addEntry(self):  # Dodanie planu na konkretny dzień
        Time = self.ui.Time.time()
        Date = self.ui.Calendar2.selectedDate()

        # Cel i długość treningu
        Target = self.ui.Target.text().strip()
        hours = Time.hour()
        minutes = Time.minute()
        seconds = Time.second()
        # Wybrany dzień
        parsed_date = Date.toString("dd-MM-yyyy").split("-")
        print(parsed_date)

        if Target == "" or Date < QDate.currentDate():
            self.ui.Message.setText("Cel jest pusty lub data jest z przeszłości")
            return

        self.ui.Message.setText("Wpis został dodany")
        # TODO komunikacja z bazą i dodanie wpisu
        pass

    def selectedDate(self):  # Wypisanie planu na wybrany dzień
        Date = self.ui.Calendar1.selectedDate()
        # Wybrany dzień
        parsed_date = Date.toString("dd-MM-yyyy").split("-")
        print(parsed_date)

        # TODO połączenie z bazą i pobranie planu na konkretny dzień
        pass

        Target = "Szybkie bieganie"  # Przykładowe dane
        Czas = "20min"

        if Target == "":
            self.ui.Target_2.setText("Brak treningu na dany dzień")
        else:
            self.ui.Target_2.setText(Target)
            self.ui.Time_2.setText(Czas)

    def setProfile(self, user):
        self.user_id = user

    def backToMainMenu(self):
        self.parent().setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = CalendarMenu()
    window.show()

    sys.exit(app.exec())