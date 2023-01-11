from data_base import DataBase

"""Модуль подключается к базе данных"""

DB = DataBase("localhost",
              3306,
              "root",
              "",
              "deadlines_data_base")
