from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F
from filters.is_admin import IsAdmin
from database.db_action import db_get_users_full, db_get_comb_groups
from data.config import logger

router = Router()


@router.callback_query(F.data == '/get_members', IsAdmin(F))
async def get_users(callback: CallbackQuery):
    """
        Handles the callback query with data '/get_members' for users who are administrators.
        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
        Returns:
            None
        """
    users_full = await db_get_users_full()
    text = ""
    for user in users_full:
        user_id = user['user_id']
        sub_until = user['sub_until']
        users_combinations = await db_get_comb_groups(user['user_id'])
        user_info = f"ID Пользователя: {user_id}\nПодписка до: {sub_until}\nКомбинации: " \
                    f"{','.join(users_combinations)}\n\n"
        text += user_info
    logger.info('Command get members')
    await callback.message.answer(text)
