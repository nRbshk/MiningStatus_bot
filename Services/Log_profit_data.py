import logging

from asyncio import sleep


from Helpers.helpers import check_balance_at_nanopool, config, get_current_profit

from Services.DB import db

logger = logging.getLogger(__name__)



async def log_data():
    coin_name = 'ETH'
    delay_time = 60 * 15
    while True:
        balance = check_balance_at_nanopool(coin_name.lower(), config['WALLET'][coin_name.lower()]).split("\n")
        if len(balance) == 1:
            continue
        balance = balance[1].split(" ")[-1]

        profit_rewards = get_current_profit(coin_name)

        if profit_rewards == 1:
            continue
        day_profit, day_reward = profit_rewards

        db.insert_balance_profit(coin_name, balance, day_profit, day_reward)



        await sleep(delay_time)




