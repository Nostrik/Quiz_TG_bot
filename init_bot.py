# import os
# from aiogram import Bot, Dispatcher
# from dotenv import load_dotenv

# load_dotenv()
# bot = Bot(token=os.getenv('BOT-TOKEN'))
# dp = Dispatcher()

import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

# Загружаем переменные из .env файла (если есть)
load_dotenv()

# Используем список возможных имен ключей (с дефисом и подчеркиванием)
possible_keys = ['BOT_TOKEN', 'BOT-TOK']

token = None

# 1. Сначала пытаемся получить токен из переменных окружения
for key in possible_keys:
    token = os.getenv(key)
    if token:
        break

# 2. Если токен не найден в окружении, пробуем Colab Secrets
if not token:
    try:
        from google.colab import userdata
        # userdata.get() может вызвать AttributeError, если запущено не в ячейке Colab
        for key in possible_keys:
            token = userdata.get(key)
            if token:
                break
    except (ImportError, AttributeError, Exception) as e:
        # Если возникла ошибка (например, нет ядра Colab), просто игнорируем и продолжаем
        print(f"DEBUG INFO: Colab Secrets access failed: {e}")
        token = None

# >>>>> ПРОВЕРКА И ОТЛАДКА <<<<<
# Эта строка покажет, какое значение (или None/пусто) в итоге попало в переменную token
print(f"DEBUG: Final token value is: '{token}'")

# 3. Финальная проверка: если токен все еще пуст, выбрасываем ошибку
if not token:
    raise ValueError("Токен бота не найден. Проверьте Colab Secrets или .env файл.")

# 4. Инициализация бота
bot = Bot(token=token)
dp = Dispatcher()

