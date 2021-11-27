import logging
import datetime
import time
import configparser

logger = logging.getLogger(__name__)

def get_config(fn: str = "config.ini") -> dict:
    logger.info(f"Reading config file {fn}.")
    config = configparser.ConfigParser()
    config.read(fn)
    logger.info(f"Read it {config.read(fn)}.")
    return config

def get_coins_names_from_config(config: configparser.ConfigParser) -> list:
    return [val for val in config.sections() if val not in not_coins_names]

def get_device_info(json: dict) -> str:
    logger.info("Getting devices at rig.")

    devices = []
    start_time = datetime.timedelta(seconds=int(time.time()) - json['start_time'])

    for device in json['miner']['devices']:
        device_item = device_fields.copy()
        device[info] = " ".join(device[info].split(" ")[-3:])
       
        for key in device_item.keys():
            value = str(device[key])
            if value == '-1':
                device_item[key] = ""
            else:
                device_item[key] = "{0:<17} {1:>14}\n".format(str(key).upper() + ":", value)
        devices.append(device_item)

    answer = ""
    for device in devices:
        for values in device.values():
            answer += values
        answer += "\n"

    answer += "{0:<17} {1:>14}\n".format("UPTIME", str(start_time))

    logger.info("Info about devices is prepared.")
    
    return answer


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
mem_temperature = 'memTemperature'

device_fields = dict.fromkeys(dict.fromkeys([info, mem_clock, core_clock, mem_utilization, core_utilization, hashrate, power, temperature, mem_temperature, fan, accepted_shares, rejected_shares, invalid_shares]))

not_coins_names = ['CLIENT', 'LIMITS', 'WALLET', 'HASHRATE', 'POWER']


