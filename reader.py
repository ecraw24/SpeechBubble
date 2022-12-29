import pyttsx3
import time


def text_to_speech(text):

    voice_dict = {'Male': 0, 'Female': 1}
    code = voice_dict['Female']
    
    engine = pyttsx3.init()

    # Setting up voice rate
    engine.setProperty('rate', 125)

    # Setting up volume level  between 0 and 1
    engine.setProperty('volume', 0.8)

    # Change voices: 0 for male and 1 for female
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[code].id)

    engine.say(text)
    engine.runAndWait()  
    engine.stop()  