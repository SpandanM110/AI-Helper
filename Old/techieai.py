import pyttsx3
import pywin32_system32
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import requests
import threading


engine = pyttsx3.init()

def change_name():
    speak("What would you like to call me, sir?")
    new_name = takecommand(name)

    with open("name.txt", "w") as file:
        file.write(new_name)
    speak(f"Thank you for giving me a new name, sir. You can now call me {new_name}.")

def load_name():
    try:
        with open("name.txt", "r") as file:
            name = file.readline()
            if name:
                return name.strip()
            else:
                return "Techie"
    except FileNotFoundError:
        return "Techie"

def list_reminders():
    with open("reminders.txt", "r") as file:
        reminders = file.readlines()
        if reminders:
            speak("Here are your reminders:")
            for reminder in reminders:
                speak(reminder)
                print(reminder.strip())
        else:
            speak("You have no reminders.")

def ask_reminder():
    speak("Which reminder would you like to know about?")
    query = takecommand()
    with open("reminders.txt", "r") as file:
        reminders = file.readlines()
        found = False
        for reminder in reminders:
            if query in reminder:
                speak(f"Your reminder is: {reminder}")
                print(f"Your reminder is: {reminder}")
                found = True
                break
        if not found:
            speak("Sorry, I couldn't find that reminder.")

def edit_reminder():
    speak("Which reminder would you like to edit?")
    query = takecommand()
    with open("reminders.txt", "r") as file:
        reminders = file.readlines()
    found = False
    for i, reminder in enumerate(reminders):
        if query in reminder:
            speak("What would you like to change the reminder to?")
            new_reminder = takecommand()
            reminders[i] = new_reminder + '\n'
            speak("Reminder edited successfully.")
            found = True
            break
    if not found:
        speak("Sorry, I couldn't find that reminder.")
    with open("reminders.txt", "w") as file:
        file.writelines(reminders)




def set_reminder():
    speak("What should I remind you about?")
    reminder_msg = takecommand()
    speak("At what time should I remind you? Please specify the hour.")
    hour = int(takecommand())
    speak("Please specify the minute.")
    minute = int(takecommand())

    current_time = datetime.datetime.now()
    reminder_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)

    while current_time > reminder_time:
        speak("The time you've entered has already passed. Please enter a future time.")
        speak("At what time should I remind you? Please specify the hour.")
        hour = int(takecommand())
        speak("Please specify the minute.")
        minute = int(takecommand())
        reminder_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)

    speak(f"I will remind you to {reminder_msg} at {hour} hour and {minute} minute.")
    print(f"I will remind you to {reminder_msg} at {hour}:{minute}.")

    # Save the reminder to the reminders.txt file
    with open("reminders.txt", "a") as file:
        file.write(f"Reminder: {reminder_msg} at {hour}:{minute}\n")

    # Calculate time difference to schedule the reminder
    delta = reminder_time - current_time
    seconds_before = delta.total_seconds() - 300  # 300 seconds = 5 minutes

    # Schedule the reminder using threading.Timer
    reminder_thread = threading.Timer(seconds_before, remind, args=[reminder_msg])
    reminder_thread.start()

def remind(reminder_msg):
    speak(f"Reminder: {reminder_msg}")
    print(f"Reminder: {reminder_msg}")






def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("the current time is")
    speak(Time)
    print("The current time is ", Time)

def get_weather(city):
    api_key = "67b1e51195f3ce0d32b98d31837c8665"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = city
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        weather = data["weather"][0]["description"]
        temperature = round(data["main"]["temp"] - 273.15, 2)  # Convert temperature from Kelvin to Celsius
        speak(f"The weather in {city} is {weather}. The temperature is {temperature} degrees Celsius.")
        print(f"The weather in {city} is {weather}. The temperature is {temperature} degrees Celsius.")
    else:
        speak("City not found.")


def date():
    day = int(datetime.datetime.now().day)
    month = int(datetime.datetime.now().month)
    year = int(datetime.datetime.now().year)
    speak("the current date is")
    speak(day)
    speak(month)
    speak(year)
    print("The current date is " + str(day) + "/" + str(month) + "/" + str(year))

def wishme(name):
    print("Welcome back sir!!")
    speak("Welcome back sir!!")
    
    hour = datetime.datetime.now().hour
    if hour >= 4 and hour < 12:
        speak(f"Good Morning {name}!!")
        print(f"Good Morning {name}!!")
    elif hour >= 12 and hour < 16:
        speak(f"Good Afternoon {name}!!")
        print(f"Good Afternoon {name}!!")
    elif hour >= 16 and hour < 24:
        speak(f"Good Evening {name}!!")
        print(f"Good Evening {name}!!")
    else:
        speak(f"Good Night {name}, See You Tommorrow")

    speak(f"{name} at your service sir, please tell me how may I help you.")
    print(f"{name} at your service sir, please tell me how may I help you.")


def screenshot():
    img = pyautogui.screenshot()
    img_dir = os.path.expanduser("~\\Pictures\\")
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    img_path = os.path.join(img_dir, "ss.png")
    img.save(img_path)
    speak("Screenshot captured successfully.")

def takecommand(name):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"{name}: Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print(f"{name}: Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(query)

    except Exception as e:
        print(e)
        speak("Please say that again")
        return "Try Again"

    return query

if __name__ == "__main__":
    name = load_name()
    wishme(name)
    while True:
        query = takecommand(name).lower()
        if name.lower() in query:
            query = query.replace(name.lower(), "")  # Remove the name from the query
            if "time" in query:
                time()

            elif "date" in query:
                date()

            elif "who are you" in query:
                speak(f"I'm {name} created by Spandan and I'm a desktop voice assistant and a Mate.")
                print(f"I'm {name} created by Spandan and I'm a desktop voice assistant and a Mate.")

            # Add other commands here with the modified name check


        elif "fine" in query:
            speak("Glad to hear that sir!!")
            print("Glad to hear that sir!!")

        elif "good" in query:
            speak("Glad to hear that sir!!")
            print("Glad to hear that sir!!")

        elif "wikipedia" in query:
            try:
                speak("Ok wait sir, I'm searching...")
                query = query.replace("wikipedia","")
                result = wikipedia.summary(query, sentences=2)
                print(result)
                speak(result)
            except:
                speak("Can't find this page sir, please ask something else")
        
        elif "open youtube" in query:
            wb.open("youtube.com") 

        elif "open google" in query:
            wb.open("google.com") 
   
        elif "open stack overflow" in query:
            wb.open("stackoverflow.com")

        elif "play music" in query:
            song_dir = os.path.expanduser("~\\Music")
            songs = os.listdir(song_dir)
            print(songs)
            x = len(songs)
            y = random.randint(0,x)
            os.startfile(os.path.join(song_dir, songs[y]))

        elif "open chrome" in query:
            chromePath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\chrome.exe"
            os.startfile(chromePath)

        elif "search on chrome" in query:
            try:
                speak("What should I search?")
                print("What should I search?")
                chromePath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\chrome.exe"
                search = takecommand()
                wb.get(chromePath).open_new_tab(search)
                print(search)

            except Exception as e:
                speak("Can't open now, please try again later.")
                print("Can't open now, please try again later.")
            
        
        elif "remember that" in query:
            speak("What should I remember")
            data = takecommand(name)

            speak("You said me to remember that" + data)
            print("You said me to remember that " + str(data))
            remember = open("data.txt", "w")
            remember.write(data)
            remember.close()

        elif "do you remember anything" in query:
            remember = open("data.txt", "r")
            speak("You told me to remember that" + remember.read())
            print("You told me to remember that " + str(remember))

        elif "screenshot" in query:
            screenshot()
            speak("I've taken screenshot, please check it")

        elif "weather in" in query:
            city = query.split("in", 1)[1].strip()
            get_weather(city)

        elif "set reminder" in query:
            set_reminder()


        elif "list reminders" in query:
            list_reminders()

        elif "ask reminder" in query:
            ask_reminder()
        
        elif "edit reminder" in query:
            edit_reminder()

        elif "change your name" in query:
            change_name()
        
        
    


        elif "offline" in query:
            quit()

