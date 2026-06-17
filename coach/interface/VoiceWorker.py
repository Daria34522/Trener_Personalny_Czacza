from __future__ import annotations

import os
import sys

from PySide6.QtCore import QThread

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from voice_control.voice_control import Speaker

from database.DBHandler import DBHandler

db_path = os.path.join(parent_dir, "database/db.sqlite")
db = DBHandler(db_path)


class VoiceWorker(QThread):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.filename = ""
        self.to_delete = True
        self.to_create = True
        self.channel_id = 0
        self.volume = 1.0
        self.current = None

    def play(
        self,
        text="",
        filename="example",
        to_delete=True,
        to_create=True,
        channel_id=0,
        volume=1.0,
    ):
        self.text = text
        self.filename = filename
        self.to_delete = to_delete
        self.to_create = to_create
        self.channel_id = channel_id
        self.volume = volume
        if not self.isRunning():
            self.start()

    def run(self):
        speaker = Speaker(voice_filename=self.filename, channel_id=self.channel_id)
        if self.to_create is True:
            speaker.gen_speak(self.text)

        self.current = speaker.speak(channel_id=self.channel_id, volume=self.volume)

        while self.current and self.current.get_busy():
            self.msleep(100)

        if self.to_delete is True:
            speaker.delete_file()

    def stop_playing(self):
        if self.current:
            self.current.stop()
            self.current = None
            self.quit()
