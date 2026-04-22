import sys
from sys import path

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


class MainMenu(QMainWindow):
    def __init__(self):
        # Ładowanie pliku .ui
        super().__init__()
        ui_path = "ui/main_menu.ui"
        loader = QUiLoader()
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Nie można otworzyć pliku: {ui_path}")
            sys.exit(-1)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setWindowTitle("Menu główne")
        # Łączenie przycisków z metodami
        self.ui.Start_training.clicked.connect(self.startTraining)
        self.ui.Settings.clicked.connect(self.settings)
        self.ui.Stats.clicked.connect(self.stats)
        self.ui.Calendar.clicked.connect(self.calendar)
        self.ui.Recommendations.clicked.connect(self.recommendations)
        self.ui.Profile_selection.clicked.connect(self.profileSelection)

        #TODO Ładowanie profili do wyboru przez użytkownika


    # obsługa przycisków oraz funkcji okienka
    def startTraining(self):
        pass

    def settings(self):
        pass

    def stats(self):
        pass

    def calendar(self):
        pass

    def recommendations(self):
        pass
    
    def profileSelection(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainMenu()
    window.show()

    sys.exit(app.exec())