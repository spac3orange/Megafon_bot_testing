from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU
from aiogram import Router

router = Router()


@router.message()
async def send_echo(message: Message):
    """
        Handles any message without a specific command.
        Args:
            message (Message): Message object containing the user's input.
        Returns:
            None
        """
    await message.reply(text=LEXICON_RU['unknown_command'])
