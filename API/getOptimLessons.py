
import pandas as pd

def getOptimLessonsData(name : str) -> pd.DataFrame:
    return pd.read_excel(f'./API/data/{name}.xlsx')