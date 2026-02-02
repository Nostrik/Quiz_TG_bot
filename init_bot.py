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

token = os.getenv('BOT_TOKEN') # Сначала проверяем .env или переменные окружения

# Если в переменных окружения пусто, пробуем Colab Secrets
if not token:
    try:
        from google.colab import userdata
        # Ключевой момент: userdata.get работает только в ячейке ноутбука
        # Если запуск из терминала, эта функция сама по себе вызовет вашу ошибку
        token = userdata.get('BOT_TOKEN')
    except (ImportError, AttributeError, Exception):
        # Если мы не в Colab или возникла ошибка ядра — просто идем дальше
        token = None

if not token:
    raise ValueError("Токен бота не найден. Проверьте Colab Secrets или .env")

bot = Bot(token=token)
dp = Dispatcher()

