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

    async def make_deadline(self, group, day, month, year, text):
        """Создает дедлайн"""

        self.cursor.execute(f"INSERT INTO '{group}'"
                            f"('date', 'deadline')"
                            f"VALUES ({year}-{month}-{day}, {text})")
        return self.connect.commit()

    async def show_deadline(self, group, day, month, year):
        """Показывает дедлайны на введенную дату"""

    async def delete_deadline(self, group, day, month, year, number):
        """Удаляет дедлайн"""

    async def show_next_n_deadline(self, group, n):
        """Показывает ближайшие n дедлайнов"""

    async def record_exist(self, group, day, month, year):
        """True если на эту дату есть дедлайн, иначе False"""

        self.cursor.execute(f"SELECT date "
                            f"FROM '{group}' "
                            f"WHERE date = ?",
                            (f"{year}-{month}-{day}",))
        for k in self.cursor:
            return True
        return False

    async def make_user(self, id, group):
        """Добавляет пользователя в базу данных или изменяет его группу"""

        self.cursor.execute(f"DELETE FROM 'users' WHERE id = {id}")
        self.cursor.execute("INSERT INTO users"
                            "('id', 'user_group')"
                            f"VALUES ({id}, {group})")
        return self.connect.commit()



    async def make_admin(self, id, group):
        """Добавляет админа в базу данных или меняет его группу"""

        self.cursor.execute(f"DELETE FROM 'admins' WHERE id = {id}")
        self.cursor.execute("INSERT INTO admins"
                            "('id', 'user_group')"
                            f"VALUES ({id}, {group})")
        return self.connect.commit()

    def take_dictionary(self, table_name):
        """Возвращает массив словарей для таблиц users и admins"""

        self.cursor.execute(f"SELECT * FROM {table_name}")
        dictionary_array = []
        if table_name == 'users':
            for k in self.cursor:
                dictionary_array += [{'id': k[0],
                                      'group': k[1]}]
        if table_name == 'admins':
            for k in self.cursor:
                dictionary_array += [{'id': k[0],
                                      'group': k[1]}]
        return dictionary_array