import speech_recognition as sr
import time

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

def start():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    while True:
        print("Say something...")
        speech = getSpeech(recognizer, microphone)
        if speech["error"]:
            print(speech["error"])
        else:
            print(speech["transcribe"])

if __name__ == "__main__":
    start()