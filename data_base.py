import pymysql
from users import users
from institutes_and_groups import groups_array
from datetime import datetime
from create_bot import bot
from time import time

async def days_substraction(day, subtrahend, month, year):
    """Функция возвращает значение day из которого вычли sybstahend
    Учитывается то, что day это не число а день"""

    day = int(day)

    if day - subtrahend<=0:
        month -= 1
        if month in [1, 3, 5, 6, 8, 10, 12]:
            return 31+day - subtrahend
        elif month == 2 and year % 400 == 0:
            return 29+day - subtrahend
        elif month == 2 and year % 100 == 0:
            return 28 + day - subtrahend
        elif month == 2 and year % 4 == 0:
            return 29+day - subtrahend
        elif month == 2:
            return 28+day - subtrahend
        else:
            return 30+day - subtrahend
    else:
        return day-subtrahend


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

        self.cursor.execute(f"INSERT INTO `{group}`"
                            f"(`date`, `deadline`)"
                            f"VALUES (%s, %s)", (f'{year}-{month}-{day}', text))
        return self.connect.commit()

    async def show_deadline(self, group: str, day, month, year):
        """Показывает дедлайны на введенную дату"""

        self.cursor.execute(f"SELECT deadline FROM `{group}`"
                            f"WHERE date = %s",
                            (f"{year}-{month}-{day}",))  # {year}-{month}-{day}
        deadlines = f"Группа: {group.replace('_', '-')}\nДедлайны на {day}.{month}.{year}:\n\n"
        n = 1
        for k in self.cursor:
            deadlines += f"{n}. {str(k)[2:-3]}\n"
            n += 1
        if deadlines == f"Группа: {group.replace('_', '-')}\nДедлайны на {day}.{month}.{year}:\n\n":
            deadlines += "Тут пусто"
            return deadlines
        return deadlines
    async def delete_deadline(self, group: str, day, month, year, number):
        """Удаляет дедлайн"""

        date = f"{year}-{month}-{day}"
        self.cursor.execute(f"SELECT deadline "
                            f"FROM `{group}`"
                            f"WHERE date = %s",
                            (date,))

        deadline = self.cursor.fetchall()[number - 1]

        self.cursor.execute(f"DELETE FROM `{group}`"
                            f"WHERE deadline = %s "
                            f"AND date = %s ", (str(deadline)[2:-3], date))
        return self.connect.commit()
    async def show_next_n_deadline(self, group, n):
        """Показывает ближайшие n дедлайнов"""

        self.cursor.execute(f"SELECT `date`, `deadline` "
                            f"FROM `{group}`"
                            f"ORDER BY date")

        deadlines = f"Группа: {group.replace('_', '-')}\nБлижайшие {n} дедлайнов:\n\n"
        n = 1

        for k in self.cursor:
            date = str(k[0])
            deadlines += f"{n}. {date[8:]}.{date[5:7]}.{date[:4]}\n" \
                         f"{k[1]}\n\n"
            n += 1
            if n == 6:
                break

        if n==1:
            deadlines += "Тут пусто"
            return deadlines

        return deadlines

    async def deadlines_notification(self, *days_before_deadline):
        """Уведомление пользователя о приближающихся дедлайнах"""

        year = datetime.now().year
        month = datetime.now().month

        for n in days_before_deadline:

            day = await days_substraction(datetime.now().day, n, month, year)
            if day>datetime.now().day:
                month-=1

            for group in groups_array:
                self.cursor.execute(f"SELECTE deadline "
                                    f"FROM `{group}` "
                                    f"WHERE date = %s",
                                    (f"{year}-{month}-{day}"), )

                deadlines = f"Группа: {group.replace('_', '-')}\n" \
                            f"Пора бы уже что-то делать, ведь уже скоро тебя ждут следующие дедлайны:\n\n"

                n = 1

                for k in self.cursor:
                    date = str(k[0])
                    deadlines += f"{n}. {date[8:]}.{date[5:7]}.{date[:4]}\n" \
                                 f"{k[1]}\n\n"
                    n += 1

                if n != 1:
                    for k in users:
                        if k['group'] == group:
                            bot.send_message(k['id'], deadlines)



    async def record_exist(self, group, day, month, year):
        """True если на эту дату есть дедлайн, иначе False"""

        self.cursor.execute(f"SELECT date "
                            f"FROM `{group}` "
                            f"WHERE date = %s",
                            (f"{year}-{month}-{day}",))
        for k in self.cursor:
            return True
        return False

    async def make_user(self, id, group):
        """Добавляет пользователя в базу данных или изменяет его группу"""

        self.cursor.execute(f"DELETE FROM `users` WHERE id = {id}")
        self.cursor.execute("INSERT INTO users"
                            "(`id`, `user_group`)"
                            f"VALUES (%s, %s)", (id, group))
        return self.connect.commit()

    async def make_admin(self, id, group):
        """Добавляет админа в базу данных или меняет его группу"""

        self.cursor.execute(f"DELETE FROM `admins` WHERE `id` = {id}")
        self.cursor.execute(f"INSERT INTO `admins` (id, user_group) VALUES (%s, %s)", (id, group))
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