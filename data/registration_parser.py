from bs4 import BeautifulSoup
import requests

url = "https://www.istu.edu/schedule/"
req = requests.get(url)
bs = BeautifulSoup(req.text, "lxml")

web_institutes= bs.find_all("ul")[-1].find_all("a")

def take_registration_dictionary() -> dict:

    """Парсит сайт и возвращает словарь с упорядоченными группами,
        которые вложены в курсы, которые вложены в институты"""

    registration_dictionary = {}

    for institute in web_institutes:

        registration_dictionary[institute.text] = {}
        institute_schedule = requests.get(url + institute.get("href"))
        institute_bs = BeautifulSoup(institute_schedule.text).find(class_="kurs-list")

        course = 1

        for web_groups in institute_bs.find_all("ul"):

            registration_dictionary[institute.text][f"Курс {course}"] = []

            for gr in web_groups.find_all("a"):
                registration_dictionary[institute.text][f"Курс {course}"].append(gr.text.replace("-", "_"))

            course += 1

    return registration_dictionary