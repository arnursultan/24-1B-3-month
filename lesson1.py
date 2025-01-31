# from aiogram import Bot, Dispatcher
# from aiogram.types import Message
# from aiogram.filters import Command
#
# BOT_TOKEN = "TOKEN"
#
# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher()
#
# @dp.message(Command("start"))
# async def start_handler(message: Message):
#     await message.answer("Привет! Я твой бот на Aiogram")
#
# @dp.message()
# async def echo_handler(message: Message):
#     await message.answer(message.text)
#
# if __name__ =="__main__":
#     dp.run_polling(bot)
#
#
# from aiogram import Bot, Dispatcher
# from aiogram.types import Message
# from aiogram.filters import Command
#
# BOT_TOKEN = "TOKEN"
#
# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher()
#
# @dp.message(Command("start"))
# async def start_handler(message: Message):
#     await message.answer("Привет! Я твой бот на Aiogram. Чем могу помочь?")
#
# @dp.message(Command("help"))
# async def help_handler(message: Message):
#     await message.answer("Вот список команд, которые я поддерживаю:\n"
#                          "/start - стартовый экран\n"
#                          "/help - справка по ботам\n"
#                          "Напишите 'Привет', и я отвечу вам!")
#
# @dp.message()
# async def echo_handler(message: Message):
#     if "привет" in message.text.lower():
#         await message.answer("Привет! Как ваши дела?")
#     elif "пока" in message.text.lower():
#         await message.answer("До свидания! Жду вас снова!")
#     else:
#         await message.answer(f"Вы написали: {message.text}. Напишите 'Привет' или 'Пока', и я отвечу вам на это!")
#
# if __name__ == "__main__":
#     dp.run_polling(bot)
