import sys
from sys import path

from PIL import Image
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QLabel
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
        self.ui.Browse.clicked.connect(self.choosePhoto)
        for i in range(1, 7):
            widget = self.findChild(QWidget, f"ProfileImage_{i}")
            widget.mousePressEvent = lambda event, w=widget: self.loadProfile(w)

        # TODO Ładowanie profili do wyboru przez użytkownika
        pass

    # obsługa przycisków oraz funkcji okienka
    def createProfile(self):
        self.ui.Message_from_database.setText("")

        # Pobranie z menu danych użytkownika i sprawdzenie ich poprawności
        user_name = self.ui.User_name.text().strip()
        image_path = self.ui.Path.text()

        # obsługa błędnych danych
        if (user_name == ""):
            self.ui.Message_from_database.setText("Proszę podać nazwe użytkownika") # Wyświetlenie błędu w gui
            return
        try:
            img = Image.open(image_path)
            img.verify()  # sprawdza integralność pliku
        except Exception:
            self.ui.Message_from_database.setText("Błędny adres lub plik nie jest obsługiwanym typem obrazu") # Wyświetlenie błędu w gui
            return

        # TODO Komunikacja z bazą danych oraz stworzenie profilu
        pass

    # TODO jednak inaczej będzie
    def loadProfile(self, widget):
        self.ui.Message_from_database_2.setText("")

        # Pobranie z menu danych użytkownika i sprawdzenie ich poprawności
        number = widget.objectName().replace("ProfileImage_", "")
        profile_name = self.findChild(QLabel, f"ProfileName_{number}")

        # TODO obsługa pustego profilu
        pass

        # TODO Komunikacja z bazą danych oraz załadowanie profilu
        pass

    def choosePhoto(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz zdjęcie",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )
        self.ui.Path.setText(file_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ProfileWindow()
    window.show()

    sys.exit(app.exec())