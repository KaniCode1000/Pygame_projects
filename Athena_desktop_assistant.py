import pyttsx3
import datetime
from random import randint
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import requests
import json

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def salutation():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!!")
    elif hour>=12 and hour<17:
        speak('Good Afternoon!!')
    else:
        speak('Good Evening!!')
    speak("I am Athena. How can I be of your service")

def takerequests():
    vr= sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        vr.pause_threshold = 1
        
        #READ THIS(pause threshold)!!
        audio = vr.listen(source)
        audio = vr.listen(source)
    try:
        print("Recognizing....")
        query = vr.recognize_google(audio, language = 'en-in')
        print(f"User said: {query}\n")
        
    except Exception as e:
        # print(e)
        
        print("Say that again please....")
        return "None"
    return query

if __name__== '__main__':
    salutation()
    speak("Please tell me your name for a better experience")
    user = input("Enter your name!\n")
    while True:
        
        query = takerequests().lower()    
        #Task execution
        if 'wikipedia' in query:
            speak('Searching Wikipedia....')
            query = query.replace("wikipedia","")
            result = wikipedia.summary(query, sentences = 3)
            speak('According to wikipedia')
            print(result)
            speak(result)
        elif 'hello' in query:
            speak(f'hello {user}')
        elif 'open youtube' in query:
            google = 'youtube.com'
            webbrowser.open_new_tab('http://www.google.com/search?btnG=1&q=%s' % google)
        elif 'open google' in query:
            webbrowser.open_new_tab('http://www.google.com/search?btnG=1&q=%s'%'google.com')
        elif 'open stackoverflow' in query:
            webbrowser.open_new_tab('http://www.google.com/search?btnG=1&q=%s'%'stackoverflow.com')
        elif 'open twitch' in query:
            webbrowser.open_new_tab('http://www.google.com/search?btnG=1&q=%s'%'twitch.tv')
        elif 'open code with harry' in query:
            webbrowser.open_new_tab('http://www.google.com/search?btnG=1&q=%s'%'codewithharry.com')
        elif 'open chess' in query:
            webbrowser.open_new_tab('http://www.google.com/search?btnG=1&q=%s'%'chess.com')
        elif 'open lichess' in query:
            webbrowser.open_new_tab('http://www.google.com/search?btnG=1&q=%s'%'lichess.org')
        elif 'open gmail' in query:
            webbrowser.open_new_tab('http://www.google.com/search?btnG=1&q=%s'%'gmail.com')
        elif 'weather' in query:
            webbrowser.open_new_tab('http://www.google.com/search?btnG=1&q=%s'%'https://weather.com/en-IN/weather/today/l/28.70,77.10?par=google&temp=c')
        elif 'play music' in query:
            music_dir = 'C:\\Users\\Goutam\\Desktop\\music'
            songs = os.listdir(music_dir)
            randomsong = randint(0,len(songs)-1)
            ranlist = []
            ranlist.append(randomsong)
            for i in ranlist:
                if i==randomsong:
                    randomsong+=1
                    continue
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[randomsong]))
        elif 'the time' in query:
            stringtime = datetime.datetime.now().strftime("%H;%M:%S")
            speak(f"The time is {stringtime}")
        elif 'open visual studio code' in query:
            codePath = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Code.exe"
            os.startfile(codePath)
        elif 'news' in query:
            speak("News for today..exclusively on KanishkTimes.....Lets begin")
            url = "https://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=49e391e7066c4158937096fb5e55fb5d"
            news = requests.get(url).text
            newskadict = json.loads(news) 
            arcle = newskadict['articles']
            i = 1
            for article in arcle:
                speak(article['title'])
                print(f"{i}.{article['title']}")
                speak("If you want in detail...write d, if you want to quit write q otherwise press enter")
                input_ = input("\nDo you want in detail? \n")
                if input_ == "d":
                    speak(article['description'])
                    print(article['description'])
                    speak("Moving on to the next news..")
                    i = i+1
                    continue
                elif input_ == "q":
                    break
                else:
                    speak("Moving on to the next news..")
                    i = i+1
                    continue
            speak("Thanks for tuning in to KanishkTimes...Hope you had a nice time.")
        elif "thanks" or "bye" in query:
            speak("Happy to help")
            break
        elif query != "none":
            webbrowser.open_new_tab('http://www.google.com/search?btnG=1&q=%s'% query)
        else:
            speak("Say that again please")
            
            