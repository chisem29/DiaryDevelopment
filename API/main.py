import pandas as pd

def getBasicLessonsData() :

    data = pd.read_excel('API\data\ШК2_расписание_дети с 25.11.2024.xlsx')

    basicColumns = data.columns.tolist()[1::8]

    data.columns =  [data.columns.tolist()[0]] + [col for _ in range(8) for col in basicColumns]
