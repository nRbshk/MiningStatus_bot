import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Helpers.helpers import config

from Handlers.Show_stat import register_handler_show_stat

logger = logging.getLogger(__name__)
proxy_url = ""

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/show_stat', description='Show miner stats'),
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

    bot = Bot(token=config['CLIENT']['token'], proxy=proxy_url)
    dp = Dispatcher(bot, storage=MemoryStorage())
    
    register_handler_show_stat(dp)

    await set_commands(bot)
    await dp.start_polling(timeout=600)

    