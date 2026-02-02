# import os
# from aiogram import Bot, Dispatcher
# from dotenv import load_dotenv

# load_dotenv()
# bot = Bot(token=os.getenv('BOT-TOKEN'))
# dp = Dispatcher()

import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

# Используйте список возможных имен
possible_keys = ['BOT_TOKEN', 'BOT-TOK'] 

token = None
for key in possible_keys:
    token = os.getenv(key)
    if token:
        break

if not token:
    try:
        from google.colab import userdata
        for key in possible_keys:
            token = userdata.get(key)
            if token:
                break
    except (ImportError, AttributeError, Exception):
        token = None

if not token:
    print(f"DEBUG: Token value is: '{token}'")
    raise ValueError("Токен бота не найден. Проверьте Colab Secrets или .env")

bot = Bot(token=token)
dp = Dispatcher()

