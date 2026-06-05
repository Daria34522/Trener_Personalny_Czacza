import os
import sys
from sys import path

from PIL import Image
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QLabel, QPushButton, QRadioButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QSize
from VoiceWorker import VoiceWorker


def loadProfileImagesAndNames(Window,):

    profiles_data = [
        ("Nazwa Użytkownika 1", "id1", "assets/icons/profile.png"),
        ("Nazwa Użytkownika 2", "id2", "assets/icons/profile.png"),
        ("Nazwa Użytkownika 3", "id3", "assets/icons/profile.png"),
        ("Nazwa Użytkownika 4", "id4", "assets/icons/profile.png"),
    ] #TODO pobrać z bazy dane w takiej postaci

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

    if hasattr(Window, 'radio_buttons'):
        Window.radio_buttons.clear()
    else:
        Window.radio_buttons = []

    for index, profile in enumerate(profiles_data):
        user_name, user_id, img_path = profile
        tile_number = index + 1

        if tile_number <= 6:
            btn = Window.findChild(QPushButton, f"ProfileImage_{tile_number}")
            label = Window.findChild(QLabel, f"ProfileName_{tile_number}")

            if btn:
                btn.setStyleSheet(profile_button_style)
                btn.setIcon(QIcon(img_path))
                btn.setIconSize(QSize(128, 128))
                btn.setText("")
                btn.setProperty("user_id", user_id)

            if label:
                label.setText(user_name)

        radio = QRadioButton(f"{user_name}")
        radio.setProperty("user_id", user_id)

        if Window.ui.scrollArea.widget() and Window.ui.scrollArea.widget().layout():
            Window.ui.scrollArea.widget().layout().addWidget(radio)
            Window.radio_buttons.append(radio)

    for empty_index in range(len(profiles_data) + 1, 7):
        btn = Window.findChild(QPushButton, f"ProfileImage_{empty_index}")
        label = Window.findChild(QLabel, f"ProfileName_{empty_index}")
        if btn:
            btn.setVisible(False)
        if label:
            label.setVisible(False)

class ProfileWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
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

        # Łączenie przycisków z metodami
        self.ui.Create_profile_button.clicked.connect(self.createProfile)
        self.ui.Browse.clicked.connect(self.choosePhoto)
        self.ui.Delete_profile_button.clicked.connect(self.deleteProfile)

        for i in range(1, 7):
            widget = self.findChild(QPushButton, f"ProfileImage_{i}")
            widget.clicked.connect(lambda event, w=widget: self.loadProfile(w))
        self.voice = VoiceWorker()
        self.voice.play("Wybierz swój profil lub utwórz nowy")

    # obsługa przycisków oraz funkcji okienka
    def createProfile(self):
        self.ui.Message_from_database.setText("")

        # Pobranie z menu danych użytkownika i sprawdzenie ich poprawności
        user_name = self.ui.User_name.text().strip()
        image_path = self.ui.Path.text()

        # Obsługa błędnych danych
        if user_name == "":
            self.ui.Message_from_database.setText("Proszę podać nazwe użytkownika")  # Wyświetlenie błędu w gui
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

    def deleteProfile(self):
        user_id = -1
        for radio in self.radio_buttons:  # szukanie zaznaczonej piosenki
            if radio.isChecked():
                user_id = radio.property("user_id")
                break
        if user_id == -1:
            self.ui.Message_from_database.setText("Proszę wybrać profil")  # Wyświetlenie błędu w gui
        else:
            # TODO usunięcie profilu z bazy

            self.ui.Message_from_database.setText("Wybrany profil został usunięty")
            loadProfileImagesAndNames(self)  # Wczytanie obrazków i nazw do UI

    def loadProfile(self, widget):
        self.ui.Message_from_database.setText("")  # Komunikat dla użytkownika

        # Pobranie z menu danych użytkownika i sprawdzenie ich poprawności
        number = widget.objectName().replace("ProfileImage_", "")
        profile_name = self.findChild(QLabel, f"ProfileName_{number}").text()
        print(profile_name)

        # TODO Obsługa pustego profilu
        pass

        # TODO Komunikacja z bazą danych oraz załadowanie profilu
        user_id = -1  # Przykładowe id użytkownika
        pass

        # Przekazanie id użytkownika i przełączenie do menu głównego
        self.parent().parent().loggedUser(user_id)
        self.parent().setCurrentIndex(0)

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
