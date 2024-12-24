import pandas as pd
import numpy as np

def getLessonsDataByClassWeekday(data : pd.DataFrame, className : str, weekday : str) -> np.ndarray : ### Получение данных ... после получения DATA

    return data.loc[className, [(weekday, n) for n in range(1, 9)]].dropna().str.split('\n').apply(pd.Series).rename(columns={0 : 'Предмет', 1 : 'Кабинет'}).values 