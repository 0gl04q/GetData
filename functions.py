import pandas as pd
from db import get_data


def create_xlsx(year, month, typesc, region):

    data_type = {
        'ХВС': 0,
        'ГВС': 1
    }

    df = pd.DataFrame(get_data(*map(int, (year, month, data_type[typesc], region))))
    df.to_excel(f'./Отчет {year} {region} {typesc}.xlsx', sheet_name='Budgets', index=False)
