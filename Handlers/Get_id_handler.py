import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


logger = logging.getLogger(__name__)


class Get_id_handler(StatesGroup):

    get_id = State()




async def get_id(message: types.Message, state: FSMContext):
    await message.answer(f"Your ID is {message.from_user.id}")
    logger.info(f"Message from user {message.from_user.id}")
    
    await state.finish()

def register_handlers_get_id(dp: Dispatcher):
    dp.register_message_handler(get_id, commands="get_id", state="*")