from aiogram import BaseMiddleware
from aiogram.types import Message
# from database.models import update_statistics
import logging

logger = logging.getLogger(__name__)

class StatisticsMiddleware(BaseMiddleware):
    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    async def __call__(self, handler, event: Message, data: dict):
        if isinstance(event, Message):
            user_id = event.from_user.id
            username = event.from_user.username
            command = event.text if event.text and event.text.startswith("/") else None
            try:
                async with self.pool.acquire() as conn:
                    await conn.execute('''
                        INSERT INTO bot_usage (user_id, username, command, message_count)
                        VALUES ($1, $2, $3, 1)
                        ON CONFLICT (user_id, date::DATE)
                        DO UPDATE SET 
                            message_count = bot_usage.message_count + 1,
                            command = COALESCE($3, bot_usage.command);
                    ''', user_id, username, command)
            except Exception as e:
                logger.error(f"{e}")
        return await handler(event, data)
