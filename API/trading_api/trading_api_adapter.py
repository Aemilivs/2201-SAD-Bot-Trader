from flask_restful import abort
from kink import inject
import requests
try:
    from .constants import key
except ImportError:
    import os
    key = os.environ['API_KEY']

@inject
class Adapter:
    def __init__(self, configuration):
        self.configuration = configuration
        self.url = configuration["DEFAULT"]["TradingApiURL"]
        # self.assets = self.search_asset()

    def validate_frequency(self, frequency):
        frequencies = {
            "daily": "TIME_SERIES_DAILY",
            "weekly": "TIME_SERIES_WEEKLY",
            "monthly": "TIME_SERIES_MONTHLY"
        }
        if frequency not in frequencies:
            raise Exception(
                f"Wrong frequency. Use {', '.join(frequencies.keys())} ")
        return frequencies.get(frequency)

    def validate_asset(self, asset):
        if len(self.assets["bestMatches"]) == 0:
            raise Exception(f"Asset {self.asset} not found")

        symbol = self.assets["bestMatches"][0].get("1. symbol")
        if symbol != asset:
            raise Exception(f"Asset {self.asset} not found")
        return asset

    def validate_interval(self, interval):
        intervals = ['1min', '5min', '15min', '30min', '60min']
        if interval not in intervals:
            raise Exception(
                f"Wrong frequency. Use {', '.join(intervals)} ")
        return interval

    def get_data(self, frequency, asset, interval, number_of_entries=0):
        frequency = self.validate_frequency(frequency)
        # asset = self.validate_asset(asset)
        interval = self.validate_interval(interval)
        number_of_entries = number_of_entries

        request_url = f'{self.url}?function={frequency}&symbol={asset}&interval={interval}&apikey={key}'

        try:
            request = requests.get(request_url)
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)

        data = request.json()

        if 'Note' in data:
            abort(
                400,
                message='Unfortunately, we cannot execute given trade tree right now. Please, try again later.')

        # needed to get value of the first key in the dict (differs by
        # frequency)
        time_data_key = str(list(data.keys())[1])

        if number_of_entries > 0 and number_of_entries > len(
                data.get(time_data_key)):
            raise Exception("Requested more entries than available. Available " +
                            str(len(data.get(time_data_key))) + " entries")

        # returning requested number of entries
        # range_data = {}
        # counter = 0
        # for entry in data.get(time_data_key):
        #     if counter != number_of_entries:
        #         range_data[entry] = data[time_data_key][entry]
        #         counter += 1

        return data.get(time_data_key)

    # search endpoint - returns best matches for the searched asset
    def search_asset(self, asset):
        request_url = f'{self.url}?function=SYMBOL_SEARCH&keywords={asset}&apikey={key}'

        try:
            request = requests.get(request_url)
            request.raise_for_status()
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)

        return request.json()
