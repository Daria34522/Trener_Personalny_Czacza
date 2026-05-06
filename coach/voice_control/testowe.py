from voice_control import Speaker, Listener

if __name__ == '__main__':
    speaker = Speaker(voice_filename="test")
    text = "Jestem twoim asystentem"
    speaker.gen_speak(text)
    speaker.speak()

    # speaker.delete_file()

    # listener = Listener()
    # print("Mów")
    # text = listener.listen()
    # print(text)