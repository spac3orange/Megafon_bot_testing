from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F
from filters.known_user import KnownUser
from database.db_action import db_get_user_regions
from typing import List
from lexicon.lexicon_ru import all_regs
from data.config import logger
router = Router()


async def get_elements_by_indexes(string: str, lst: List[str]) -> List[str]:
    indexes = [int(idx.strip()) for idx in string.split(',')]
    return [lst[idx] for idx in indexes]


@router.callback_query(F.data == '/get_regs', KnownUser(F))
async def get_users(callback: CallbackQuery):
    """
        Handles the callback query with data '/get_regs' for users who are known.
        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
        Returns:
            None
        """
    try:
        uid = callback.from_user.id
        regs_full = await db_get_user_regions(uid)
        if not regs_full:
            await callback.message.answer(text='Нет добавленных регионов для поиска')
        else:
            regs_full = await get_elements_by_indexes(regs_full, all_regs)
            await callback.message.answer(text='\n'.join(regs_full))
    except Exception as e:
        logger.error(e)

