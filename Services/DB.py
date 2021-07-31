import sqlite3
from Helpers.helpers import get_h_m, get_day_month_year
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


    def insert_balance_profit(self, name, balance, profit_fiat, profit_coin, y_m_d=None, time=None):
        logger.info("START insert_balance_profit")
        conn = sqlite3.connect(f"{name}.db")
        cursor = conn.cursor()

        if y_m_d==None:
            y, m, d = get_day_month_year()
        else:
            y,m,d = y_m_d

        if time==None:
            time = get_h_m()

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

    def get_last_value(self, name):
        logger.info("START get_last_value")

        conn = sqlite3.connect(f"{name}.db")

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM db_profit_Balance WHERE ID = (SELECT MAX(ID)  FROM db_profit_Balance)")

        executed_data = cursor.fetchone()

        conn.commit()
        conn.close()

        logger.info("END get_last_value")
    
        return executed_data[DB_positions.date.value], executed_data[DB_positions.time.value], executed_data[DB_positions.balance.value]

db = DB()