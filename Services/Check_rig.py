import logging

from asyncio import sleep

from aiogram.utils.markdown import code
from aiogram import types


from Helpers.helpers import check_maximum_profit, config, prepare_message, save_config

from aiogram import Bot

from requests import get


logger = logging.getLogger(__name__)


async def check_rig(bot: Bot):
    delay = 30

    while True:
        logger.info("Starting check rigs")
        if config['chat_id'] == '-1':
            await sleep(delay)
            continue
        edited_msg = "STATISTIC\n"

        edited_msg += check_maximum_profit(config['coins'], config['avg_hashrates'], config['avg_powers'], config['wallets'])
        for port in config['ports']:
            try:
                response = get(f'http://127.0.0.1:{port}/api/v1/status')
            except:
                edited_msg += f"\nRig at port {port} is not active!\n\n"
                continue

            if response.status_code == 200:
                json = response.json()
                edited_msg += prepare_message(json)
                edited_msg += "\n\n"

            del response

                
        edited_msg = code(edited_msg)
        if config['last_message'] == "-1":
            last_message = await bot.send_message(chat_id=config['chat_id'], text=edited_msg, parse_mode=types.ParseMode.MARKDOWN_V2)
            config['last_message'] = last_message['message_id']
            save_config(config)
        else:
            try:
                await bot.edit_message_text(edited_msg, config['chat_id'], config['last_message'], parse_mode=types.ParseMode.MARKDOWN_V2)
            except:
                logger.error("cant edit message")

        del edited_msg
        await sleep(delay)

