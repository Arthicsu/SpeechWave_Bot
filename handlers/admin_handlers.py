import logging
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram_dialog import DialogManager, StartMode

from filters.is_admin import IsAdminFilter
from database.methods.statistics import fetch_statistics
from database.methods.user import fetch_users
from states.states import AdminDialogStates

admin_router = Router()

async def show_stats(dialog_manager: DialogManager, **kwargs) -> dict:
    bot: Bot = dialog_manager.middleware_data.get("bot")  # Получаем объект бота из middleware_data
    pool = getattr(bot, "db_pool", None)  # Получаем пул через атрибут бота
    bot_id = bot.id  # Получаем айдишник ботяры

    stats = await fetch_statistics(pool, bot_id)
    return {
        "total_users": stats.get("total_users", 0),
        "today_users": stats.get("today_users", 0),
        "total_requests": stats.get("total_requests", 0),
        "today_requests": stats.get("today_requests", 0),
    }


async def show_users(dialog_manager: DialogManager, **kwargs) -> dict:
    """
    Получает список всех пользователей из базы данных для отображения в диалоге.
    """
    bot = dialog_manager.middleware_data.get("bot")  # Получаем объект бота из middleware_data
    pool = getattr(bot, "db_pool", None)  # Получаем пул соединений через объект бота
    users = await fetch_users(pool)    # Получаем список пользователей

    # Формируем текст для отображения списка пользователей
    users_text = ""
    for user in users:
        users_text += (
            f"👤 Username: {user['username'] or '—'}\n"
            f" ├ ID Telegram: {user['id_telegram']}\n"
            f" ├ Премиум: {'Да' if user['is_premium'] else 'Нет'}\n"
            f" ├ Подписка с: {user['subscription_start'].strftime('%d-%m-%Y') if user['subscription_start'] else '—.—.—'}\n"
            f" └ Подписка до: {user['subscription_end'].strftime('%d-%m-%Y') if user['subscription_end'] else '—.—.—'}\n\n"
        )
    return {"users_text": users_text}


# вызов диалога админа
@admin_router.message(Command("admin"), IsAdminFilter)
async def admin_panel(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AdminDialogStates.admin_menu, mode=StartMode.RESET_STACK)
