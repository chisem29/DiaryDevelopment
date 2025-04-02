import pandas as pd

def getFreeClassesData(data : pd.DataFrame, weekday, num) :
    return data[data[f"{(weekday, int(num))}"].isna()].index.tolist()