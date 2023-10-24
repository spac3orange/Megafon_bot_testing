from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_buttons_user():
    """
        Creates an inline keyboard markup for start buttons for regular users.
        Returns:
            InlineKeyboardMarkup: Inline keyboard markup for start buttons.
        """
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text='Мои комбинации', callback_data='/my_combinations')
    kb_builder.button(text='Оповещения', callback_data='/notifications_menu')
    kb_builder.button(text='Регионы', callback_data='/regs_menu')
    kb_builder.button(text='Проверить номера', callback_data='/check_numbers')

    kb_builder.adjust(2)
    return kb_builder.as_markup(resize_keyboard=True)