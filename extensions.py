import requests
import json
from config import keys

class ConvertionException(Exception):
    #обработка исключений
    pass

class CryptoConverter:
    #обработка информации, полученной от бота
    #валютная пара и количество первой валюты в паре 
    @staticmethod
    def convert(val_1, val_2, count_val_1):
        
        if val_1 == val_2:
        #проверка валютной пары - конвертация при условии
        #валюты должны быть указаны разные
            raise ConvertionException(f'Одинаковые валюты {val_1} - {val_2}')
            
        try:
            val_1_ticker = keys[val_1]
        #проверка правильности ввода названия первой валюты список /values
        except KeyError:
            raise ConvertionException(f'Неправильное название криптовалюты - '
                                      f'{val_1}')
        try:
             val_2_ticker = keys[val_2]
        #проверка правильности ввода названия второй валюты - список /values
        except KeyError:
            raise ConvertionException(f'Неправильное название фиата - {val_2}')

        try:
            count_val_1 = float(count_val_1)
        #проверка правильности ввода количества криптовалюты - числовое значение
        except ValueError:
            raise ConvertionException(f'Неправильное колличество - {count_val_1}')
        
        #отправка запроса на сайт
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym='
                         f'{val_1_ticker}&tsyms={val_2_ticker}')

        #обработка данных, полученных с сайта
        price_val_1 = round(json.loads(r.content)[keys[val_2]]*count_val_1, 2)

        return price_val_1