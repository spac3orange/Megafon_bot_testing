from aiogram.types import (CallbackQuery, Message)
from states.states import AddRegState
from aiogram import Router
from aiogram import F
from lexicon.lexicon_ru import LEXICON_RU
from lexicon.reg_dictionary import all_regs_str
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from filters.known_user import KnownUser
from database.db_action import db_add_user_regions, db_get_user_regions
from data.config import config, logger
from keyboards import kb_user, kb_admin
import datetime
from data.config import bot
from typing import List


router = Router()


valid_regs_filter = lambda text: text == 'all' or all(part.strip().isdigit() and 0 <= int(part.strip()) <= 86 for part
                                                     in text.split(','))



@router.callback_query(F.data == '/add_reg', KnownUser(F))
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
        text=LEXICON_RU['add_reg']
    )
    await state.set_state(AddRegState.input_regs)


@router.message(StateFilter(AddRegState.input_regs), lambda message: valid_regs_filter(message.text))
async def regs_added(message: Message, state: FSMContext):
    regs = message.text
    uid = message.from_user.id
    cur_regs = await db_get_user_regions(uid)
    check_regs = regs.split(',')
    print(check_regs)
    if regs == 'all':
        all_regs = all_regs_str
        await db_add_user_regions(uid, all_regs)
        await message.answer(text=LEXICON_RU['reg_added_db'],
                             reply_markup=kb_admin.edit_regions_buttons())
        await state.clear()
    # if cur_regs:
    #     for reg in check_regs:
    #         if reg in cur_regs:
    #             await message.answer('Ошибка. В вашем списке уже есть такой регион.')
    #             break
    # else:
    else:
        await db_add_user_regions(uid, regs)
        await message.answer(text=LEXICON_RU['reg_added_db'],
                             reply_markup=kb_admin.edit_regions_buttons())
        await state.clear()


@router.message(StateFilter(AddRegState.input_regs))
async def inv_regs(message: Message):
    await message.answer(text=LEXICON_RU['inv_regs'])
