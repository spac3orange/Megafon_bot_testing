import asyncio
from pprint import pprint
import aiohttp
from fake_useragent import UserAgent


reg_dict = {'altay': '738', 'amur': '495', 'arhangelsk': '655', 'astrakhan': '255', 'bel': '815', 'brn': '596',
            'vl': '615', 'volgograd': '97', 'vologda': '656', 'vrn': '835', 'eao': '455', 'chita': '519', 'iv': '658',
            'irkutsk': '496', 'kaliningrad': '657', 'klg': '616', 'kamchatka': '517', 'kem': '742', 'kirov': '477',
            'kis': '855', 'kstr': '695', 'krasnodar': '756', 'kras': '675', 'kurgan': '415', 'ks': '535', 'lc': '875',
            'magadan': '516', 'moscow': '3', 'murmansk': '696', 'nn': '356', 'chelny': '376', 'novgorod': '697',
            'nkz': '737', 'nsk': '555', 'omsk': '736', 'orenburg': '275', 'orl': '617', 'penza': '315', 'perm': '215',
            'prim': '75', 'pskov': '698', 'adygea': '895', 'altrep': '741', 'bashkortostan': '156', 'buryatia': '518',
            'dagestan': '1015', 'ingushetia': '1035', 'kbr': '775', 'kalmykia': '375', 'kchr': '955', 'karelia': '699',
            'komi': '478', 'mariel': '255', 'mordovia': '335', 'sakha': '521', 'alania': '975', 'tatarstan': '116',
            'tyva': '740', 'hakas': '739', 'rostov': '995', 'rzn': '536', 'samara': '12', 'spb': '14',
            'saratov': '175', 'skh': '520', 'svr': '36', 'sml': '700', 'sochi': '915', 'stavropol': '795',
            'syzran': '12', 'tmb': '935', 'tver': '701', 'tlt': '12', 'tom': '735', 'tula': '595', 'tyumen': '395',
            'udm': '476', 'ulyanovsk': '635', 'khb': '60', 'xmao': '136', 'chel': '195', 'cher': '715',
            'chechnya': '1036', 'chuvashia': '475', 'chukotka': '435', 'yanao': '416', 'yar': '702'}

rd2 = {'altay': '738', 'amur': '495', 'arhangelsk': '655', 'astrakhan': '255'}


async def check2(mask):
    ua = UserAgent()
    fake_ua = {'user-agent': ua.random}
    res = dict()
    for k, v in rd2.items():
        url = f'https://api.shop.megafon.ru/number/{v}/maskSelection?offset=0&limit=44&mask={mask}'
        async with aiohttp.ClientSession(trust_env=True, headers=fake_ua) as session:
            async with session.get(url=url) as response:
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
    return res


async def main(masks: list):
    tasks = []
    for m in masks:
        task = asyncio.create_task(check2(m))
        tasks.append(task)
    return await asyncio.gather(*tasks)

# pprint(asyncio.run(main(['XXXX555', 'XXX8888'])))
