# from aiogram import Bot, types, Router
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
#
# router = Router()
# keyboard = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text="Нажми меня!", callback_data="pressed")]
#     ]
# )
#
# @router.message()
# async def send_button(message: types.Message):
#     await message.answer("Нажми на кнопку:", reply_markup=keyboard)
#
# @router.callback_query(lambda call: call.data == "pressed")
# async def button_pressed(call: types.CallbackQuery):
#     await call.message.answer("Ты нажал на кнопку!")
#
