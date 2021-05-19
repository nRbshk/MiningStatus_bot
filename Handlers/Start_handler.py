import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Helpers.helpers import config, save_config
logger = logging.getLogger(__name__)


class Start_handler(StatesGroup):

    start = State()




async def start_h(message: types.Message, state: FSMContext):
    cid = message.from_user.id
    last_message = await message.answer(f"Config file succesfully updated.\nIf config file is configured it will update automaticaly.")
    logger.info(f"Message from user {cid}")

    config['chat_id'] = cid
    config['last_message'] = last_message['message_id']
    
    save_config(config)
    
    await state.finish()

def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start_h, commands="start", state="*")