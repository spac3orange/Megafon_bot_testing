from aiogram.types import (CallbackQuery, Message)
from states.states import DelRegState
from aiogram import Router
from aiogram import F
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from filters.known_user import KnownUser
from database.db_action import db_get_user_regions, db_remove_user_regions
from data.config import config, logger
from keyboards import kb_user, kb_admin
import datetime
from data.config import bot
from typing import List


router = Router()

valid_regs_filter = lambda text: all(part.strip().isdigit() and 0 <= int(part.strip()) <= 86 for part in text.split(
    ','))


@router.callback_query(F.data == '/del_reg', KnownUser(F))
async def add_user(callback: CallbackQuery, state: FSMContext):
    """
       Handles the callback query with data '/add_reg' for users who are known.
       Args:
           callback (CallbackQuery): CallbackQuery object containing callback data.
           state (FSMContext): FSMContext object for managing the state.
       Returns:
           None
       """
    await callback.message.answer(
        text=LEXICON_RU['del_reg']
    )
    await state.set_state(DelRegState.del_reg)


@router.message(StateFilter(DelRegState.del_reg))
async def regs_added(message: Message, state: FSMContext):
    uid = message.from_user.id
    if message.text == 'all':
        await db_remove_user_regions(uid, ['all'])
        await message.answer(text=LEXICON_RU['regs_deleted'],
                             reply_markup=kb_admin.edit_regions_buttons())
        await state.clear()
    else:
        del_regs = message.text.split(',')
        cur_regs = await db_get_user_regions(uid)

        for reg in del_regs:
            if reg.strip() not in cur_regs:
                await message.answer('Регионы введены не верно.\n'
                                     'Пожалуйста, повторите попытку.')
                break
        else:
            del_regs = [int(x) for x in del_regs]
            await db_remove_user_regions(uid, del_regs)
            await message.answer(text=LEXICON_RU['regs_deleted'],
                                 reply_markup=kb_admin.edit_regions_buttons())
            await state.clear()

