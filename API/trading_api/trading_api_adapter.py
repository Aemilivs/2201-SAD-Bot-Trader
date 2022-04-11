import requests
from constants import key
import configparser

config = configparser.ConfigParser()
config.read('../configuration.ini')
trading_api_url = config.get("DEFAULT", "TradingApiURL")


class Adapter:
    def __init__(self, frequency, asset, number_of_entries):
        self.frequency = frequency
        self.asset = asset
        self.number_of_entries = number_of_entries

    def validate_frequency(self):
        frequencies = {
            "daily": "TIME_SERIES_DAILY",
            "weekly": "TIME_SERIES_WEEKLY",
            "monthly": "TIME_SERIES_MONTHLY"
        }
        if self.frequency not in frequencies:
            raise Exception(
                "Wrong frequency. Use 'daily', 'monthly' or 'weekly' ")
        return frequencies.get(self.frequency)

    def validate_asset(self):
        data = self.search_asset()
        if len(data["bestMatches"]) == 0:
            raise Exception(f"Asset {self.asset} not found")

        symbol = data["bestMatches"][0].get("1. symbol")
        if symbol != self.asset:
            raise Exception(f"Asset {self.asset} not found")
        return True

    def get_data(self):
        # self.validate_asset()
        function = self.validate_frequency()
        request_url = f'{trading_api_url}?function={function}&symbol={self.asset}&apikey={key}'

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
