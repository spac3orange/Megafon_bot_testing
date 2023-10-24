import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

reg_links = ['https://shop.megafon.ru/?rp=altay', 'https://shop.megafon.ru/?rp=amur',
             'https://shop.megafon.ru/?rp=arhangelsk', 'https://shop.megafon.ru/?rp=astrakhan',
             'https://shop.megafon.ru/?rp=bel', 'https://shop.megafon.ru/?rp=brn',
             'https://shop.megafon.ru/?rp=vl', 'https://shop.megafon.ru/?rp=volgograd',
             'https://vologda.shop.megafon.ru/', 'https://shop.megafon.ru/?rp=vrn',
             'https://shop.megafon.ru/?rp=eao', 'https://shop.megafon.ru/?rp=chita',
             'https://shop.megafon.ru/?rp=iv', 'https://shop.megafon.ru/?rp=irkutsk',
             'https://shop.megafon.ru/?rp=kaliningrad', 'https://shop.megafon.ru/?rp=klg',
             'https://shop.megafon.ru/?rp=kamchatka', 'https://shop.megafon.ru/?rp=kem',
             'https://shop.megafon.ru/?rp=kirov', 'https://shop.megafon.ru/?rp=kis',
             'https://shop.megafon.ru/?rp=kstr', 'https://shop.megafon.ru/?rp=krasnodar',
             'https://shop.megafon.ru/?rp=kras', 'https://shop.megafon.ru/?rp=kurgan',
             'https://shop.megafon.ru/?rp=ks', 'https://shop.megafon.ru/?rp=lc',
             'https://shop.megafon.ru/?rp=magadan', 'https://shop.megafon.ru/?rp=moscow',
             'https://shop.megafon.ru/?rp=murmansk', 'https://shop.megafon.ru/?rp=nn',
             'https://shop.megafon.ru/?rp=chelny', 'https://shop.megafon.ru/?rp=novgorod',
             'https://shop.megafon.ru/?rp=nkz', 'https://shop.megafon.ru/?rp=nsk',
             'https://shop.megafon.ru/?rp=omsk', 'https://shop.megafon.ru/?rp=orenburg',
             'https://shop.megafon.ru/?rp=orl', 'https://shop.megafon.ru/?rp=penza',
             'https://shop.megafon.ru/?rp=perm', 'https://shop.megafon.ru/?rp=prim']

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


def check_numbers(masks: list):
    with webdriver.Chrome() as browser:
        for reg in reg_names:
            try:
                print(reg)
                url = f'https://{reg}.shop.megafon.ru/connect/chnumber/masknum'
                browser.get(url)

                wait = WebDriverWait(browser, 10)
                found_element = False

                try:
                    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.popmechanic-close')))
                    found_element = True
                    print('элемент найден')
                    action = ac(browser)
                    action.send_keys(Keys.ESCAPE).perform()
                except Exception as e:
                    print(e)
                    continue

                time.sleep(0.3)

                for m in masks:
                    for i in range(1, 8):
                        field = browser.find_element(By.XPATH, f'//input[@name="maskSelection_{i}"]')
                        print('элемент найден')
                        if m[i] in ['x', 'X']:
                            continue
                        else:
                            field.send_keys(m[i-1])



                time.sleep(1)

            except Exception as e:
                print(e)
                continue


check_numbers(['123456', '789000'])
