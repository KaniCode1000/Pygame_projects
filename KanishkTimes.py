#password is KanishkTimes
import requests
import json
from win32com.client import Dispatch
def speak(str):
    
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(str)

if __name__ == '__main__':
    
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
            if not i >= len(newskadict['articles']):
                speak("Moving on to the next news..")
                i = i+1
                continue
        
        break
    speak("Oh!...There are no more news update.")
    speak("Thanks for tuning in to KanishkTimes...Hope you had a nice time.")