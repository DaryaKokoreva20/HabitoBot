from dotenv import load_dotenv
import os # для работы с переменными окружения

load_dotenv() # загружает переменные из .env в окружение Python
BOT_TOKEN = os.getenv("ACCESS_TOKEN")
DB_URL = os.getenv("DATABASE_URL") 