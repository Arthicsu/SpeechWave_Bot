async def create_tables(pool):
    async with pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT,
                id_telegram BIGINT UNIQUE NOT NULL,
                is_premium BOOLEAN DEFAULT FALSE,
                subscription_start TIMESTAMP DEFAULT NULL,
                subscription_end TIMESTAMP DEFAULT NULL
            );
        ''')

        await conn.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id_bot BIGINT PRIMARY KEY,
                total_users INT DEFAULT 0,
                today_users INT DEFAULT 0,
                total_requests INT DEFAULT 0,
                today_requests INT DEFAULT 0
            );
        ''')