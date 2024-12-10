import pandas as pd

def getBasicLessonsData() :

    data = pd.read_excel('./API\data\ШК2_расписание_дети с 25.11.2024.xlsx')

    basicColumns = data.columns.tolist()[1::8]

    data.columns =  [data.columns.tolist()[0]] + list(zip([col for col in basicColumns for _ in range(8)], data.iloc[0, 1:]))

    data.drop(0, inplace=True)

    data.head()

    return data