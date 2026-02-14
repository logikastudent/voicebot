import asyncio
import speech_recognition as sr
import subprocess
import webbrowser
import urllib.parse
import customtkinter as ctk
import python_weather
from threading import Thread
import datetime
import pyttsx3
import os
import random

# ================== Налаштування GUI ==================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ================== Голосовий розпізнавач ==================
recognizer = sr.Recognizer()

# ================== Голосовий вихід ==================
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def capture_voice_input():
    with sr.Microphone() as source:
        app.log("🎤 Слухаю...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
    return audio

def convert_speech_to_text(audio):
    try:
        text = recognizer.recognize_google(audio, language="uk-UA")
        app.log(f"🗣 Ви сказали: {text}")
        return text
    except sr.UnknownValueError:
        app.log("❌ Не вдалося розпізнати мову")
    except sr.RequestError as e:
        app.log(f"❌ Помилка сервісу: {e}")
    return ""

# ================== Погода ==================
async def get_weather(city):
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(city)
        msg = f"🌤 Погода у {city}: {weather.temperature}°C, стан: {weather.description}"
        app.log(msg)
        speak(msg)

# ================== Команди ==================
def open_program(name):
    paths = {
        "калькулятор": "calc",
        "хром": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "блокнот": "notepad",
    }
    path = paths.get(name)
    if path:
        try:
            subprocess.Popen(path)
            app.log(f"🟢 Відкрито {name}")
        except Exception as e:
            app.log(f"❌ Не вдалося відкрити {name}: {e}")

def tell_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    msg = f"🕒 Зараз {now}"
    app.log(msg)
    speak(msg)

def open_website(query, site="google"):
    if site == "google":
        url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
    elif site == "youtube":
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
    webbrowser.open(url)
    app.log(f"🌐 Відкрито {site} з пошуком: {query}")

def random_fun():
    jokes = [
        "Чому програмісти плутають Різдво і Хелловін? Бо Oct 31 = Dec 25!",
        "Я б хотів бути Wi-Fi, щоб бути завжди поруч із тобою.",
        "Що сказав нуль одиниці? «Привіт, друг!»"
    ]
    joke = random.choice(jokes)
    app.log(f"🤣 {joke}")
    speak(joke)

# ================== Обробка команд ==================
def process_voice_command(text):
    text_lower = text.lower()
    
    if "привіт" in text_lower:
        app.log("👋 Привіт! Як можу допомогти?")
        speak("Привіт! Як можу допомогти?")
    elif "як справи" in text_lower:
        app.log("😎 Все чітко, а у тебе?")
        speak("Все добре, а ти як?")
    elif "час" in text_lower:
        tell_time()
    elif "калькулятор" in text_lower or "хром" in text_lower or "блокнот" in text_lower:
        for prog in ["калькулятор", "хром", "блокнот"]:
            if prog in text_lower:
                open_program(prog)
                break
    elif "знайди відео" in text_lower:
        query = text_lower.replace("знайди відео", "").strip()
        if query:
            open_website(query, site="youtube")
    elif "знайди у гуглі" in text_lower or "знайди в гуглі" in text_lower:
        query = text_lower.replace("знайди у гуглі", "").replace("знайди в гуглі", "").strip()
        if query:
            open_website(query, site="google")
    elif "погода" in text_lower:
        city = text_lower.replace("погода", "").strip()
        if city == "":
            city = "Kyiv"
        app.log(f"🌦 Перевіряю погоду у {city}")
        asyncio.run(get_weather(city))
    elif "розкажи жарт" in text_lower or "жарт" in text_lower:
        random_fun()
    elif "вийти" in text_lower or "прощавай" in text_lower:
        app.log("👋 До побачення!")
        speak("До побачення!")
        app.stop()
    else:
        app.log("🤔 Команду не розпізнано")
        speak("Не розпізнав команду")

# ================== GUI ==================
class VoiceAssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Голосовий Асистент")
        self.geometry("500x500")
        
        self.textbox = ctk.CTkTextbox(self, width=480, height=300)
        self.textbox.pack(pady=10)
        
        self.listen_button = ctk.CTkButton(self, text="🎤 Слухати", command=self.start_listening_thread)
        self.listen_button.pack(pady=5)
        
        self.stop_button = ctk.CTkButton(self, text="❌ Вийти", command=self.stop)
        self.stop_button.pack(pady=5)
        
    def log(self, message):
        self.textbox.insert("end", message + "\n")
        self.textbox.see("end")
        
    def start_listening_thread(self):
        thread = Thread(target=self.listen)
        thread.start()
        
    def listen(self):
        audio = capture_voice_input()
        text = convert_speech_to_text(audio)
        if text:
            process_voice_command(text)
            
    def stop(self):
        self.destroy()

# ================== Запуск ==================
if __name__ == "__main__":
    app = VoiceAssistantApp()
    app.mainloop()
