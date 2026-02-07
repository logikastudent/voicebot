import speech_recognition as sr
import subprocess
import webbrowser
import urllib.parse
import asyncio
import python_weather

recognizer = sr.Recognizer()


# 🎤 Отримання голосу
def capture_voice_input():
    with sr.Microphone() as source:
        print("🎤 Слухаю...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
    return audio


# 🧠 Speech to text
def convert_speech_to_text(audio):
    try:
        text = recognizer.recognize_google(audio, language="uk-UA")
        print("🗣 Ви сказали:", text)
        return text
    except sr.UnknownValueError:
        print("❌ Не вдалося розпізнати мову")
    except sr.RequestError as e:
        print(f"❌ Помилка сервісу: {e}")
    return ""


# 🌤 Погода (без API key)
async def get_weather(city):
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(city)

        print(f"🌤 Погода у {city}:")
        print(f"Температура: {weather.temperature}°C")
        print(f"Стан: {weather.description}")


# 🎯 Обробка команд
def process_voice_command(text):
    text_lower = text.lower()

    if "привіт" in text_lower:
        print("👋 Привіт! Як можу допомогти?")
    
    elif "як справи" in text_lower:
        print("😎 Все чітко, а у тебе?")
    
    elif "калькулятор" in text_lower:
        print("🧮 Відкриваю калькулятор")
        subprocess.call(["calc"])
    
    elif "хром" in text_lower or "chrome" in text_lower:
        print("🌐 Відкриваю Chrome")
        subprocess.call([r"C:\Program Files\Google\Chrome\Application\chrome.exe"])

    # 🎬 YouTube
    elif "знайди відео" in text_lower:
        query = text_lower.replace("знайди відео", "").strip()
        if query:
            print(f"🎬 Шукаю відео: {query}")
            url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
            webbrowser.open(url)

    # 🔎 Google
    elif "знайди у гуглі" in text_lower or "знайди в гуглі" in text_lower:
        query = text_lower.replace("знайди у гуглі", "").replace("знайди в гуглі", "").strip()
        if query:
            print(f"🔎 Гуглю: {query}")
            url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
            webbrowser.open(url)

    # 🌤 Погода
    elif "погода" in text_lower:
        city = text_lower.replace("погода", "").strip()
        if city == "":
            city = "Kyiv"

        print(f"🌦 Перевіряю погоду у {city}")
        asyncio.run(get_weather(city))

    elif "прощавай" in text_lower or "вийти" in text_lower:
        print("👋 До побачення!")
        return True

    else:
        print("🤔 Команду не розпізнано")

    return False


# 🚀 Main loop
def main():
    end_program = False
    while not end_program:
        audio = capture_voice_input()
        text = convert_speech_to_text(audio)
        if text:
            end_program = process_voice_command(text)


if __name__ == "__main__":
    main()
