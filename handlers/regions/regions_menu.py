from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F
from lexicon.lexicon_ru import LEXICON_RU
from filters.known_user import KnownUser
from keyboards.kb_admin import edit_regions_buttons
router = Router()


@router.callback_query(F.data == '/regs_menu', KnownUser(F))
async def combinations_menu(callback: CallbackQuery):
    """
       Handles the callback query with data '/regs_menu' for known users.
       Args:
           callback (CallbackQuery): CallbackQuery object containing callback data.
       Returns:
           None
       """
    await callback.message.answer(
        text=LEXICON_RU['regions'],
        reply_markup=edit_regions_buttons()
    )


@router.callback_query(F.data == '/regs_menu')
async def get_numbers(callback: CallbackQuery):
    """
        Handles the callback query with data '/regs_menu'.
        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
        Returns:
            None
        """
    await callback.message.answer(text=LEXICON_RU['no_sub'])