from datetime import datetime


user_languages = {} #словарь для выбранного языка пользователя

async def add_user(pool, username: str, id_telegram: int, is_premium: bool, subscription_start: datetime, subscription_end: datetime):
    async with pool.acquire() as conn:
        query = '''
            INSERT INTO users (username, id_telegram, is_premium, subscription_start, subscription_end)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (id_telegram) DO UPDATE 
            SET is_premium = $3, subscription_start = $4, subscription_end = $5;
        '''
        await conn.execute(query, username, id_telegram, is_premium, subscription_start, subscription_end)


async def fetch_users(pool):
    async with pool.acquire() as conn:
        users = await conn.fetch('SELECT * FROM users;')
        return users

async def get_subscription_status(pool, id_telegram: int):
    async with pool.acquire() as conn:
        query = '''
            SELECT is_premium, subscription_end 
            FROM users 
            WHERE id_telegram = $1;
        '''
        result = await conn.fetchrow(query, id_telegram)
        if result:
            return result['is_premium'], result['subscription_end']
        return False, None
