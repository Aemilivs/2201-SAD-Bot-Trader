import requests
from constants import key
import configparser

config = configparser.ConfigParser()
config.read('../configuration.ini')
trading_api_url = config.get("DEFAULT", "TradingApiURL")


class Adapter:
    def __init__(self, frequency, asset, interval, number_of_entries):
        self.frequency = self.validate_frequency(frequency)
        self.asset = asset
        self.interval = self.validate_interval(interval)
        self.number_of_entries = number_of_entries

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

    def validate_asset(self):
        data = self.search_asset()
        if len(data["bestMatches"]) == 0:
            raise Exception(f"Asset {self.asset} not found")

        symbol = data["bestMatches"][0].get("1. symbol")
        if symbol != self.asset:
            raise Exception(f"Asset {self.asset} not found")
        return True

    def validate_interval(self, interval):
        intervals = ['1min', '5min', '15min', '30min', '60min']
        if interval not in intervals:
            raise Exception(
                f"Wrong frequency. Use {', '.join(intervals)} ")
        return interval

    def get_data(self):
        # self.validate_asset()
        request_url = f'{trading_api_url}?function={self.frequency}&symbol={self.asset}&interval={self.interval}&apikey={key}'

        try:
            request = requests.get(request_url)
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)

        data = request.json()
        del data["Meta Data"]

        # needed to get value of the first key in the dict (differs by
        # frequency)
        time_data_key = str(list(data.keys())[0])

        if self.number_of_entries > len(data.get(time_data_key)):
            raise Exception("Requested more entries than available. Available " +
                            str(len(data.get(time_data_key))) + " entries")

        # returning requested number of entries
        range_data = {}
        counter = 0
        for entry in data.get(time_data_key):
            if counter != self.number_of_entries:
                range_data[entry] = data[time_data_key][entry]
                counter += 1

        return range_data

    # search endpoint - returns best matches for the searched asset
    def search_asset(self):
        request_url = f'{trading_api_url}?function=SYMBOL_SEARCH&keywords={self.asset}&apikey={key}'

        try:
            request = requests.get(request_url)
            request.raise_for_status()
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)

        return request.json()
