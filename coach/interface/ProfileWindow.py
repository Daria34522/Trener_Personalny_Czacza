import sys
from sys import path

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


class ProfileWindow(QMainWindow):
    def __init__(self):
        # Ładowanie pliku .ui
        super().__init__()
        ui_path = "ui/profile_selection_menu.ui"
        loader = QUiLoader()
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Nie można otworzyć pliku: {ui_path}")
            sys.exit(-1)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setWindowTitle("Wybór profilu")

        # Łączenie przycisków z metodami
        self.ui.Create_profile_button.clicked.connect(self.createProfile)
        self.ui.Select_profile_button.clicked.connect(self.loadProfile)

        # TODO Ładowanie profili do wyboru przez użytkownika
        pass

    # obsługa przycisków oraz funkcji okienka
    def createProfile(self):
        self.ui.Message_from_database.setText("")

        # Pobranie z menu danych użytkownika i sprawdzenie ich poprawności
        user_name = self.ui.User_name.text().strip()
        age = self.ui.Age.text().strip()
        # obsługa błędnych danych
        if (age == "" or user_name == ""):
            self.ui.Message_from_database.setText("Błędne dane") # Wyświetlenie błędu w gui
            return

        # TODO Komunikacja z bazą danych oraz stworzenie profilu
        pass

    def loadProfile(self):
        self.ui.Message_from_database_2.setText("")

        # Pobranie z menu danych użytkownika i sprawdzenie ich poprawności
        data = self.ui.Select_profile.currentText()
        if(data == ""):
            self.ui.Message_from_database_2.setText("Proszę wybrać profil do załadowania") # Wyświetlenie błędu w gui
            return

        # TODO Komunikacja z bazą danych oraz załadowanie profilu
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ProfileWindow()
    window.show()

    sys.exit(app.exec())