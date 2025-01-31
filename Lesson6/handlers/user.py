from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def start_user(message: Message):
    await message.answer("Привет, пользователь!")
