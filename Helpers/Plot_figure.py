import matplotlib.pyplot as plt
from Services.DB import DB_positions as dbp

import logging
from numpy import arange

logger = logging.getLogger(__name__)
def split_data_from_list(data_list: list):
    logger.info("split data from list")
    date_time: list[str] = []
    balance: list[str] = []
    profit_fiat: list[str] = []
    profit_crypto: list[str] = []
    
    length = len(data_list)
    # step = 6
    # max_length_before_skip = 4 * 24 * 5
    # if length > max_length_before_skip:
    #     logger.info("the length is big. skipping some data")
    #     data_list = data_list[0:length:step]
        
    for data in data_list:
        date_time.append(data[dbp.date.value] + " " +  data[dbp.time.value])
        balance.append(float("{0:.5f}".format(float(data[dbp.balance.value]))))
        profit_fiat.append(float("{0:.2f}".format(float(data[dbp.profit_fiat.value]))))
        profit_crypto.append(float("{0:.5f}".format(float(data[dbp.profit_crypto.value]))))


    logger.info(f"prepared data for length {len(balance)}")
    return [date_time, balance, profit_fiat, profit_crypto]

def plot_figure(data_list: list):
    logger.info("plot graph")
    date_time, balance, profit_fiat, profit_crypto = split_data_from_list(data_list)
    # list_with_spaces = ["" for _ in range(len(date_time))]
    plt.figure(figsize=(19.2, 14.6), dpi=250)
    plt.subplot(3, 1, 1)
    plt.plot(date_time, balance, color='red', label='balance')
    plt.xticks(rotation=45)
    plt.xticks([])
    # plt.yticks(calculate_yticks(max(balance)))
    plt.legend()
    plt.ylim(bottom=0)
    plt.grid()
    plt.subplot(3, 1, 2)
    plt.plot(date_time, profit_fiat, color='green', label='profit_fiat$')
    plt.xticks(rotation=45)
    plt.xticks([])
    # plt.yticks(calculate_yticks(max(profit_fiat)))
    plt.legend()
    plt.grid()
    plt.ylim(bottom=0)
    plt.subplot(3, 1, 3)
    plt.plot(date_time, profit_crypto, color='blue', label='profit_crypto')
    plt.xticks(rotation=90)
    if len(date_time) > 100:
        plt.xticks(date_time[0::len(date_time) // 20])
    # plt.yticks(calculate_yticks(max(profit_crypto)))
    plt.legend()
    plt.grid()
    plt.ylim(bottom=0)

    
    plt.savefig('plt.png')
    logger.info("plot saved into plt.png")

def calculate_yticks( stop_point: float) -> list[float]:

    step = stop_point / 10
    return list(arange(0, stop_point, step))
