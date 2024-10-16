import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib

from decouple import config
from groq import Groq

client = Groq()

# Load email credentials from environment variables
EMAIL = config('EMAIL')
PASSWORD = config('PASSWORD')
GROQ_API_KEY = config('GROQ_API_KEY')
YOUR_NEWSAPI_KEY=config('YOUR_NEWSAPI_KEY')

def find_my_ip():
    """Fetch the public IP address of the machine."""
    try:
        ip_address = requests.get('https://api.ipify.org?format=json').json()
        return ip_address["ip"]
    except Exception:
        return None

def search_on_wikipedia(query):
    """Search for a query on Wikipedia and return a summary."""
    try:
        results = wikipedia.summary(query, sentences=2)
        return results
    except Exception:
        return "No results found."
    


def search_on_google(query):
    """Search for a query on Google using pywhatkit."""
    try:
        kit.search(query)
    except Exception:
        pass

def youtube(video):
    """Play a YouTube video using pywhatkit."""
    try:
        kit.playonyt(video)
    except Exception:
        pass
    
def send_email(receiver_add, subject, message):
    """Send an email using the provided details."""
    try:
        email = EmailMessage()
        email['To'] = receiver_add
        email['Subject'] = subject
        email['From'] = EMAIL
        email.set_content(message)
        
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception:
        return False 

def get_news():
    """Fetch the latest news headlines."""
    try:
        news_headlines = []
        result = requests.get("https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=728454940f314b218618d18e93b1aaf4").json()
        articles = result["articles"]
        for article in articles:
            news_headlines.append(article["title"])
        return news_headlines[:6]
    except Exception:
        return ["No news found."]

def weather_forecast(city):
    """Fetch the weather forecast for a given city."""
    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={"a374279117418158bd02c9cef1b09acd"}&units=metric"
        )
        response.raise_for_status()  # Raise an HTTPError for bad responses
        res = response.json()

        if 'weather' in res and 'main' in res:
            weather = res["weather"][0]["main"]
            temp = res["main"]["temp"]
            feels_like = res["main"]["feels_like"]
            return weather, f"{temp}°C", f"{feels_like}°C"
        else:
            return None, None, None
    except requests.exceptions.RequestException:
        return None, None, None


def execute(prompt):
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    response = ''
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    print(response)

    return response