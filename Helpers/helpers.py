import logging
import datetime
import time
from requests import get, post
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


count_to_write = 0

def get_config(fn: str = "config.ini") -> dict:
    data = [line.strip("\n") for line in open(fn, 'r').readlines()]
    config = {}
    for line in data:
        if line.count('['):
            continue
        key, value = line.split("=")
        if key in ['ports', 'miners', 'active_miners', 'name_miners', 'avg_hashrates', 'avg_powers', 'wallets']:
            value = value.split(",")
        config.update({key : value})

    return config

def save_config( config: dict, fn: str = "config.ini") -> None:
    with open(fn, 'w') as f:
        for key, value in config.items():
            if key in ['active_miners', 'avg_hashrates', 'avg_powers']:
                for index, val in enumerate(config[key]):
                    config['active_miners'][index] = str(val)
            if key in ['ports', 'miners', 'active_miners', 'name_miners', 'avg_hashrates', 'avg_powers', 'wallets']:
                value = ",".join(value)
            if key == 'chat_id':
                f.write("[CLIENT]\n")
            if key == 'ports':
                f.write('[MINERS]\n')
            
            f.write(f"{key}={value}\n")
    
info = 'info'
mem_clock = 'mem_clock'
core_clock = 'core_clock'
mem_utilization = 'mem_utilization'
core_utilization = 'core_utilization'
hashrate = 'hashrate'
power = 'power'
temperature = 'temperature'
fan = 'fan'
accepted_shares = 'accepted_shares'
rejected_shares = 'rejected_shares'
invalid_shares =  'invalid_shares'

coins_dict = {'ergo' : '340-erg-autolykos', 'eth' : '151-eth-ethash', 'ethash' : '151-eth-ethash'}


def get_device_info(json: dict) -> str:
    devices = []
    warning_info = ""
    start_time = datetime.timedelta(seconds=int(time.time()) - json['start_time'])

    for device in json['miner']['devices']:
        device_item = dict.fromkeys([info, mem_clock, core_clock, mem_utilization, core_utilization, hashrate, power, temperature, fan, accepted_shares, rejected_shares, invalid_shares])
        device[info] = " ".join(device[info].split(" ")[-2:]) # can be NVIDIA GEFORCE RTX 3060ti, getting only RTX 3060ti. Not Tested for AMD
       
        for key in device_item.keys():
            device_item[key] = "{0:<17} {1:>14}\n".format(str(key).upper() + ":", str(device[key]))


        if int(device[temperature]) > int(config['temp_limit']):
            warning_info += f"Temperature is {device[temperature]} at device {device[info]}!\n"

        devices.append(device_item)
    answer = ""
    for device in devices:
        for values in device.values():
            answer += values
        answer += "\n"

    answer += "{0:<17} {1:>14}\n".format("UPTIME", str(start_time))
    answer += warning_info
    
    return answer

def get_profit(json: dict) -> str:

    coin = coins_dict[json['stratum']['algorithm']]
    device_count = { }
    total_hashrate = 0.0
    total_power = 0.0
    
    for device in json['miner']['devices']:
        key = device[info]
        hrate = float(device[hashrate].split('.')[0])
        dpower = float(device[power])
        if key in device_count.keys():
            device_count[key] += 1
        else:
            device_count.update({key : 1 })
        total_hashrate += hrate
        total_power += dpower

    response = get(f"https://whattomine.com/coins/{coin}?cost={config['cost']}&hr={total_hashrate}&p={total_power}")
    if response.status_code != 200:
        return "Whattomine is not reachable!"
    

    soup = BeautifulSoup(response.text, 'lxml')

    table = [line for line in soup.find('tr', {'class' : 'table-active'}).text.split("\n") if line != ""]

    daily_profit = float(table[-1][1:])
    week_profit = "{0:.2f}".format(daily_profit * 7)
    month_profit = "{0:.2f}".format(daily_profit * 30)
    daily_estimated_rewards = float(table[2])
    week_estimated_rewards = "{0:.6f}".format(daily_estimated_rewards * 7)
    month_estimated_rewards = "{0:.6f}".format(daily_estimated_rewards * 30)

    answer = ""
    answer += "{0:<10}${1:<9}{2:>12}\n".format("DAY", daily_profit, daily_estimated_rewards)
    answer += "{0:<10}${1:<9}{2:>12}\n".format("WEEK", week_profit, week_estimated_rewards)
    answer += "{0:<10}${1:<9}{2:>12}\n".format("MONTH", month_profit, month_estimated_rewards)

    return answer


def prepare_message(json: dict) -> str:
    global count_to_write
    answer = "{0:<17} {1:>14}\n".format("COIN:", json['stratum']['algorithm'])
    answer += get_device_info(json)
    answer += "\n"
    answer += get_profit(json)
    answer += "\n"
    answer += f"Updated at {get_time()}"
    if count_to_write % 10 == 0:
        logger.info(answer)
        count_to_write = 1
    else:
        count_to_write += 1
    return answer


def get_time() -> str:
    logger.info("START Getting date")
    """
    return date in format day.month.year
    """
    time = str(datetime.datetime.now())
    return time[0:19]


def check_maximum_profit(coins: list, hashrates: list, powers: list, wallets: list) -> str:
    profit_dict = dict.fromkeys(coins)
    answer = ""
    for index, coin in enumerate(coins):
        current_coin = coins_dict[coin]
        response = get(f"https://whattomine.com/coins/{current_coin}?cost={config['cost']}&hr={hashrates[index]}&p={powers[index]}")
        if response.status_code != 200:
            return "Whattomine is not reachable!"
            
        soup = BeautifulSoup(response.text, 'lxml')

        table = [line for line in soup.find('tr', {'class' : 'table-active'}).text.split("\n") if line != ""]

        profit_dict[coin] = float(table[-1][1:])

        if wallets[index] != '-':
            answer += check_ergo_balance_at_nanopool(coins[index], wallets[index])
    
    max_profit = max(profit_dict.values())
    max_profit_index = list(profit_dict.values()).index(max_profit)
    max_profit_coin = list(profit_dict.keys())[max_profit_index]

    answer += "\nBEST PROFIT COIN RIGHT NOW\n" 
    answer += "{0:<10}${1:<9}\n".format(max_profit_coin.upper(), "FIAT")
    answer += "{0:<10}${1:.2f}\n".format("DAY", max_profit)
    answer += "{0:<10}${1:.2f}\n".format("WEEK", max_profit * 7)
    answer += "{0:<10}${1:.2f}\n\n".format("MONTH", max_profit * 30)

    return answer


def check_ergo_balance_at_nanopool(coin, wallet):

    response = get(f"https://api.nanopool.org/v1/{coin}/user/{wallet}")

    if response.status_code != 200:
        return "Nanopool is not reachable!"
    
    data = response.json()['data']
    balance = data['balance']
    unconfirmed_balance = data['unconfirmed_balance']
    answer = "{0:<20}{1:<10}\n".format("COIN", coin.upper())
    answer += "{0:<20}{1:<10}\n".format("BALANCE", balance)
    answer += "{0:<20}{1:<10}\n".format("UNCONFIRMED BALANCE", unconfirmed_balance)
    return answer

config = get_config("config.ini")


