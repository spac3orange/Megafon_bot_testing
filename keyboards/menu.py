from aiogram.types import BotCommand


async def set_commands_menu(bot):
    """
        Set up the main menu commands for the bot.
        Args:
            bot (telegram.Bot): The Telegram bot instance.
        Returns:
            None
        """
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Главное меню'),
        BotCommand(command='/about',
                   description='Информация о боте'),
        BotCommand(command='/subscribe',
                   description='Подписаться'),
        BotCommand(command='/contacts',
                   description='Контакты')
    ]

    await bot.set_my_commands(main_menu_commands)
