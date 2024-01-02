import pandas as pd
import json
import requests
from pandas import json_normalize

# Открываем имеющийся json, перевариваем в DataFrame
with open(r'C:\Users\1\Desktop\данные по компьютеру\GreaterBrisbaneGrid6km.txt', 'r') as file:
    json_data = file.read() 

data = json.loads(json_data)
features = data['features']
df = json_normalize(features)

# Функция для получения DataFrame только из retail-объектов
def get_retail_object(
    data: pd.DataFrame, # Входной df
    url: str = "https://api.foursquare.com/v3/places/search", #URL для поиска мест
    client_secret: str = '5XQMZXHUFWYGCTZ2KHKUZ0T3QDQEYP2WT0JTSWVPNJNRFI1G', # Передаю данные проекта ForeSquare
    client_id: str = 'T2DI4EOJ1KTKEMCELIEJXF0J3PURV3SSDDFIFZ0DSM2IU2BP',
    need_category: list = [17069, 17114, 17115, 17104, 16040, 16041]) -> pd.DataFrame: # По умолчанию ищем эти категории,  
                                                                                       # но можем и дополнить список 
    def is_retail_object(row: pd.Series) -> bool: # Функция: получает Series, возвращает факт/не факт принадлежности типу retail
        params = { # Передаю параметры объекта (долгота + широта) и проекта + версию чтения
            "client_id": client_id,
            "client_secret": client_secret,
            "v": "20220101",  
            "ll": row['geometry.coordinates']
        }
        
        response = requests.get(url, params=params) # Делаем запрос на поиск имеющегося объекта в ForeSquare  
        data = response.json() # Перевариваем полученный объект-выписку (или его отсутствие) в json
        venue = data.get("response", {}).get("venues", [])[0] # Углебляемся в json'е до словаря с параметрами найденого объекта 
        categories = venue.get("categories", []) # Извлекаем категории, к которым принадлежит объект
        
        return any(i in categories for i in need_category) #Если категория из перечня есть среди categories, то наш пациент
        
    return data[data.apply(is_retail_object,axis=1)] # Возвращем входной df с логической индексацией 

new_data = get_retail_object(data=df)
