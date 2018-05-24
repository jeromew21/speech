import wikipedia
import nltk
import urllib
import urllib.parse
import urllib.request
import os
import vlc
import json

from bs4 import BeautifulSoup

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

info = {
    "name" : ""
}

pastas = {
   ("seal", "navy"): NAVY_SEAL
}

SEARCH = ("search", "info", "information", "look", "research", "what", "who", "where")
PLAY = ("play",)

KEYWORDS = SEARCH + PLAY

def classify(tags):
    result = {
        "query": "none",
        "nouns": [],
        "query_phrase": ""
    }
    for word, part in reversed(tags):
        if word in PLAY:
            result["query"] = word
        if word in SEARCH:
            result["query"] = word
    if result["query"] not in PLAY:
        for word, part in tags:
            if part in ("NN", "NNS") and word not in KEYWORDS:
                result["nouns"].append(word)
        result["query_phrase"] = " ".join(result["nouns"])
    else:
        query = []
        for word, part in tags:
            if word != result["query"]:
                query.append(word)
        result["query_phrase"] = " ".join(query)
    return result

def play_sound(filepath):
    p = vlc.MediaPlayer(filepath)
    p.play()
    while p.get_state() != vlc.State.Ended:
        pass

song_cache = {}
JSON_CACHE = "songs/cache.json"
if os.path.isfile(JSON_CACHE):
    with open(JSON_CACHE, "r") as f:
        song_cache = json.load(f)
else:
    with open(JSON_CACHE, "w") as f:
        f.write(json.dumps(song_cache))

def play_song(name):
    name = name.trim()
    if not name:
        return "play what"
    FOLDER = "songs"
    YOUTUBE = 'https://www.youtube.com'
    filename = os.path.join(FOLDER, name) + ".mp3"
    print("Playing {}".format(name))
    if name in song_cache:
        play_sound(song_cache[name])
    else:
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(name)
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, "lxml")
        links = []
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            if not vid['href'].startswith("https://googleads.g.doubleclick.net/"):
                links.append(vid['href'])
        url = YOUTUBE + links[0]
        hash = url.split("=")[-1]
        path = os.path.join(FOLDER, hash)
        filename = path + ".mp3"
        song_cache[name] = filename
        if os.path.isfile(filename):
              play_sound(filename)
        else:
            command = "youtube-dl --extract-audio --audio-format mp3 -o '{0}.%(ext)s' {1}".format(path, url)
            print(command)
            os.system(command)
            print("Finished DL")
            play_sound(filename)
        with open(JSON_CACHE, "w") as f:
            f.write(json.dumps(song_cache))

def get_tags(words):
    return nltk.pos_tag(nltk.word_tokenize(words))

def clean_text(text):
    return text.replace("\n", " ").replace("'", "")

def response(words):
    words = clean_text(words).lower()
    for key in pastas:
        if key[0] in words and key[1] in words:
            return pastas[key]
    tokens = clean_text(words).split(" ")
        
    if len(tokens) >= 3 and (tokens[0], tokens[1]) in (("call", "me"), ("i", "am")):
        info["name"] = tokens[2]
        return "yes {}".format(tokens[2])
    tags = get_tags(words)
    data = classify(tags)
    print(data)
    if data["query"] in PLAY:
        play_song(data["query_phrase"])
        return ""
    elif data["query"] in SEARCH:
        return clean_text(wikipedia.summary(data["query_phrase"]))
    return "you said {}".format(words)
