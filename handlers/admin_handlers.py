import logging
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters.command import Command
from filters.is_admin import IsAdminFilter
from config_data.config import Config
from database.methods.statistics import fetch_statistics
from database.methods.user import fetch_users

router = Router()

@router.message(Command(commands=['stats']), IsAdminFilter)
async def show_stats(message: Message, bot: Bot, config: Config):
    try:
        pool = getattr(bot, "db_pool", None)  # получаем пул через bot
        id_bot = bot.id
        if pool is None:
            await message.reply("Ошибка подключения к базе данных.")
            return

        stats = await fetch_statistics(pool, id_bot)  # Передаём pool в метод статистики
        total_users = stats.get("total_users", 0)
        today_users = stats.get("today_users", 0)
        total_requests = stats.get("total_requests", 0)
        today_requests = stats.get("today_requests", 0)

        text = (
            f"📊 Статистика использования бота:\n"
            f" ├ Всего пользователей: {total_users}\n"
            f" ├ Пользователей сегодня: {today_users}\n"
            f" ├ Всего запросов: {total_requests}\n"
            f" └ Запросов сегодня: {today_requests}"
        )
        await message.reply(text)
    except Exception as e:
        logging.error(f"Error in show_stats: {e}")
        await message.reply("Ошибка при получении статистики.")



@router.message(Command(commands=['users']), IsAdminFilter)
async def show_users(message: Message, bot: Bot):
    """
    Показывает список всех пользователей в бд.
    """
    pool = getattr(bot, "db_pool", None)  # пул с БД
    users = await fetch_users(pool)

    # проверка, есть ли пользователи в базе
    if not users:
        await message.reply("В базе данных пока нет пользователей.")
        return

    text = "📋 Список пользователей:\n"
    for user in users:
        text += (
            f"👤 Username: {user['username'] or '—'}\n"
            f" ├ ID Telegram: {user['id_telegram']}\n"
            f" ├ Премиум: {'Да' if user['is_premium'] else 'Нет'}\n"
            f" ├ Подписка с: {user['subscription_start'].strftime('%Y-%m-%d') if user['subscription_start'] else '—'}\n"
            f" └ Подписка до: {user['subscription_end'].strftime('%Y-%m-%d') if user['subscription_end'] else '—'}\n\n"
        )

    if len(text) > 4000:
        text = text[:3997] + "..."

    await message.reply(text)
