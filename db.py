""" Файл работы с базой данных """

import mysql.connector


class BaseConnect:
    """Контекстный менеджер подключения к MySQL и создания курсора"""

    def __init__(self, user='root', password='DerParol', host='server-new', database='poverka_db'):
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def __enter__(self):
        # Подключаем базу
        self.cnx = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database
        )
        # Инициализируем курсор
        self.cursor = self.cnx.cursor()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Закрываем менеджер
        self.cursor.close()
        self.cnx.close()


def get_data(year, month, region, typesc):
    """Функция получения информации о поверках"""

    add_type = f'''AND TypeSc = {typesc}''' if typesc else ''

    with BaseConnect() as connect_obj:
        query = (f'''
            SELECT  
                DATE_FORMAT(p.DPoverki, "%d.%m.%Y") as "Дата поверки",
                p.FIO as "ФИО",   
                p.Adress as "Адресс",
                p.Tel as "Телефон",    
                s.Mesto as "Место установки",
                s.MSchet as "Тип, марка СИ", 
                s.TypeSc as "Вид счетчика",
                s.GodVip as "Год выпуска",    
                s.DSPovN as "Дата сл. поверки",
                s.NSvid as "Свидетельство"
            FROM poverka as p
            JOIN Svidetelstva as s ON p.Id = s.id_Poverki
            WHERE
                YEAR(p.DPoverki) IN ({year})
                AND MONTH(p.DPoverki) IN ({month})
                {add_type}
                AND p.id_region IN ({region})
            ORDER BY
                DPoverki
        ''')

        connect_obj.cursor.execute(query)

        # Создаем столбцы и строки таблицы
        data = {
            "Дата поверки": [],
            "ФИО": [],
            "Адресс": [],
            "Телефон": [],
            "Место установки": [],
            "Тип, марка СИ": [],
            "Вид счетчика": [],
            "Год выпуска": [],
            "Дата сл. поверки": [],
            "Свидетельство": []
        }

        # Получаем информацию по запросу
        response = connect_obj.cursor.fetchall()

        # Наполняем словарь
        for row in response:
            for col in range(10):
                data[list(data.keys())[col]].append(row[col])

        # Возвращаем готовые данные
        return data


def get_region():
    """Функция получения информации о регионах"""

    with BaseConnect() as connect_obj:
        query = (f'''
                    SELECT  
                        Region,
                        id
                    FROM Region
                    ORDER BY id
                ''')

        connect_obj.cursor.execute(query)

        # Возвращаем регионы (Region, id)
        return connect_obj.cursor.fetchall()
