from aiogram.filters.command import Command
from aiogram import types, F, Router
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils import update_quiz_index, get_question, get_quiz_index
from quiz_questions import questions_list


router = Router()

current_question_index = 0
correct_count = 0
total_correct_count = 0
@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = questions_list[current_question_index]['correct_option']
    

    await callback.message.answer(f"Верно! \nЭто: {questions_list[current_question_index]['options'][correct_option]}")

    global correct_count, total_correct_count
    correct_count += 1
    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)


    if current_question_index < len(questions_list):
        await get_question(callback.message, callback.from_user.id)
    else:
        total_correct_count = correct_count
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен!\nВаш результат записан\nВы ответили правильно на {total_correct_count} вопросов из {len(questions_list)}")


@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    # Получение текущего вопроса из словаря состояний пользователя
    global current_question_index
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = questions_list[current_question_index]['correct_option']

    await callback.message.answer(f"Неправильно. Правильный ответ: {questions_list[current_question_index]['options'][correct_option]}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    global total_correct_count
    if current_question_index < len(questions_list):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен!\nВаш результат записан\nВы ответили правильно на {total_correct_count} вопросов из {len(questions_list)}")


# Хэндлер на команду /start


@router.message(Command("start"))
async def cmd_start(message: types.Message):
  builder = ReplyKeyboardBuilder()
  builder.add(types.KeyboardButton(text="Начать игру"))
  builder.add(types.KeyboardButton(text="Последний результат"))
  await message.answer("Добро пожаловать в quiz", reply_markup=builder.as_markup(resize_keyboard=True))


@router.message(F.text=="Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
  await message.answer(f"Давайте начнем квиз!\n!Внимание!\nДля записи вашего результата необходимо ответить на все вопросы, в противном случае результат записан не будет")
  await new_quiz(message)


@router.message(F.text=="Последний результат")
@router.message(Command("last_result"))
async def cmd_last_result(message: types.Message):
  await message.answer("Результат вашей последней игры")
  await last_result(message)


async def last_result(message):
   user_id = message.from_user.id
   await message.answer(f"Вы ответили правильно на {total_correct_count} вопросов из {len(questions_list)}")    
   print(f"user_ID:  {user_id}")

async def new_quiz(message):
  user_id = message.from_user.id
  current_question_index = 0
  global correct_count
  correct_count = 0
  await update_quiz_index(user_id, current_question_index)
  await get_question(message, user_id)