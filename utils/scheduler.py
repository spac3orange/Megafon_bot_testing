import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .regular_send import regular_send
from .schedule_unsub import scheduled_unsub
from data.config import logger

scheduler = AsyncIOScheduler()


async def work_timer() -> None:
    """
        Initiates a work timer that starts a scheduler and schedules a recurring job.
        Returns:
            None
        """
    scheduler.start()
    scheduler.add_job(scheduled_unsub, 'cron', day_of_week='mon-sun', hour=0, minute=0)
    while True:
        await asyncio.sleep(1)


async def add_schedule(uid: int, send_days: str, send_time: str) -> None:
    """
        Adds or updates a schedule for a user identified by their UID.
        Args:
            uid (int): User ID.
            send_days (str): Days of the week to send messages.
            send_time (str): Time to send messages (in HH:MM format).
        Returns:
            None
        """
    job = scheduler.get_job(str(uid))
    if job:
        job.reschedule(trigger='cron', day_of_week=send_days, hour=int(send_time.split(":")[0]), minute=int(
            send_time.split(":")[1]))
        logger.info(f'Schedule for {uid} updated')
    else:
        scheduler.add_job(regular_send, 'cron', day_of_week=send_days, hour=int(send_time.split(":")[
                                                                                                   0]),
                          minute=int(send_time.split(":")[1]), id=str(uid), args=(uid, ))
        logger.info(f'Schedule for {uid} created')


async def remove_schedule(uid: int) -> None:
    """
        Removes the schedule for a user identified by their UID.
        Args:
            uid (int): User ID.
        Returns:
            None
        """
    job = scheduler.get_job(str(uid))
    if job:
        scheduler.remove_job(str(uid))
        logger.info(f'Schedule for {uid} removed')
    else:
        logger.info(f'No schedule found for {uid}')
