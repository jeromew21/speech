import speech_recognition as sr
import time
import subprocess
from gtts import gTTS

NAVY_SEAL = """
What the fuck did you just fucking say about me, you little bitch? 
I'll have you know I graduated top of my class in the Navy Seals, 
and I've been involved in numerous secret raids on Al-Quaeda, 
and I have over 300 confirmed kills. I am trained in gorilla 
warfare and I'm the top sniper in the entire US armed forces. 
You are nothing to me but just another target. I will wipe you 
the fuck out with precision the likes of which has never been 
seen before on this Earth, mark my fucking words. You think you 
can get away with saying that shit to me over the Internet? 
Think again, fucker. As we speak I am contacting my secret network 
of spies across the USA and your IP is being traced 
right now so you better prepare for the storm, maggot. 
The storm that wipes out the pathetic little thing you 
call your life. You're fucking dead, kid. I can be anywhere,
 anytime, and I can kill you in over seven hundred ways, 
 and that's just with my bare hands. Not only am I extensively 
 trained in unarmed combat, but I have access to the entire 
 arsenal of the United States Marine Corps and I will use it 
 to its full extent to wipe your miserable ass off the face of 
 the continent, you little shit. If only you could have known 
 what unholy retribution your little "clever" comment was about 
 to bring down upon you, maybe you would have held your fucking 
 tongue. But you couldn't, you didn't, and now you're paying the 
 price, you goddamn idiot. I will shit fury all over you and you 
 will drown in it. You're fucking dead, kiddo.
 """

def get_speech(r, m):
    with m as source:
        audio = r.listen(source)

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
    subprocess.call(["mpg123", "-q", "500-milliseconds-of-silence.mp3"])
    tts = gTTS(stuff)
    tts.save('temp.mp3')
    print("Now I am talking...")
    subprocess.call(["mpg123", "-q", "temp.mp3"])

def start():
    print("Readying...")
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source: 
        r.adjust_for_ambient_noise(source)
    while True:
        m = sr.Microphone()
        print("You may say something...")
        speech = get_speech(r, m)
        if speech["error"]:
            print(speech["error"])
        else:
            words = speech["transcribe"]
            print("Heard: {}".format(words))
            say("You said " + words) 

if __name__ == "__main__":
    start()
