import asyncio
from utils import check_numbers
import os
from aiogram.types.input_file import FSInputFile
from database.db_action import get_all_combinations_list
from data.config import bot


async def get_all_data_regular():

    RESULTS_DIR = "utils/saved_results/"
    data = await get_all_combinations_list()
    try:
        for d in data:
            uid = d['user_id']
            combs = d['combinations']
            print(uid, combs)
            result_paths = await check_numbers.main(combs)
            if result_paths:
                for path in result_paths:
                    if path:
                        filename = os.path.basename(path)
                        file_path = os.path.join(RESULTS_DIR, filename)
                        res = FSInputFile(file_path)
                        await bot.send_document(uid, res)
                        os.remove(file_path)
    except Exception as e:
        print(e)
# asyncio.run(get_all_data_regular())