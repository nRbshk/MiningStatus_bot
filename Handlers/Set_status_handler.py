from typing import Set
from Handlers.Run_miner_handler import choose_rig
import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Helpers.helpers import config, save_config, get_coins_names_from_config
logger = logging.getLogger(__name__)


class Set_status_handler(StatesGroup):

    choose_rig = State()


async def start_set_status(message: types.Message, state: FSMContext):
    cid = str(message.from_user.id)
    if config['CLIENT']['chat_id'] == '-1':
        await message.answer("You need to specify your ID at bot. You can do this with /start.")
        await state.finish()
    elif config['CLIENT']['chat_id'] !=  cid:
        await message.answer("You are not admin and you can't use this bot.")
        await state.finish()
    else:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        names = get_coins_names_from_config(config)
        for val in names:
            kb.add(val)
        del names

        await message.answer("Choose rig.", reply_markup=kb)
        await Set_status_handler.choose_rig.set()

async def change_status(message: types.Message, state: FSMContext):
    name = message.text
    logger.info(f"change_status {name}")
    names = get_coins_names_from_config(config)
    if name not in names:
        await message.answer("Use keyboard.")
        return

    del names
    config[name]['active_miner'] = '0'
    save_config(config)
    await message.answer(f"Status disabled for rig {name} seted.", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

def register_handler_set_status(dp: Dispatcher):
    dp.register_message_handler(start_set_status, commands="set_status", state="*")
    dp.register_message_handler(change_status, state=Set_status_handler.choose_rig)