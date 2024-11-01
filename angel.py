import wikipedia  # pip install wikipedia
import requests
import pyttsx3
import datetime
from datetime import date
import speech_recognition as sr
import smtplib
import webbrowser as wb
import os
import psutil
import pyjokes
import pyautogui
import random
import wolframalpha
import cv2
import numpy as np
from playsound import playsound

today = date.today()
r = sr.Recognizer()
engine = pyttsx3.init('sapi5')
wolframalpha_app_id = "J3PX89-PL3RW48LPJ"  # Replace with your Wolfram Alpha App ID
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Directory to save screenshots
screenshot_dir = "E:\\test1"
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time_():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is")
    speak(Time)

def date_():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    speak("The current date is")
    speak(day)
    speak(month)
    speak(year)

def wishme():
    speak("Welcome back sir")
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning! I am Angel, how can I help you, sir?")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon! I am Angel, how can I help you, sir?")
    else:
        speak("Good Evening! I am Angel, how can I help you, sir?")

def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.energy_threshold = 500
        r.dynamic_energy_threshold = False
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')
        server.sendmail('your_email@gmail.com', to, content)
        server.close()
        speak("Email has been sent.")
    except Exception as e:
        speak("Unable to send email.")

def screenshot():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
    img = pyautogui.screenshot()
    img.save(screenshot_path)
    speak("Screenshot taken.")

def show_screenshot():
    screenshots = sorted(os.listdir(screenshot_dir), reverse=True)
    if screenshots:
        latest_screenshot = os.path.join(screenshot_dir, screenshots[0])
        os.startfile(screenshot_dir)  # Opens the folder
        os.startfile(latest_screenshot)  # Opens the latest screenshot
        speak("Here is the latest screenshot.")
    else:
        speak("No screenshots available to show.")

def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU is at ' + usage)
    battery = psutil.sensors_battery()
    speak('Battery is at')
    speak(battery.percent)

def joke():
    speak(pyjokes.get_joke())

def close_tab():
    pyautogui.hotkey('ctrl', 'w')
    speak("Closed the current tab.")

def close_application(app_name):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name'] == app_name:
            proc.terminate()  # Use terminate instead of os.kill
            speak(f"{app_name} has been closed.")
            return
    speak(f"No running instance of {app_name} found.")

# Main program loop
if __name__ == "__main__":
    wishme()

    while True:
        query = TakeCommand().lower()

        if 'time' in query:
            time_()
        elif 'date' in query:
            date_()
        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(result)
            speak(result)
        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = TakeCommand()
                speak('Who is the receiver?')
                receiver = input("Enter Receiver's Email: ")
                sendEmail(receiver, content)
            except Exception as e:
                speak("Unable to send Email.")
        elif 'open chrome' in query:
            speak('What should I search?')
            chromepath = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            search = TakeCommand().lower()
            wb.get(chromepath).open_new_tab(search + '.com')
        elif 'cpu' in query:
            cpu()
        elif 'joke' in query:
            joke()
        elif 'go offline' in query:
            speak("Going offline, sir.")
            quit()
        elif 'screenshot' in query:
            screenshot()
        elif 'show screenshot' in query:
            show_screenshot()
        elif 'play song' in query:
            songs_dir = 'D:/desktop/songs'
            music = os.listdir(songs_dir)
            song = random.choice(music)
            os.startfile(os.path.join(songs_dir, song))
        elif 'open youtube' in query:
            speak('What should I search?')
            search_Term = TakeCommand().lower()
            wb.open(f'https://www.youtube.com/results?search_query={search_Term}')
        elif 'open google' in query:
            speak("What should I search?")
            search_Term = TakeCommand().lower()
            wb.open(f'https://www.google.com/search?q={search_Term}')
        elif 'where is' in query:
            query = query.replace("where is", "")
            location = query
            speak("User asked to locate " + location)
            wb.open_new_tab("https://www.google.com/maps/place/" + location)
        elif 'calculate' in query:
            client = wolframalpha.Client(wolframalpha_app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            speak(f'The answer is {answer}')
        elif 'who is' in query or 'what is' in query:
            client = wolframalpha.Client(wolframalpha_app_id)
            res = client.query(query)
            try:
                answer = next(res.results).text
                speak(answer)
            except StopIteration:
                speak("No results found.")
        elif 'close tab' in query:
            close_tab()
        elif 'close chrome' in query:
            close_application('chrome.exe')
        else:
            speak("I didn't understand. Can you repeat that, please?")
