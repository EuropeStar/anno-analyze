import numpy as np
import sqlite3
from app.configs import DevConfig
from app.categories import ACTIVE_CATEGORIES


class DataSetCreator:
    N = 20

    def __init__(self, n_len):
        self.__DATA = []
        self.items_len = n_len

    def __build_dataset(self, n):
        for x in range(self.items_len):
            x = np.random.normal([n] * len(ACTIVE_CATEGORIES.keys()), size=len(ACTIVE_CATEGORIES.keys()))
            self.__DATA.append(
                list(map(round, x))
            )

    def __insert(self, required_flush=False):
        conn = sqlite3.connect(DevConfig.SQL_DB_PATH)
        with conn:
            crs = conn.cursor()
            if required_flush:
                crs.execute("DELETE FROM \"user\"")
            for x in self.__DATA:
                crs.execute("INSERT INTO \"user\" (sparse_vector) VALUES (?)", [x])


    def apply(self):
        self.__build_dataset()
        self.__insert(True)

    def create_data_set(self):
        self.__build_dataset(20)
        self.__build_dataset(80)
        return self.__DATA

if __name__ == '__main__':
    print(DataSetCreator(10000).create_data_set())
