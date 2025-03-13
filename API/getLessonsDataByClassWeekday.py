import pandas as pd

def getLessonsDataByClassWeekday(data : pd.DataFrame, className : str, weekday : str) : ### Получение данных ... после получения DATA
    return data.loc[className, [f"{(weekday, n)}" for n in range(1, 9)]].dropna().str.replace('\n', ',').values