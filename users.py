from create_data_base import DB

"""В модуле содержатся словари пользователей и администраторов, 
а также user_id главного администратора"""

main_admin = 545762112

admins = DB.take_dictionary('admins')
users = DB.take_dictionary('users')
