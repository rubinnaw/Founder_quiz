import aiosqlite
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from quiz_questions import questions_list



async def create_table():
    # Создаем соединение с базой данных (если она не существует, то она будет создана)
    async with aiosqlite.connect('quiz_bot.db') as db:
        # Выполняем SQL-запрос к базе данных
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        # Сохраняем изменения
        await db.commit()

# Запускаем создание таблицы базы данных
create_table()



def generate_options_keyboard(answer_options, right_answer):
  builder = InlineKeyboardBuilder()
  for option in answer_options:
    builder.add(types.InlineKeyboardButton(
        text=option,
        callback_data="right_answer" if option == right_answer else "wrong_answer"
    ))
  builder.adjust(1)
  return builder.as_markup()


async def get_question(message, user_id):
  current_question_index = await get_quiz_index(user_id)
  correct_index = questions_list[current_question_index]['correct_option']
  opts = questions_list[current_question_index]['options']
  kb = generate_options_keyboard(opts, opts[correct_index])
  await message.answer(f"{questions_list[current_question_index]['question']}", reply_markup=kb)


async def get_quiz_index(user_id):
  async with aiosqlite.connect('quiz_bot.db') as db:
    async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
      result = await cursor.fetchone()
      if result is not None:
        return result[0]
      else:
        return 0


async def update_quiz_index(user_id, index):
    async with aiosqlite.connect('quiz_bot.db') as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        # Сохраняем изменения
        await db.commit()



async def create_table():
    async with aiosqlite.connect('quiz_bot.db') as db:
        # Выполняем SQL-запрос к базе данных
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        # Сохраняем изменения
        await db.commit()