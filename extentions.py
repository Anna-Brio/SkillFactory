import requests
import json
from telebot_config import keys


class ConversionException(Exception):
    pass


class CryptoConvertor(Exception):
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        try:
            quote_ticker = keys[quote]

        except KeyError:
            raise ConversionException(f"Failed to convert currency {quote}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f"Failed to convert into currency {base}")

        if quote == base:
            raise ConversionException(f"<From> currency and <To> currency should differ.")

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f"Failed to convert amount {amount}")

        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={quote_ticker}&symbols={base_ticker}')

        result = round(float(amount) * float(json.loads(r.content)['rates'][keys[base]]), 2)

        return result
