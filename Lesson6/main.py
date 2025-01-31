# /Lesson6
#         /main.py
#         handlers
#                 /commands.py
#                 /messages.py
#         /config.py

import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
# from handlers import commands
# from handlers import messages
# from handlers import inline_buttons
from handlers import user, admin

bot = Bot(token=TOKEN)
dp = Dispatcher()

# dp.include_router(commands.router)
# dp.include_router(messages.router)
# dp.include_router(inline_buttons.router)
dp.include_router(user.router)
dp.include_router(admin.router)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

