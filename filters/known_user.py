from aiogram.filters import BaseFilter
from aiogram.types import Message
from database.db_action import db_get_users
from data.config import config

class KnownUser(BaseFilter):
    """
       Initializes a KnownUser instance.
       Args:
           user: User object or user-related data.
       Returns:
           None
       """
    def __init__(self, user) -> None:
        self.known_users = None

    async def get_all_users(self):
        users = await db_get_users()
        return users

    async def __call__(self, message: Message) -> bool:
        self.known_users = await self.get_all_users()
        # admin_id = config.admin_id
        # if admin_id not in self.known_users:
        #     self.known_users.append(admin_id)

        return message.from_user.id in self.known_users
