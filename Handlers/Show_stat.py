from typing import Set
import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import code

from Helpers.helpers import config, get_coins_names_from_config, get_device_info
from requests import get
logger = logging.getLogger(__name__)


class Show_stat(StatesGroup):

    show_stat = State()


async def start(message: types.Message, state: FSMContext):

    cid = str(message.from_user.id)
    if config['CLIENT']['chat_id'] == '-1':
        await message.answer("You need to specify your ID at bot. You can do this with /start.")
        await state.finish()
    elif config['CLIENT']['chat_id'] !=  cid:
        await message.answer("You are not admin and you can't use this bot.")
        await state.finish()
    else:
        coins = get_coins_names_from_config(config)
        msg = ""
        for coin in coins:
            try:
                port = config[coin]['port']
                response = get(f'http://127.0.0.1:{port}/api/v1/status')
            except:
                # edited_msg += f"\nRig at port {port} is not active!\n\n"
                logger.info(f"Rig at port {port} is not active!")
                continue

            if response.status_code == 200:
                json = response.json()
                msg += get_device_info(json)
                msg += "\n"

        await message.answer(code(msg), parse_mode=types.ParseMode.MARKDOWN_V2)


def register_handler_show_stat(dp: Dispatcher):
    dp.register_message_handler(start, commands="show_stat", state="*")