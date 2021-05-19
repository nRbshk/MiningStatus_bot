import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Helpers.helpers import config, save_config

import subprocess

logger = logging.getLogger(__name__)


class Start_miner(StatesGroup):

    choose_rig = State()
    run_rig = State()


def run_rig(index):
    path = config['miner_path'] + '\\' + config['miners'][index]
    
    p = subprocess.Popen(path, creationflags=subprocess.CREATE_NEW_CONSOLE)

    config['active_miners'][index] = 1


async def choose_rig(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for val in config['name_miners']:
        kb.add(val)
    await message.answer("Choose rig.", reply_markup=kb)
    await Start_miner.choose_rig.set()

async def start_rig(message: types.Message, state: FSMContext):
    name = message.text
    if name not in config['name_miners']:
        await message.answer("Use keyboard.")
        return
    
    index = config['name_miners'].index(name)

    if '1' == config['active_miners'][index]:
        await message.answer("You need to stop this rig before launch new one.", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:    
        run_rig(index)

        await message.answer("Mining is running.", reply_markup=types.ReplyKeyboardRemove())

        last_message = await message.answer("Mining statistic will automaticaly updated here.")

        config['last_message'] = last_message['message_id']
        save_config(config)

        await state.finish()
    


def register_handlers_start_miner(dp: Dispatcher):
    dp.register_message_handler(choose_rig, commands="start_miner", state="*")
    dp.register_message_handler(start_rig, state=Start_miner.choose_rig)