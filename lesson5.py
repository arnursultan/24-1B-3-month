# import logging
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from aiogram import Bot, Dispatcher
# from aiogram.filters import Command
# from aiogram.types import Message
# import asyncio
#
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
#
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587
# EMAIL = "EMAIL"
# PASSWORD = "PASSWORD"
#
# BOT_TOKEN = "TOKEN"
#
# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher()
#
# def send_email(to_email, subject, text):
#     try:
#         logging.info("Подключаемся к SMTP-серверу...")
#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#         server.starttls()
#         logging.info("Успешно подключились. Авторизация...")
#         server.login(EMAIL, PASSWORD)
#         logging.info("Авторизация успешна. Отправляем письмо...")
#
#         msg = MIMEMultipart()
#         msg['From'] = EMAIL
#         msg['To'] = to_email
#         msg['Subject'] = subject
#         msg.attach(MIMEText(text, 'plain', 'utf-8'))
#
#         server.sendmail(EMAIL, to_email, msg.as_string())
#         server.quit()
#         logging.info(f"Письмо успешно отправлено на {to_email}")
#         return True
#     except Exception as e:
#         logging.error(f"Ошибка при отправке письма: {e}")
#         return False
#
# @dp.message(Command("sendmail"))
# async def send_mail_handler(message: Message):
#     args = message.text.split()
#     if len(args) < 2:
#         await message.answer("Используйте: /sendmail <email>")
#         return
#
#     to_email = args[1]
#     subject = "Привет от Telegram-бота!"
#     text = "Это тестовое письмо, отправленное через вашего Telegram-бота."
#
#     if send_email(to_email, subject, text):
#         await message.answer(f"Письмо успешно отправлено на {to_email}.")
#     else:
#         await message.answer("Произошла ошибка при отправке письма.")
#
# async def main():
#     logging.info("Бот запущен.")
#     await dp.start_polling(bot)
#
# if __name__ == "__main__":
#     asyncio.run(main())

import logging  # Импортируем библиотеку для логирования
import smtplib  # Импортируем библиотеку для работы с SMTP-серверами (для отправки email)
from aiogram import Bot, Dispatcher, types  # Импортируем компоненты aiogram для работы с ботом
from aiogram.filters import Command  # Импортируем фильтр для обработки команд
from aiogram.fsm.context import FSMContext  # Импортируем класс для работы с состояниями бота
from aiogram.fsm.state import StatesGroup, State  # Импортируем классы для создания состояний
from aiogram.fsm.storage.memory import MemoryStorage  # Хранилище состояний в памяти
import asyncio  # Импортируем asyncio для асинхронных задач
from aiogram.types import Message  # Импортируем тип Message для работы с сообщениями

# Настройка логирования, чтобы сообщения логировались с уровнем INFO
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Конфигурация для SMTP-сервера (для отправки email)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "EMAIL"
PASSWORD = "PASSWORD"

# Конфигурация для бота (токен, полученный от BotFather)
BOT_TOKEN = "TOKEN"

# Инициализация бота и диспетчера с использованием памяти для хранения состояний
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Определение машины состояний для работы с состояниями в боте
class BulkMailForm(StatesGroup):
    recipients = State()  # Состояние для получения email-адресов
    subject = State()  # Состояние для получения темы письма
    body = State()  # Состояние для получения текста письма

# Функция для отправки массовых email-рассылок
def send_bulk_email(to_emails, subject, text):
    try:
        # Подключаемся к SMTP-серверу и начинаем шифрованное соединение
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Шифрованное соединение
        server.login(EMAIL, PASSWORD)  # Аутентификация на сервере

        # Формируем сообщение с темой и текстом письма
        message = f"Subject: {subject}\n\n{text}"

        # Отправляем письма всем получателям
        for email in to_emails:
            server.sendmail(EMAIL, email, message)
            logging.info(f"Письмо успешно отправлено на {email}")  # Логируем успех
        server.quit()  # Закрываем соединение с сервером

        return True
    except Exception as e:
        logging.error(f"Ошибка при отправке писем: {e}")  # Логируем ошибку
        return False

# Обработчик команды /start, когда пользователь начинает взаимодействие с ботом
@dp.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await message.answer("Введите email-адреса получателей через запятую:")  # Запрашиваем email-адреса
    await state.set_state(BulkMailForm.recipients)  # Переходим к состоянию "recipients"

# Обработчик для состояния "recipients" (получение email-адресов)
@dp.message(BulkMailForm.recipients)
async def recipients_handler(message: Message, state: FSMContext):
    recipients = [email.strip() for email in message.text.split(",")]  # Разделяем введённые email по запятой
    await state.update_data(recipients=recipients)  # Сохраняем email-адреса в состояние
    await message.answer("Введите тему письма:")  # Запрашиваем тему письма
    await state.set_state(BulkMailForm.subject)  # Переходим к состоянию "subject"

# Обработчик для состояния "subject" (получение темы письма)
@dp.message(BulkMailForm.subject)
async def subject_handler(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)  # Сохраняем тему письма в состояние
    await message.answer("Введите текст письма:")  # Запрашиваем текст письма
    await state.set_state(BulkMailForm.body)  # Переходим к состоянию "body"

# Обработчик для состояния "body" (получение текста письма)
@dp.message(BulkMailForm.body)
async def body_handler(message: Message, state: FSMContext):
    data = await state.get_data()  # Получаем все данные из текущего состояния
    recipients = data["recipients"]  # Извлекаем email-адреса
    subject = data["subject"]  # Извлекаем тему письма
    body = message.text  # Получаем текст письма

    # Пытаемся отправить массовую рассылку
    if send_bulk_email(recipients, subject, body):
        await message.answer(f"Письма успешно отправлены на: {', '.join(recipients)}.")  # Успешный ответ
    else:
        await message.answer("Ошибка при отправке писем.")  # Ошибка при отправке

    await state.clear()  # Очищаем состояние после выполнения

# Основная асинхронная функция для запуска бота
async def main():
    logging.info("Бот запущен.")  # Логируем запуск бота
    await dp.start_polling(bot)  # Запускаем поллинг для обработки сообщений

# Запускаем основную функцию, если скрипт запускается напрямую
if __name__ == "__main__":
    asyncio.run(main())  # Запускаем асинхронную функцию main

# Мы написали Telegram-бота, который позволяет пользователям отправлять массовые email-рассылки. Бот собирает от пользователя следующие данные:
# Email-адреса получателей.
# Тему письма.
# Текст письма.
# После этого бот отправляет сообщение всем указанным получателям через SMTP-сервер Gmail.
# Всё взаимодействие с пользователем происходит через бота с использованием машины состояний для последовательного сбора данных.
