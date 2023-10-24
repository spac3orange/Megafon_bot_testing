from aiogram.types import (CallbackQuery, Message)
from states.states import EditCombGroupsState, RemoveCombState
from aiogram import Router
from aiogram import F
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from filters.known_user import KnownUser
from database.db_action import db_get_comb_groups, db_add_combinations_to_group, db_remove_combinations_from_group
from data.config import config, logger
from keyboards import kb_user, kb_admin
from data.config import bot

router = Router()


def is_valid_combination(text: str) -> bool:
    valid_symb = '0123456789XABCDFG'
    combinations = text.split(',')
    for combination in combinations:
        combination = combination.strip()  # Удаляем лишние пробелы вокруг комбинации
        if len(combination) != 7 or not all(x in valid_symb for x in combination):
            return False
    return True

async def comb_exists(uid, index):
    comb_list = await db_get_comb_groups(uid)
    if len(comb_list) >= int(index):
        return True
    return False


@router.message(Command(commands='cancel'), StateFilter(EditCombGroupsState.edit_index))
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


@router.callback_query(F.data == '/edit_comb_group', KnownUser(F))
async def select_comb_index(callback: CallbackQuery, state: FSMContext):
    """
        Handles the callback query with data '/add_combination' for known users.

        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
            state (FSMContext): FSMContext object for managing the state.

        Returns:
            None
        """
    uid = callback.from_user.id
    try:
        combinations = await db_get_comb_groups(uid)
        if combinations:
            combinations_text = '\n'.join(
                f"{i + 1}. {combination.strip(',')}" for i, combination in enumerate(combinations)
            )
            await callback.message.answer(text='Пожалуйста выберите группу комбинаций для редактирования:\n\n'
                                               f'{combinations_text}')
            logger.info('Command edit combinations')
            await state.set_state(EditCombGroupsState.edit_index)
        else:
            await callback.message.answer(text='Группы комбинаций не найдены')

    except:
        logger.error('Combinations not found')
        await callback.message.answer(text='Группы комбинаций не найдены')


@router.message(StateFilter(EditCombGroupsState.edit_index))
async def edit_comb_group(message: Message, state: FSMContext):
    if await comb_exists(message.from_user.id, message.text):
        await state.update_data(comb_index=message.text)
        await message.answer('Операции с группой: \n\n'
                             '1. Добавить маски в группу.\n'
                             '2. Удалить маски из группы.\n\n'
                             'Пожалуйста введите номер операции:')
        await state.set_state(EditCombGroupsState.select_operation)
    else:
        await message.answer('Комбинации с таким номером не найдена')
        return

#-----------------------------------------------------------------------------


@router.message(StateFilter(EditCombGroupsState.select_operation), lambda message: message.text == '1')
async def group_add_masks(message: Message, state: FSMContext):
    await message.answer(LEXICON_RU['/add_combination'])
    await state.set_state(EditCombGroupsState.add_to_group)


@router.message(StateFilter(EditCombGroupsState.add_to_group), lambda message: is_valid_combination(message.text))
async def mask_add_user_comb(message: Message, state: FSMContext):
    uid = message.from_user.id
    grp_index = await state.get_data()
    await db_add_combinations_to_group(uid, grp_index['comb_index'], message.text)
    await message.answer(text='Группа комбинаций успешно обновлена', reply_markup=kb_admin.edit_comb_groups())
    await state.clear()


@router.message(StateFilter(EditCombGroupsState.add_to_group))
async def mask_invalid_comb(message: Message, state: FSMContext):
    await message.answer(LEXICON_RU['error_mask'])

#------------------------------------------------------------------------------


@router.message(StateFilter(EditCombGroupsState.select_operation), lambda message: message.text == '2')
async def group_del_mask(message: Message, state: FSMContext):
    await message.answer('Введите маски для удаления из группы:\n\n'
                         'Пример: XXAAABB, BBCCXXAA')
    await state.set_state(EditCombGroupsState.remove_from_group)


@router.message(StateFilter(EditCombGroupsState.remove_from_group), lambda message: is_valid_combination(message.text))
async def group_mask_deleted(message: Message, state: FSMContext):
    uid = message.from_user.id
    grp_index = await state.get_data()
    await db_remove_combinations_from_group(uid, grp_index['comb_index'], message.text)
    await message.answer(text='Группа комбинаций успешно обновлена', reply_markup=kb_admin.edit_comb_groups())
    await state.clear()


