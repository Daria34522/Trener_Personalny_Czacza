import sys

from PySide6.QtCore import QThread
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from voice_control.voice_control import Speaker, Listener


class VoiceWorker(QThread):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.filename = ""

    def say(self, text, filename="example"):
        self.text = text
        self.filename = filename
        if not self.isRunning():
            self.start()
    def run(self):
        speaker = Speaker(voice_filename = self.filename)
        speaker.gen_speak(self.text)
        speaker.speak()
        speaker.delete_file()