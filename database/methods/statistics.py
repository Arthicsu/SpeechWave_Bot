from typing import Optional, Dict, Any

async def initialize_statistics(pool, id_bot: int):
    async with pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO statistics (id_bot, total_users, today_users, total_requests, today_requests)
            VALUES ($1, 0, 0, 0, 0)
            ON CONFLICT (id_bot) DO NOTHING;
        ''', id_bot)

async def update_statistics(pool, id_bot: int, total_users: Optional[int] = None,
                            today_users: Optional[int] = None, total_requests: Optional[int] = None,
                            today_requests: Optional[int] = None):
    async with pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO statistics (id_bot, total_users, today_users, total_requests, today_requests)
            VALUES ($1, COALESCE($2, 0), COALESCE($3, 0), COALESCE($4, 0), COALESCE($5, 0))
            ON CONFLICT (id_bot) DO UPDATE SET 
                total_users = statistics.total_users + COALESCE($2, 0),
                today_users = statistics.today_users + COALESCE($3, 0),
                total_requests = statistics.total_requests + COALESCE($4, 0),
                today_requests = statistics.today_requests + COALESCE($5, 0);
        ''', id_bot, total_users, today_users, total_requests, today_requests)


async def fetch_statistics(pool, id_bot: int) -> Dict[str, Any]:
    async with pool.acquire() as conn:
        stats = await conn.fetchrow('SELECT * FROM statistics WHERE id_bot = $1;', id_bot)
        return dict(stats) if stats else {}