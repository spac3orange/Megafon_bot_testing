from aiogram.types import CallbackQuery, Message
from states.states import UserRemoveState
from aiogram import Router
from aiogram import F
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from filters.is_admin import IsAdmin
from database.db_action import db_remove_user
from keyboards import kb_admin
from utils.scheduler import remove_schedule
from data.config import logger

router = Router()


@router.callback_query(F.data == '/delete_member', IsAdmin(F))
async def remove_user_input(callback: CallbackQuery, state: FSMContext):
    """
        Handles the callback query with data '/delete_member' for users who are administrators.
        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
            state (FSMContext): FSMContext object for managing the state.
        Returns:
            None
        """
    await callback.message.answer(
        text=LEXICON_RU['/remove_member']
    )
    await state.set_state(UserRemoveState.user_id)


@router.message(StateFilter(UserRemoveState.user_id))
async def remove_user(message: Message, state: FSMContext):
    """
        Handles a message in the state 'UserRemoveState.user_id'.
        Args:
            message (Message): Message object containing the user's input.
            state (FSMContext): FSMContext object for managing the state.
        Returns:
            None
        """
    await state.update_data(id=message.text)
    await message.answer(
        text=LEXICON_RU['user_removed'],
        reply_markup=kb_admin.edit_users_buttons()
    )
    user_data = await state.get_data()
    logger.info(f'User with {user_data["id"]} removed from database')
    await remove_schedule(user_data['id'])
    await db_remove_user(user_data['id'])
    await state.clear()

