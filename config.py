"""
en: Configuration module for the project
ru: Модуль конфигурации для проекта
"""
import os
from dotenv import load_dotenv

# en: Load environment variables from .env file
# ru: Загрузить переменные окружения из файла .env
load_dotenv()
# en: Get the environment variables
# ru: Получить переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# en: Get the path to the project / ru: Получить путь к проекту
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(PROJECT_PATH, 'static')
DATABASE_PATH = os.path.join(PROJECT_PATH, 'db', 'zazhibot.db')

# en: Dicts for create tables / ru: Словари для создания таблиц
# en: The table of the quiz / ru: Таблица викторины
FRAME_QUIZ_TABLE = {
    "name": 'frame_quiz',
    "columns": [
        'id INTEGER PRIMARY KEY AUTOINCREMENT',
        'question_img TEXT NOT NULL ',
        'answer_img TEXT NOT NULL',
        'question_file_id TEXT',
        'answer_file_id TEXT',
        'correct TEXT',
        'incorrect_1 TEXT',
        'incorrect_2 TEXT',
        'incorrect_3 TEXT',
    ]
}
# en: The table of the phrases sorted by theme/ ru: Таблица фраз, отсортированных по темам
THEME_PHRASE_TABLE = {
    "name": 'theme_phrase',
    "columns": [
        'id INTEGER PRIMARY KEY AUTOINCREMENT',
        'theme TEXT NOT NULL',
        'phrase TEXT NOT NULL',
    ]
}
# en: The table of the good news / ru: Таблица хороших новостей
GOOD_NEWS_TABLE = {
    "name": 'good_news',
    "columns": [
        'id INTEGER PRIMARY KEY AUTOINCREMENT',
        'news TEXT NOT NULL',
    ]
}
# en: The table of the regular phrases by members of project
# ru: Таблица обычных фраз участников проекта
REGULAR_PHRASE_TABLE = {
    "name": 'regular_phrase',
    "columns": [
        'id INTEGER PRIMARY KEY AUTOINCREMENT',
        'name TEXT NOT NULL',
        'phrase TEXT NOT NULL',
    ]
}
# en: The table of the users / ru: Таблица пользователей
USERS_TABLE = {
    "name": 'users',
    "columns": [
        'id INTEGER PRIMARY KEY AUTOINCREMENT',
        'user_id INTEGER NOT NULL',
        'username TEXT',
        'full_name TEXT',
        'date TEXT',
    ]
}
# en: The table of audio files for Piter Pens' tale / ru: Таблица аудиофайлов для сказки о Питере Пэне
PITER_TABLE = {
    "name": 'piter',
    "columns": [
        'id INTEGER PRIMARY KEY AUTOINCREMENT',
        'file_path TEXT NOT NULL',
        'file_id TEXT',
        'description TEXT'
    ]
}
# en: The teble of the bot's images / ru: Таблица изображений бота
BOT_IMG_TABLE = {
    "name": 'bot_img',
    "columns": [
        'id INTEGER PRIMARY KEY AUTOINCREMENT',
        'name TEXT NOT NULL',
        'file_path TEXT NOT NULL',
        'file_id TEXT'
    ]
}
# en: The table of the users' messages / ru: Таблица сообщений пользователей
USERS_MESSAGES_TABLE = {
    "name": 'users_messages',
    "columns": [
        'id INTEGER PRIMARY KEY AUTOINCREMENT',
        'user_id INTEGER NOT NULL',
        'username TEXT',
        'full_name TEXT',
        'message TEXT NOT NULL',
        'date TEXT NOT NULL',
    ]
}
