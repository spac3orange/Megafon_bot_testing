from aiogram.types import (CallbackQuery, Message)
from aiogram.fsm.state import StatesGroup, State
from states.states import AddMaskState
from aiogram import Router
from aiogram import F
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from filters.known_user import KnownUser
from database.db_action import db_get_user_combinations
from utils import check_numbers

router = Router()


@router.callback_query(F.data == '/check_numbers', KnownUser(F))
async def get_numbers(callback: CallbackQuery):
    uid = callback.from_user.id
    combinations = await db_get_user_combinations(uid)
    print(combinations)

    result = await test.main(combinations)
    print(result)

    if result:
        for i in result:
            for k, v in i.items():
                reg = k
                type = v['classType']
                nums = v['phones']

                await callback.message.answer(text=f'Регион: {reg}\nТип номера: {type}\n Номера: {str(nums)}')
    else:
        await callback.message.answer(text='ничего не найдено')







