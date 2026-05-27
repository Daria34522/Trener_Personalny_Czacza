import os
import sys
from sys import path

from PIL import Image
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QLabel, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QSize


def loadProfileImagesAndNames(Window):
    profile_button_style = """
        QPushButton {
            background-color: #f8f9fa;
            border: 2px solid #dee2e6;
            border-radius: 20px;
            padding: 50px;
            outline: none;
        }

        QPushButton:hover {
            background-color: #e9ecef;
            border: 2px solid #00ff00;
        }

        QPushButton:pressed {
            background-color: #d1d4d7;
        }
    """

    for i in range(1, 7):
        btn = Window.findChild(QPushButton, f"ProfileImage_{i}")
        if not btn:
            continue
        number = btn.objectName().replace("ProfileImage_", "")

        # TODO: Wczytanie obrazu oraz nazwy użytkownika z bazy danych
        user_name = "xyz" # przykładowa nazwa użytkownika
        img_path = "assets/icons/profile.png" # przykładowa ścieżka

        label = Window.findChild(QLabel, f"ProfileName_{number}")
        if label:
            label.setText(user_name)
        btn.setStyleSheet(profile_button_style)
        btn.setIcon(QIcon(img_path))
        btn.setIconSize(QSize(128, 128))
        btn.setText("")

class ProfileWindow(QMainWindow):
    def __init__(self):
        # Ładowanie pliku .ui
        super().__init__()
        ui_path = f"{os.path.dirname(__file__)}/ui/profile_selection_menu.ui"
        loader = QUiLoader()
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Nie można otworzyć pliku: {ui_path}")
            sys.exit(-1)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setWindowTitle("Wybór profilu")
        loadProfileImagesAndNames(self) # Ładowanie nazw użytkowików oraz zdjęć
        self.showMaximized()

        # Łączenie przycisków z metodami
        self.ui.Create_profile_button.clicked.connect(self.createProfile)
        self.ui.Browse.clicked.connect(self.choosePhoto)

        for i in range(
            1, 7
        ):  # Łączy każdy przycisk z metodą loadProfile a jako argument metody ustawia nazwe użytkownika
            widget = self.findChild(QPushButton, f"ProfileImage_{i}")
            widget.clicked.connect(lambda event, w=widget: self.loadProfile(w))

    # obsługa przycisków oraz funkcji okienka
    def createProfile(self):
        self.ui.Message_from_database.setText("")

        # Pobranie z menu danych użytkownika i sprawdzenie ich poprawności
        user_name = self.ui.User_name.text().strip()
        image_path = self.ui.Path.text()

        # obsługa błędnych danych
        if user_name == "":
            self.ui.Message_from_database.setText(
                "Proszę podać nazwe użytkownika"
            )  # Wyświetlenie błędu w gui
            return
        try:
            img = Image.open(image_path)
            img.verify()  # sprawdza integralność pliku
        except Exception:
            self.ui.Message_from_database.setText(
                "Błędny adres lub plik nie jest obsługiwanym typem obrazu"
            )  # Wyświetlenie błędu w gui
            return

        # TODO Komunikacja z bazą danych oraz stworzenie profilu
        pass

        # Wczytanie obrazków i nazw do UI
        loadProfileImagesAndNames(self)

    def loadProfile(self, widget):
        self.ui.Message_from_database.setText("")  # Komunikat dla użytkownika

        # Pobranie z menu danych użytkownika i sprawdzenie ich poprawności
        number = widget.objectName().replace("ProfileImage_", "")
        profile_name = self.findChild(QLabel, f"ProfileName_{number}").text()
        print(profile_name)

        # TODO Obsługa pustego profilu
        pass

        # TODO Komunikacja z bazą danych oraz załadowanie profilu
        pass

    def choosePhoto(self):  # Obsługa wybierania lokalizacji zdjęcia z dysku
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Wybierz zdjęcie", "", "Images (*.png *.jpg *.jpeg)"
        )
        self.ui.Path.setText(file_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ProfileWindow()
    window.show()

    sys.exit(app.exec())
