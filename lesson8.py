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
# TOKEN = "7741398834:AAHOhzzcOmH5ZvF-n0vW7MEb8PoJ4FB0SUk"
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
# TOKEN = "7741398834:AAHOhzzcOmH5ZvF-n0vW7MEb8PoJ4FB0SUk"
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
import asyncio
import aiohttp
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CMC_API_KEY = os.getenv("CMC_API_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def get_crypto():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": CMC_API_KEY
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()

    if "data" in data:
        btc = next((coin for coin in data["data"] if coin["symbol"] == "BTC"), None)
        eth = next((coin for coin in data["data"] if coin["symbol"] == "ETH"), None)

        btc_price = f"${btc['quote']['USD']['price']:.2f}" if btc else "❌ Данные недоступны"
        eth_price = f"${eth['quote']['USD']['price']:.2f}" if eth else "❌ Данные недоступны"

        return f"💰 BTC: {btc_price}\n🪙 ETH: {eth_price}"
    return "❌ Ошибка получения данных"

@dp.message(Command("crypto"))
async def send_crypto(message: Message):
    crypto = await get_crypto()
    await message.answer(f"Курс криптовалют:\n{crypto}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())