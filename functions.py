""" Файл функций """

import pandas as pd
from db import get_data


def create_xlsx(year: int, month: int, typesc: int | None, region: tuple[int, str]):
    """ Функция создания Excel """

    # Получаем ID и имя региона
    region_name, region_id = region

    data_type = {
        'ХВС': 0,
        'ГВС': 1
    }

    # Получаем сведения из БД в зависимости от типа
    data = get_data(*map(int, (year, month, region_id)), typesc=data_type[typesc] if typesc else None)

    # Создаем файл
    df = pd.DataFrame(data)
    df.to_excel(f'./Отчет {year} {region_name} {typesc if typesc else "ХГ"}.xlsx', sheet_name='Отчет', index=False)
