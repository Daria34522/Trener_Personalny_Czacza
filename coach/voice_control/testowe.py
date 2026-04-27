from gtts import gTTS
import pygame

tts = gTTS("  Cześć, to test głosu będę twoim asystentem", lang="pl")
tts.save("voice.mp3")

pygame.mixer.init()
pygame.mixer.music.load("voice.mp3")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pass