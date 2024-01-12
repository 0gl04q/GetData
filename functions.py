""" Файл функций """

import pandas as pd
from db import get_data


def create_xlsx(year: int, month: int, typesc: int, region: tuple[int, str]):
    """ Функция создания Excel """

    # Получаем ID и имя региона
    region_id, region_name = region

    data_type = {
        'ХВС': 0,
        'ГВС': 1
    }

    # Получаем сведения из БД
    data = get_data(*map(int, (year, month, data_type[typesc], region_id)))

    # Создаем файл
    df = pd.DataFrame(data)
    df.to_excel(f'./Отчет {year} {region_name} {typesc}.xlsx', sheet_name='Отчет', index=False)
