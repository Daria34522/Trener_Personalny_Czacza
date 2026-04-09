import speech_recognition as sr
from translate import Translator
import pyttsx3


def init_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)
    return engine


def speak(text):
    print("Program:", text)
    temp_engine = init_engine()
    try:
        temp_engine.say(text)
        temp_engine.runAndWait()
        temp_engine.stop()
    except Exception as e:
        print("Błąd audio:", e)


def recognise(lang):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.energy_threshold = 200
        print(f"[{lang}] Słucham...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            rec_txt = r.recognize_google(audio, language=lang)
            return rec_txt.lower()
        except:
            return None


def main():
    trans_to_en = Translator(to_lang="en", from_lang="pl")
    trans_to_pl = Translator(to_lang="pl", from_lang="en")

    choice_lan = "polski"
    speak("Start. Domyślnie tłumaczę z polskiego na angielski.")

    while True:
        listen_lang = "pl-PL" if choice_lan == "polski" else "en-US"
        phrase = recognise(listen_lang)

        if not phrase:
            continue

        print(f"Usłyszano: {phrase}")
        if "polski" in phrase or "polish" in phrase:
            choice_lan = "polski"
            speak("Tryb: polski na angielski")
            continue

        elif "angielski" in phrase or "english" in phrase:
            choice_lan = "angielski"
            speak("Mode: English to Polish")
            continue

        elif "bywaj" in phrase or "goodbye" in phrase:
            speak("Do widzenia")
            break
        try:
            if choice_lan == "polski":
                translation = trans_to_en.translate(phrase)
                speak(translation)
            else:
                translation = trans_to_pl.translate(phrase)
                speak(translation)
        except Exception as e:
            print("Błąd tłumaczenia:", e)


if __name__ == "__main__":
    main()