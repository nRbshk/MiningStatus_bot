import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


logger = logging.getLogger(__name__)

class Show_handler(StatesGroup):

    get_info = State()



async def get_info(message: types.Message):
    pass