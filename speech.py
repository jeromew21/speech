import speech_recognition as sr
import time
import subprocess
from gtts import gTTS

def getSpeech(recognizer, mike):
    with mike as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "transcribe": None,
        "error": None,
    }

    try:
        response["transcribe"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["error"] = "API error"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"\

    return response

def say(stuff):
    tts = gTTS(stuff)
    tts.save('temp.mp3')
    subprocess.Popen(["mpg123", "-q", "temp.mp3"])

def start():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    while True:
        print("Say something...")
        speech = getSpeech(recognizer, microphone)
        if speech["error"]:
            print(speech["error"])
        else:
            words = speech["transcribe"]
            print(words)
            say("You said, " + words + ".")
            

if __name__ == "__main__":
    start()
