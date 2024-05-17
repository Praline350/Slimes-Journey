import os
import time
import threading
from tinydb import TinyDB, Query

PNJ_DATA_PATH = "../data/"

class PNJ:
    def _init__(self):
        self.db_pnj = TinyDB()


class Enemy(PNJ):
    def __init__(self):
        super().__init()

