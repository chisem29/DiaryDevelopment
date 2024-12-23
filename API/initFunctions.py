import pandas as pd
import numpy as np

def getBasicLessonsData() -> pd.DataFrame :

    data = pd.read_excel('API/data/data.xlsx')

    basicColumns = data.columns.tolist()[1::8]

    data.columns =  [data.columns.tolist()[0]] + list(zip([col for col in basicColumns for _ in range(8)], data.iloc[0, 1:]))

    data.drop(0, inplace=True)

    data.set_index('Класс', inplace=True)

    return data

def getLessonsDataByClassWeekday(data : pd.DataFrame, className : str, weekday : str) -> np.ndarray :

    return data.loc[className, [(weekday, n) for n in range(1, 9)]].dropna().str.split('\n').apply(pd.Series).rename(columns={0 : 'Предмет', 1 : 'Кабинет'}).values