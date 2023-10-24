from aiogram.types import CallbackQuery, Message
from aiogram import Router
from aiogram import F
from filters.known_user import KnownUser
from database.db_action import db_get_comb_groups, db_update_comb_group_status
from data.config import logger
from aiogram.fsm.context import FSMContext
from states.states import SetActiveGroups
from aiogram.filters import Command, StateFilter
from keyboards.kb_admin import edit_combinations_buttons

router = Router()

async def comb_exists(uid, indexes):
    comb_list = await db_get_comb_groups(uid)
    flag = False
    for index in indexes:
        if len(comb_list) >= int(index):
            continue
        else:
            return False
    return True

@router.callback_query(F.data == '/set_active_groups', KnownUser(F))
async def set_active_groups(callback: CallbackQuery, state: FSMContext):
    """
        Handles the callback query with data '/set_active_groups' for known users.
        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
        Returns:
            None
        """
    uid = callback.from_user.id
    try:
        active_groups = await db_get_comb_groups(uid)
        combinations_text = '\n'.join(
            f"{i + 1}. {combination.strip(',')}" for i, combination in enumerate(active_groups)
        )
        await callback.message.answer(text='Пожалуйста, через запятую введите номера групп комбинаций, которые вы '
                                           'хотите активировать:\n\n'
                                           'Пример: 1, 3, 4, 7\n\n'
                                           'Сохраненные группы комбинаций:\n'
                                           f'{combinations_text}')
        await state.set_state(SetActiveGroups.groups)
        logger.info('Command get combinations')

    except:
        logger.error('Combinations not found')
        await callback.message.answer(text='Группы комбинаций не найдены')


@router.message(StateFilter(SetActiveGroups.groups))
async def active_groups_updated(message: Message, state: FSMContext):
    try:
        uid = message.from_user.id
        index_list = message.text.split(',')
        index_list = [int(x.strip()) for x in index_list]
        print(index_list)
        if await comb_exists(uid, index_list):
            await db_update_comb_group_status(uid, index_list)
            await message.answer('Активные группы комбинаций успешно обновлены', reply_markup=edit_combinations_buttons())
        else:
            await message.answer('Группы комбинаций введены не верно')
    except Exception as e:
        logger.error(e)
        await message.answer('Ошибка при установке активных групп комбинаций.\n\nПожалуйста, попробуйте еще раз.',
                             reply_markup=edit_combinations_buttons())




