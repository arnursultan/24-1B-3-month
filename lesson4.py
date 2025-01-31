# from aiogram import Bot, Dispatcher, types
# from aiogram.filters import Command
# from aiogram .fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.fsm.storage.memory import MemoryStorage
# import asyncio
#
# BOT_TOKEN = "7741398834:AAHOhzzcOmH5ZvF-n0vW7MEb8PoJ4FB0SUk"
#
# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher(sterage=MemoryStorage())
#
# class Form(StatesGroup):
#     name = State()
#     age = State()
#     city = State()
#
# @dp.message(Command("start"))
# async def start_handler(message: types.Message, state: FSMContext):
#     await message.answer("Привет! Как тебя зовут?")
#     await state.set_state(Form.name)
#
# @dp.message(Form.name)
# async def ask_age(message: types.Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.answer("Сколько тебе лет")
#     await state.set_state(Form.age)
#
# @dp.message(Form.age)
# async def ask_city(message: types.Message, state: FSMContext):
#     await state.update_data(age=message.text)
#     await message.answer("Из какого ты города?")
#     await state.set_state(Form.city)
#
# @dp.message(Form.city)
# async def finish_form(message: types.Message, state: FSMContext):
#     await state.update_data(city=message.text)
#     data = await state.get_data()
#     await message.answer(f"Спасибо за ответы!\nИмя: {data["name"]}\nВозраст: {data["age"]}\nГород: {data["city"]}")
#     await state.clear()
#
# async def main():
#     await dp.start_polling(bot)
#
# if __name__ == '__main__':
#     asyncio.run(main())

# import aiogram
# from aiogram import Bot, Dispatcher, types
# from aiogram.filters import Command, state
# from aiogram.fsm.context import  FSMContext
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.fsm.storage.memory import MemoryStorage
# import asyncio
#
# BOT_TOKEN = "TOKEN"
#
# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher(storage=MemoryStorage())
# class Form(StatesGroup):
#      name = State()
#      age = State()
#
# @dp.message(Command("start"))
# async def start_handler(message: types.Message, state: FSMContext):
#     await message.answer("Привет! Как тебя зовут?")
#     await state.set_state(Form.name)
#
# @dp.message(Form.name)
# async def ask_age(message: types.Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.answer("Сколько тебе лет?")
#     await state.set_state(Form.age)
#
# @dp.message(Form.age)
# async def finish_form(message: types.Message, state: FSMContext):
#     if not message.text.isdigit():
#         await message.answer("Пожалуйста, введите возраст числом.")
#         return
#     await state.update_data(age=int(message.text))
#     data = await state.get_data()
#     await message.answer(f"Спасибо, {data["name"]}!\nВозраст: {data["age"]}")
#     await state.clear()
#
# async def main():
#     await dp.start_polling(bot)
#
# if __name__ == '__main__':
#     asyncio.run(main())


from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio
import random

BOT_TOKEN = "TOKEN"

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)

menu_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Информация', callback_data='info')],
            [InlineKeyboardButton(text='Опции', callback_data='options')],
            [InlineKeyboardButton(text='Контакты', callback_data='contacts')]
        ]
    )

option_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Опция 1', callback_data='option1')],
                [InlineKeyboardButton(text='Опция 2', callback_data='option2')],
                [InlineKeyboardButton(text='Назад', callback_data='back')]
            ]
        )

back_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Назад', callback_data='back')]
            ]
        )

back1_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Назад', callback_data='back1')]
            ]
        )

@dp.message(Command('start'))
async def start_handler(message: types.Message):
    await message.answer('Нажми на кнопку, чтобы выбрать действие:', reply_markup=menu_kb)

@dp.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.data == 'info':
        await callback_query.message.edit_text('Этот бот показывает работу динамических кнопок', reply_markup=back_kb)
    elif callback_query.data == 'options':
        await callback_query.message.edit_text('Меню опций:', reply_markup=option_kb)
    elif callback_query.data == 'contacts':
        await callback_query.message.edit_text('Свяжитесь с нами: support@example.com', reply_markup=back_kb)
    elif callback_query.data == 'option1':
        await callback_query.message.edit_text('Вы выбрали Опцию 1', reply_markup=back1_kb)
    elif callback_query.data == 'option2':
        await callback_query.message.edit_text('Вы выбрали Опцию 2', reply_markup=back1_kb)
    elif callback_query.data == 'back':
        await callback_query.message.edit_text('Нажми на кнопку, чтобы выбрать действие:', reply_markup=menu_kb)
    elif callback_query.data == 'back1':
        await callback_query.message.edit_text('Меню опций:', reply_markup=option_kb)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())