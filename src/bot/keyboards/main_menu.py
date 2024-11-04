from aiogram import Bot
from aiogram.types import BotCommand

from bot.lexicon.lexicon_ru import LEXICON_COMMANDS_RU

async def set_main_menu(bot: Bot):
    """Creates main menu"""
    main_menu_commands: list[BotCommand] = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in LEXICON_COMMANDS_RU.items()
    ]
    await bot.set_my_commands(main_menu_commands)
