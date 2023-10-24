from aiogram.types import (CallbackQuery, Message)
from data.config import logger
from states.states import RemoveCombState
from aiogram import Router
from aiogram import F
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from filters.known_user import KnownUser
from database.db_action import db_get_comb_groups, db_remove_combination_group
from keyboards.kb_admin import edit_comb_groups

router = Router()


@router.callback_query(F.data == '/del_combination', KnownUser(F))
async def del_comb_group(callback: CallbackQuery, state: FSMContext):
    """
        Handles the callback query with data '/del_combination' for known users.
        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
            state (FSMContext): FSMContext object for managing the state.
        Returns:
            None
        """
    try:
        uid = callback.from_user.id
        combinations = await db_get_comb_groups(uid)
        await callback.message.answer(
            text=LEXICON_RU['/del_combination']
        )

        combinations_text = '\n'.join(
            f"{i+1}. {combination}" for i, combination in enumerate(combinations)
        )

        await state.set_state(RemoveCombState.remove_comb)
        await callback.message.answer(combinations_text)
    except:
        await callback.message.answer(text='Комбинации не найдены')


@router.message(StateFilter(RemoveCombState.remove_comb))
async def remove_comb_group(message: Message, state: FSMContext):
    """
    Handles a message in the state 'RemoveCombState.remove_comb'.
    Args:
        message (Message): Message object containing the user's input.
        state (FSMContext): FSMContext object for managing the state.
    Returns:
        None
    """
    uid = message.from_user.id
    comb_indices = message.text.split(',')
    comb_indices = [int(x.strip()) for x in comb_indices]
    await db_remove_combination_group(uid, comb_indices)
    removed_comb_indices = ', '.join(str(x) for x in comb_indices)
    await message.answer(text=f'Группы комбинаций {removed_comb_indices} удалены')
    logger.info(f'Combination groups at indices {comb_indices} deleted')
    await message.answer('Мои группы комбинаций:', reply_markup=edit_comb_groups())
    await state.clear()
