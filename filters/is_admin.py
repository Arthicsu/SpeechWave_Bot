import logging
from aiogram.filters import BaseFilter
from aiogram.types import Message

logger = logging.getLogger(__name__)
class IsAdminFilter(BaseFilter):
    def __init__(self, admin_ids: list[int]):
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        is_admin = message.from_user.id in self.admin_ids
        logging.info(f"Admin check for {message.from_user.id}: {is_admin}")
        return is_admin
