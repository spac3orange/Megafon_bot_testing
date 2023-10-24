from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F
from lexicon.lexicon_ru import LEXICON_RU
from filters.known_user import KnownUser
from keyboards.kb_admin import edit_users_buttons

router = Router()


@router.callback_query(F.data == '/users_ops', KnownUser(F))
async def members_menu(callback: CallbackQuery):
    """
       Handles the callback query with data '/users_ops' for known users.
       Args:
           callback (CallbackQuery): CallbackQuery object containing callback data.
       Returns:
           None
       """
    await callback.message.answer(
        text=LEXICON_RU['members'],
        reply_markup=edit_users_buttons()
    )
