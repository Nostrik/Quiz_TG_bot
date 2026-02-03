# import os
# import logging
# from aiogram import Bot, Dispatcher
# from dotenv import load_dotenv

# load_dotenv()
# bot = Bot(token=os.getenv('BOT-TOKEN'))
# dp = Dispatcher()

import os
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from pathlib import Path

# 1. Проверяем наличие .env файла. Если он есть — загружаем.
env_path = Path('.env')
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    # print(f"DEBUG: Keys found in .env: {list(os.environ.keys())[-5:]}")

    # print("DEBUG: .env file found and loaded.")
    logging.info(".env file found and loaded.")
else:
    logging.info(".env file NOT found. Searching in environment/Colab secrets..")
    # print("DEBUG: .env file NOT found. Searching in environment/Colab secrets...")

# 2. Ищем токен (сначала в env, переданном через export, затем в Colab Secrets)
possible_keys = ['BOT_TOKEN', 'BOT-TOK', 'BOT-TOKEN']
token = None

for key in possible_keys:
    # os.getenv вытащит значение, которое вы передали через export BOT_TOKEN="..."
    token = os.getenv(key)
    if token:
        # print(f"DEBUG: Token found in environment variables (via {key}).")
        logging.info(f"Token found in environment variables (via {key}).")
        break

# 3. Если в обычном окружении нет, идем в Colab Secrets
if not token:
    try:
        from google.colab import userdata
        for key in possible_keys:
            token = userdata.get(key)
            if token:
                logging.info(f"Token found in Colab Secrets (via {key}).")
                # print(f"DEBUG: Token found in Colab Secrets (via {key}).")
                break
    except (ImportError, AttributeError):
        pass

# 4. Проверка и запуск
if not token:
    raise ValueError("Токен бота не найден! Либо создайте .env, либо используйте export BOT_TOKEN=\"...\", либо добавьте в Colab Secrets.")

bot = Bot(token=token)
dp = Dispatcher()
