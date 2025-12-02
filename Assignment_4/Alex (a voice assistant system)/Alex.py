import speech_recognition as sr
import pyttsx3
import logging
import os
import datetime
import wikipedia
import webbrowser
import random
import subprocess
import google.generativeai as genai 


#logging configuration
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"

os.makedirs(LOG_DIR, exist_ok=True)

log_path = os.path.join(LOG_DIR,LOG_FILE_NAME)

logging.basicConfig(
    filename=log_path,
    format = "[%(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)

# activating voice from our system
engine = pyttsx3.init("sapi5")
engine.setProperty('rate',170)
voices = engine.getProperty("voices")
# print(voices[1].id) 
engine.setProperty('voice', voices[1].id) # set the female version
 
# this is speak function
def speak(text):
    """This is text to speech convert function

    Args:
        text 
    returns:
        voice
    """
    engine.say(text)
    engine.runAndWait()
    
# speak("Hello everyone My name is Apurbo")
# This function recognize the speech and convert it to text

def takeCommand():
    """This is speech to text convert & recognize function
    
    Returns:
        text as query
    """    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)  
    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")     
    except Exception as e:
        logging.info(e)
        print("Say that again please")
        return "None"
    return query

def greeting():
    hour = (datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning sir!")
    elif hour>=12 and hour<=18:
        speak("Good Afternoon sir!")
    else:
        speak("Good Evening sir!")
           
    speak("how may I help you?")



def play_music():
    music_dir = r"Alex (a voice assistant system)\music"   # add your music directory
    try: 
        songs = os.listdir(music_dir)
        if songs:
            random_song = random.choice(songs)
            speak(f"Playing a random song sir: {random_song}")
            os.startfile(os.path.join(music_dir, random_song))
        else:
            speak("No music files found in your music directory")
    except Exception as e:
        speak("Sorry sir, I could not find your music folder.")


def gemini_model_response(user_input):
    GEMINI_API_KEY = ""      # set your api key here
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"Your name is Alex, you act like Alex.Answer shortly, Question: {user_input}"
    response = model.generate_content(prompt)
    result = response.text
    
    return result



greeting()

while True:
    query = takeCommand().lower()
    print(query)    
    # speak(query)
      
    if "your name" in query:
        speak("My name is Alex!")
        logging.info("User asked for assistant,s name.")
        
    elif "who are you" in query or "introduce" in query:
        speak("Hi sir,i am Alex made by Apurbo Sharma")
        logging.info("User asked about assistant's response")   
    
    elif "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir the time is {strTime}")
        logging.info("User asked for current time.")
    
    # Small talk
    elif "hear me" in query or "Alex" in query:
        speak("Yes sir how can i help you")
        logging.info("User asked about assistant's response")
        
    elif "how are you" in query:
        speak("I am functioning at full capacity sir!")
        logging.info("User asked about assistant's well-being.")

    
    elif "who made you" in query:
        speak("I was created by Apurbo Sharma, a brilliant mind!")
        logging.info("User asked about assistant's creator.")

    
    elif "thank" in query or "thanks" in query:
        speak("It's my pleasure sir.")
        logging.info("User expressed gratitude.")

    
    elif "open google" in query:
        speak("ok sir. please type here what do you want to read")
        webbrowser.open("google.com")
        logging.info("User requested to open Google.")

    
    # Calculator
    elif "open calculator" in query or "calculator" in query:
        speak("Opening calculator")
        subprocess.Popen("calc.exe")
        logging.info("User requested to open Calculator.")

    
     # Notepad
    elif "open notepad" in query:
        speak("Opening Notepad")
        subprocess.Popen("notepad.exe")
        logging.info("User requested to open Notepad.")

    
    # Command Prompt
    elif "open terminal" in query or "open cmd" in query:
        speak("Opening Command Prompt terminal")
        subprocess.Popen("cmd.exe")
        logging.info("User requested to open Command Prompt.")

    
    # Calendar
    elif "open calendar" in query or "calendar" in query:
        speak("Opening Windows Calendar")
        webbrowser.open("https://calendar.google.com")
        logging.info("User requested to open Calendar.")

    
    # YouTube search
    elif "youtube" in query:
        speak("Opening YouTube for you.")
        query = query.replace("youtube", "")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        logging.info("User requested to search on YouTube.")

    
    elif "open facebook" in query:
        speak("ok sir. opening facebook")
        webbrowser.open("facebook.com")
        logging.info("User requested to open Facebook.")

    
    elif "open github" in query:
        speak("ok sir. opening github")
        webbrowser.open("github.com")
        logging.info("User requested to open GitHub.")


    
    elif "joke" in query:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why was the JavaScript developer sad? Because he didn't Node how to Express himself.",
            "Why did the developer go broke? Because he used up all his cache.",
            "Why do Python programmers wear glasses? Because they can't C.",
            "What do you call 8 hobbits? A hobbyte.",
            "Why was the computer cold? It forgot to close its Windows.",
            "Why did the coder quit his job? Because he didn't get arrays.",
            "Why did the computer show up at work late? It had a hard drive.",
            "Why did the functions break up? They had constant arguments.",
            "Why was the computer so smart? It had lots of bytes.",
            "Why don't programmers like nature? Too many bugs.",
            "I told my computer I needed a break. It said no problem, it will go to sleep.",
            "Why do Java developers wear glasses? Because they don't C sharp."
        ]
        speak(random.choice(jokes))
        logging.info("User requested a joke.")


    
    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
        logging.info("User requested information from Wikipedia.")

    
    elif "play music" in query or "music" in query:
        play_music()
    
    elif "ok bye" in query:
        speak("Thank you sir, have a nice day!")
        logging.info("User exited the program.")
        exit()
        
    else:
        # speak("I can not help you.")
        response = gemini_model_response(query)
        speak(response)
        logging.info("User asked for other question")