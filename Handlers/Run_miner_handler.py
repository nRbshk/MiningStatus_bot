import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Helpers.helpers import config, save_config, get_coins_names_from_config

import subprocess

logger = logging.getLogger(__name__)


class Start_miner(StatesGroup):

    choose_rig = State()
    run_rig = State()


def run_rig(name):
    temp_limit = config['LIMITS']['temp_limit']
    
    coin = name.lower()
    
    port = config[name]['port']
    
    pool_name = config[name]['pool_name']
    pool1 = config[name]['pool1']
    pool2 = config[name]['pool2']
    
    wallet = config[name]['wallet']
    rig_name = config[name]['rig_name']
    email = config[name]['email']

    devices = config[name]['devices']
    
    wallet_plus_rig_name = ""
    
    if pool_name == 'nicehash':
        wallet_plus_rig_name = f"{wallet}.{rig_name}"
    else:
        wallet_plus_rig_name = f"{wallet}.{rig_name}/{email}"

    run_miner =  f"nbminer -a {coin} -o {pool1} -u {wallet_plus_rig_name} "   

    if pool2 != '-':
        run_miner += f"-o1 {pool2} -u1 {wallet_plus_rig_name} "

    run_miner += f'-log --temperature-limit {temp_limit} --devices {devices} --api 127.0.0.1:{port}'
    
    logger.info(f"Running command:\n{run_miner}")
    p = subprocess.Popen(run_miner, creationflags=subprocess.CREATE_NEW_CONSOLE)

    config[name]['active_miner'] = '1'


async def choose_rig(message: types.Message, state: FSMContext):
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
        await Start_miner.choose_rig.set()

async def start_rig(message: types.Message, state: FSMContext):
    name = message.text
    names = get_coins_names_from_config(config)
    if name not in names:
        await message.answer("Use keyboard.")
        return
    
    del names
    if '1' == config[name]['active_miner']:
        await message.answer("You need to stop this rig before launch new one.", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:    
        run_rig(name)

        await message.answer("Mining is running.", reply_markup=types.ReplyKeyboardRemove())

        last_message = await message.answer("Mining statistic will automaticaly updated here.")

        config['CLIENT']['last_message'] = str(last_message['message_id'])
        save_config(config)

        await state.finish()
    


def register_handlers_start_miner(dp: Dispatcher):
    dp.register_message_handler(choose_rig, commands="run", state="*")
    dp.register_message_handler(start_rig, state=Start_miner.choose_rig)