import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN

# Routers import
from bot.handlers.handlers import router
# Middlewares import
# ...
# Additional functions import
# ...
# Main menu keyboard import
from bot.keyboards.main_menu import set_main_menu

# Logger initizlization
logger = logging.getLogger(__name__)

async def main():
    """Configures and starts bot"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')

    storage = ...

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(
        # storage=storage,
    )

    # Initialize DB

    # dp.workflow_data.update({})

    await set_main_menu(bot)

    logger.info('Routers connection')
    dp.include_router(router=router)

    logger.info('Middlewares connection')
    # ...

    await bot.delete_webhook(drop_pending_updates=True) # skiping backlogging updates
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


