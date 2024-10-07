import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import requests
import threading
from pdfminer.high_level import extract_text


import streamlit as st
from txtai.pipeline import Summary
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text
import webbrowser
from requests import get
import pyjokes


import pyttsx3
import speech_recognition as sr





st.set_page_config(layout="wide")

@st.cache_resource
def text_summary(text, maxlength=None):
    # Create summary instance
    summary = Summary()
    result = summary(text)
    return result

def extract_text_from_pdf(file_path):
    # Extract text from PDF using pdfminer
    text = extract_text(file_path)
    return text

def change_voice(voice_id):
    """
    Change the voice of the TTS engine.

    Args:
        voice_id (str): Identifier of the voice. Use 'sapi5', 'nsss', 'espeak', 'google', or 'pico'.
    """
    engine.setProperty('voice', voice_id)


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

def summarize_document():
    try:
        # Your existing code for document summarization
        st.subheader("Summarize Document using txtai")
        input_file = st.file_uploader("Upload your document here", type=['pdf'])
        if input_file is not None:
            if st.button("Summarize Document"):
                with open("doc_file.pdf", "wb") as f:
                    f.write(input_file.getbuffer())
                col1, col2 = st.columns([1,1])
                with col1:
                    st.info("File uploaded successfully")
                    extracted_text = extract_text_from_pdf("doc_file.pdf")
                    st.markdown("**Extracted Text is Below:**")
                    st.info(extracted_text)
                with col2:
                    st.markdown("**Summary Result**")
                    text = extract_text_from_pdf("doc_file.pdf")
                    doc_summary = text_summary(text)
                    st.success(doc_summary)
        else:
            st.error("No document uploaded.")
            doc_summary = "No document uploaded."  # Set a default value
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        doc_summary = "An error occurred during summarization."  # Set a default value

    return doc_summary



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

def news():
    api_key = '655cf0b44b9841c9b6fd80bdc8f3b87a'  # Replace this with your actual News API key
    main_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'

    try:
        main_page = requests.get(main_url).json()
        articles = main_page.get("articles", [])  # Use .get() to handle missing key gracefully

        if not articles:
            speak("No articles found.")
            return

        head = []
        day = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
        for i, ar in enumerate(articles[:len(day)]):
            head.append(ar.get("title", ""))
            speak(f"Today's {day[i]} news is: {head[i]}")

    except Exception as e:
        speak(f"An error occurred while fetching news: {e}")


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

def takeCommand(name, engine):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"{name}: Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print(f"{name}: Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")

        if "change voice to Google" in query:
            change_voice(engine, 'google')
            speak("Voice changed to Google Text-to-Speech API.")
        elif "change voice to Microsoft" in query:
            change_voice(engine, 'sapi5')
            speak("Voice changed to Microsoft Speech API 5.")
        elif "change voice to espeak" in query:
            change_voice(engine, 'espeak')
            speak("Voice changed to eSpeak.")
        elif "change voice to pico" in query:
            change_voice(engine, 'pico')
            speak("Voice changed to Pico TTS.")
        elif "change voice to default" in query:
            change_voice(engine, None)  # Set to None to use the default voice
            speak("Voice changed to default.")
        else:
            # Other commands
            pass

    except Exception as e:
        print(e)
        speak("Please say that again")
        return None

    return query.lower()


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

        elif "tell me news" in query:
            speak("Please wait Sir,fetching the latest news")
            news()

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
        
        elif "summarize text" in query or "summarise text " in query:
                st.subheader("Summarize Text using txtai")
                input_text = st.text_area("Enter your text here")
                if input_text is not None:
                    if st.button("Summarize Text"):
                        col1, col2 = st.columns([1,1])
                        with col1:
                            st.markdown("**Your Input Text**")
                            st.info(input_text)
                        with col2:
                            st.markdown("**Summary Result**")
                            result = text_summary(input_text)
                            st.success(result)

        elif "summarize document" in query or "summarise document" in query:
                summary_result = summarize_document()
                st.subheader("Summarize Document using txtai")
                input_file = st.file_uploader("Upload your document here", type=['pdf'])
                if input_file is not None:
                    if st.button("Summarize Document"):
                        with open("doc_file.pdf", "wb") as f:
                            f.write(input_file.getbuffer())
                        col1, col2 = st.columns([1,1])
                        with col1:
                            st.info("File uploaded successfully")
                            extracted_text = extract_text_from_pdf("doc_file.pdf")
                            st.markdown("**Extracted Text is Below:**")
                            st.info(extracted_text)
                        with col2:
                            st.markdown("**Summary Result**")
                            text = extract_text_from_pdf("doc_file.pdf")
                            doc_summary = text_summary(text)
                            st.success(doc_summary)

        elif 'open github' in query:
            webbrowser.open("https://www.github.com")
            speak("opening github")

        elif 'search on google' in query:
            speak("What would you like to search on google?")
            cm = takeCommand().lower()
            webbrowser.open(f"{cm}")

        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")
        
        
        elif "Tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "where i am" in query or "where are we" in query:
            speak("wait sir let me check")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                # print(geo_data)
                city = geo_data['city']
                state = geo_data['state']
                country = geo_data['country']
                speak(f"Sir im not sure, but we are in {city} city {state} state of {country} country")
            except Exception as e:
                speak("Sorry Sir, Due to network issue i am not able to find where we are.")
                pass
        
        elif "maximize the window" in query:
            pyautogui.hotkey('alt', 'space')
            time.sleep(0.1)
            pyautogui.press('x')

        elif "minimize the window" in query:
            pyautogui.hotkey('win', 'd')
            
        elif "google search" in query:
            query = query.replace("google search", "")
            pyautogui.hotkey('alt', 'd')
            pyautogui.write(f"{query}", 0.1)
            pyautogui.press('enter')

        elif "youtube search" in query:
            query = query.replace("youtube search", "")
            pyautogui.hotkey('alt', 'd')
            # time.sleep(1)
            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('tab')
            # time.sleep(1)
            pyautogui.write(f"{query}", 0.1)
            pyautogui.press('enter')

        elif "opem new window" in query:
            pyautogui.hotkey('ctrl', 'n')

        elif "open incognito window" in query:
            pyautogui.hotkey('ctrl', 'shift', 'n')
        
        elif "minimize this window" in query:
            pyautogui.hotkey('alt', 'space')
            time.sleep(1)
            pyautogui.press('n')

        elif "open history" in query:
            pyautogui.hotkey('ctrl', 'h')

        elif "open downloads" in query:
            pyautogui.hotkey('ctrl', 'j')

        elif "previous tab" in query:
            pyautogui.hotkey('ctrl', 'shift', 'tab')
        
        elif "next tab" in query:
            pyautogui.hotkey('ctrl', 'tab')

        elif "close tab" in query:
            pyautogui.hotkey('ctrl','shift' ,'w')

        elif "clear browsing history" in query:
            pyautogui.hotkey('ctrl', 'shift', 'delete')

        elif "offline" in query:
            quit()

# After commading the voice change it should continue to work in that voice