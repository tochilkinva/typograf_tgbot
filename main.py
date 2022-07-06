
"""
Пример Telegram бота с функцией Типографа через сайт
https://www.artlebedev.ru/typograf/
Стэк: aiogram, remotetypograf, python 3.7.9
"""

import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from RemoteTypograf import RemoteTypograf

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = Bot(token=TELEGRAM_TOKEN)  # Объект бота
dp = Dispatcher(bot)  # Диспетчер для бота

TEXT_TEST1 = '"Вы все еще кое-как верстаете в "Ворде"? - Тогда мы идем к вам!"'
TEXT_TEST2 = (
    '...Когда В. И. Пупкин увидел в газете ',
    '("Сермяжная правда" № 45) рубрику Weather Forecast®,',
    ' он не поверил своим глазам — температуру обещали ±451 °F.'
)

# Включаем логирование. Пишем логи в файл
logging.basicConfig(
    filename='typograf_tgbot.log',
    level=logging.DEBUG,
)

# Тут инициализация сервиса Типографа
rt = RemoteTypograf()
rt.htmlEntities()
rt.br(1)
rt.p(1)
rt.nobr(3)


# Ответ на команду /help
@dp.message_handler(commands="help")
async def cmd_help(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [TEXT_TEST1, TEXT_TEST2]
    keyboard.add(*buttons)
    await message.reply("Это примеры текста, выбери любой",
                        reply_markup=keyboard)


# Ответ на команду /start
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    text = ('Привет! Это Типограф-бот, присылай текст и я его оттипографлю.',
            ' Команда /help показывает 2 примера')
    await message.answer(text)


# Обращение к сервису Типографа
def get_typogred_text(text: str) -> str:
    return rt.processText(text)


# Ответ на любой текст
@dp.message_handler()
async def cmd_test(message: types.Message):
    try:
        result = get_typogred_text(message.text)
    except Exception:
        result = 'Ошибка доступа к Типографу'
        logging.error(result)

    await message.answer(result)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)  # Запуск бота
