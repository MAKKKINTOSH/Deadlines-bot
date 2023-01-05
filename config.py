from datetime import datetime
from create_bot import DB

"""В модуле содержатся переменные для работы бота, токен содержится в файле TOKEN.py"""

current_year = datetime.now().year
current_month = datetime.now().month
current_day = datetime.now().day

days_array = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
              '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
              '25', '26', '27', '28', '29', '30', '31']
callback_for_days = ['d01', 'd02', 'd03', 'd04', 'd05', 'd06', 'd07', 'd08', 'd09',
                     'd10', 'd11', 'd12', 'd13', 'd14', 'd15', 'd16', 'd17', 'd18',
                     'd19', 'd20', 'd21', 'd22', 'd23', 'd24', 'd25', 'd26', 'd27',
                     'd28', 'd29', 'd30', 'd31']
month_array = ['01', '02', '03', '04', '05', '06',
               '07', '08', '09', '10', '11', '12']
ru_month_array = ['Январь', 'Февраль', 'Март', 'Апрель',
                  'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
                  'Октябрь', 'Ноябрь', 'Декабрь']

groups_array = ["АСУб-22-1", "ЭВМб-22-2"]
callback_for_groups = ["asub-22-1", "evmb-22-2"]

main_admin = 545762112

admins = DB.take_dictionary('admins', current_month, current_year)
users = DB.take_dictionary('users', current_month, current_year)
