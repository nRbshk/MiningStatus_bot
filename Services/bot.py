import logging

from aiogram import Bot, Dispatcher, dispatcher, executor
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Helpers.helpers import config

from Handlers.Run_miner_handler import register_handlers_start_miner
from Handlers.Start_handler import register_handlers_start
from Handlers.Stop_rigs_handler import register_handlers_stop

from Services.Check_rig import check_rig

from asyncio import create_task

logger = logging.getLogger(__name__)
proxy_url = ""

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='How to start'),
        BotCommand(command='/cancel', description='Reset to start'),
        BotCommand(command='/stop', description='Stop all rigs'),
        BotCommand(command='/run', description='Run choosen miner')

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
    
    register_handlers_start(dp)
    register_handlers_start_miner(dp)
    register_handlers_stop(dp)

    await set_commands(bot)

    create_task(check_rig(bot))
    
    await dp.start_polling(timeout=600)

    