import requests
import json
from config import keys

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
       if quote == base:
           raise APIException(f'Невозможно перевести одинаковую валюту {base}.')

       try:
           quote_ticker = keys[quote]
       except KeyError:
           raise APIException(f'Не удалось обработать валюту {quote}')

       try:
           base_ticker = keys[base]
       except KeyError:
           raise APIException(f'Невозможно перевести валюту {base}')

       try:
           amount = float(amount)
       except KeyError:
           raise APIException(f'Не удалось обработать колличество {amount}')

       r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
       total_base = json.loads(r.content)[keys[base]]
       return total_base * amount






