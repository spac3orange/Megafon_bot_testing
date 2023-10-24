import asyncio
from aiogram import Dispatcher
from data.config import config, logger, bot
from handlers import (other_handlers, basic_handlers, get_numbers)
from handlers.notifications import not_menu, set_not
from aiogram.fsm.storage.memory import MemoryStorage
from keyboards.menu import set_commands_menu
from utils import scheduler
from database.db_action import (db_start, db_add_user,
                                db_get_users, db_remove_notifications)
from handlers.members import (add_member, get_members,
                              remove_member, members_menu)
from handlers.combinations import (add_combination, get_combinations,
                                   combinations_menu, del_combination,
                                   groups_menu, edit_comb_group,
                                   set_groups, get_avctive_groups)
from handlers.regions import (regions_menu, add_region,
                              get_regions, del_regions)


async def main_func() -> None:
    """
        Main function for the bot.
        Returns:
            None
        """
    dp = Dispatcher(storage=MemoryStorage())

    # Загружаем конфиг в переменную config
    logger.info('Bot started')
    try:
        users = await db_get_users()
        await db_remove_notifications()
        for u in users:
            alert = 'Бот был перезапущен.\n\n' \
                    'Пожалуйста, проверьте настройки оповещений.\n\n' \
                    'Хорошего дня!'

            await bot.send_message(u, alert)
    except Exception as e:
        logger.error(e)

    # Регистриуем роутеры в диспетчере
    dp.include_router(basic_handlers.router)
    dp.include_router(members_menu.router)
    dp.include_router(add_member.router)
    dp.include_router(remove_member.router)
    dp.include_router(get_members.router)
    dp.include_router(combinations_menu.router)
    dp.include_router(add_combination.router)
    dp.include_router(get_combinations.router)
    dp.include_router(del_combination.router)
    dp.include_router(get_numbers.router)
    dp.include_router(not_menu.router)
    dp.include_router(set_not.router)
    dp.include_router(regions_menu.router)
    dp.include_router(add_region.router)
    dp.include_router(get_regions.router)
    dp.include_router(del_regions.router)
    dp.include_router(groups_menu.router)
    dp.include_router(edit_comb_group.router)
    dp.include_router(set_groups.router)
    dp.include_router(get_avctive_groups.router)
    dp.include_router(other_handlers.router)


    # Регистрируем меню команд
    await set_commands_menu(bot)

    # инициализирем БД
    await db_start()

    # добавляем админа в БД
    await db_add_user(int(config.admin_id))

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def main() -> None:
    """
        Main function for running the bot and scheduler.
        Returns:
            None
        """
    task1 = asyncio.create_task(main_func())
    task2 = asyncio.create_task(scheduler.work_timer())
    await asyncio.gather(task1, task2)

if __name__ == '__main__':
    try:
        while True:
            asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning('Бот остановлен')
    except Exception as e:
        logger.error(e)
