from aiogram.types import (CallbackQuery, Message)
from aiogram import Router
from aiogram import F
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.filters import StateFilter
from filters.known_user import KnownUser
from states.states import EditNotifState
from aiogram.fsm.context import FSMContext
from database.db_action import db_set_notification_settings
from keyboards.kb_admin import edit_notifications_buttons
from utils.scheduler import add_schedule
from data.config import logger
router = Router()

async def get_weekdays(string: str) -> str:
    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    indexes = [int(idx.strip()) for idx in string.split(',')]
    return ', '.join([weekdays[idx] for idx in indexes])

valid_days_filter = lambda text: all(part.strip().isdigit() and 0 <= int(part.strip()) <= 6 for part in text.split(','))


@router.callback_query(F.data == '/edit_notif', KnownUser(F))
async def set_notif_days(callback: CallbackQuery, state: FSMContext):
    """
        Handles the callback query with data '/edit_notif' for known users.
        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
            state (FSMContext): FSMContext object for managing the state.
        Returns:
            None
        """
    await callback.message.answer(text=LEXICON_RU['setting_days'])
    await state.set_state(EditNotifState.days)


@router.message(StateFilter(EditNotifState.days), lambda message: valid_days_filter(message.text))
async def set_notif_time(message: Message, state: FSMContext):
    """
        Handles a message with specific criteria for the message text in the state 'EditNotifState.days'.
        Args:
            message (Message): Message object containing the user's input.
            state (FSMContext): FSMContext object for managing the state.
        Returns:
            None
        """
    await state.update_data(days=message.text)
    await message.answer(text=LEXICON_RU['setting_time'])
    await state.set_state(EditNotifState.time)


@router.message(StateFilter(EditNotifState.time))
async def update_db_schedule(message: Message, state: FSMContext):
    """
        Handles a message in the state 'EditNotifState.time'.
        Args:
            message (Message): Message object containing the user's input.
            state (FSMContext): FSMContext object for managing the state.
        Returns:
            None
        """
    await state.update_data(time=message.text)
    data = await state.get_data()
    uid = message.from_user.id

    await db_set_notification_settings(uid, data['days'], data['time'])

    await add_schedule(uid, data['days'], data['time'])
    days = await get_weekdays(data['days'])
    await message.answer(text='Настройки оповещений обновлены'
                              f'\nДни: {days}'
                              f'\nВремя: {data["time"]}',
                         reply_markup=edit_notifications_buttons())
    logger.info(f'Notification settings for user {uid} updated')
    await state.clear()


@router.message(StateFilter(EditNotifState.days))
async def invalid_days(message: Message):
    """
        Handles a message in the state 'EditNotifState.days' when the input is invalid.
        Args:
            message (Message): Message object containing the user's input.
        Returns:
            None
        """
    await message.answer(LEXICON_RU['inv_notif_days'])
