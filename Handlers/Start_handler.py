import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Helpers.helpers import config, save_config
logger = logging.getLogger(__name__)


class Start_handler(StatesGroup):

    start = State()

async def cmd_cancel(message: types.Message, state: FSMContext):
    logger.info("CMD cancel")
    await state.finish()
    await message.answer("Cancel", reply_markup=types.ReplyKeyboardRemove())




async def start_h(message: types.Message, state: FSMContext):
    cid = str(message.from_user.id)
    if config['chat_id'] == "-1":
        last_message = await message.answer(f"Config file succesfully updated.\nIf config file is configured it will update automaticaly.")
        logger.info(f"Message from user {cid}")

        config['chat_id'] = cid
        config['last_message'] = last_message['message_id']
        
        save_config(config)
        
        await state.finish()
    elif config['chat_id'] != cid:
        await message.answer("You are not admin and you can't use this bot.")
        await state.finish()


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start_h, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')