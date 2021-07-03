import logging

from asyncio import sleep

from aiogram.utils.markdown import code
from aiogram import types


from Helpers.helpers import check_maximum_profit, config, prepare_message, save_config, get_coins_names_from_config, get_time

from aiogram import Bot

from requests import get


logger = logging.getLogger(__name__)


async def check_rig(bot: Bot):
    delay = int(config['CLIENT']['delay'])

    while True:
        logger.info("Checking rigs")
        if config['CLIENT']['chat_id'] == '-1':
            logger.warning("User id is '-1'. Its should be specified.")
            await sleep(delay)
            continue

        edited_msg = "STATISTIC\n"
        coins = get_coins_names_from_config(config)
        edited_msg += check_maximum_profit(config)

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
                edited_msg += await prepare_message(json)
                edited_msg += "\n"

            del response

        edited_msg += f"Updated at {get_time()}"
        edited_msg = code(edited_msg)
        if config['CLIENT']['last_message'] == "-1":
            last_message = await bot.send_message(chat_id=config['CLIENT']['chat_id'], text=edited_msg, parse_mode=types.ParseMode.MARKDOWN_V2)
            config['CLIENT']['last_message'] = str(last_message['message_id'])
            save_config(config)
        else:
            try:
                await bot.edit_message_text(edited_msg, config['CLIENT']['chat_id'], config['CLIENT']['last_message'], parse_mode=types.ParseMode.MARKDOWN_V2)
            except:
                logger.error("cant edit message")

        del edited_msg

        logger.info("Rigs are checked.")
        await sleep(delay)

