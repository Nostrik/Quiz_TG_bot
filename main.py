import os
import asyncio
import logging
import config
from init_bot import bot, dp
from database import create_table, get_quiz_data
from handlers import router as quiz_router, new_quiz
from aiogram import F
from aiogram import types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Welcomes the user and provides a reply keyboard with a 'Start Game' button.
    """
    logging.info(f"User {message.from_user.id} press start")
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))


@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    """
    Triggers the start of a new quiz session when the user sends the command or clicks the button.
    """
    await message.answer(f"Давайте начнем квиз!", reply_markup=types.ReplyKeyboardRemove())
    await new_quiz(message)


@dp.message(Command("statistics"))
async def show_stats(message: types.Message):
    """Выводит последний результат пользователя."""
    data = await get_quiz_data(message.from_user.id)
    if data:
        await message.answer(f"Ваш последний результат: {data[1]} правильных ответов.")
    else:
        await message.answer("Вы еще не проходили квиз.")
    

async def main():
    dp.include_router(quiz_router)
    await create_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
