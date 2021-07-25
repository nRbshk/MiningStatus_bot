import logging
import datetime
import time
from attr import has
from requests import get
from bs4 import BeautifulSoup
import configparser

logger = logging.getLogger(__name__)



def get_config(fn: str = "config.ini") -> dict:
    logger.info(f"Reading config file {fn}.")
    config = configparser.ConfigParser()
    config.read(fn)
    logger.info(f"Read it {config.read(fn)}.")
    return config

def save_config( config: configparser.ConfigParser, fn: str = "config.ini") -> None:
    logger.info(f"Saving config file {fn}.")
    with open(fn, 'w') as f:
        config.write(f)

    logger.info(f"Saved config config file {fn}.")



def get_device_info(json: dict) -> str:
    logger.info("Getting devices at rig.")

    devices = []
    start_time = datetime.timedelta(seconds=int(time.time()) - json['start_time'])

    for device in json['miner']['devices']:
        device_item = device_fields.copy()
        device[info] = " ".join(device[info].split(" ")[-2:]) # can be NVIDIA GEFORCE RTX 3060ti, getting only 3060 ti. Not Tested for AMD
       
        for key in device_item.keys():
            device_item[key] = "{0:<17} {1:>14}\n".format(str(key).upper() + ":", str(device[key]))

        devices.append(device_item)
    answer = ""
    for device in devices:
        for values in device.values():
            answer += values
        answer += "\n"

    answer += "{0:<17} {1:>14}\n".format("UPTIME", str(start_time))

    logger.info("Info about devices is prepared.")
    
    return answer

def get_profit(json: dict) -> str:
    logger.info("Checking profit for setuped rig")
    
    coin = coins_dict[json['stratum']['algorithm']]
    device_count = { }
    total_hashrate = 0.0
    total_power = 0.0
    
    for device in json['miner']['devices']:
        key = device[info]
        hrate = float(device[hashrate].split(' ')[0])
        dpower = float(device[power])
        if key in device_count.keys():
            device_count[key] += 1
        else:
            device_count.update({key : 1 })
        total_hashrate += hrate
        total_power += dpower

    response = get(f"https://whattomine.com/coins/{coin}?cost={config['LIMITS']['cost']}&hr={total_hashrate}&p={total_power}&fee={config['LIMITS']['fee']}&commit=Calculate")
    if response.status_code != 200:
        logger.info("Whattomine is not reachable!")
        return "Whattomine is not reachable!\n"
    

    soup = BeautifulSoup(response.text, 'lxml')

    table = [line for line in soup.find('tr', {'class' : 'table-active'}).text.split("\n") if line != ""]

    try:
        daily_profit = float(table[-1][1:])
        daily_estimated_rewards = float(table[2])
    except:
        logger.info("Whattomine is not reachable!")
        return "Whattomine is not reachable!"


    answer = print_profit_rewards(daily_profit, daily_estimated_rewards, json['stratum']['algorithm'])

    logger.info("Profit is generated for setuped rig.")


    return answer


async def prepare_message(json: dict) -> str:
    global count_to_write
    logger.info(f"Preparing message for count {count_to_write}.")

    answer = "{0:<17} {1:>14}\n".format("COIN:", json['stratum']['algorithm'])
    answer += get_device_info(json)
    answer += "\n"
    answer += get_profit(json)
    if count_to_write % 10 == 0:
        logger.info(answer)
        count_to_write = 1
    else:
        count_to_write += 1

    logger.info("Message is prepared.")
    return answer


def get_time() -> str:
    logger.info("START Getting date.")
    time = str(datetime.datetime.now())
    return time[0:19]


def check_maximum_profit(config) -> str:
    map_key_wallet =  dict(config.items("WALLET"))

    coins = map_key_wallet.keys()
    logger.info(f"Checking maximum profit for coins {map_key_wallet.keys()}")
    profit_dict = dict.fromkeys(coins)
    rewards_dict = dict.fromkeys(coins)
    answer = ""
    for coin in coins:
        current_coin = coins_dict[coin.lower()]
        response = get(f"https://whattomine.com/coins/{current_coin}?cost={config['LIMITS']['cost']}&hr={config['HASHRATE'][coin]}&p={config['POWER'][coin]}&fee={config['LIMITS']['fee']}&commit=Calculate")
        if response.status_code != 200:
            logger.warning("Whattomine is not reachable!")
            return "Whattomine is not reachable!\n"
            
        soup = BeautifulSoup(response.text, 'lxml')

        table = [line for line in soup.find('tr', {'class' : 'table-active'}).text.split("\n") if line != ""]
        try:
            profit_dict[coin] = float(table[-1][1:])
            rewards_dict[coin] = float(table[2])
        except:
            logger.warning("Whattomine is not reachable!")
            return "Whattomine is not reachable!\n"
        
        if config['WALLET'][coin] != '':
            answer += check_balance_at_nanopool(coin.lower(), config['WALLET'][coin])
        
        time.sleep(0.5)
        
    answer += "\nESTIMATED REWARDS\n" 

    for coin in coins:
        daily_profit = profit_dict[coin]

        daily_estimated_rewards = rewards_dict[coin]

        answer += print_profit_rewards(daily_profit, daily_estimated_rewards, coin)
        answer += "\n"


    logger.info(f"Profit is generate for {coins}.")

    return answer


def check_balance_at_nanopool(coin, wallet):
    logger.info(f"Checking balance for {coin} at nanopool.")

    response = get(f"https://api.nanopool.org/v1/{coin}/user/{wallet}")
    

    if response.status_code != 200:
        logger.warning("Nanopool is not reachable!")
        return "Nanopool is not reachable!\n"
    
    try:
        error = response.json()['error']
        logger.error(f"Nanopool error {error}")
        return f"Nanopool return error:\n{error}.\n"
    except:
        pass
        
    data = response.json()['data'] 
    balance = data['balance']
    unconfirmed_balance = data['unconfirmed_balance']
    answer = "{0:<20}{1:<10}\n".format("COIN", coin.upper())
    answer += "{0:<20}{1:<10}\n".format("BALANCE", balance)
    answer += "{0:<20}{1:<10}\n".format("UNCONFIRMED BALANCE", unconfirmed_balance)

    logger.info(f"Balance is checked for {coin} at nanopool.")

    return answer


def get_coins_names_from_config(config: configparser.ConfigParser) -> list:
    return [val for val in config.sections() if val not in not_coins_names]

def print_profit_rewards(profit: float, rewards: float, coin: str):
    answer  = "{0:<10}${1:<9}\n".format(coin.upper(), "FIAT")
    answer += "{0:<10}${1:<9}{2:>12}\n".format("DAY", profit, rewards)
    answer += "{0:<10}${1:<9}{2:>12}\n".format("WEEK", "{0:.2f}".format(profit * 7), "{0:.6f}".format(rewards * 7))
    answer += "{0:<10}${1:<9}{2:>12}\n".format("MONTH", "{0:.2f}".format(profit * 30), "{0:.6f}".format(rewards * 30))
    return answer


def get_day_month_year():
    logger.info("START get_day_month_year date")
    import datetime
    """
    return date in format day.month.year
    """
    time = str(datetime.datetime.now())
    time = time[0:10]
    year, month, day = time.split("-")
    return int(year), int(month), int(day)

def get_time():
    logger.info("START get_time")
    import datetime

    time = str(datetime.datetime.now()).split(" ")[1]
    time = ":".join(time.split(":")[0:2])

    return time


def get_current_profit(coin_name):
    coins = get_coins_names_from_config(config)
    coins = [coin for coin in coins if coin.startswith(coin_name.upper())]
    total_hashrate = 0.0
    total_power = 0.0
    for coin in coins:
        port = config[coin]['port']

        try:
            response = get(f'http://127.0.0.1:{port}/api/v1/status')
        except:
            logger.info(f"Rig at port {port} is not active!")
            continue
        json = response.json()
        for device in json['miner']['devices']:
            hrate = device[hashrate].split(" ")[0]
            total_hashrate += float(hrate)

            pwr = device[power]
            total_power += float(pwr)
    current_coin = coins_dict[coin_name.lower()]
    response = get(f"https://whattomine.com/coins/{current_coin}?cost={config['LIMITS']['cost']}&hr={total_hashrate}&p={total_power}&fee={config['LIMITS']['fee']}&commit=Calculate")
    
    if response.status_code != 200:
        logger.warning("Whattomine is not reachable!")
        return 1
    soup = BeautifulSoup(response.text, 'lxml')
    table = [line for line in soup.find('tr', {'class' : 'table-active'}).text.split("\n") if line != ""]
    try:
        day_profit = float(table[-1][1:])
        day_rewards = float(table[2])
    except:
        logger.warning("Whattomine is not reachable!")
        return "Whattomine is not reachable!\n"
    return day_profit, day_rewards


config = get_config("config.ini")


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


device_fields = dict.fromkeys(dict.fromkeys([info, mem_clock, core_clock, mem_utilization, core_utilization, hashrate, power, temperature, fan, accepted_shares, rejected_shares, invalid_shares]))

not_coins_names = ['CLIENT', 'LIMITS', 'WALLET', 'HASHRATE', 'POWER']

count_to_write = 0

coins_dict = {'ergo' : '340-erg-autolykos', 
              'ergo2' : '340-erg-autolykos', 
              'eth' : '151-eth-ethash',
              'eth2' : '151-eth-ethash',
              'ethash' : '151-eth-ethash',
              'ethash2' : '151-eth-ethash'}
