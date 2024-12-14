from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from database.models import fetch_statistics
from filters.is_admin import IsAdminFilter
from config_data.config import Config

router = Router()

@router.message(Command(commands=['stats']), IsAdminFilter)
async def show_stats(message: Message, config: Config):
    stats = await fetch_statistics()
    total_users = stats["total_users"]
    today_users = stats["today_users"]
    total_requests = stats["total_requests"]
    today_requests = stats["today_requests"]

    text = (
        f"📊 Статистика использования бота:\n"
        f" ├ Всего пользователей: {total_users}\n"
        f" ├ Пользователей сегодня: {today_users}\n"
        f" ├ Всего запросов: {total_requests}\n"
        f" └ Запросов сегодня: {today_requests}"
    )
    await message.reply(text)
