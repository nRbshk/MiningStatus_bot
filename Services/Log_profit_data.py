import logging

from asyncio import sleep


from Helpers.helpers import check_balance_at_nanopool, config, get_current_profit, get_day_month_year, get_h_m

from Services.DB import db

from sqlite3 import Date

from datetime import datetime, timedelta
logger = logging.getLogger(__name__)



async def log_data():
    coin_name = 'ETH'
    delay_time = 60 * 15
    await check_at_start_disabled_time(coin_name)
    while True:
        await sleep(delay_time)
        logger.info("start log data")
        balance = check_balance_at_nanopool(coin_name.lower(), config['WALLET'][coin_name.lower()]).split("\n")
        if len(balance) == 1:
            continue
        balance = balance[1].split(" ")[-1]

        profit_rewards = get_current_profit(coin_name)

        if profit_rewards == 1:
            continue
        day_profit, day_reward = profit_rewards

        db.insert_balance_profit(coin_name, balance, day_profit, day_reward)


        logger.info("end log data")



async def check_at_start_disabled_time(coin_name):
    last_date, last_time, balance = db.get_last_value("eth")
    y, m, d = [int(v) for v in last_date.split("-")]
    last_date = Date(y,m,d)
    del y, m, d
    year, month, day = get_day_month_year()
    now_date = Date(year, month, day)
    now_time = get_h_m()
    hh_last, mm_last = [int(v) for v in last_time.split(":")]
    hh_now, mm_now = [int(v) for v in now_time.split(":")]

    last_minutes = hh_last * 60 + mm_last
    now_minutes = hh_now * 60 + mm_now

    if (now_date > last_date):
        total_minutes = int((now_date - last_date).total_seconds() / 60)
        step = 15
        date = datetime(last_date.year, last_date.month, last_date.day)
        date_was_updated = False
        for minutes in range(last_minutes + step, total_minutes + now_minutes, step):
            hh =(minutes // 60) % 24 
            mm = minutes % 60
            if hh == 0 and mm <= 15 and not date_was_updated:
                date += timedelta(days=1)
                date_was_updated = True
            elif date_was_updated:
                date_was_updated = False
            db.insert_balance_profit(coin_name, balance, 0.0, 0.0, (date.year, date.month, date.day), time=f"{hh}:{mm}")
    elif last_date == now_date and now_minutes - last_minutes > 20:
        step = 15
        for minutes in range(last_minutes + step, now_minutes, step):
            hh =(minutes // 60) % 24 
            mm = minutes % 60
            db.insert_balance_profit(coin_name, balance, 0.0, 0.0, (now_date.year, now_date.month, now_date.day), time=f"{hh}:{mm}")  




