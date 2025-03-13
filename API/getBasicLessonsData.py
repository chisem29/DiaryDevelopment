import pandas as pd

def getBasicLessonsData(name : str) -> pd.DataFrame :

    data = pd.read_excel(f'API/data/{name}.xlsx')

    basicColumns = data.columns.tolist()[1::8]

    data.columns =  [data.columns.tolist()[0]] + list(zip([col for col in basicColumns for _ in range(8)], data.iloc[0, 1:]))

    data.drop(0, inplace=True)

    data.set_index(data.columns.tolist()[0], inplace=True)

    return data