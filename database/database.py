import asyncpg

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/SpeechWaveBotDB"

async def get_pool():
    return await asyncpg.create_pool(DATABASE_URL)