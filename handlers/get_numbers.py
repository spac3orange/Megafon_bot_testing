from aiogram.types import (CallbackQuery)
from aiogram import Router
from aiogram import F
from filters.known_user import KnownUser
from database.db_action import db_get_active_combinations, db_get_user_regions
from utils import check_numbers
import os
from aiogram.types.input_file import FSInputFile
from lexicon.lexicon_ru import LEXICON_RU
from lexicon.reg_dictionary import reg_dict
from data.config import logger

router = Router()


async def get_dict_by_indexes(string: str, dictionary: dict) -> dict:
    indexes = [int(idx.strip()) for idx in string.split(',')]
    return {key: value for idx, (key, value) in enumerate(dictionary.items()) if idx in indexes}


RESULTS_DIR = "utils/saved_results"


@router.callback_query(F.data == '/check_numbers', KnownUser(F))
async def get_numbers_known_user(callback: CallbackQuery):
    """
        Handles the callback query with data '/check_numbers' for known users.
        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
        Returns:
            None
        """
    try:
        uid = callback.from_user.id
        combinations = await db_get_active_combinations(uid)
        print(combinations)
        logger.info('Searching for combinations...')
        msg = 'Запущен поиск номеров\n' \
              'Это займет несколько минут'
        await callback.message.answer(msg)
        if not combinations:
            await callback.message.answer(text='Активные комбинации не установлены')
            return
        user_regions = await db_get_user_regions(uid)
        if not user_regions:
            await callback.message.answer(text='Регионы не установлены')
            return

        # Проверка и разделение комбинаций
        valid_combinations = []
        for combination_group in combinations:
            split_combinations = combination_group.split(', ')
            for combination in split_combinations:
                if len(combination) == 7:
                    valid_combinations.append(combination)
        print(valid_combinations)
        if not valid_combinations:
            await callback.message.answer(text='Некорректные комбинации')
            return

        regions = await get_dict_by_indexes(user_regions, reg_dict)
        result_paths = await check_numbers.main(valid_combinations, regions)



        if result_paths:
            for path in result_paths:
                if not path.endswith('empty'):
                    filename = os.path.basename(path)
                    file_path = os.path.join(RESULTS_DIR, filename)
                    res = FSInputFile(file_path)
                    await callback.message.answer_document(res)
                    os.remove(file_path)
                else:
                    await callback.message.answer(f'Номеров по маске {path.split("_")[0]} не найдено')
        else:
            await callback.message.answer(text='Номера не найдены')
    except Exception as e:
        logger.error(e)


@router.callback_query(F.data == '/check_numbers')
async def get_numbers(callback: CallbackQuery):
    """
        Handles the callback query with data '/check_numbers'.
        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
        Returns:
            None
        """
    await callback.message.answer(text=LEXICON_RU['no_sub'])