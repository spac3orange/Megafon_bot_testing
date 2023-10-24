from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F
from filters.known_user import KnownUser
from database.db_action import db_get_comb_groups
from data.config import logger

router = Router()


@router.callback_query(F.data == '/get_combinations', KnownUser(F))
async def get_combinations_groups(callback: CallbackQuery):
    """
        Handles the callback query with data '/get_combinations' for known users.
        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
        Returns:
            None
        """
    uid = callback.from_user.id
    try:
        combinations = await db_get_comb_groups(uid)
        combinations_text = '\n'.join(
            f"{i + 1}. {combination.strip(',')}" for i, combination in enumerate(combinations)
        )
        await callback.message.answer(text=combinations_text)
        logger.info('Command get combinations')

    except:
        logger.error('Combinations not found')
        await callback.message.answer(text='Группы комбинаций не найдены')






