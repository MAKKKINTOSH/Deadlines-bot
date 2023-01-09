from create_bot import DB

"""В модуле содержатся словари пользователей и администраторов, 
а также id главного администратора"""

main_admin = 545762112

admins = DB.take_dictionary('admins')
users = DB.take_dictionary('users')
