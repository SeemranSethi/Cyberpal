import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
import pyaudio
import requests
import time
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

#new emails dictionary added
#can add some more
emails = {
    "purvi":"purvitashu450Agmail.com",
    "riya":"riyatyagi06ms@gmail.com"
}

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query
#new functionality of taking password from a file
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    f=open('email.txt')
    for word in f:
        pswd=word
    server.login('seemransethi@gmail.com', pswd)
    server.sendmail('seemransethi@gmail.com', to, content)
    server.close()

def basicDetails():
    speak("Let's Start with some basic information exchange. ")
    speak("Hi, I am your Cyber Pal")
    speak("What shall I call you?")
    query=takeCommand().lower()
    speak("Nice to meet you "+query+"How may I help you?")
    return query

if __name__ == "__main__":
    wishMe()
    #interacting with the user
    name=basicDetails()
    while True:
        query = takeCommand().lower()

        # searching on wikipedia
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        #capabilities of CyberPal
        elif 'can you do' in query:
            speak('I can open websites like Youtube, Google, Wikipedia and Music Player. Let me inform you todays time and date. What else am I forgetting? ')
            speak('Yes, I can ask you Riddles, tell you a joke and can suggest you some random activity.')
            speak("Well, I can even search on youtube and google too, which you want me to.")
            speak('I am at your service'+name)

        #search on youtube
        elif 'search on youtube' in query:
            innerquery = query.replace("search on youtube", "")
            speak("Searching "+innerquery)
            webbrowser.open("https://www.youtube.com/results?search_query="+innerquery)

        #opening youtube
        elif 'open youtube' in query:
            speak("Opening Youtube")
            webbrowser.open("youtube.com")

        #opening google web browser
        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("google.com")

        #opening music player
        elif 'open music player' in query:
            speak("Opening WYNk player")
            webbrowser.open("https://wynk.in/music")  

        #time
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        #suggest random activity
        elif 'random activity' in query:
            speak("Let's see What "+name+" should do")
            response = requests.get('https://www.boredapi.com/api/activity')
            data=response.json()
            print(data['activity'])
            speak(data['activity'])

        #riddles
        elif 'riddle' in query:
            speak("Let's see if "+name+" can answer this")
            response = requests.get('https://riddles-api.vercel.app/random')
            data=response.json()
            print(data['riddle'])
            speak(data['riddle'])
            print("You have 10 seconds to guess the answer")
            speak("You have 10 seconds to guess the answer")
            
            time.sleep(10)
            print("here is the answer")
            print(data["answer"])
            speak(data["answer"])
        
        #random joke
        elif 'joke' in query:
            speak("This one specially for you "+name)
            response = requests.get('https://icanhazdadjoke.com/slack')
            data=response.json()
            jokeText=str(data['attachments'])
            joke=jokeText[jokeText.find('text')+6:-2]
            print(joke)
            speak(joke)

        #new functionality added for multiple email addresses
        #for eg: send an email to Riya
        #it splits the command giving, ['send','an','email','to','Riya']
        #it takes the last item in the list, i.e. the name and sends the email correspondigly
        #change the sender's name and email address accordingly
        elif 'email to' in query:
            try:
                ename = query.split()[-1]
                speak("What should I say?")
                content = takeCommand()
                to = emails[ename]  
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend "+name+" I am not able to send this email")

         #function for 2 volume up
        elif 'volume up' in query:
            pyautogui.press('volumeup')

        #function for 2 volume down
        elif 'volume down' in query:
            pyautogui.press('volumedown')

        #function for mute and unmute
        elif 'mute' in query:
            pyautogui.press('volumemute')

        #function to set volume to full
        elif (('full volume' in query) or ('volume to full' in query)):
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevel(0.0, None)

        #function to quit the program
        elif 'quit' in query:
            exit()

        else:
            speak("Searching "+query)
            webbrowser.open("https://www.google.com/search?q="+query)
        
                
