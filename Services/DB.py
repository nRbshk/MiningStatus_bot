import sqlite3
from Helpers.helpers import get_time, get_day_month_year
from enum import Enum, unique
import logging

logger = logging.getLogger(__name__)

@unique
class DB_positions(Enum):
    id_position = 0
    date = 1
    time = 2
    balance = 3
    profit_fiat = 4
    profit_crypto = 5


class DB:


    def insert_balance_profit(self, name, balance, profit_fiat, profit_coin):
        logger.info("START insert_balance_profit")
        conn = sqlite3.connect(f"{name}.db")
        cursor = conn.cursor()
       
        y, m, d = get_day_month_year()
        time = get_time()

        cursor.execute("INSERT INTO db_profit_balance VALUES (?, ?, ?, ?, ?, ?)", (None, sqlite3.Date(y, m , d), time, balance, profit_fiat, profit_coin))
        
        conn.commit()
        
        conn.close()

        logger.info("END insert_balance_profit")

        return 0

    def get_balance_profit(self, name, year, month, day):
        logger.info("START get_balance_profit")

        conn = sqlite3.connect(f"{name}.db")

        cursor = conn.cursor()
        start_date = sqlite3.Date(year, month, day)

        cursor.execute(f"SELECT * FROM db_profit_balance WHERE date_time >= ?", (start_date,))

        exucuted_data = cursor.fetchall()
        conn.commit()
        conn.close()

        logger.info("END get_balance_profit")
        return exucuted_data

db = DB()