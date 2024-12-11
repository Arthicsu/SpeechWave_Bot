import asyncpg
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/SpeechWaveBotDB"

async def get_pool():
    return await asyncpg.create_pool(DATABASE_URL)

async def create_tables(pool):
    async with pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT,
                id_telegram BIGINT UNIQUE NOT NULL,
                is_premium BOOLEAN DEFAULT FALSE
            );
        ''')
        logger.info("Таблица users - ок")

        await conn.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id_bot BIGINT PRIMARY KEY,
                total_users INT DEFAULT 0,
                today_users INT DEFAULT 0,
                total_requests INT DEFAULT 0,
                today_requests INT DEFAULT 0
            );
        ''')
        logger.info("Таблица statistics - ок")

async def add_user(pool, username: str, id_telegram: int, is_premium: Optional[bool] = False):
    async with pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO users (username, id_telegram, is_premium) 
            VALUES ($1, $2, $3) 
            ON CONFLICT (id_telegram) DO NOTHING;
        ''', username, id_telegram, is_premium)

async def fetch_users(pool):
    async with pool.acquire() as conn:
        users = await conn.fetch('SELECT * FROM users;')
        return users

async def update_statistics(pool, id_bot: int, total_users: Optional[int] = None,
                            today_users: Optional[int] = None, total_requests: Optional[int] = None,
                            today_requests: Optional[int] = None):
    async with pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO statistics (id_bot, total_users, today_users, total_requests, today_requests)
            VALUES ($1, COALESCE($2, 0), COALESCE($3, 0), COALESCE($4, 0), COALESCE($5, 0))
            ON CONFLICT (id_bot) DO UPDATE SET 
                total_users = COALESCE($2, statistics.total_users),
                today_users = COALESCE($3, statistics.today_users),
                total_requests = COALESCE($4, statistics.total_requests),
                today_requests = COALESCE($5, statistics.today_requests);
        ''', id_bot, total_users, today_users, total_requests, today_requests)

async def fetch_statistics(pool, id_bot: int) -> Dict[str, Any]:
    async with pool.acquire() as conn:
        stats = await conn.fetchrow('SELECT * FROM statistics WHERE id_bot = $1;', id_bot)
        return dict(stats) if stats else {}