from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_buttons_admin():
    """
        Creates an inline keyboard markup for start buttons for administrators.
        Returns:
            InlineKeyboardMarkup: Inline keyboard markup for start buttons.
        """
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text='Мои комбинации', callback_data='/my_combinations')
    kb_builder.button(text='Оповещения', callback_data='/notifications_menu')
    kb_builder.button(text='Пользователи', callback_data='/users_ops')
    kb_builder.button(text='Регионы', callback_data='/regs_menu')
    kb_builder.button(text='Проверить номера', callback_data='/check_numbers')

    kb_builder.adjust(2)
    return kb_builder.as_markup(resize_keyboard=True)


def edit_users_buttons():
    """
        Creates an inline keyboard markup for editing users for administrators.
        Returns:
            InlineKeyboardMarkup: Inline keyboard markup for editing users.
        """
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text='Добавить', callback_data='/add_member')
    kb_builder.button(text='Удалить', callback_data='/delete_member')
    kb_builder.button(text='Вывести список', callback_data='/get_members')
    kb_builder.button(text='Назад', callback_data='/back_btn')

    kb_builder.adjust(2)
    return kb_builder.as_markup(resize_keyboard=True)


def edit_combinations_buttons():
    """
       Creates an inline keyboard markup for editing combinations.
       Returns:
           InlineKeyboardMarkup: Inline keyboard markup for editing combinations.
       """
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text='Активные группы', callback_data='/get_active_groups')
    kb_builder.button(text='Установить группы', callback_data='/set_active_groups')
    kb_builder.button(text='Настройки групп', callback_data='/comb_groups')
    kb_builder.button(text='Назад', callback_data='/back_btn')

    kb_builder.adjust(2)
    return kb_builder.as_markup(resize_keyboard=True)


def edit_comb_groups():
    """
       Creates an inline keyboard markup for editing combinations.
       Returns:
           InlineKeyboardMarkup: Inline keyboard markup for editing combinations.
       """
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text='Просмотреть', callback_data='/get_combinations')
    kb_builder.button(text='Добавить', callback_data='/add_combination')
    kb_builder.button(text='Изменить', callback_data='/edit_comb_group')
    kb_builder.button(text='Удалить', callback_data='/del_combination')
    kb_builder.button(text='Назад', callback_data='/back_btn_comb')
    kb_builder.adjust(2)
    return kb_builder.as_markup(resize_keyboard=True)


def edit_notifications_buttons():
    """
        Creates an inline keyboard markup for editing notifications.
        Returns:
            InlineKeyboardMarkup: Inline keyboard markup for editing notifications.
        """
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text='Изменить', callback_data='/edit_notif')
    kb_builder.button(text='Назад', callback_data='/back_btn')

    kb_builder.adjust(2)
    return kb_builder.as_markup(resize_keyboard=True)


def edit_regions_buttons():
    """
           Creates an inline keyboard markup for editing notifications.
           Returns:
               InlineKeyboardMarkup: Inline keyboard markup for editing notifications.
           """
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text='Добавить', callback_data='/add_reg')
    kb_builder.button(text='Удалить', callback_data='/del_reg')
    kb_builder.button(text='Просмотреть', callback_data='/get_regs')
    kb_builder.button(text='Назад', callback_data='/back_btn')

    kb_builder.adjust(2)
    return kb_builder.as_markup(resize_keyboard=True)


def sub_buttons():
    """
        Creates an inline keyboard markup for subscription options.
        Returns:
            InlineKeyboardMarkup: Inline keyboard markup for subscription options.
        """
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text='Оформить подписку', callback_data='/add_subscription')

    kb_builder.adjust(2)
    return kb_builder.as_markup(resize_keyboard=True)


def pay_completed():
    """
        Creates an inline keyboard markup for indicating payment completion.
        Returns:
            InlineKeyboardMarkup: Inline keyboard markup for indicating payment completion.
        """
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text='Я оплатил', callback_data='/payment_complete')

    kb_builder.adjust(2)
    return kb_builder.as_markup(resize_keyboard=True)