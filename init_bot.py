# import os
# from aiogram import Bot, Dispatcher
# from dotenv import load_dotenv

# load_dotenv()
# bot = Bot(token=os.getenv('BOT-TOKEN'))
# dp = Dispatcher()

import os
try:
    from google.colab import userdata
except ImportError:
    userdata = None

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

if userdata and 'BOT_TOKEN' in userdata:
    token = userdata.get('BOT_TOKEN')
else:
    token = os.getenv('BOT_TOKEN')

if not token:
    raise ValueError("Токен бота не найден. Проверьте Colab Secrets или ваш .env файл.")

bot = Bot(token=token)
dp = Dispatcher()
