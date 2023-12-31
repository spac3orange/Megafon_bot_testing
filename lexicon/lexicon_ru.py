"""
    File contains all bot replies
"""

LEXICON_RU: dict[str, str] = {
    '/start': 'Добро пожаловать!\n\n',

    '/about': 'Привет!\n'
              'Я бот, который умеет искать красивые номера на сайте оператора Megafon по заданным тобой маскам\n\n'
              'Для того, чтобы пользоваться моим функционалом, тебе необходимо оформить подписку\n\n'
              'Для оформления подписки введи команду /subscribe',

    '/add_member': 'Режим добавления пользователей в базу данных\n\n'
                   'Пожалуйста, введите id пользователя: ',

    'sub_date': 'Пожалуйста, введите количество дней подписки: ',

    '/remove_member': 'Режим удаления пользователей из базы данных\n\n'
                      'Пожалуйста, введите id пользователя: ',

    'user_removed': 'Пользователь удален из базы данных',

    'members': 'Мои пользователи:',

    'no_sub': 'Извините, функция доступна только подписчикам бота\n\n'
              'Для оформления подписки введите \n/subscribe',

    '/get_members': 'Список пользователей бота: ',

    '/add_combination': 'Пожалуйста, введите маски номеров через запятую.\n\n'
                        'Маска номера должна состоять из 7 символов и может содержать:\n\n'
                        '- латинские буквы — A,B,C,D,E,F,G;\n'
                        '- или цифры — от 0 до 9\n'
                        '- X если может быть любая цифра\n'
                        'Буквы и цифры можно комбинировать.\n\n'
                        'Например:\n'
                        '- маска ААА–BB11 — это номер 777–3311;\n'
                        '- маска 313–1BBB — это номер 313–1888',

    '/del_combination': 'Пожалуйста, введите номер удаляемой группы комбинаций:',

    'combinations': 'Мои комбинации:\n\n'
                    'Для получения дополнительной информации введите команду \n/help_combinations',

    'help_combinations': 'Активные группы - текущие активные группы комбинаций,'
                         ' по которым будет происходить поиск подходящих номеров.\n\n'
                         'Установить группы - выбрать и установить активные группы комбинаций из списка всех групп '
                         'комбинаций.\n\n'
                         'Настройки групп - добавление, удаление и изменение групп комбинаций.',

    'comb_saved': 'Группа комбинаций успешно сохранена',

    'error_mask': 'Маска номера введена не правильно\n\nМаска должна состоять из 7 символов\n\nПример:\nXAAX555\n\n'
                  'Для отмены ввода введите /cancel',

    'error_id': 'id пользователя введен не правильно\n\nid может состоять только из цифр\n\nПример:\n3495822345\n\n'
                'Для отмены ввода введите /cancel',

    'error_date': 'Не правильный ввод\n\nПожалуйста, введите количество дней подписки\n\nПример:\n7\n\n'
                  'Для отмены ввода введите /cancel',

    'cancel': 'Ввод отменён',

    'setting_time': 'Пожалуйста, введите время оповещения в формате hh:mm:\n\nПример: 23:00',

    'setting_days': 'Пожалуйста, введите дни по которым будут приходить оповещения\n\nПример: 0, 3, 6\n\n'
                    '0 - Понедельник\n6 - Воскресенье',

    'inv_notif_days': 'Не верно введены дни оповещения\n'
                      'Пожалуйста, введите дни по которым будут приходить оповещения\n\nПример: 0, 3, 6\n\n'
                      '0 - Понедельник\n6 - Воскресенье',

    'inv_notif_time': 'Не верно введено время оповещения'
                      'Пожалуйста, введите время оповещения в формате hh:mm:\n\nПример: 23:00',


    'unknown_command': 'Я не знаю такой команды',

    'subscribe': 'Прайс-лист:\n\n1 день - 990 рублей\n'
                 '1 неделя - 1990 рублей\n'
                 '2 недели - 2990 рублей\n'
                 '1 месяц - 4990 рублей',
    
    'sub_days': 'Для оформления подписки, пожалуйста переведите сумму соответствующую интересующему вас тарифному '
                'плану на карту администратору\n\n'
                'Номер карты: XXXXXXXXXXXXXXXXX\n\n'
                'После осуществления перевода, пожалуйста нажмите кнопку "Я оплатил"\n\n'
                'Администратор получит уведомление об оплате и добавит вас в список пользователей бота',

    'payment_complete': 'Спасибо!\n\n'
                        'Администратору отправлено уведомление об оплате',

    'contacts': 'Администратор - @A_Mike',

    'regions': 'Мои регионы для поиска номеров\n\n'
               'Получить список всех доступных регионов можно командой /regions',

    'add_reg': 'Пожалуйста, введите номера регионов через запятую:\n\n'
               'Пример: 0, 21, 22, 23, 67, 50\n\n'
               'Для ввода всех регионов введите all\n\n'
               'Получить список всех доступных регионов и их номеров можно командой /regions',

    'del_reg': 'Пожалуйста, введите номера удаляемых регионов через запятую:\n\n'
               'Для удаления всех регионов введите all',

    'regs_deleted': 'Регионы успешно обновлены',

    'reg_added_db': 'Регионы поиска номеров успешно обновлены',

    'inv_regs': 'Номера регионов указаны не верно\n\n'
                'Номера должны быть числами от 0 до 86 разделенными запятой\n\n'
                'Пример: 0, 22, 23, 47, 59, 80, 81\n\n'
                'Получить список всех доступных регионов и их номеров можно командой /regions',

    'groups': 'Мои группы комбинаций:',

    'edit_comb_grp': 'Пожалуйста выберите группу комбинаций для редактирования  :'



}

all_regs = ['0. Алтайский край',
            '1. Амурская область',
            '2. Архангельская область',
            '3. Астраханская область',
            '4. Белгородская область',
            '5. Брянская область',
            '6. Владимирская область',
            '7. Волгоградская область',
            '8. Вологодская область',
            '9. Воронежская область',
            '10. Еврейская автономная область',
            '11. Забайкальский край',
            '12. Ивановская область',
            '13. Иркутская область',
            '14. Калининградская область',
            '15. Калужская область',
            '16. Камчатский край',
            '17. Кемеровская область',
            '18. Кировская область',
            '19. Кисловодск',
            '20. Костромская область',
            '21. Краснодарский край',
            '22. Красноярский край',
            '23. Курганская область',
            '24. Курская область',
            '25. Липецкая область',
            '26. Магаданская область',
            '27. Москва и область',
            '28. Мурманская область',
            '29. Н.Новгород и область',
            '30. Набережные челны',
            '31. Новгородская область',
            '32. Новокузнецк',
            '33. Новосибирская область',
            '34. Омская область',
            '35. Оренбургская область',
            '36. Орловская область',
            '37. Пензенская область',
            '38. Пермский край',
            '39. Приморский край',
            '40. Псковская область',
            '41. Республика Адыгея',
            '42. Республика Алтай',
            '43. Республика Башкортостан',
            '44. Республика Бурятия',
            '45. Республика Дагестан',
            '46. Республика Ингушетия',
            '47. Республика Кабардино-Балкария',
            '48. Республика Калмыкия',
            '49. Республика Карачаево-Черкесия',
            '50. Республика Карелия',
            '51. Республика Коми',
            '52. Республика Марий-Эл',
            '53. Республика Мордовия',
            '54. Республика Саха (Якутия)',
            '55. Республика Северная Осетия',
            '56. Республика Татарстан',
            '57. Республика Тыва',
            '58. Республика Хакасия',
            '59. Ростовская область',
            '60. Рязанская область',
            '61. Самарская область',
            '62. Санкт-Петербург и область',
            '63. Саратовская область',
            '64. Сахалинская область',
            '65. Свердловская область',
            '66. Смоленская область',
            '67. Сочи',
            '68. Ставропольский край',
            '69. Сызрань',
            '70. Тамбовская область',
            '71. Тверская область',
            '72. Тольятти',
            '73. Томская область',
            '74. Тульская область',
            '75. Тюменская область',
            '76. Удмуртская Республика',
            '77. Ульяновская область',
            '78. Хабаровский край',
            '79. Ханты-Мансийский АО',
            '80. Челябинская область',
            '81. Череповец',
            '82. Чеченская республика',
            '83. Чувашская республика',
            '84. Чукотский АО',
            '85. Ямало-Ненецкий АО',
            '86. Ярославская область']

