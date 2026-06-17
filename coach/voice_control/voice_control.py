from __future__ import annotations

import os.path

import pygame
import speech_recognition as sr
from gtts import gTTS
from PySide6.QtCore import QMutex

pygame.mixer.init()
pygame.mixer.set_num_channels(2)


# Klasa nasłuchująca co mówi użytkownik
class Listener:
    def __init__(self, language="pl"):
        self.language = language
        self.recognizer = sr.Recognizer()

        self.microphone = sr.Microphone()
        self.source = self.microphone.__enter__()
        self.recognizer.energy_threshold = 200
        self.recognizer.adjust_for_ambient_noise(self.source, duration=0.5)

    # Zwracanie jako tekstu tego co mówi użytkownik
    def listen(self):
        try:
            audio = self.recognizer.listen(self.source, timeout=5, phrase_time_limit=5)
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text
        except sr.WaitTimeoutError:
            return "Nic nie powiedziano."
        except sr.UnknownValueError:
            return "Nie zrozumiano. Powtórz"
        except sr.RequestError as e:
            return e
        finally:
            self.microphone.__exit__(None, None, None)
            self.source = None


# Obsługa mowy asystenta
class Speaker:
    _channel_locks = {
        0: QMutex(),
    }

    def __init__(self, lang="pl", voice_filename="voice.mp3", channel_id=0):
        self.lang = lang
        self.voice_filename = voice_filename
        now_dir = os.path.dirname(os.path.abspath(__file__))
        if channel_id == 0:
            self.folder = os.path.join(now_dir, "voice_records")
            self.voice_filename = os.path.join(
                self.folder,
                self.voice_filename + ".mp3",
            )
        else:
            self.folder = os.path.join(now_dir, "../database/music")
            self.voice_filename = os.path.join(self.folder, self.voice_filename)

    # Tworzenie pliku audio
    def gen_speak(self, text):
        tts = gTTS(text=text, lang=self.lang)
        tts.save(self.voice_filename)

    # Funkcja mówiąca
    def speak(self, channel_id, volume=1.0):
        pygame.mixer.init()
        lock = self._channel_locks.get(channel_id)
        if lock:
            lock.lock()

        try:
            sound = pygame.mixer.Sound(self.voice_filename)
            channel = pygame.mixer.Channel(channel_id)
            channel.set_volume(volume)

            channel.play(sound)

            return channel
        finally:
            if lock:
                lock.unlock()

    # Kasowanie pliku audio
    def delete_file(self):
        if os.path.exists(self.voice_filename):
            os.remove(self.voice_filename)
