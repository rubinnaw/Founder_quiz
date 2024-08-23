from threading import current_thread
import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import router
from aiogram.enums.parse_mode import ParseMode
from utils import create_table


# Установим библиотеку nest_asyncio
import nest_asyncio
nest_asyncio.apply()

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Замените "YOUR_BOT_TOKEN" на токен, который вы получили от BotFather
API_TOKEN = '7416431584:AAE4mWXCjqA1oIJeoMurb7OLZXnAWAppDMc'


# Запуск процесса поллинга новых апдейтов
async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    await create_table()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())