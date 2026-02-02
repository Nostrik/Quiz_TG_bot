# import os
# from aiogram import Bot, Dispatcher
# from dotenv import load_dotenv

# load_dotenv()
# bot = Bot(token=os.getenv('BOT-TOKEN'))
# dp = Dispatcher()

import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

try:
    from google.colab import userdata
except ImportError:
    userdata = None

load_dotenv()

token = None
if userdata:
    token = userdata.get('BOT_TOKEN') # Используйте метод .get()

if not token:
    token = os.getenv('BOT_TOKEN')

if not token:
    raise ValueError("Токен бота не найден. Проверьте Colab Secrets или ваш .env файл.")

bot = Bot(token=token)
dp = Dispatcher()

