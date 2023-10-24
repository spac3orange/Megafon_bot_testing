from aiogram.types import (CallbackQuery, Message)
from states.states import AddMaskState
from aiogram import Router
from aiogram import F
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from filters.known_user import KnownUser
from database.db_action import db_add_comb_group
from data.config import config, logger
from keyboards import kb_user, kb_admin

router = Router()

valid_symb = '0123456789XABCDFG'


def is_valid_combination(text: str) -> bool:
    valid_symb = '0123456789XABCDFG'
    combinations = text.split(',')
    for combination in combinations:
        combination = combination.strip()  # Удаляем лишние пробелы вокруг комбинации
        if len(combination) != 7 or not all(x in valid_symb for x in combination):
            return False
    return True


@router.message(Command(commands='cancel'), StateFilter(AddMaskState.input_combination))
async def process_cancel_command_state(message: Message, state: FSMContext):
    """
       Processes the 'cancel' command when in a specific state (AddMaskState.input_combination).

       Args:
           message (Message): Message object containing the user's command.
           state (FSMContext): FSMContext object for managing the state.

       Returns:
           None
       """
    if message.from_user.id == int(config.admin_id):
        await message.answer(
            text=LEXICON_RU['cancel'],
            reply_markup=kb_admin.start_buttons_admin()
        )
    else:
        await message.answer(
            text=LEXICON_RU['cancel'],
            reply_markup=kb_user.start_buttons_user()
        )
    await state.clear()


@router.callback_query(F.data == '/add_combination', KnownUser(F))
async def add_combination(callback: CallbackQuery, state: FSMContext):
    """
        Handles the callback query with data '/add_combination' for known users.

        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
            state (FSMContext): FSMContext object for managing the state.

        Returns:
            None
        """
    await callback.message.answer(
        text=LEXICON_RU['/add_combination']
    )
    await state.set_state(AddMaskState.input_combination)


@router.message(StateFilter(AddMaskState.input_combination),
                lambda message: is_valid_combination(message.text))
async def save_combination(message: Message, state: FSMContext):
    """
        Handles a message with specific criteria for the message text in the state 'AddMaskState.input_combination'.
        Args:
            message (Message): Message object containing the user's input.
            state (FSMContext): FSMContext object for managing the state.
        Returns:
            None
        """
    await state.update_data(combination=message.text)
    await message.answer(
        text=LEXICON_RU['comb_saved'],
        reply_markup=kb_admin.edit_comb_groups()
    )
    uid = message.from_user.id
    comb = message.text
    lst = []
    lst.append(uid)
    lst.append(comb)
    logger.info('Combination saved')
    await db_add_comb_group(uid, comb)

    await state.clear()


@router.message(StateFilter(AddMaskState.input_combination))
async def inv_save_combination(message: Message, state: FSMContext):
    """
        Handles a message in the state 'AddMaskState.input_combination'.

        Args:
            message (Message): Message object containing the user's input.
            state (FSMContext): FSMContext object for managing the state.

        Returns:
            None
        """
    await message.answer(LEXICON_RU['error_mask'])



