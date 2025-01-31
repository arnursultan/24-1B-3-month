# from aiogram import Bot, Dispatcher, types
# from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
# from aiogram.filters import Command
#
# BOT_TOKEN = 'TOKEN'
#
# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher()
#
# keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")],
#         [KeyboardButton(text="О погоде"), KeyboardButton(text="Новости")]
#     ],
#     resize_keyboard=True
# )
#
# @dp.message(Command("start"))
# async def start_handler(message: Message):
#     await message.answer("Привет! Выберите команду:", reply_markup=keyboard)
#
# @dp.message()
# async def handler_buttons(message: Message):
#     if message.text == "Привет":
#         await message.answer("Привет! Рад вас видеть!")
#     elif message.text == "Пока":
#         await message.answer("До свидания! Будем ждать вас снова!")
#     elif message.text == "О погоде":
#         await message.answer("Сегодня погода дождливая, +10 C")
#     elif message.text == "Новости":
#         await message.answer("Последние новости: Приближаются кратковременные дожди")
#     else:
#         await message.answer("Я не понимаю команду Вы введи неправильно. Выберите кнопку на клавиатуре.")
#
# if __name__ == "__main__":
#     dp.run_polling(bo

# from aiogram import Bot, Dispatcher, types
# from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
# from aiogram.filters import Command
# import random
#
# BOT_TOKEN = 'TOKEN'
#
# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher()
#
# keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="😀  Смайлик"), KeyboardButton(text="🎲 Случайное число")],
#         [KeyboardButton(text="👋 Приветствие"), KeyboardButton(text="❓ Помощь")]
#     ],
#     resize_keyboard=True
# )
#
# @dp.message(Command("start"))
# async def start_handler(message: Message):
#     await message.answer("Привет! я второй бот. Выберите действие:", reply_markup=keyboard)
#
# @dp.message()
# async def handle_buttons(message: Message):
#     if message.text == "😀  Смайлик":
#         await message.answer("Вот ваш смайлик 👋 ")
#     elif message.text == "🎲 Случайное число":
#         random_number = random.randint(1, 100)
#         await message.answer(f"Ваше случайное число: {random_number}")
#     elif message.text == "👋 Приветствие":
#         await message.answer("Привет! Как у вас делишки?")
#     elif message.text == "❓ Помощь":
#         await message.answer("Обратитесь в больницу, либо звоните 991")
#     else:
#         await message.answer("Я не понимаю такую команду Выберите действие из меню")
#
# if __name__ == "__main__":
#     dp.run_polling(bot)
