import logging
from aiogram import types, F, Router
from aiogram.filters.command import Command
from database import update_quiz_score, get_quiz_data, get_quiz_index, update_quiz_index
from quizdata import quiz_data
from keyboards import generate_options_keyboard

router = Router()


async def new_quiz(message):
    """
    Starts a new quiz session for the user by resetting their progress to zero.
    """
    user_id = message.from_user.id
    await update_quiz_index(user_id, 0)
    await update_quiz_score(user_id, 0)
    await get_question(message, user_id)


async def get_question(message, user_id):
    """
    Fetches the current question for the user and sends it with an inline keyboard.
    """
    current_question_index = await get_quiz_index(user_id)

    if current_question_index >= len(quiz_data):
        data = await get_quiz_data(user_id)
        final_score = data[1] if data else 0
        
        await message.answer(
            f"🏁 **Квиз завершен!**\n"
            f"Ваш итоговый результат: {final_score} из {len(quiz_data)} правильных ответов."
        )
        return
    
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']

    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)


@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    """
    Handles correct answers: removes the keyboard, increments progress, and proceeds to the next question.
    """
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )
    data = await get_quiz_data(callback.from_user.id)
    current_index, current_score = data if data else (0, 0)
    
    await callback.message.answer("Верно! ✅")
    
    new_index = current_index + 1
    new_score = current_score + 1
    
    await update_quiz_index(callback.from_user.id, new_index)
    await update_quiz_score(callback.from_user.id, new_score)
    await get_question(callback.message, callback.from_user.id)


@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    """
    Handles incorrect answers: removes the keyboard, reveals the correct answer, and moves to the next question.
    """
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']

    await callback.message.answer(f"Неправильно ❌. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    await get_question(callback.message, callback.from_user.id)
