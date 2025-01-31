# from aiogram import Bot, Dispatcher, types
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.filters import Command
# import asyncio
#
# BOT_TOKEN = "TOKEN"
#
# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher()
#
# inline_kb = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text="Сказать Привет", callback_data="hello")],
#         [InlineKeyboardButton(text="Сказать Пока", callback_data="bye")]
#     ]
# )
#
# @dp.message(Command("start"))
# async def start_handler(message: types.Message):
#     await message.answer("Привет! Выберите действие:", reply_markup=inline_kb)
#
# @dp.callback_query()
# async def process_callback(callback_query: types.CallbackQuery):
#     if callback_query.data == "hello":
#         await callback_query.message.answer("Привет! Рад вас видеть!")
#     elif callback_query.data == "bye":
#         await callback_query.message.answer("Пока! Рад был с вами работать!")
#
# async def main():
#     await dp.start_polling(bot)
#
# if __name__ == "__main__":
#     asyncio.run(main())
#

# from aiogram import Bot, Dispatcher, types
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.filters import Command
# import asyncio
# import random
#
# BOT_TOKEN = 'TOKEN'
#
# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher()
#
# @dp.message(Command('start'))
# async def start_handler(message: types.Message):
#     inline_kb = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text="Показать случайное число", callback_data="random")]
#         ]
#     )
#     await message.answer("Нажми на кнопку, чтобы получить число:", reply_markup=inline_kb)
#
# @dp.callback_query()
# async def process_callback(callback_query: types.CallbackQuery):
#     if callback_query.data == "random":
#         random_number = random.randint(0, 100)
#         new_kb = InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [InlineKeyboardButton(text=f"Случайное число: {random_number}", callback_data="random")]
#             ]
#         )
#         await callback_query.message.edit_reply_markup(reply_markup=new_kb)
#
# async def main():
#     await dp.start_polling(bot)
#
# if __name__ == '__main__':
#     asyncio.run(main())

from aiogram import Bot, Dispatcher, types
from aiogram.handlers import callback_query
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio

BOT_TOKEN = "TOKEN"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Категория 1", callback_data="cat1")],
            [InlineKeyboardButton(text="Категория 2", callback_data="cat2")]
        ]
    )
    await message.answer("Выберите категорию:", reply_markup=inline_kb)

@dp.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "cat1":
        sub_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Подкатегория 1.1", callback_data="subcat1")],
                [InlineKeyboardButton(text="Назад", callback_data="back")]
            ]
        )
        await callback_query.message.edit_text("Вы выбрали Категорию 1. Выберите подкатегорию:", reply_markup=sub_kb)
    elif callback_query.data == "cat2":
        await callback_query.message.edit_text("Вы выбрали категорию 2.")
    elif callback_query.data == "subcat1":
        await callback_query.message.edit_text('Вы выбрали подкатегорию 1.1')
    elif callback_query.data == "back":
        await start_handler(callback_query.message)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())