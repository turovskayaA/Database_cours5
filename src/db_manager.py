import psycopg2


class DBManager:

    def __init__(self, params):
        self.params = params

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """SELECT name_company, open_vacancies
                    FROM employers"""
                    )
                    result = cur.fetchall()
                conn.commit()
        finally:
            conn.close()
        return result

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """SELECT name_vacancy, name_company, salary, url
                    FROM vacancy"""
                    )
                    result = cur.fetchall()
                conn.commit()
        finally:
            conn.close()
        return result

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """SELECT AVG(salary) AS avg_salary
                    FROM vacancy"""
                    )
                    result = cur.fetchall()
                conn.commit()
        finally:
            conn.close()
        return result

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """SELECT * FROM vacancy
                    WHERE salary > (SELECT AVG(salary) FROM vacancy)"""
                    )
                    result = cur.fetchall()
                conn.commit()
        finally:
            conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых
        содержатся переданные в метод слова.
        """
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        f"""SELECT name_vacancy, name_company
                    FROM vacancy 
                    WHERE name_vacancy LIKE '%{keyword}%'"""
                    )
                    result = cur.fetchall()
                conn.commit()
        finally:
            conn.close()
        return result
