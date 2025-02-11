import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
import aiosqlite

API_TOKEN = "7741398834:AAHOhzzcOmH5ZvF-n0vW7MEb8PoJ4FB0SUk"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def init_db():
    async with aiosqlite.connect("users.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT UNIQUE
            )
        """)
        await db.commit()

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}! Добро пожаловать в бота.\n"
                         "Команды:\n"
                         "/add – добавить себя\n"
                         "/add_user <username> – добавить другого пользователя\n"
                         "/list – список пользователей\n"
                         "/debug – отладка базы данных\n"
                         "/clear_db – очистить базу данных")

@dp.message(Command("add"))
async def add_self(message: Message):
    user_id = message.from_user.id
    username = (message.from_user.username or message.from_user.first_name).strip().lower()

    async with aiosqlite.connect("users.db") as db:
        try:
            await db.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
            await db.commit()
            await message.answer(f"Ваш username @{username} добавлен в базу данных!")
        except aiosqlite.IntegrityError:
            await message.answer(f"@{username} уже существует в базе данных.")

@dp.message(Command("add_user"))
async def add_user_command(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Пожалуйста, укажите имя пользователя. Пример: /add_user username")
        return

    username = command.args.strip().lstrip('@').lower()

    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT username FROM users WHERE LOWER(username) = ?", (username,)) as cursor:
            exists = await cursor.fetchone()

        if exists:
            await message.answer(f"Пользователь @{username} уже существует в базе данных.")
        else:
            await db.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (None, username))
            await db.commit()
            await message.answer(f"Пользователь @{username} добавлен в базу данных!")

@dp.message(Command("list"))
async def list_users(message: Message):
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT username FROM users") as cursor:
            rows = await cursor.fetchall()

    if rows:
        user_list = "\n".join([f"@{row[0]}" for row in rows])
        await message.answer(f"Зарегистрированные пользователи:\n{user_list}")
    else:
        await message.answer("В базе данных пока нет пользователей.")

@dp.message(Command("debug"))
async def debug_db(message: Message):
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT id, user_id, username FROM users") as cursor:
            rows = await cursor.fetchall()

    if rows:
        debug_info = "\n".join([f"ID: {row[0]}, Telegram ID: {row[1]}, Username: @{row[2]}" for row in rows])
        await message.answer(f"Текущие данные в базе:\n{debug_info}")
    else:
        await message.answer("База данных пуста.")

@dp.message(Command("clear_db"))
async def clear_db(message: Message):
    async with aiosqlite.connect("users.db") as db:
        await db.execute("DELETE FROM users")
        await db.commit()
    await message.answer("База данных полностью очищена.")

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())