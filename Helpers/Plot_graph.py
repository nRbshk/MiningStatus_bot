import matplotlib.pyplot as plt
from Services.DB import DB_positions as dbp

import logging

logger = logging.getLogger(__name__)
def split_data_from_list(data_list: list):
    logger.info("split data from list")
    date_time: list[str] = []
    balance: list[str] = []
    profit_fiat: list[str] = []
    profit_crypto: list[str] = []
    
    length = len(data_list)
    step = 6
    max_length_before_skip = 4 * 24 * 5
    if length > max_length_before_skip:
        logger.info("the length is big. skipping some data")
        data_list = data_list[0:length:step]

    for data in data_list:
        date_time.append(data[dbp.date.value] + " " +  data[dbp.time.value])
        balance.append("{0:.5f}".format(float(data[dbp.balance.value])))
        profit_fiat.append("{0:.2f}".format(float(data[dbp.profit_fiat.value])))
        profit_crypto.append("{0:.5f}".format(float(data[dbp.profit_crypto.value])))

    logger.info("prepared data for length", len(balance))
    return [date_time, balance, profit_fiat, profit_crypto]

def plot_graph(data_list: list):
    logger.info("plot graph")
    date_time, balance, profit_fiat, profit_crypto = split_data_from_list(data_list)
    plt.figure(figsize=(19.2, 10.8), dpi=100)
    plt.plot(date_time, balance, color='red', marker='x', label='balance')
    plt.xticks(rotation=45)
    plt.plot(date_time, profit_fiat, color='green', marker='+', label='profit_fiat$')
    plt.xticks(rotation=45)
    plt.plot(date_time, profit_crypto, color='blue', marker='o', label='profit_crypto')
    plt.xticks(rotation=45)
    plt.legend()
    plt.savefig('plt.png')
    logger.info("plot saved into plt.png")
