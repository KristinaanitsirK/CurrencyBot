import requests
import json
from config import keys, headers

class APIException(Exception):
    pass

class Converter:
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Impossible to convert same currencies {base}')

        try:
            quote_ticker = keys[quote]
        except:
            KeyError
            raise APIException(f'Failed to process currency {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Failed to process currency {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Failed to process amount {amount}')

        r = requests.get(
            f'https://api.apilayer.com/exchangerates_data/convert?to={quote_ticker}&from={keys[base]}&amount={amount}',
            headers=headers)
        res = json.loads(r.content)['result']

        return res