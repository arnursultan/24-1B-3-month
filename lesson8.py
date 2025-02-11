# №1
# import aiohttp
# from bs4 import BeautifulSoup
#
# async def fetch_html(url: str):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.text()
#
# async def parse_data():
#     url = "https://quotes.toscrape.com/"
#     html = await fetch_html(url)
#     soup = BeautifulSoup(html, "lxml")
#
#     quotes = soup.find_all("span", class_="text")
#     for quote in quotes:
#         print(quote.text)
#
# №2
# import asyncio
# asyncio.run(parse_data())

# import asyncio
# import aiohttp
# from bs4 import BeautifulSoup
# from aiogram import Bot, Dispatcher, types
# from aiogram.types import Message
# from aiogram.filters import Command
#
# TOKEN = "TOKEN"
#
# bot = Bot(token=TOKEN)
# dp = Dispatcher()
#
# async def fetch_html(url: str):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.text()
#
# async def get_quotes():
#     url = "https://quotes.toscrape.com/"
#     html = await fetch_html(url)
#     soup = BeautifulSoup(html, "lxml")
#
#     quotes = soup.find_all("span", class_="text")
#     return [quote.text for quote in quotes[:5]]
#
# @dp.message(Command("quotes"))
# async def send_quotes(message: Message):
#     quotes = await get_quotes()
#     text = "\n\n".join(quotes)
#     await message.answer(f" Цитаты: \n{text}")
#
# async def main():
#     await dp.start_polling(bot)
#
# if __name__ == '__main__':
#     asyncio.run(main())

# №3

# import asyncio
# import aiohttp
# from bs4 import BeautifulSoup
# from aiogram import Bot, Dispatcher, types
# from aiogram.types import Message
# from aiogram.filters import Command
#
# TOKEN = "TOKEN"
#
# bot = Bot(token=TOKEN)
# dp = Dispatcher()
#
# async def fetch_html(url: str):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.text()
#
# async def get_currency():
#     url = "https://www.cbr.ru/currency_base/daily/"
#     html = await fetch_html(url)
#     soup = BeautifulSoup(html, 'lxml')
#
#     rows = soup.find("table", class_="data").find_all("tr")[1:]
#     rates = {}
#
#     for row in rows:
#         cols = row.find_all("td")
#         code = cols[1].text.strip()
#         value = cols[4].text.strip()
#         if code in ["USD", "EUR", "KGS"]:
#             rates[code] = value
#
#     return rates
#
# @dp.message(Command("currency"))
# async def send_currency(message: Message):
#     rates = await get_currency()
#     text = f"💰 Курс валют:\n🇺🇸 USD: {rates['USD']} руб.\n🇪🇺 EUR: {rates['EUR']} руб.\n🇰🇬 KGS: {rates['KGS']} руб."
#     await message.answer(text)
#
# async def main():
#     await dp.start_polling(bot)
#
# if __name__ == "__main__":
#     asyncio.run(main())

# №4
# import asyncio
# import aiohttp
# import os
# from aiogram import Bot, Dispatcher
# from aiogram.types import Message
# from aiogram.filters import Command
# from dotenv import load_dotenv
#
# load_dotenv()
# TOKEN = os.getenv("BOT_TOKEN")
# CMC_API_KEY = os.getenv("CMC_API_KEY")
#
# bot = Bot(token=TOKEN)
# dp = Dispatcher()
#
# async def get_crypto():
#     url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
#     headers = {
#         "Accepts": "application/json",
#         "X-CMC_PRO_API_KEY": CMC_API_KEY
#     }
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, headers=headers) as response:
#             data = await response.json()
#
#     if "data" in data:
#         btc = next((coin for coin in data["data"] if coin["symbol"] == "BTC"), None)
#         eth = next((coin for coin in data["data"] if coin["symbol"] == "ETH"), None)
#
#         btc_price = f"${btc['quote']['USD']['price']:.2f}" if btc else "❌ Данные недоступны"
#         eth_price = f"${eth['quote']['USD']['price']:.2f}" if eth else "❌ Данные недоступны"
#
#         return f"💰 BTC: {btc_price}\n🪙 ETH: {eth_price}"
#     return "❌ Ошибка получения данных"
#
# @dp.message(Command("crypto"))
# async def send_crypto(message: Message):
#     crypto = await get_crypto()
#     await message.answer(f"Курс криптовалют:\n{crypto}")
#
# async def main():
#     await dp.start_polling(bot)
#
# if __name__ == "__main__":
#     asyncio.run(main())

# import asyncio
# import aiohttp
# import os
# from aiogram import Bot, Dispatcher
# from aiogram.types import Message
# from aiogram.filters import Command
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv
#
# load_dotenv()
# TOKEN = os.getenv("BOT_TOKEN")
#
# bot = Bot(token=TOKEN)
# dp = Dispatcher()
#
#
# async def fetch_html(url: str):
#     """Функция для загрузки HTML-страницы"""
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.text()
#
#
# async def get_news():
#     """Функция парсинга новостей с lenta.ru"""
#     url = "https://lenta.ru/"
#     html = await fetch_html(url)
#     soup = BeautifulSoup(html, "lxml")
#
#     news_cards = soup.find_all("h3", class_="card-mini__title", limit=5)
#
#     if not news_cards:
#         return "❌ Не удалось получить новости."
#
#     news_list = []
#     for card in news_cards:
#         title = card.text.strip()
#         link = "https://lenta.ru" + card.find_parent("a")["href"]  # Берем ссылку у родительского тега <a>
#         news_list.append(f"🔹 <b>{title}</b>\n<a href='{link}'>Читать подробнее</a>")
#
#     return "\n\n".join(news_list)
#
#
# @dp.message(Command("news"))
# async def send_news(message: Message):
#     """Обработчик команды /news"""
#     news = await get_news()
#     await message.answer(news, parse_mode="HTML", disable_web_page_preview=True)
#
#
# async def main():
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())

# import asyncio
# import aiohttp
# import os
# from aiogram import Bot, Dispatcher
# from aiogram.types import Message
# from aiogram.filters import Command
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv
#
# load_dotenv()
# TOKEN = os.getenv("BOT_TOKEN")
#
# bot = Bot(token=TOKEN)
# dp = Dispatcher()
#
# async def fetch_html(url: str):
#     """Функция для загрузки HTML-страницы"""
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.text()
#
# async def get_exchange_rates():
#     """Парсим курс валют с ЦБ РФ"""
#     url = "https://www.cbr.ru/currency_base/daily/"
#     html = await fetch_html(url)
#     soup = BeautifulSoup(html, "lxml")
#
#     rows = soup.find("table", class_="data").find_all("tr")[1:]  # Пропускаем заголовок таблицы
#     rates = {"RUB": 1.0}  # Рубль сам к себе всегда 1.0
#
#     for row in rows:
#         cols = row.find_all("td")
#         code = cols[1].text.strip()  # Код валюты (USD, EUR, KGS и т.д.)
#         nominal = float(cols[2].text.replace(",", "."))  # Номинал (например, 100 для KZT)
#         value = float(cols[4].text.replace(",", "."))  # Курс в рублях
#         rates[code] = value / nominal  # Курс за 1 единицу валюты
#
#     return rates
#
# @dp.message(Command("convert"))
# async def convert_currency(message: Message):
#     """Обработчик команды /convert сумма валюта1 валюта2"""
#     try:
#         parts = message.text.split()
#         if len(parts) != 4:
#             await message.answer("❌ Формат команды: /convert <сумма> <из валюты> <в валюту>\nПример: /convert 100 USD KGS")
#             return
#
#         amount, from_currency, to_currency = parts[1], parts[2].upper(), parts[3].upper()
#         amount = float(amount)  # Преобразуем сумму в число
#
#         rates = await get_exchange_rates()
#
#         if from_currency not in rates or to_currency not in rates:
#             await message.answer("❌ Одна из валют не найдена. Доступные валюты: USD, EUR, KGS, RUB и др.")
#             return
#
#         converted_amount = (amount * rates[from_currency]) / rates[to_currency]
#         await message.answer(f"💱 {amount} {from_currency} = {converted_amount:.2f} {to_currency}")
#
#     except ValueError:
#         await message.answer("❌ Неверный формат суммы. Введите число, например: /convert 100 USD KGS")
#     except Exception as e:
#         await message.answer(f"❌ Ошибка: {str(e)}")
#
# async def main():
#     await dp.start_polling(bot)
#
# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import uuid

logging.basicConfig(level=logging.INFO)

TOKEN = "7741398834:AAHOhzzcOmH5ZvF-n0vW7MEb8PoJ4FB0SUk"


class Reminder(StatesGroup):
    waiting_for_text = State()
    waiting_for_time = State()


class RepeatReminder(StatesGroup):
    waiting_for_text = State()
    waiting_for_interval = State()
    waiting_for_repetitions = State()


router = Router()
bot_instance: Bot = None
scheduler: AsyncIOScheduler = None
active_reminders = {}


@router.message(Command("remind"))
async def set_reminder(message: types.Message, state: FSMContext):
    await message.answer("Введите текст напоминания:")
    await state.set_state(Reminder.waiting_for_text)


@router.message(Reminder.waiting_for_text)
async def get_reminding(message: types.Message, state: FSMContext):
    await state.update_data(reminder_text=message.text)
    await message.answer("Введите время в секундах через:")
    await state.set_state(Reminder.waiting_for_time)


@router.message(Reminder.waiting_for_time, F.text.isdigit())
async def get_time(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    reminder_text = user_data.get("reminder_text")
    delay = int(message.text)

    run_time = datetime.now().astimezone() + timedelta(seconds=delay)

    scheduler.add_job(
        send_reminder,
        'date',
        run_date=run_time,
        args=[message.chat.id, reminder_text, bot_instance]
    )

    await message.answer(f"Напоминание установлено на {delay} секунд!")
    await state.clear()


async def send_reminder(chat_id: int, text: str, bot: Bot):
    await bot.send_message(chat_id=chat_id, text=f"Напоминание: {text}")


@router.message(Command("repeat"))
async def repeat_reminder(message: types.Message, state: FSMContext):
    await message.answer("Введите текст напоминания:")
    await state.set_state(RepeatReminder.waiting_for_text)


@router.message(RepeatReminder.waiting_for_text)
async def repeating_text(message: types.Message, state: FSMContext):
    await state.update_data(reminder_text=message.text)
    await message.answer("Введите интервал в секундах:")
    await state.set_state(RepeatReminder.waiting_for_interval)


@router.message(RepeatReminder.waiting_for_interval, F.text.isdigit())
async def repeat_interval(message: types.Message, state: FSMContext):
    await state.update_data(interval=int(message.text))
    await message.answer("Введите количество повторений:")
    await state.set_state(RepeatReminder.waiting_for_repetitions)


@router.message(RepeatReminder.waiting_for_repetitions, F.text.isdigit())
async def get_epetitions(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    reminder_text = user_data.get("reminder_text")
    interval = user_data.get("interval")
    repetitions = int(message.text)
    job_id = f"{message.chat.id}_{uuid.uuid4()}"
    print(f"Создано напоминание")
    active_reminders[job_id] = scheduler.add_job(
        send_repeating_reminder,
        'interval',
        seconds=interval,
        args=[message.chat.id, reminder_text, bot_instance, job_id, repetitions],
        id=job_id
    )
    await message.answer(f"Повторяющееся напоминание установлено! ID:")
    await state.clear()


async def send_repeating_reminder(chat_id: int, text: str, bot: Bot, job_id: str, repetitions: int):
    if repetitions != 0:
        repetitions -= 1
        if repetitions == 0:
            scheduler.remove_job(job_id)
            del active_reminders[job_id]
    await bot.send_message(chat_id=chat_id, text=f"Напоминание: {text}")


@router.message(Command("cancel_repeat"))
async def cancel_repeat(message: types.Message):
    if not active_reminders:
        await message.answer("Нет активных напоминаний для удаления.")
        return

    reminder_list = "\n".join([f"{job_id}" for job_id in active_reminders.keys()])
    await message.answer(f"Активные напоминания:\n{reminder_list}\nОтправьте ID для удаления.")


@router.message()
async def remove_repeat(message: types.Message):
    job_id = message.text.strip()
    if job_id in active_reminders:
        scheduler.remove_job(job_id)
        del active_reminders[job_id]
        await message.answer(f"Напоминание {job_id} удалено!")
    else:
        active_list = "\n".join(active_reminders.keys()) if active_reminders else "Нет активных ID."
        await message.answer(f"Некорректный ID!\nДоступные ID:\n{active_list}")


async def main():
    global bot_instance, scheduler
    bot_instance = Bot(token=TOKEN)
    scheduler = AsyncIOScheduler()
    scheduler.start()
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot_instance)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("DONE")


