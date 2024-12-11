from aiogram import BaseMiddleware
from aiogram.types import Message
from database.database import update_statistics
import logging

logger = logging.getLogger(__name__)

class StatisticsMiddleware(BaseMiddleware):
    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    async def on_pre_process_message(self, message: Message, data: dict):
        user_id = message.from_user.id
        username = message.from_user.username or "Unknown"
        command = message.text if message.text.startswith("/") else None

        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO bot_usage (user_id, username, command, message_count)
                VALUES ($1, $2, $3, 1)
                ON CONFLICT (user_id, date::DATE)
                DO UPDATE SET 
                    message_count = bot_usage.message_count + 1,
                    command = COALESCE($3, bot_usage.command);
            ''', user_id, username, command)
