from typing import Set

import logging
from aiogram.types import user
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, ReplyKeyboardRemove

from aiogram.utils.callback_data import CallbackData
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Helpers.helpers import config
from Helpers.Plot_figure import plot_figure

logger = logging.getLogger(__name__)

from Services.DB import db

keys = [['1','2','3'], ['4','5','6'] , ['7','8','9'] , ['SP', '0' , '<'], ['OK']]


kb_buttons = CallbackData('key', 'key_value')


class Show_figure_handler(StatesGroup):

    enter_date = State()
    # date_entered = State()


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
        # kb = types.InlineKeyboardMarkup(resize_keyboard=True)

        # for key_line in keys:
        #     buttons = []
        #     for key in key_line:
        #         buttons.append(types.InlineKeyboardButton(text=key, callback_data=kb_buttons.new(key_value=key)))
        #     kb.add(*buttons)
        await state.update_data(date="")
        await state.update_data(message=message)
        await message.answer("Enter start date for graph in format year month day.", reply_markup=None)
        await Show_figure_handler.enter_date.set()

async def show_graph(message: types.Message, state: FSMContext):
    logger.info("show graph")
    if len(message.text.split(" ")) != 3:
        logger.info("incorrect format")
        await message.answer("Enter in format year month day.")
    year, month, day = message.text.split(" ")
    logger.info(f"{year}, {month}, {day}")
    data = db.get_balance_profit('eth', int(year), int(month), int(day))

    if (len(data)) == 0:
        await message.answer("No data for this period.", reply_markup=ReplyKeyboardRemove())
    else:
        plot_figure(data)
        await message.answer_document(open('plt.png', 'rb'), reply_markup=ReplyKeyboardRemove())
        await state.finish()
    
# async def callback_enter_number(call: types.CallbackQuery, state: FSMContext):
#     user_data = await state.get_data("date")
#     value = call.data.split(":")[1]
#     if value == 'OK':
#         kb = ReplyKeyboardMarkup(resize_keyboard=True)
#         kb.add(user_data['date'])
#         await user_data['message'].answer('Press button', reply_markup=kb)
#         await Show_graph_handler.date_entered.set()
#     elif value == 'SP':
#         user_data['date'] += " "
#     elif value == '<':
#         user_data['date'] = user_data['date'][:-1]
#     else:
#         user_data['date'] += value
#     await call.answer(user_data['date'])
#     await state.set_data(user_data)

def register_handler_show_figure(dp: Dispatcher):
    dp.register_message_handler(start_enter_date, commands="show_figure", state="*")
    # dp.register_callback_query_handler(callback_enter_number, state=Show_graph_handler.enter_date)
    # dp.register_message_handler(show_graph, state=Show_graph_handler.date_entered)
    dp.register_message_handler(show_graph, state=Show_figure_handler.enter_date)