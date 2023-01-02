import pymysql

class DataBase:
    """Класс для работы с базой данных"""

    def __init__(self, data_base):
        """Подключение базы данных, создание курсора"""

    def show_deadline(self, group, day, month, year):
        """Показывает дедлайны на введенную дату"""

    def delete_deadline(self, group, day, month, year, number):
        """Удаляет дедлайн"""

    def show_next_n_deadline(self, group, n):
        """Показывает ближайшие n дедлайнов"""

    def record_exist(self, group, day, month, year):
        """True если на эту дату есть дедлайн, иначе False"""

    def make_user(self, id, group):
        """Добавляет пользователя в базу данных или изменяет его группу"""

    def make_admin(self, id, group):
        """Добавляет админа в базу данных или меняет его группу"""

    def take_dictionary(self, table_name, month, year):
        """Возвращает массив словарей для таблиц users и admins"""