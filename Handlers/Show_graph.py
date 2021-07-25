from typing import Set

import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Helpers.helpers import config
from Helpers.Plot_graph import plot_graph

logger = logging.getLogger(__name__)

from Services.DB import db

class Show_graph_handler(StatesGroup):

    enter_date = State()


async def start_enter_date(message: types.Message, state: FSMContext):
    logger.info("start enter date")
    cid = str(message.from_user.id)
    if config['CLIENT']['chat_id'] == '-1':
        await message.answer("You need to specify your ID at bot. You can do this with /start.")
        await state.finish()
    elif config['CLIENT']['chat_id'] !=  cid:
        await message.answer("You are not admin and you can't use this bot.")
        await state.finish()
    else:
        await message.answer("Enter start date for graph in format year month day.")
        await Show_graph_handler.enter_date.set()

async def show_graph(message: types.Message, state: FSMContext):
    logger.info("show graph")
    if len(message.text.split(" ")) != 3:
        logger.info("incorrect format")
        await message.answer("Enter in format year month day.")
    year, month, day = message.text.split(" ")
    logger.info(f"{year}, {month}, {day}")
    data = db.get_balance_profit('eth', int(year), int(month), int(day))

    if (len(data)) == 0:
        await message.answer("No data for this period.")
    else:
        plot_graph(data)
        await message.answer_document(open('plt.png', 'rb'))
        await state.finish()
    
    

def register_handler_show_graph(dp: Dispatcher):
    dp.register_message_handler(start_enter_date, commands="show_graph", state="*")
    dp.register_message_handler(show_graph, state=Show_graph_handler.enter_date)