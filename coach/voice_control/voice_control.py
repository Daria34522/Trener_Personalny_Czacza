import os.path
from gtts import gTTS
import pygame
import time
import speech_recognition as sr
from PySide6.QtCore import QMutex

pygame.mixer.init()
pygame.mixer.set_num_channels(2)

# Klasa nasłuchująca co mówi użytkownik
class Listener:
    def __init__(self, language = "pl"):
        self.language = language
        self.recognizer = sr.Recognizer()

    # Zwracanie jako tekstu tego co mówi użytkownik
    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.energy_threshold = 200
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio, language=self.language)
                return text
            except sr.WaitTimeoutError:
                return "Nic nie powiedziano."
            except sr.UnknownValueError:
                return "Nie zrozumiano. Powtórz"
            except sr.RequestError as e:
                return e

# Obsługa mowy asystenta
class Speaker:
    _channel_locks = {
        0: QMutex(),
    }

    def __init__(self, lang ="pl", voice_filename= "voice.mp3", channel_id = 0):
        self.lang = lang
        self.channel_id = channel_id
        now_dir = os.path.dirname(os.path.abspath(__file__))
        self.folder = os.path.join(now_dir, "voice_records")
        self.voice_filename = os.path.join(self.folder, voice_filename + ".mp3")
        pygame.mixer.init()

    # Tworzenie pliku audio
    def gen_speak(self, text):
        tts = gTTS(text=text, lang=self.lang)
        tts.save(self.voice_filename)

    # Funkcja mówiąca
    def speak(self, chanel_id, volume=1.0):
        lock = self._channel_locks.get(chanel_id)
        if lock:
            lock.lock()

        try:
            sound = pygame.mixer.Sound(self.voice_filename)
            channel = pygame.mixer.Channel(chanel_id)
            channel.set_volume(volume)

            channel.play(sound)
            # czekanie aż skończy
            while channel.get_busy():
                time.sleep(0.1)

            return channel
        finally:
            if lock:
                lock.unlock()

    # Kasowanie pliku audio
    def delete_file(self):
        if(os.path.exists(self.voice_filename)):
            os.remove(self.voice_filename)