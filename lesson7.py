import asyncio
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from apscheduler.schedulers.asyncio import AsyncIOScheduler


TOKEN = '7741398834:AAHOhzzcOmH5ZvF-n0vW7MEb8PoJ4FB0SUk'


# Определяем состояния для машины состояний (FSM) для ввода напоминания
class ReminderStates(StatesGroup):
    waiting_for_text = State()  # Ожидание текста напоминания
    waiting_for_time = State()  # Ожидание времени (в секундах)


# Создаем роутер для регистрации хэндлеров
router = Router()

# Глобальные переменные для бота и планировщика
bot_instance: Bot = None
scheduler: AsyncIOScheduler = None


@router.message(Command("remind"))
async def set_reminder(message: types.Message, state: FSMContext):
    """
    Хэндлер для команды /remind.
    Запрашивает у пользователя текст напоминания и переводит состояние FSM в waiting_for_text.
    """
    await message.answer("Введите текст напоминания:")
    await state.set_state(ReminderStates.waiting_for_text)


@router.message(ReminderStates.waiting_for_text)
async def get_text(message: types.Message, state: FSMContext):
    """
    Хэндлер для получения текста напоминания.
    Сохраняет введенный текст в данные состояния и запрашивает время напоминания (в секундах),
    переводя состояние FSM в waiting_for_time.
    """
    await state.update_data(reminder_text=message.text)
    await message.answer("Введите время (в секундах):")
    await state.set_state(ReminderStates.waiting_for_time)


@router.message(ReminderStates.waiting_for_time, F.text.isdigit())
async def get_reminder_time(message: types.Message, state: FSMContext):
    """
    Хэндлер для получения времени напоминания в секундах.
    Если введено число, то вычисляется время запуска напоминания.

    """
    user_data = await state.get_data()
    reminder_text = user_data.get("reminder_text")
    delay = int(message.text)

    # Вычисляем время запуска с учетом таймзоны.
    run_time = datetime.now().astimezone() + timedelta(seconds=delay)

    # Добавляем задачу в планировщик.
    scheduler.add_job(
        send_reminder,  # Функция, которая будет вызвана по расписанию
        'date',  # Тип триггера "date" (однократный запуск)
        run_date=run_time,  # Время запуска (timezone-aware)
        args=[message.chat.id, reminder_text, bot_instance]
    )

    await message.answer(f"Напоминание установлено на {delay} секунд!")
    await state.clear()  # Сбрасываем состояние FSM


@router.message(ReminderStates.waiting_for_time)
async def invalid_time_input(message: types.Message):
    """
    Хэндлер для случая, когда пользователь вводит некорректное значение времени.
    Если введенное значение не является числом, отправляем сообщение с просьбой ввести число.
    """
    await message.answer("Пожалуйста, введите число секунд")


async def send_reminder(chat_id: int, text: str, bot: Bot):
    """
    Функция для отправки напоминания.
    Вызывается планировщиком APScheduler по заданному времени.
    """
    print("Отправка напоминания")
    await bot.send_message(chat_id=chat_id, text=f"Напоминание: {text}")


async def main():
    """
    Основная функция для запуска бота:
    - Инициализация бота.
    - Создание и запуск планировщика APScheduler.
    - Настройка диспетчера и запуск поллинга.
    """
    global bot_instance, scheduler
    bot_instance = Bot(token=TOKEN)

    # Получаем текущий событийный цикл
    loop = asyncio.get_running_loop()

    # Инициализируем планировщик с использованием текущего событийного цикла
    scheduler = AsyncIOScheduler(event_loop=loop)
    scheduler.start()  # Запускаем планировщик

    # Инициализируем диспетчер и подключаем роутер с нашими хэндлерами
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot_instance)


if __name__ == '__main__':
    asyncio.run(main())