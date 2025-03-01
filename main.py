# Джарвис - голосовой помощник, вдохновленный фильмом "Мстители"
# Автор: Нурислам Абдималиков

import os
import time
import datetime
import webbrowser
import random
import subprocess
import platform

try:
    import speech_recognition as sr
    import pyttsx3
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Установка необходимых библиотек...")
    os.system('pip3 install SpeechRecognition pyttsx3 requests beautifulsoup4 PyAudio')
    import speech_recognition as sr
    import pyttsx3
    import requests
    from bs4 import BeautifulSoup

# Инициализация движка для преобразования текста в речь
engine = pyttsx3.init()

# Настройка голоса
voices = engine.getProperty('voices')
for voice in voices:
    if 'russian' in voice.languages and 'RU' in voice.id:
        engine.setProperty('voice', voice.id)
        break

# Настройка скорости речи
engine.setProperty('rate', 180)

def speak(text):
    """Функция для озвучивания текста"""
    print(f"Джарвис: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Функция для распознавания речи"""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Слушаю...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        print("Распознавание...")
        query = recognizer.recognize_google(audio, language='ru-RU')
        print(f"Вы сказали: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Извините, я не понял, что вы сказали.")
        return ""
    except sr.RequestError:
        speak("Извините, сервис распознавания речи недоступен.")
        return ""

def get_time():
    """Функция для получения текущего времени"""
    now = datetime.datetime.now()
    return f"Сейчас {now.hour} часов {now.minute} минут"

def get_date():
    """Функция для получения текущей даты"""
    now = datetime.datetime.now()
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    return f"Сегодня {now.day} {months[now.month-1]} {now.year} года"

def search_web(query):
    """Функция для поиска информации в интернете"""
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return "Вот что я нашел по вашему запросу"

def open_application(app_name):
    """Функция для открытия приложений"""
    system = platform.system()
    
    # Словарь с названиями приложений и соответствующими командами для разных ОС
    apps = {
        'браузер': {
            'Darwin': 'open -a Safari',  # macOS
            'Windows': 'start msedge',   # Windows
            'Linux': 'xdg-open https://www.google.com'
        },
        'музыка': {
            'Darwin': 'open -a Music',
            'Windows': 'start mswindowsmusic:',
            'Linux': 'xdg-open https://music.youtube.com'
        },
        'календарь': {
            'Darwin': 'open -a Calendar',
            'Windows': 'start outlookcal:',
            'Linux': 'xdg-open https://calendar.google.com'
        },
        'почта': {
            'Darwin': 'open -a Mail',
            'Windows': 'start outlook:',
            'Linux': 'xdg-open https://mail.google.com'
        }
    }
    
    if app_name in apps and system in apps[app_name]:
        try:
            os.system(apps[app_name][system])
            return f"Открываю {app_name}"
        except:
            return f"Не удалось открыть {app_name}"
    else:
        return f"Я не знаю, как открыть {app_name}"

def get_weather(city="Москва"):
    """Функция для получения информации о погоде (упрощенная версия)"""
    # В реальном приложении здесь был бы запрос к API погоды
    # Для примера возвращаем случайные данные
    temp = random.randint(-5, 30)
    conditions = ["ясно", "облачно", "дождливо", "снежно", "туманно"]
    condition = random.choice(conditions)
    return f"В городе {city} сейчас {condition}, температура {temp} градусов"

def get_joke():
    """Функция для получения случайной шутки"""
    jokes = [
        "Почему программисты путают Хэллоуин и Рождество? Потому что 31 октября = 25 декабря в восьмеричной системе.",
        "Как называется восемь хоббитов? Хоббайт.",
        "Почему у Железного человека никогда не бывает похмелья? Потому что он всегда пьёт ответственно.",
        "Что сказал Тор, когда увидел Таноса? 'О, щелк!'",
        "Почему Капитан Америка не пользуется Интернетом? Он не любит открывать новые вкладки."
    ]
    return random.choice(jokes)

def greet():
    """Функция приветствия"""
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Доброе утро, сэр! Чем я могу помочь?")
    elif 12 <= hour < 18:
        speak("Добрый день, сэр! Чем я могу помочь?")
    else:
        speak("Добрый вечер, сэр! Чем я могу помочь?")

def process_command(command):
    """Функция для обработки команд пользователя"""
    if not command:
        return
    
    # Приветствие
    if any(word in command for word in ["привет", "здравствуй", "доброе утро", "добрый день", "добрый вечер"]):
        greet()
    
    # Время
    elif any(word in command for word in ["время", "который час"]):
        speak(get_time())
    
    # Дата
    elif any(word in command for word in ["дата", "какое сегодня число", "какой сегодня день"]):
        speak(get_date())
    
    # Поиск в интернете
    elif "найди" in command or "поиск" in command or "загугли" in command:
        query = command.replace("найди", "").replace("поиск", "").replace("загугли", "").strip()
        speak(search_web(query))
    
    # Открытие приложений
    elif "открой" in command:
        app = command.replace("открой", "").strip()
        speak(open_application(app))
    
    # Погода
    elif "погода" in command:
        city = "Москва"  # По умолчанию
        if "в городе" in command:
            city = command.split("в городе")[1].strip()
        speak(get_weather(city))
    
    # Шутка
    elif any(word in command for word in ["шутка", "анекдот", "рассмеши", "развесели"]):
        speak(get_joke())
    
    # Выключение
    elif any(word in command for word in ["пока", "до свидания", "выключись", "отключись", "спасибо за помощь"]):
        speak("До свидания, сэр! Рад был помочь.")
        return False
    
    # Если команда не распознана
    else:
        speak("Извините, я не понимаю эту команду. Пожалуйста, повторите.")
    
    return True

def main():
    """Основная функция программы"""
    speak("Джарвис запущен и готов к работе!")
    greet()
    
    running = True
    while running:
        command = listen()
        running = process_command(command)

if __name__ == "__main__":
    main()