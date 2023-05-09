#Модуль содержит словарь с отсортированными
#по институтам и курсам группами для регистрации
from data.registration_parser import take_registration_dictionary

groups_array = []                   #Спсок групп
institutes = {}                     #Словарь институтов для регистрационной клавиатуры
institutes_callback = {}            #Словарь колбеков институтов для регистрационной клавиатуры
courses = []                        #список курсов
                                    #вышеперечисленные словари и списки сделаны для регистрационной клавиатуры
registration_dictionary = {}        #словарь регистрации, содержащий все группы, сортированные по курсам, сортированные по институтам

def data_initialization():

    """Заполняет словарь регистрации и массивы групп, курсов и институтов"""

    global registration_dictionary, institutes, institutes_callback, courses, groups_array

    registration_dictionary = take_registration_dictionary()

    for institute in registration_dictionary:
        institutes[institute[-10:]] = institute
        institutes_callback[institute] = institute[-10:]
        for course in registration_dictionary[institute]:
            if not course in courses: courses += [course]
            groups_array += registration_dictionary[institute][course]

data_initialization()

    #print(registration_dictionary, "\n\n", institutes, "\n\n", institutes_callback, "\n\n", courses, "\n\n", groups_array)
    #print(len(groups_array))