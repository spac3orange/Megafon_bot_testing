from aiogram.types import CallbackQuery, Message
from aiogram import Router
from aiogram import F
from lexicon.lexicon_ru import LEXICON_RU
from filters.known_user import KnownUser
from keyboards.kb_admin import edit_combinations_buttons
from aiogram.filters import Command

router = Router()


@router.callback_query(F.data == '/my_combinations', KnownUser(F))
async def combinations_menu(callback: CallbackQuery):
    """
       Handles the callback query with data '/my_combinations' for known users.
       Args:
           callback (CallbackQuery): CallbackQuery object containing callback data.
       Returns:
           None
       """
    await callback.message.answer(
        text=LEXICON_RU['combinations'],
        reply_markup=edit_combinations_buttons()
    )


@router.message(Command(commands='help_combinations'))
async def help_combinations(message: Message):
    await message.answer(LEXICON_RU['help_combinations'])


@router.callback_query(F.data == '/my_combinations')
async def inv_combinations_menu(callback: CallbackQuery):
    """
        Handles the callback query with data '/my_combinations'.
        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
        Returns:
            None
        """
    await callback.message.answer(text=LEXICON_RU['no_sub'])