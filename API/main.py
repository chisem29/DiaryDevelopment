import pandas as pd

def getBasicLessonsData() :

    data = pd.read_excel('data/data.xlsx')

    basicColumns = data.columns.tolist()[1::8]

    data.columns =  [data.columns.tolist()[0]] + list(zip([col for col in basicColumns for _ in range(8)], data.iloc[0, 1:]))

    data.drop(0, inplace=True)

    data.set_index('Класс', inplace=True)

    return data

def getLessonsDataByClassWeekday(data : pd.DataFrame, className : str, weekday : str) :

    return data.loc[className, [(weekday, n) for n in range(1, 9)]].dropna().to_dict()
