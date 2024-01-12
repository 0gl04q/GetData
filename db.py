import mysql.connector


class MySQLManagerConnect:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def __enter__(self):
        self.cnx = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database
        )
        return self.cnx

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.close()


class CursorManager:
    def __init__(self, connect):
        self.connect = connect

    def __enter__(self):
        self.cursor = self.connect.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()


class BaseConnect:
    def __init__(self, user='root', password='DerParol', host='server-new', database='poverka_db'):
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def __enter__(self):
        self.cnx = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database
        )
        self.cursor = self.cnx.cursor()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.cnx.close()


def get_data(year, month, typesc, region):
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
                AND TypeSc IN ({typesc})
                AND p.id_region IN ({region})
            ORDER BY
                DPoverki
        ''')

        connect_obj.cursor.execute(query)

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

        response = connect_obj.cursor.fetchall()

        for row in response:
            for col in range(10):
                data[list(data.keys())[col]].append(row[col])

        return data


def get_region():
    with BaseConnect() as connect_obj:
        query = (f'''
                    SELECT  
                        Region,
                        id
                    FROM Region
                    ORDER BY id
                ''')

        connect_obj.cursor.execute(query)

        return connect_obj.cursor.fetchall()