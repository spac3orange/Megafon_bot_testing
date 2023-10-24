from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from lexicon.lexicon_ru import LEXICON_RU, all_regs
from aiogram import Router
from filters.known_user import KnownUser
from filters.is_admin import IsAdmin
from aiogram import F
from keyboards import kb_user, kb_admin
from data.config import config, logger, bot
router = Router()


@router.message(CommandStart(), IsAdmin(F))
async def process_start_command(message: Message):
    """
       Handles the '/start' command for users who are administrators.
       Args:
           message (Message): Message object containing the user's command.
       Returns:
           None
       """
    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=kb_admin.start_buttons_admin()
    )


@router.message(CommandStart())
async def process_start_command(message: Message):
    """
        Handles the '/start' command for all users.
        Args:
            message (Message): Message object containing the user's command.
        Returns:
            None
        """
    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=kb_user.start_buttons_user()
    )


@router.message(Command(commands='about'))
async def process_help_command(message: Message):
    """
        Handles the '/about' command.
        Args:
            message (Message): Message object containing the user's command.
        Returns:
            None
        """
    await message.answer(text=LEXICON_RU['/about'])


@router.callback_query(F.data == '/back_btn', KnownUser(F))
async def go_back(callback: CallbackQuery):
    """
        Handles the callback query with data '/back_btn' for known users.
        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
        Returns:
            None
        """
    if callback.from_user.id == int(config.admin_id):
        await callback.message.answer(
            text=LEXICON_RU['/start'],
            reply_markup=kb_admin.start_buttons_admin()
        )
    else:
        await callback.message.answer(
            text=LEXICON_RU['/start'],
            reply_markup=kb_user.start_buttons_user()
        )


@router.message(Command(commands='subscribe'))
async def subscribe(message: Message):
    """
        Handles the '/subscribe' command.
        Args:
            message (Message): Message object containing the user's command.
        Returns:
            None
        """
    await message.answer(text=LEXICON_RU['subscribe'],
                         reply_markup=kb_admin.sub_buttons())


@router.message(Command(commands='contacts'))
async def subscribe(message: Message):
    """
        Handles the '/contacts' command.
        Args:
            message (Message): Message object containing the user's command.
        Returns:
            None
        """
    await message.answer(text=LEXICON_RU['contacts'])


@router.message(Command(commands='regions'))
async def subscribe(message: Message):
    """
        Handles the '/regions' command.
        Args:
            message (Message): Message object containing the user's command.
        Returns:
            None
        """
    msg = '\n'.join(all_regs)
    await message.answer(text=msg)


@router.callback_query(F.data == '/add_subscription')
async def add_subscription(callback: CallbackQuery):
    """
        Handles the callback query with data '/add_subscription'.
        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
        Returns:
            None
        """
    await callback.message.answer(text=LEXICON_RU['sub_days'],
                                  reply_markup=kb_admin.pay_completed())


@router.callback_query(F.data == '/payment_complete')
async def add_subscription(callback: CallbackQuery):
    """
        Handles the callback query with data '/payment_complete'.
        Args:
            callback (CallbackQuery): CallbackQuery object containing callback data.
        Returns:
            None
        """
    uid = callback.from_user.id
    uname = callback.from_user.username
    logger.info(f'User {uid} approved payment')

    await callback.message.answer(text=LEXICON_RU['payment_complete'])
    msg = f'Пользователь @{uname} оплатил подписку\n' \
          f'ID Пользователя: {uid}\n' \
          f'Пожалуйста, проверьте баланс.'
    await bot.send_message(config.admin_id, msg)
