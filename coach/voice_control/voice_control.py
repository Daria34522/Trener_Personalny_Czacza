from asyncio import timeout

import speech_recognition as sr

class Listener:
    def __init__(self, language:str):
        self.language = language
        self.recognizer = sr.Recognizer()

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
                return "Nie zrozumiano. Powtorz"
            except sr.RequestError as e:
                return e