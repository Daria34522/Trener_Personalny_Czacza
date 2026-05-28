import sys
from sys import path

from PySide6.QtWidgets import QApplication, QMainWindow, QRadioButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from VoiceWorker import VoiceWorker

class Settings(QMainWindow):
    def __init__(self):
        # Ładowanie pliku .ui
        super().__init__()
        ui_path = "ui/settings.ui"
        loader = QUiLoader()
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Nie można otworzyć pliku: {ui_path}")
            sys.exit(-1)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setWindowTitle("Ustawienia")
        self.showMaximized()

        self.radio_buttons = [] # Kontener na piosenki
        self.loadSongsAsSelectableList() # ładowanie muzyki do menu

        # Przycisk zatwierdzenia wyboru
        self.ui.Confirm_selection.clicked.connect(self.confirmSelection)
        self.voice = VoiceWorker()
        self.voice.say("Wybierz piosenkę d której chcesz ćwiczyć")

    def loadSongsAsSelectableList(self):
        # TODO połączenie z bazą i wpisanie tytułu oraz ścieżki do 'rows'
        rows = [
            ("tytul1", "assets/music/1"),
            ("2", "assets/music/2"),
            ("3", "assets/music/3")
        ] # Przykład

        for row in rows:
            tytul, sciezka = row  # Rozpakowujemy tytuł i ścieżkę
            radio = QRadioButton(f"🎵 {tytul}")
            radio.setProperty("song_path", sciezka)
            self.ui.scrollArea.widget().layout().addWidget(radio)
            self.radio_buttons.append(radio)

    def confirmSelection(self):
        selected_song_path = None
        selected_song_title = ""
        for radio in self.radio_buttons: # szukanie zaznaczonej piosenki
            if radio.isChecked():
                selected_song_path = radio.property("song_path")
                selected_song_title = radio.text()
                break
        if selected_song_path is None:
            self.ui.Message.setText("Proszę wybrać utwór") # Wyświetlenie błędu w gui
        else:
            ## TODO zwrócenie tytułu oraz ścieżki do Maina
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Settings()
    window.show()

    sys.exit(app.exec())
