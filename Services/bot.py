import logging

from aiogram import Bot, Dispatcher, dispatcher, executor
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Helpers.helpers import get_token

logger = logging.getLogger(__name__)
proxy_url = ""

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/show', description='Show current mining stat')

    ]

    await bot.set_my_commands(commands)




async def start():
    logging.basicConfig(
        filename='log.log',
        filemode='w',
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt='%d-%m-%y %H:%M:%S'
    )
    logger.info("Starting bot")

    bot = Bot(token=get_token(), proxy=proxy_url)
    dp = Dispatcher(bot, storage=MemoryStorage())

    