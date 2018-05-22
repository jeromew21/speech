import speech_recognition as sr
import time
import subprocess
import vlc
import responder
from gtts import gTTS

def get_response(words):
    return responder.response(words)

def get_speech(r):
    with sr.Microphone() as source:
        audio = r.listen(source, timeout=5.0)

    response = {
        "transcribe": None,
        "error": None,
    }

    try:
        print("Heard ya. Now trying to get what you said") 
        response["transcribe"] = r.recognize_google(audio)
    except sr.RequestError:
        response["error"] = "API error"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def say(stuff):
    print("Thinking about what to say")
    #subprocess.call(["mpg123", "-q", "500-milliseconds-of-silence.mp3"])
    tts = gTTS(stuff)
    tts.save('temp.mp3')
    print("Now I am talking...")
    p = vlc.MediaPlayer('temp.mp3')
    p.play()
    while p.get_state() != vlc.State.Ended:
        pass
    time.sleep(3)
    #subprocess.call(["mpg123", "-q", "temp.mp3"])

def start():
    print("Readying...")
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    with sr.Microphone() as source: 
        r.adjust_for_ambient_noise(source)
    say("Hello")
    while True:
        print("You may say something...")
        speech = get_speech(r)
        if speech["error"]:
            print(speech["error"])
        else:
            words = speech["transcribe"]
            print("Heard: {}".format(words))
            response = get_response(words)
            say(response)

if __name__ == "__main__":
    start()
