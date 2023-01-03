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
    def get_price(base, quote, amount):
        
        if base == quote:
        #проверка валютной пары - конвертация при условии
        #валюты должны быть указаны разные
            raise ConvertionException(f'Одинаковые валюты {base} - {quote}')
            
        try:
            base_ticker = keys[base]
        #проверка правильности ввода названия первой валюты список /values
        except KeyError:
            raise ConvertionException(f'Неправильное название валюты №1 - '
                                      f'{base}')
        try:
             quote_ticker = keys[quote]
        #проверка правильности ввода названия второй валюты - список /values
        except KeyError:
            raise ConvertionException(f'Неправильное название валюты №2 - {quote}')

        try:
            amount = float(amount)
        #проверка правильности ввода количества криптовалюты - числовое значение
        except ValueError:
            raise ConvertionException(f'Неправильное количество - {amount}')
        
        #отправка запроса на сайт
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym='
                         f'{base_ticker}&tsyms={quote_ticker}')

        #обработка данных, полученных с сайта
        price_base = round(json.loads(r.content)[keys[quote]]*amount, 2)

        return price_base
