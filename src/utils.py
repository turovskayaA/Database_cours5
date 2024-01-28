import requests
import psycopg2


def get_employer(employers_id):
    """
    Запрос на компании с HH.ru
    :param employers_id: id компаний
    """
    response = requests.get(f"https://api.hh.ru/employers/{employers_id}").json()
    hh_company = {
        "employers_id": response["id"],
        "name_company": response["name"],
        "open_vacancies": response["open_vacancies"],
    }
    return hh_company


def get_vacancy(employers_id):
    """
    Запрос на вакансии определенной компании
    :param employers_id: id компаний
    """
    response = requests.get(
        f"https://api.hh.ru/vacancies?employer_id={employers_id}"
    ).json()
    all_request = []
    for i in response["items"]:
        hh_vacancy = {
            "employers_id": int(employers_id),
            "name_company": i["employer"]["name"],
            "name_vacancy": i["name"],
            "salary": i["salary"]["from"] if i["salary"] else None,
            "url": i["alternate_url"],
            "requirement": i["snippet"]["requirement"],
        }
        if hh_vacancy["salary"] is not None:
            all_request.append(hh_vacancy)
    return all_request


def create_table():
    """
    Создание таблиц в БД
    """
    try:
        with psycopg2.connect(
            host="localhost", database="course_work", user="postgres", password="12345"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """CREATE TABLE employers 
                (employers_id int PRIMARY KEY,
                name_company varchar(100) NOT NULL,
                open_vacancies int)"""
                )
                cur.execute(
                    """CREATE TABLE vacancy
                (employers_id int REFERENCES employers(employers_id),
                name_company varchar(100) NOT NULL,
                name_vacancy varchar(100) NOT NULL,
                salary int,
                url text,
                requirement text)"""
                )
    finally:
        conn.close()


def add_info_table(employers_list):
    """
    Внесение данных в таблицы
    :param employers_list: список компаний
    """
    try:
        with psycopg2.connect(
            host="localhost", database="course_work", user="postgres", password="12345"
        ) as conn:
            with conn.cursor() as cur:
                for employer in employers_list:
                    employer_list = get_employer(employer)
                    cur.execute(
                        f"INSERT INTO employers VALUES (%s, %s, %s)",
                        (
                            employer_list["employers_id"],
                            employer_list["name_company"],
                            employer_list["open_vacancies"],
                        ),
                    )
                for employer in employers_list:
                    vacancy_list = get_vacancy(employer)
                    for vacancy in vacancy_list:
                        cur.execute(
                            f"INSERT INTO vacancy VALUES (%s, %s, %s, %s, %s, %s)",
                            (
                                vacancy["employers_id"],
                                vacancy["name_company"],
                                vacancy["name_vacancy"],
                                vacancy["salary"],
                                vacancy["url"],
                                vacancy["requirement"],
                            ),
                        )
    finally:
        conn.close()
