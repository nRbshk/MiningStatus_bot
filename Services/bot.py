import logging

from aiogram import Bot, Dispatcher, dispatcher, executor
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Helpers.helpers import config

from Handlers.Show_handler import register_handlers_show
from Handlers.Get_id_handler import register_handlers_get_id

from Services.Check_rig import check_rig

from asyncio import create_task

logger = logging.getLogger(__name__)
proxy_url = ""

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/show', description='Show current mining stat'),
        BotCommand(command='/setup', description='Setup miner'),
        BotCommand(command='/get_id', description='Return your ID')

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

    bot = Bot(token=config['token'], proxy=proxy_url)
    dp = Dispatcher(bot, storage=MemoryStorage())


    register_handlers_show(dp)
    register_handlers_get_id(dp)

    await set_commands(bot)

    create_task(check_rig(bot))
    await dp.start_polling(timeout=600)

    