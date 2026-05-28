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
        self.to_delete= True
        self.to_create = True
        self.channel_id =0
        self. volume =1.0

    def play(self, text, filename="example", to_delete=True, to_create=True, chanel_id=0, volume=1.0):
        self.text = text
        self.filename = filename
        self.to_delete = to_delete
        self.to_create = to_create
        self.channel_id = chanel_id
        self.volume = volume
        if not self.isRunning():
            self.start()

    def run(self):
        speaker = Speaker(voice_filename = self.filename)
        if self.to_create is True:
            speaker.gen_speak(self.text)

        channel = speaker.speak(channel_id=self.channel_id, volume=self.volume)

        while self.get_busy():
            self.msleep(100)

        if self.to_delete is True:
            speaker.delete_file()