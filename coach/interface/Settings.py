from __future__ import annotations

import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from database.DBHandler import DBHandler

from PySide6.QtWidgets import QApplication, QMainWindow, QRadioButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

db_path = os.path.join(parent_dir, "database/db.sqlite")
db = DBHandler(db_path)


class Settings(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        ui_path = f"{os.path.dirname(__file__)}/ui/settings.ui"
        loader = QUiLoader()
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Nie można otworzyć pliku: {ui_path}")
            sys.exit(-1)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setWindowTitle("Ustawienia")

        self.radio_buttons = []  # Kontener na piosenki
        self.loadSongsAsSelectableList()  # ładowanie muzyki do menu

        # Przycisk zatwierdzenia wyboru
        self.ui.Confirm_selection.clicked.connect(self.confirmSelection)
        self.ui.Main_menu.clicked.connect(self.backToMainMenu)  # Menu główne

    def loadSongsAsSelectableList(self):
        rows = db.get_all_songs()
        for row in rows:
            tytul, artysta, sciezka = row  # Rozpakowujemy tytuł i ścieżkę
            radio = QRadioButton(f"🎵 {artysta} - {tytul}")
            full_path = os.path.join("database/music/", sciezka)
            radio.setProperty("song_path", full_path)
            self.ui.scrollArea.widget().layout().addWidget(radio)
            self.radio_buttons.append(radio)

    def confirmSelection(self):
        selected_song_path = None
        selected_song_title = ""
        selected_song_id = -1
        for radio in self.radio_buttons:  # szukanie zaznaczonej piosenki
            if radio.isChecked():
                selected_song_path = radio.property("song_path")
                full_text = radio.text()
                if " - " in full_text:
                    selected_song_title = full_text.split(" - ")[-1].strip()
                else:
                    selected_song_title = full_text.strip()
                break
        if selected_song_path is None:
            self.ui.Message.setText("Proszę wybrać utwór")  # Wyświetlenie błędu w gui
        else:
            selected_song_id = db.get_songid(selected_song_title)
            print(selected_song_title, selected_song_id)
            self.parent().parent().selectedSong(selected_song_id)
            self.parent().setCurrentIndex(0)

    def backToMainMenu(self):
        self.parent().setCurrentIndex(0)
        self.main_window.voice.stop_playing()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Settings()
    window.show()

    sys.exit(app.exec())
