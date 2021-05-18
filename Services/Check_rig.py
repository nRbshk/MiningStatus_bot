import logging

from asyncio import sleep

from aiogram.utils.markdown import code, bold
from aiogram import types


from Helpers.helpers import config, prepare_message

from aiogram import Bot

from requests import get, post


logger = logging.getLogger(__name__)

url = 'http://127.0.0.1:22333/api/v1/status'

async def check_rig(bot: Bot):
    delay = 10

    while True:
        logger.info("Starting check rigs")
        response = get(url)

        if response.status_code != 200:
            await sleep(delay)
            continue
        
        json = response.json()

        miner = json['miner']
        start_time = json['start_time']

        edited_msg = code(prepare_message(json))

        await bot.edit_message_text(edited_msg, config['chat_id'], config['last_message'], parse_mode=types.ParseMode.MARKDOWN_V2)



        await sleep(delay)

