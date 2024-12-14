import asyncio, logging
import locale
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from filters.is_admin import IsAdminFilter
from config_data.config import Config, load_config
from handlers import user_handlers, admin_handlers, payment_handlers, voice_handlers, other_handlers
from middlewares.config_middleware import ConfigMiddleware
from middlewares.stats_middleware import StatisticsMiddleware
from database.models import create_tables
from database.database import get_pool

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
         level=logging.INFO,
         format='%(filename)s:%(lineno)d #%(levelname)-8s '
                '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    pool = await get_pool()
    await create_tables(pool)
    setattr(bot, "db_pool", pool)
    dp.update.middleware(ConfigMiddleware(config))
    dp.update.middleware(StatisticsMiddleware(pool))
    dp.include_router(user_handlers.router)
    dp.include_router(payment_handlers.router)
    dp.include_router(voice_handlers.router)
    dp.include_router(admin_handlers.router)
    dp.message.filter(IsAdminFilter(config))
    # dp.include_router(other_handlers.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())