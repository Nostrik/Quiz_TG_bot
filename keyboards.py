from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def generate_options_keyboard(answer_options, right_answer):
    """
    Generates an inline keyboard with answer options.
    Assigns 'right_answer' or 'wrong_answer' callback data based on the correct answer.
    """
    builder = InlineKeyboardBuilder()
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer")
        )
    builder.adjust(1)
    return builder.as_markup()
