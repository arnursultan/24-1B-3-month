import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "badasspubgm@gmail.com"
PASSWORD = "hymiikhjonmmzjdv"

BOT_TOKEN = "7741398834:AAHOhzzcOmH5ZvF-n0vW7MEb8PoJ4FB0SUk"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Form(StatesGroup):
    recipient = State()
    subject = State()
    text = State()
    confirmation = State()

@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer("Здравствуйте, напишите email адрес получателя.\nДля сброса введите команду /cancel")
    await state.set_state(Form.recipient)
    
@dp.message(Command("cancel"))
async def finish_form(message: types.Message, state: FSMContext):
    await message.answer("Отправка сброшена")
    await state.clear()

@dp.message(Form.recipient)
async def ask_subject(message: types.Message, state: FSMContext):
    if not '@' in message.text:
        await message.answer('Введите адрес правильно')
        return
    await state.update_data(recipient=message.text)
    await message.answer("Введите тему письма")
    await state.set_state(Form.subject)

@dp.message(Form.subject)
async def ask_text(message: types.Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await message.answer("Напишите содержимое(текст) письма")
    await state.set_state(Form.text)

@dp.message(Form.text)
async def ask_confirmation(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await message.answer(f'''Подтверждение отправки:
Получатель: {data['recipient']}
Тема: {data['subject']}
Содержимое: {data['text']}

Для подтверждения, напишите "да", для отмены /cancel''')
    await state.set_state(Form.confirmation)

@dp.message(Form.confirmation)
async def send_email(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        data = await state.get_data()
        recipients = [email.strip() for email in data['recipient'].split(',') if '@' in email]
        subject = data['subject']
        text = data['text']

        success, failed = [], []
        for email in recipients:
            try:
                logging.info("Подключаемся к SMTP-серверу...")
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
                logging.info("Успешно подключились. Авторизация...")
                server.login(EMAIL, PASSWORD)
                logging.info("Авторизация успешна. Отправляем письмо...")

                msg = MIMEMultipart()
                msg['From'] = EMAIL
                msg['To'] = email
                msg['Subject'] = subject
                msg.attach(MIMEText(text, 'plain', 'utf-8'))

                server.sendmail(EMAIL, email, msg.as_string())
                server.quit()
                logging.info(f"Письмо успешно отправлено на {email}")
                success.append(email)
            except Exception as e:
                logging.error(f"Ошибка при отправке письма: {e}")
                failed.append(email)

        response = ""
        if success:
            response += f"✅ Письмо успешно отправлено на:\n" + "\n".join(success) + "\n"
        if failed:
            response += f"❌ Ошибка при отправке на:\n" + "\n".join(failed)

        await message.answer(response or "Ни одно письмо не было отправлено.")
        await state.clear()
    else:
        await state.clear()

async def main():
    logging.info("Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
