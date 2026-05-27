import os.path
from gtts import gTTS
import pygame
import time
import speech_recognition as sr

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
    def __init__(self, lang ="pl", voice_filename= "voice.mp3"):
        self.lang = lang
        now_dir = os.path.dirname(os.path.abspath(__file__))
        self.folder = os.path.join(now_dir, "voice_records")
        self.voice_filename = os.path.join(self.folder, voice_filename + ".mp3")
        pygame.mixer.init()

    # Tworzenie pliku audio
    def gen_speak(self, text):
        tts = gTTS(text=text, lang=self.lang)
        tts.save(self.voice_filename)

    # Funkcja mówiąca
    def speak(self):
        pygame.mixer.music.load(self.voice_filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.unload()

    # Kasowanie pliku audio
    def delete_file(self):
        if(os.path.exists(self.voice_filename)):
            os.remove(self.voice_filename)