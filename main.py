import pyttsx3
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import imdb
import wolframalpha

from decouple import config
from datetime import datetime
from convy import get_random_response
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, send_email, get_news, weather_forecast,execute

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.0)  # volume levels from 0.0 to 1.0
engine.setProperty('rate', 220)  # speed of the speech
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # set voice to the first option (can be adjusted)

USER = config('USER')
HOSTNAME = config('BOT')


def speak(text):
    engine.say(text)
    engine.runAndWait()
    

def greet_me():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good morning {USER}")
    elif 12 <= hour <= 16:
        speak(f"Good afternoon {USER}")
    elif 16 <= hour < 19:
        speak(f"Good evening {USER}")
    speak(f"I am {HOSTNAME}. How may I assist you, {USER}?")


listening = False


def start_listening():
    global listening
    listening = True
    print("Started listening")


def pause_listening():
    global listening
    listening = False
    print("Stopped listening")


keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 2
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(query)
        if 'stop' in query or 'exit' in query:
            hour = datetime.now().hour
            if 21 <= hour or hour < 6:
                speak("Good night, sir. Take care!")
            else:
                speak("Have a good day, sir!")
            exit()
        else:
            speak(get_random_response('acknowledgment'))
    except Exception:
        speak(get_random_response('error'))
        return 'None'
    return query


if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you" in query:
                speak("I am absolutely fine, sir. What about you?")
            elif "open command prompt" in query:
                speak("Opening Command Prompt")
                os.system('start cmd')
                speak(get_random_response('confirmation'))

            elif "open camera" in query:
                speak("Opening camera, sir")
                sp.run('start microsoft.windows.camera:', shell=True)
                speak(get_random_response('confirmation'))
 
            elif "open notepad" in query:
                speak("Opening Notepad for you, sir")
                notepad_path = "C:\\Windows\\notepad.exe"
                os.startfile(notepad_path)
                speak(get_random_response('confirmation'))
                
            elif "open studio" in query:
                speak("Opening DaVinci Studio for you, sir")
                davinci_path = "E:\\Editing\\setup\\Resolve.exe"
                os.startfile(davinci_path)
                speak(get_random_response('confirmation'))
            
            elif 'ip address' in query:
                ip_address = find_my_ip()
                if ip_address:
                    speak(f'Your IP Address is {ip_address}. For your convenience, I am printing it on the screen, sir.')
                    print(f'Your IP Address is {ip_address}')
                else:
                    speak("I couldn't fetch your IP address. Please try again.")
                
            elif "open youtube" in query:
                speak("What do you want to play on YouTube, sir?")
                video = take_command().lower()
                youtube(video)
                speak(get_random_response('confirmation'))

            elif "open google" in query:
                speak(f"What do you want to search on Google, {USER}?")
                search_query = take_command().lower()
                search_on_google(search_query)
                speak(get_random_response('confirmation'))

            elif "open wikipedia" in query:
                speak("What do you want to search on Wikipedia, sir?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to Wikipedia, {results}")
                speak("I am printing it on the terminal")
                print(results)
            
            elif "send an email" in query:
                speak("On what email address do you want to send, sir? Please enter it in the terminal.")
                receiver_add = input("Email address: ")
                speak("What should be the subject, sir?")
                subject = take_command().capitalize()
                speak("What is the message?")
                message = take_command().capitalize()
                if send_email(receiver_add, subject, message):
                    speak("I have sent the email, sir.")
                    print("I have sent the email, sir.")
                else:
                    speak("Something went wrong. Please check the error log.")
                    
            elif " news" in query:
                speak(f"I am reading out the latest headlines of today, sir.")
                news = get_news()
                for headline in news:
                    speak(headline)
                speak("I am printing them on the screen, sir.")
                print(*news, sep='\n')
                
            elif 'weather' in query:
                speak("Tell me the name of your city.")
                city = take_command().capitalize()
                speak(f"Getting weather report for {city}.")
                weather, temp, feels_like = weather_forecast(city)
                if weather and temp and feels_like:
                    speak(f"The current temperature is {temp}, but it feels like {feels_like}. Also, the weather report talks about {weather}.")
                    speak("For your convenience, I am printing it on the screen, sir.")
                    print(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")
                else:
                    speak("I couldn't fetch the weather details. Please check the city name and try again.")
                    
            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Please tell me the movie name:")
                movie_name = take_command().lower()
                if movie_name != 'None':
                    speak(f"Searching for {movie_name}")
                    movies = movies_db.search_movie(movie_name)
                    if movies:
                        speak("I found these:")
                        for movie in movies[:5]:  # Limiting to top 5 results
                            title = movie.get("title")
                            year = movie.get("year")
                            speak(f"{title} - {year}")
                            movie_info = movies_db.get_movie(movie.movieID)
                            rating = movie_info.get("rating", "N/A")
                            cast = movie_info.get("cast", [])[:5]
                            actors = ', '.join([str(actor) for actor in cast])
                            plot = movie_info.get('plot outline', 'Plot summary not available')
                            speak(f"{title} was released in {year} and has IMDb ratings of {rating}. It has a cast of {actors}. The plot summary of the movie is {plot}")
                            print(f"{title} was released in {year} and has IMDb ratings of {rating}.\nIt has a cast of {actors}.\nThe plot summary of the movie is {plot}")
                    else:
                        speak("Sorry, I couldn't find any movies by that name.")
                else:
                    speak("Sorry, I didn't catch the movie name. Please try again.")
                    
            elif "calculate" in query:
                app_id = config("WOLFRAMALPHA_APP_ID")
                client = wolframalpha.Client(app_id)
                try:
                    ind = query.lower().split().index("calculate")
                    text = query.split()[ind + 1:]
                    result = client.query(" ".join(text))
                    ans = next(result.results).text
                    speak("The answer is " + ans)
                    print("The answer is " + ans)
                except Exception:
                    speak("I couldn't find that. Please try again.")
                            
            elif "ask" in query:
                speak("I can answer any question for you. What do you want to ask?")
                question = take_command().lower()
                try:
                    answer = execute(question)
                    speak("The answer is " + answer)
                    print("The answer is " + answer)
                except Exception:
                    speak("I couldn't find that. Please try again.")
            else:
                speak("Sorry, I didn't understand that. Can you please repeat?") 