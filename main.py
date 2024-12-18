import asyncio  # Библиотека для работы с асинхронным программированием
from aiogram import Bot, Dispatcher  # Основные компоненты Telegram-бота
from aiogram.fsm.storage.memory import MemoryStorage  # Хранилище состояний (в памяти)
from aiogram_dialog import setup_dialogs  # Подключение диалогов

# Импорт диалогов, обработчиков, фильтров, middleware и других модулей
from dialogs.admin_menu import admin_dialog  # Диалог для меню администратора
from database.methods.statistics import initialize_statistics  # Инициализация статистики
from filters.is_admin import IsAdminFilter  # Фильтр для проверки администратора
from config_data.config import Config, load_config  # Конфигурация приложения
from handlers import user_handlers, admin_handlers, payment_handlers, voice_handlers  # Обработчики
from handlers.admin_handlers import admin_router  # Роутер для администраторов
from middlewares.admin_middleware import AdminMiddleware  # Middleware для проверки администратора
from middlewares.config_middleware import ConfigMiddleware  # Middleware для передачи конфигурации
from middlewares.stats_middleware import StatisticsMiddleware  # Middleware для записи статистики
from database.models import create_tables  # Функция создания таблиц в БД
from database.database import get_pool  # Получение пула соединений с базой данных


# Асинхронная главная функция приложения
async def main():
    """
    Основная функция для запуска Telegram-бота.
    """

    # Загрузка конфигурации из файла .env
    config: Config = load_config()

    # Создание экземпляра Telegram-бота с переданным токеном
    bot = Bot(token=config.tg_bot.token)

    # Инициализация хранилища для состояний FSM (в оперативной памяти)
    storage = MemoryStorage()

    # Создание диспетчера для управления ботом
    dp = Dispatcher(storage=storage)

    # Настройка базы данных
    pool = await get_pool()  # Получение пула соединений с БД
    await create_tables(pool)  # Создание таблиц в БД (если их нет)
    await initialize_statistics(pool, bot.id)  # Инициализация статистики для бота
    setattr(bot, "db_pool", pool)  # Сохраняем пул соединений как атрибут бота

    # Настройка middleware
    dp.update.middleware(ConfigMiddleware(config))  # Middleware для передачи конфигурации
    dp.update.middleware(StatisticsMiddleware(pool))  # Middleware для работы со статистикой
    # dp.update.middleware(AdminMiddleware(db_pool=pool, bot_id=bot.id))  # (опционально) Middleware для админов

    # Регистрация обработчиков
    dp.include_router(user_handlers.user_router)  # Обработчики команд для пользователей
    dp.include_router(payment_handlers.user_router)  # Обработчики команд для платежей
    dp.include_router(voice_handlers.user_router)  # Обработчики команд для голосовых сообщений
    dp.include_router(admin_handlers.admin_router)  # Обработчики команд для администраторов

    # Настройка диалогов
    setup_dialogs(dp)  # Подключение системы диалогов
    dp.include_router(admin_dialog)  # Регистрация диалога администратора

    # Применение фильтра для сообщений от администраторов
    admin_ids = config.tg_bot.admin_ids  # Получение списка ID администраторов из конфигурации
    admin_router.message.filter(IsAdminFilter(admin_ids=admin_ids))  # Фильтр для администраторских сообщений

    # Удаление webhook (если был установлен) и запуск polling (опроса Telegram API)
    await bot.delete_webhook()  # Удаление webhook для перехода на polling
    await dp.start_polling(bot)  # Запуск обработки событий


# Точка входа в приложение
if __name__ == "__main__":
    asyncio.run(main())  # Запуск асинхронной функции main()