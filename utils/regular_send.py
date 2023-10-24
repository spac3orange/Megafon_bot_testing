from utils import check_numbers
import os
from aiogram.types.input_file import FSInputFile
from database.db_action import db_get_active_combinations, db_get_user_regions
from data.config import bot, logger
from lexicon.reg_dictionary import reg_dict


async def get_dict_by_indexes(string: str, dictionary: dict) -> dict:
    indexes = [int(idx.strip()) for idx in string.split(',')]
    return {key: value for idx, (key, value) in enumerate(dictionary.items()) if idx in indexes}


async def regular_send(uid: int) -> None:
    """
        Sends results to a user identified by their UID.
        Args:
            uid (int): User ID.
        Returns:
            None
        """
    try:
        RESULTS_DIR = "utils/saved_results"
        combinations = await db_get_active_combinations(uid)
        print(combinations)
        if not combinations:
            await bot.send_message(text='Комбинации не установлены')
            return

        user_regions = await db_get_user_regions(uid)
        if not user_regions:
            await bot.send_message(text='Регионы не установлены')
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
            await bot.send_message(text='Некорректные комбинации')
            return

        regions = await get_dict_by_indexes(user_regions, reg_dict)
        result_paths = await check_numbers.main(valid_combinations, regions)

        if result_paths:
            for path in result_paths:
                if not path.endswith('empty'):
                    filename = os.path.basename(path)
                    file_path = os.path.join(RESULTS_DIR, filename)
                    res = FSInputFile(file_path)
                    await bot.send_document(uid, res)
                    os.remove(file_path)
                else:
                    msg = f'Номеров по маске {path.split("_")[0]} не найдено'
                    await bot.send_message(uid, msg)
        else:
            await bot.send_message(uid, text='Номера не найдены')
    except Exception as e:
        logger.error(e)
