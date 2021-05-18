import logging
import datetime
import time
logger = logging.getLogger(__name__)

count_to_write = 0

def get_config(fn: str = "config.config") -> dict:
    data = [line.strip("\n") for line in open(fn, 'r').readlines()]
    config = {}
    for line in data:
        key, value = line.split("=")
        config.update({key : value})

    return config

def save_config( config: dict, fn: str = "config.config") -> None:
    with open(fn, 'w') as f:
        for key, value in config.items():
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

json_dict = dict.fromkeys([info, mem_clock, core_clock, mem_utilization, core_utilization, hashrate, power, temperature, fan, accepted_shares, rejected_shares])

def prepare_message(json: dict) -> str:
    global count_to_write
    devices = []
    warning_info = ""
    start_time = datetime.timedelta(seconds=int(time.time()) - json['start_time'])

    for device in json['miner']['devices']:
        device_item = dict.fromkeys([info, mem_clock, core_clock, mem_utilization, core_utilization, hashrate, power, temperature, fan, accepted_shares, rejected_shares])
        device[info] = " ".join(device[info].split(" ")[-2:]) # can be NVIDIA GEFORCE RTX 3060ti, getting only RTX 3060ti. Not Tested for AMD
       
        accepted = int(device[accepted_shares])
        rejected = int(device[rejected_shares])
        
        percent_of_rejected = 100 * rejected / (accepted + rejected)

        for key in json_dict.keys():
            device_item[key] = "{0:<17} {1:>14}\n".format(str(key).upper() + ":", str(device[key]))


        if int(device[temperature]) > int(config['temp_limit']):
            warning_info += f"Temperature is {device[temperature]} at device {device[info]}!\n"
        if percent_of_rejected > int(config['allowed_percent_of_rejected_shares']):
            warning_info += f"Too much rejected shares {percent_of_rejected:.2f}%"

        devices.append(device_item)
    answer = ""
    for device in devices:
        for values in device.values():
            answer += values
        answer += "\n\n"

    answer += "Some profit\n"
    answer += "{0:<17} {1:>14}\n".format("UPTIME", str(start_time))
    answer += warning_info
    answer += "\n\n"
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

config = get_config("config.config")


