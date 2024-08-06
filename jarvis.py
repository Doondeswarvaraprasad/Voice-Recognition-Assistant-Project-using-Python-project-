import pyttsx3
import pandas as pd
import numpy as np
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import subprocess
import requests

engine = pyttsx3.init()
CHROME_PATH = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
CHROME_SHORTCUT_PATH = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome.lnk"
MUSIC_DIR = os.path.expanduser("~\\Music")
SCREENSHOT_PATH = os.path.expanduser(
    r"C:\Users\Doondeswarvaraprasad\OneDrive - K L University\Pictures\Screenshots\ss.png")
DATA_FILE = "data.txt"
DOCUMENTS_PATH = os.path.expanduser(r"C:\Users\Doondeswarvaraprasad\OneDrive - K L University\Documents")
APP_PATHS = {
    "notepad": "C:\\Windows\\system32\\notepad.exe",
    "calculator": "C:\\Windows\\system32\\calc.exe",
    "chrome": CHROME_PATH,
}
WEATHER_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your OpenWeatherMap API key
CITY_NAME = "your_city_name"  # Replace with your city name


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def get_time():
    return datetime.datetime.now().strftime("%I:%M:%S")


def get_date():
    now = datetime.datetime.now()
    return now.day, now.month, now.year


def tell_time():
    current_time = get_time()
    speak("The current time is")
    speak(current_time)
    print("The current time is ", current_time)


def tell_date():
    day, month, year = get_date()
    speak("The current date is")
    speak(f"{day} {month} {year}")
    print(f"The current date is {day}/{month}/{year}")


def wish_me():
    hour = datetime.datetime.now().hour
    now = datetime.datetime.now()
    weekday = now.strftime("%A")
    day, month, year = get_date()

    print("Welcome back! How can I assist you today?")
    speak("Welcome back! How can I assist you today?")

    if 4 <= hour < 12:
        speak(f"Good morning! Today is {weekday}, {day} of {month}, {year}. Hope you have a productive day ahead.")
        print(f"Good morning! Today is {weekday}, {day} of {month}, {year}. Hope you have a productive day ahead.")
    elif 12 <= hour < 16:
        speak(f"Good afternoon! It's {weekday}, {day} of {month}, {year}. How's your day going so far?")
        print(f"Good afternoon! It's {weekday}, {day} of {month}, {year}. How's your day going so far?")
    elif 16 <= hour < 20:
        speak(f"Good evening! Today is {weekday}, {day} of {month}, {year}. How was your day?")
        print(f"Good evening! Today is {weekday}, {day} of {month}, {year}. How was your day?")
    else:
        speak(f"Hello! Today is {weekday}, {day} of {month}, {year}. How can I help you this late?")
        print(f"Hello! Today is {weekday}, {day} of {month}, {year}. How can I help you this late?")

    speak("Jarvis at your service, please tell me how may I help you.")
    print("Jarvis at your service, please tell me how may I help you.")


def take_screenshot():
    img = pyautogui.screenshot()
    img.save(SCREENSHOT_PATH)
    speak("I've taken the screenshot, please check it.")
    print(f"Screenshot saved at {SCREENSHOT_PATH}")


def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-in")
        print(query)
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        speak("Please say that again.")
        return "Try Again"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        speak("I'm having trouble understanding you. Please try again later.")
        return "Try Again"

    return query.lower()


def open_chrome():
    if os.path.exists(CHROME_SHORTCUT_PATH):
        os.startfile(CHROME_SHORTCUT_PATH)
    else:
        speak("Chrome shortcut not found.")


def search_on_chrome():
    try:
        speak("What should I search?")
        print("What should I search?")
        search_query = take_command()
        wb.get(CHROME_PATH).open_new_tab(f"https://www.google.com/search?q={search_query}")
        print(search_query)
    except Exception as e:
        print(f"Error: {e}")
        speak("Can't open now, please try again later.")


def remember_data(data):
    with open(DATA_FILE, "w") as remember_file:
        remember_file.write(data)
    speak("You told me to remember that " + data)
    print("You told me to remember that " + data)


def recall_data():
    try:
        with open(DATA_FILE, "r") as remember_file:
            data = remember_file.read()
            speak("You told me to remember that " + data)
            print("You told me to remember that " + data)
    except FileNotFoundError:
        speak("I don't have any data to remember.")


def open_documents():
    if os.path.exists(DOCUMENTS_PATH):
        os.startfile(DOCUMENTS_PATH)
        speak("Opening your Documents folder.")
        print("Opening your Documents folder.")
    else:
        speak("Documents folder not found.")


def open_application(app_name):
    app_path = APP_PATHS.get(app_name.lower())
    if app_path and os.path.exists(app_path):
        os.startfile(app_path)
        speak(f"Opening {app_name}.")
        print(f"Opening {app_name}.")
    else:
        speak(f"Application {app_name} not found.")
        print(f"Application {app_name} not found.")


def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        weather_data = response.json()

        if weather_data["cod"] == 200:
            temp = weather_data["main"]["temp"]
            weather_desc = weather_data["weather"][0]["description"]
            speak(f"The current temperature is {temp} degrees Celsius with {weather_desc}.")
            print(f"The current temperature is {temp} degrees Celsius with {weather_desc}.")
        else:
            speak("I couldn't fetch the weather information.")
    except Exception as e:
        print(f"Error: {e}")
        speak("Couldn't retrieve weather information.")


def main():
    wish_me()
    online = True
    while online:
        query = take_command()
        if "time" in query:
            tell_time()
        elif "date" in query:
            tell_date()
        elif "who are you" in query:
            speak("I'm JARVIS created by Mr. Doondeswar, and I'm a desktop voice assistant.")
            print("I'm JARVIS created by Mr. Doondeswar, and I'm a desktop voice assistant.")
        elif "how are you" in query:
            speak("I'm fine sir, What about you?")
            print("I'm fine sir, What about you?")
        elif "fine" in query or "good" in query:
            speak("Glad to hear that sir!!")
            print("Glad to hear that sir!!")
        elif "let's be friends" in query:
            speak("You are always a good friend of mine, sir!!")
            print("You are always a good friend of mine, sir!!\n")
        elif "wikipedia" in query:
            try:
                speak("Ok wait sir, I'm searching...")
                query = query.replace("wikipedia", "")
                result = wikipedia.summary(query, sentences=2)
                print(result)
                speak(result)
            except Exception:
                speak("Can't find this page sir, please ask something else.")
        elif "open youtube" in query:
            wb.open("https://www.youtube.com")
        elif "open google" in query:
            wb.open("https://www.google.com")
        elif "open stack overflow" in query:
            wb.open("https://stackoverflow.com")

        elif "open instagram" in query:
            wb.open("https://www.instagram.com")
        elif "cricket score" in query:
            wb.open("https://www.cricbuzz.com")
        elif "open whatsapp" in query:
            wb.open("https://web.whatsapp.com/")
        elif "play music" in query:
            try:
                songs = os.listdir(MUSIC_DIR)
                if songs:
                    song = random.choice(songs)
                    os.startfile(os.path.join(MUSIC_DIR, song))
                    print(f"Playing {song}")
                else:
                    speak("No music files found in your music directory.")
            except FileNotFoundError:
                speak("Music directory not found.")
        elif "open chrome" in query:
            open_chrome()
        elif "search on chrome" in query:
            search_on_chrome()
        elif "remember" in query:
            speak("What should I remember?")
            data = take_command()
            remember_data(data)
        elif "recall" in query:
            recall_data()
        elif "screenshot" in query:
            take_screenshot()
        elif "open documents" in query:
            open_documents()
        elif "open notepad" in query:
            open_application("notepad")
        elif "open calculator" in query:
            open_application("calculator")
        elif "weather" in query:
            get_weather()
        elif "offline" in query:
            speak("Going offline. Have a great day!")
            online = False
        else:
            speak("Sorry, I didn't understand that. Please try again.")
            print("Sorry, I didn't understand that. Please try again.")


if __name__ == "__main__":
    main()
