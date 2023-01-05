import pymysql


class DataBase:
    """Класс для работы с базой данных"""

    def __init__(self, host, port, user, password, database):
        """Подключение базы данных, создание курсора"""

        try:
            self.connect = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
            )
        except Exception as e:
            print(e)
        else:
            print("db is connected")

        self.cursor = self.connect.cursor()

    async def show_deadline(self, group, day, month, year):
        """Показывает дедлайны на введенную дату"""

    async def delete_deadline(self, group, day, month, year, number):
        """Удаляет дедлайн"""

    async def show_next_n_deadline(self, group, n):
        """Показывает ближайшие n дедлайнов"""

    async def record_exist(self, group, day, month, year):
        """True если на эту дату есть дедлайн, иначе False"""

    async def make_user(self, id, group):
        """Добавляет пользователя в базу данных или изменяет его группу"""

    async def make_admin(self, id, group):
        """Добавляет админа в базу данных или меняет его группу"""

    def take_dictionary(self, table_name, month, year):
        """Возвращает массив словарей для таблиц users и admins"""
        self.cursor.execute(f"SELECT * FROM {table_name}")
        dictionary_array = []
        if table_name == 'users':
            for k in self.cursor:
                dictionary_array += [{'id': k[0],
                                      'group': k[1],
                                      'month': month,
                                      'year': year,
                                      'edit_type': 3}]
        if table_name == 'admins':
            for k in self.cursor:
                dictionary_array += [{'id': k[0],
                                      'group': k[1]}]
        return dictionary_array
