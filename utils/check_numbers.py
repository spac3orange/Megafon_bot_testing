import asyncio
import aiohttp
import aiofiles
from fake_useragent import UserAgent
from data.config import logger
from lexicon.reg_dictionary import reg_dict, rd2


async def check2(mask: str, req_regs: dict) -> str:
    ua = UserAgent()
    fake_ua = {'user-agent': ua.random}
    res = dict()
    for k, v in req_regs.items():
        url = f'https://api.shop.megafon.ru/number/{v}/maskSelection?offset=0&limit=44&mask={mask}'
        username = 'sp6i015wn0'
        password = 'mVmuv81ifB8DNpvc1m'
        proxy = f"http://{username}:{password}@ru.smartproxy.com:40000"
        retries = 3  # Количество попыток повторного запроса в случае ошибки
        while retries > 0:
            try:
                async with aiohttp.ClientSession(trust_env=True, headers=fake_ua) as session:
                    async with session.get(url=url, proxy=proxy) as response:  # Замените 'http://your-proxy-url' на
                        # фактический URL вашего прокси
                        jason = await response.json()
                        numbers = jason.get('numbers')
                        for item in numbers:
                            class_type = item['classType']
                            if class_type == 1:
                                class_type = 'Простой'
                            elif class_type == 2:
                                class_type = 'Серебряный'
                            elif class_type == 3:
                                class_type = 'Золотой'
                            elif class_type == 4:
                                class_type = 'Платиновый/VIP'
                            elif class_type == 5:
                                class_type = 'Бронзовый'
                            phones = item['phones']
                            res[k] = ({'classType': class_type, 'phones': phones})
                break  # Если запрос успешен, выходим из цикла
            except Exception as e:
                retries -= 1
                print(f"Ошибка при запросе: {e}. Повторный запрос...")

    file_content = ""
    if not res:
        return f'{mask}_empty'
    for k, v in res.items():
        file_content += f"Регион: {k}\n"
        file_content += f"Тип номера: {v['classType']}\n"
        file_content += "Номера: " + ", ".join(str(phone) for phone in v['phones']) + "\n"
        file_content += "\n"

    filename = f"{mask}.txt"
    async with aiofiles.open(f'utils/saved_results/{filename}', 'w', encoding='utf-8') as file:
        await file.write(file_content)
    return filename


async def main(masks: list, req_dict: dict):
    """
        Main entry point to check multiple masks.
        Args:
            masks (list): List of masks to check.
            req_dict (dict): dict of regs.
        Returns:
            list: List of filenames where the results are saved.
        """
    tasks = []
    if masks:
        for m in masks:
            task = asyncio.create_task(check2(m, req_dict))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
    else:
        logger.error('Маски не установлены')
        return None
    if results:
        logger.info('Sending results')
        print(results)
        return results
    logger.error('Ничего не найдено')
    return None



# # Example usage
# masks = ['XXXX555', 'XXX8888']
# result_paths = asyncio.run(main(masks))
# print(result_paths)