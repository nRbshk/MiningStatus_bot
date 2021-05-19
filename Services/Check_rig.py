import logging

from asyncio import sleep

from aiogram.utils.markdown import code, bold
from aiogram import types


from Helpers.helpers import config, prepare_message, save_config

from aiogram import Bot

from requests import get


logger = logging.getLogger(__name__)


async def check_rig(bot: Bot):
    delay = 60

    while True:
        logger.info("Starting check rigs")
        if config['chat_id'] == '-1':
            await sleep(delay)
            continue
        edited_msg = ""
        for port in config['ports']:

            try:
                response = get(f'http://127.0.0.1:{port}/api/v1/status')
            except:
                edited_msg += f"Rig at port {port} is not active!\n\n"
                continue

            if response.status_code == 200:
                json = response.json()

                edited_msg += prepare_message(json)
                edited_msg += "\n\n"
        edited_msg = code(edited_msg)

        if config['last_message'] == "-1":
            last_message = await bot.send_message(chat_id=config['chat_id'], text=edited_msg, parse_mode=types.ParseMode.MARKDOWN_V2)
            config['last_message'] = last_message['message_id']
            save_config(config)
        else:
            await bot.edit_message_text(edited_msg, config['chat_id'], config['last_message'], parse_mode=types.ParseMode.MARKDOWN_V2)



        await sleep(delay)

