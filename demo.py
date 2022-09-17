import pyttsx3 # for text to speech
from datetime import datetime # for time
import speech_recognition as user_audio # user input by voice
import pyaudio
import os
import subprocess as sp

import requests
import wikipedia
import pywhatkit as kit
import webbrowser 
import smtplib


USERNAME = 'AYUSH'
BOTNAME = 'ALEXA'


# main engine
engine = pyttsx3.init()

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
# print (rate)                        #printing current voice rate
engine.setProperty('rate', 121)     # setting up new voice rate


"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

# for i in voices:
#     print(i.id)

"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
# print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1



# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""
    
    engine.say(text)
    engine.runAndWait()
    

def greet_user():
    """Greets the user according to the time"""
    
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")
    

# greet_user()
def sendEmail(to, content):
    smtplib = any
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('divyanshusahucoc@gmail.com', 'your-password')
    server.sendmail('divyashusahu@gmail.com', to, content)
    server.close()
    



def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

    r = user_audio.Recognizer()
    with user_audio.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1 # limit of audio # time for audio capturing
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        if not 'exit' in query or 'stop' in query:
            speak(query)
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night sir, take care!")
            else:
                speak('Have a good day sir!')
            exit()
    except Exception:
        speak('Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    return query


# take_user_input()




paths = {
    'notepad': "C:\\Windows\\notepad.exe",
    
    'calculator': "C:\\Windows\\System32\\calc.exe"
}

def open_notepad():
    os.startfile(paths['notepad'])

def open_cmd():
    os.system('start cmd')
  
def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)  
    
def open_calculator():
    sp.Popen(paths['calculator'])
    
def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results
def search_on_google(query):
    kit.search(query)

def  weather_forcast(city):
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=11112d61dad6beb077f4c80f5b7b4156&units=metric").json()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"

    
if __name__ == '__main__':
   
    greet_user()
    while True:
        query = take_user_input().lower()

        if 'open notepad' in query:
            open_notepad()
            
        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()
        elif 'open camera' in query:
            open_camera()    
          
        elif 'open calculator' in query:
            open_calculator()    
          
        elif 'exit' in query or 'quit' in query:
           exit()
        elif 'wikipedia' in query:
            speak('What do you want to search on Wikipedia, sir?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"According to Wikipedia, {results}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(results)
        
        elif 'youtube' in query:
            search_on_google("youtube")
            exit()
        elif 'search on google' in query or 'search' in query:
            speak('What do you want to search on Google, sir?')
            query = take_user_input().lower()
            search_on_google(query)
            exit()
        elif 'send email' in query or 'email' in query:
                try:
                    speak("whome do you want to send email")
                    to = take_user_input().lower()
                    
                    speak("What should I say?")
                    content = take_user_input().lower()
                     
                    sendEmail(to, content)
                    speak("Email has been sent!")
                except Exception as e:
                   
                    speak("Sorry"+USERNAME+ "I am not able to send this email")
        elif 'weather' in query or 'weather report' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Getting weather report for your city {city}")
            weather, temperature, feels_like =  weather_forcast(city)
            speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            speak(f"Also, the weather report talks about {weather}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")
            
            
