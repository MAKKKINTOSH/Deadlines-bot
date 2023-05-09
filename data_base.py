import pymysql
from datetime import datetime
from data.date_variables import days_array

async def days_substraction(day, added, month, year):
    """Функция возвращает значение day из которого вычли substrahend
    Учитывается то, что day это не натуральное число а день"""

    day = int(day)

    if month in [1, 3, 5, 6, 8, 10, 12]:
        if day + added > 31:
            return day + added - 31
        return day + added
    elif month == 2 and year % 400 == 0:
        if day + added > 29:
            return day + added - 29
        return day + added
    elif month == 2 and year % 100 == 0:
        if day + added > 28:
            return day + added - 28
        return day + added
    elif month == 2 and year % 4 == 0:
        if day + added > 29:
            return day + added - 29
        return day + added
    elif month == 2:
        if day + added > 28:
            return day + added - 28
        return day + added
    if day + added > 30:
        return day + added - 30
    return day + added


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

        current_date = int(str(datetime.now().date()).replace("-", ""))

        for k in self.cursor:
            date = str(k[0])
            if int(date.replace("-", ""))<current_date:
                continue
            deadlines += f"{n}. {date[8:]}.{date[5:7]}.{date[:4]}\n" \
                         f"{k[1]}\n\n"
            n += 1
            if n == 6:
                break

        if n==1:
            deadlines += "Тут пусто"
            return deadlines

        return deadlines

    async def deadlines_notification(self, group, days_before_deadline):
        """Уведомление пользователя о приближающихся дедлайнах"""

        year = datetime.now().year
        month = datetime.now().month

        day = await days_substraction(datetime.now().day, days_before_deadline, month, year)
        if day<datetime.now().day:
            month+=1
        day = days_array[day-1]

        self.cursor.execute(f"SELECT `date`, `deadline` "
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

        if n == 1: return False

        return deadlines



    async def record_exist(self, group, day, month, year):
        """True если на эту дату есть дедлайн, иначе False"""

        self.cursor.execute(f"SELECT date "
                            f"FROM `{group}` "
                            f"WHERE date = %s",
                            (f"{year}-{month}-{day}",))
        for k in self.cursor:
            return True
        return False

    async def make_user(self, user_id, group):
        """Добавляет пользователя в базу данных или изменяет его группу"""

        self.cursor.execute(f"DELETE FROM `users` WHERE user_id = {user_id}")
        self.cursor.execute("INSERT INTO users"
                            "(`user_id`, `user_group`)"
                            f"VALUES (%s, %s)", (user_id, group))
        return self.connect.commit()

    async def make_admin(self, user_id, group):
        """Добавляет админа в базу данных или меняет его группу"""

        self.cursor.execute(f"DELETE FROM `admins` WHERE `user_id` = {user_id}")
        self.cursor.execute(f"INSERT INTO `admins` (user_id, user_group) VALUES (%s, %s)", (user_id, group))
        return self.connect.commit()

    def take_dictionary(self, table_name):
        """Возвращает массив словарей для таблиц users и admins"""

        self.cursor.execute(f"SELECT * FROM {table_name}")
        dictionary_array = []
        if table_name == 'users':
            for k in self.cursor:
                dictionary_array += [{'user_id': int(k[1]),
                                      'group': k[2]}]
        if table_name == 'admins':
            for k in self.cursor:
                dictionary_array += [{'user_id': int(k[1]),
                                      'group': k[2]}]
        return dictionary_array