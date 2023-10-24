from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F
from lexicon.lexicon_ru import LEXICON_RU
from filters.known_user import KnownUser
from keyboards.kb_admin import edit_comb_groups, edit_combinations_buttons

router = Router()


@router.callback_query(F.data == '/comb_groups', KnownUser(F))
async def combinations_groups_menu(callback: CallbackQuery):
    """
       Handles the callback query with data '/my_combinations' for known users.
       Args:
           callback (CallbackQuery): CallbackQuery object containing callback data.
       Returns:
           None
       """
    await callback.message.answer(
        text=LEXICON_RU['groups'],
        reply_markup=edit_comb_groups()
    )


@router.callback_query(F.data == '/back_btn_comb')
async def grp_menu_back(callback: CallbackQuery):
    """
        Handles the callback query with data '/my_combinations'.
        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
        Returns:
            None
        """
    await callback.message.answer(text='Мои комбинации:', reply_markup=edit_combinations_buttons())