from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F
from filters.known_user import KnownUser
from keyboards.kb_admin import edit_notifications_buttons
from database.db_action import db_get_notification_settings
from lexicon.lexicon_ru import LEXICON_RU
from data.config import logger
router = Router()


async def get_weekdays(string: str) -> str:
    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    indexes = [int(idx.strip()) for idx in string.split(',')]
    return ', '.join([weekdays[idx] for idx in indexes])


@router.callback_query(F.data == '/notifications_menu', KnownUser(F))
async def combinations_menu(callback: CallbackQuery):
    """
       Handles the callback query with data '/notifications_menu' for known users.
       Args:
           callback (CallbackQuery): CallbackQuery object containing callback data.
       Returns:
           None
       """
    try:
        uid = callback.from_user.id
        cur_days, cur_time = await db_get_notification_settings(uid)
        if cur_days:
            cur_days = await get_weekdays(cur_days)
        await callback.message.answer(
            text=f'Текущие настройки:\n\nДни недели: {cur_days}\n\nВремя: {cur_time}',
            reply_markup=edit_notifications_buttons()
        )
    except Exception as e:
        logger.error(e)


@router.callback_query(F.data == '/notifications_menu')
async def get_numbers(callback: CallbackQuery):
    """
        Handles the callback query with data '/notifications_menu'.
        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
        Returns:
            None
        """
    await callback.message.answer(text=LEXICON_RU['no_sub'])