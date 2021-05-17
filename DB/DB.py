import logging
import sqlite3

from enum import Enum, unique

class DB:
    def __init__(self, db_file: str) -> None:
        """Connection to DB and saving cursor"""
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def setup_miner(self, args):
        """Setup miner"""
        pass

    def get_miner_info(self, args):
        """Get info about miner"""
        pass