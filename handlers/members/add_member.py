from aiogram.types import (CallbackQuery, Message)
from states.states import UserAddState
from aiogram import Router
from aiogram import F
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from filters.is_admin import IsAdmin
from database.db_action import db_add_user
from data.config import config, logger
from keyboards import kb_user, kb_admin
import datetime
from data.config import bot


router = Router()


def calculate_future_date(days: str) -> str:
    """
        Calculates a future date based on the provided number of days from the current date.
        Args:
            days (int): Number of days to add to the current date.
        Returns:
            str: Formatted future date in the format "dd-mm-yyyy".
        """
    days = int(days) + 1
    current_date = datetime.date.today()
    future_date = current_date + datetime.timedelta(days=int(days))
    formatted_date = future_date.strftime("%d-%m-%Y")
    return formatted_date


@router.message(Command(commands='cancel'), StateFilter(UserAddState.update_db))
async def process_cancel_command_state(message: Message, state: FSMContext):
    """
        Processes the 'cancel' command when in a specific state (UserAddState.update_db).
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


@router.callback_query(F.data == '/add_member', IsAdmin(F))
async def add_user(callback: CallbackQuery, state: FSMContext):
    """
       Handles the callback query with data '/add_member' for users who are administrators.
       Args:
           callback (CallbackQuery): CallbackQuery object containing callback data.
           state (FSMContext): FSMContext object for managing the state.
       Returns:
           None
       """
    await callback.message.answer(
        text=LEXICON_RU['/add_member']
    )
    await state.set_state(UserAddState.user_id)


@router.message(StateFilter(UserAddState.user_id), lambda message: message.text.isdigit())
async def input_uid(message: Message, state: FSMContext):
    """
       Handles a message with specific criteria for the message text in the state 'UserAddState.user_id'.
       Args:
           message (Message): Message object containing the user's input.
           state (FSMContext): FSMContext object for managing the state.
       Returns:
           None
       """
    await state.update_data(id=message.text)
    await message.answer(
        text=LEXICON_RU['sub_date']
    )

    await state.set_state(UserAddState.update_db)


@router.message(StateFilter(UserAddState.update_db), lambda message: message.text.isdigit())
async def input_sub_time(message: Message, state: FSMContext):
    """
        Handles a message with specific criteria for the message text in the state 'UserAddState.update_db'.
        Args:
            message (Message): Message object containing the user's input.
            state (FSMContext): FSMContext object for managing the state.
        Returns:
            None
        """
    sub_days = message.text
    fut_data = calculate_future_date(sub_days)

    await state.update_data(subscription_until=fut_data)

    user_info = await state.get_data()
    await message.answer(
        text=f'Пользователь добавлен в базу данных\n\n'
             f'ID Пользователя: {user_info["id"]}\n'
             f'Подписка до: {user_info["subscription_until"]}\n',
        reply_markup=kb_admin.edit_users_buttons()
    )
    await db_add_user(user_info['id'], user_info['subscription_until'])
    logger.info(f'User {user_info["id"]} added to database')
    msg = 'Администратор подтвердил вашу заявку.\n' \
          'Теперь вы можете пользоваться функционалом бота.\n\n' \
          'Хорошего дня!'

    await bot.send_message(user_info['id'], msg)
    await state.clear()


@router.message(StateFilter(UserAddState.user_id))
async def input_sub_time(message: Message, state: FSMContext):
    """
        Handles a message in the state 'UserAddState.user_id'.
        Args:
            message (Message): Message object containing the user's input.
            state (FSMContext): FSMContext object for managing the state.
        Returns:
            None
        """
    await message.answer(
        text=LEXICON_RU['error_id']
    )

@router.message(StateFilter(UserAddState.update_db))
async def input_sub_time(message: Message, state: FSMContext):
    """
        Handles a message in the state 'UserAddState.update_db'.
        Args:
            message (Message): Message object containing the user's input.
            state (FSMContext): FSMContext object for managing the state.
        Returns:
            None
        """
    await message.answer(
        text=LEXICON_RU['error_date']
    )
