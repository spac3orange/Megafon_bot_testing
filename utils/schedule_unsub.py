from database.db_action import get_users_with_matching_date, db_remove_user
from data.config import logger, bot



async def scheduled_unsub():
    """
       Handles scheduled unsubscription for users whose subscription date has expired.

       Returns:
           None
       """
    users = await get_users_with_matching_date()
    for u in users:
        await db_remove_user(u)
        msg = 'Ваша подписка истекла\n' \
              'Чтобы пользоваться функционалом бота, пожалуйста продлите подписку\n\n' \
              'Подписаться /subscribe'
        bot.send_message(u, )
        logger.info(f'User {u} subscription date expired\nUser was removed from database')