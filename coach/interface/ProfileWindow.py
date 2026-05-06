import sys
from sys import path

from PIL import Image
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QLabel, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

def loadProfileImagesAndNames(Window):
    for i in range(1, 7):
        widget = Window.findChild(QPushButton, f"ProfileImage_{i}")
        number = widget.objectName().replace("ProfileImage_", "")

        # TODO Wczytanie obrazy oraz nazwy użytkownika
        # Podczas każdego obrotu pętli ustawiany jest jeden blok tj. ikona i nazwa
        user_name = "xyz"
        img_path = "xyz"

        # Ustawianie obrazka oraz nazwy użytkownika dla jednego bloku
        Window.findChild(QLabel, f"ProfileName_{number}").setText(user_name)
        Window.ui.Start_training.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-image: url('{img_path}');
                background-position: center;
                background-repeat: no-repeat;
            }}
            QPushButton:hover {{
                border: 2px solid #00ff00;
            }}
        """)


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
        loadProfileImagesAndNames(self) # Ładowanie nazw użytkowików oraz zdjęć

        # Łączenie przycisków z metodami
        self.ui.Create_profile_button.clicked.connect(self.createProfile)
        self.ui.Browse.clicked.connect(self.choosePhoto)

        for i in range(1, 7): # Łączy każdy przycisk z metodą loadProfile a jako argument metody ustawia nazwe użytkownika
            widget = self.findChild(QPushButton, f"ProfileImage_{i}")
            widget.clicked.connect(lambda event, w=widget: self.loadProfile(w))


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

        # Wczytanie obrazków i nazw do UI
        loadProfileImagesAndNames(self)

    def loadProfile(self, widget):
        self.ui.Message_from_database.setText("") # Komunikat dla użytkownika

        # Pobranie z menu danych użytkownika i sprawdzenie ich poprawności
        number = widget.objectName().replace("ProfileImage_", "")
        profile_name = self.findChild(QLabel, f"ProfileName_{number}").text()
        print(profile_name)

        # TODO Obsługa pustego profilu
        pass

        # TODO Komunikacja z bazą danych oraz załadowanie profilu
        pass

    def choosePhoto(self): # Obsługa wybierania lokalizacji zdjęcia z dysku
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