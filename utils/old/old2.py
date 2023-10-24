import asyncio
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import aiohttp

    reg_names = ['altay', 'amur', 'arhangelsk', 'astrakhan', 'bel', 'brn', 'vl', 'volgograd', 'vologda', 'vrn',
             'eao', 'chita', 'iv', 'irkutsk', 'kaliningrad', 'klg', 'kamchatka', 'kem', 'kirov', 'kis',
             'kstr', 'krasnodar', 'kras', 'kurgan', 'ks', 'lc', 'magadan', 'moscow', 'murmansk',
             'nn', 'chelny', 'novgorod', 'nkz', 'nsk', 'omsk', 'orenburg', 'orl', 'penza', 'perm', 'prim',
             'pskov', 'adygea', 'altrep', 'bashkortostan', 'buryatia', 'dagestan', 'ingushetia',
             'kbr', 'kalmykia', 'kchr', 'karelia', 'komi', 'mariel', 'mordovia', 'sakha', 'alania',
             'tatarstan', 'tyva', 'hakas', 'rostov', 'rzn', 'samara', 'spb', 'saratov', 'skh',
             'svr', 'sml', 'sochi', 'stavropol', 'syzran', 'tmb', 'tver', 'tlt', 'tom', 'tula', 'tyumen',
             'udm', 'ulyanovsk', 'khb', 'xmao', 'chel', 'cher', 'chechnya', 'chuvashia', 'chukotka', 'yanao',
             'yar']

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
async def check_numbers(masks: list):
    urls = []

    for m in masks:
        if len(m) == 7:
            url = f'https://moscow.shop.megafon.ru/connect/chnumber/masknum?maskSelection_1={m[0]}' \
                  f'&maskSelection_2={m[1]}&maskSelection_3={m[2]}&maskSelection_4={m[3]}&' \
                  f'maskSelection_5={m[4]}&maskSelection_6={m[5]}' \
                  f'&maskSelection_7={m[6]}'

            urls.append(url)

    pprint(urls)

    for u in urls:

        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(url=u) as response:
                print(await response.text())


asyncio.run(check_numbers(['2227755']))