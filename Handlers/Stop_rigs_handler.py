import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Helpers.helpers import config, save_config

import psutil

logger = logging.getLogger(__name__)


class Start_handler(StatesGroup):

    stop = State()


def stop_rigs():
    name = 'nbminer.exe'
    for proc in psutil.process_iter():
        if name.lower() == proc.name().lower():
            proc.kill()
    for index in range(len(config['active_miners'])):
        config['active_miners'][index] = 0

async def stop(message: types.Message, state: FSMContext):
    cid = message.from_user.id
    if config['chat_id'] == '-1':
        await message.answer("You need to specify your ID at bot. You can do this with /start.")
        await state.finish()
    elif config['chat_id'] != cid:
        await message.answer("You are not admin and you can't use this bot.")
        await state.finish()
    else:
        stop_rigs()
        await message.answer("All rigs are stoped.")    
        save_config(config)
        
        await state.finish()

def register_handlers_stop(dp: Dispatcher):
    dp.register_message_handler(stop, commands="stop", state="*")