import requests
# add key to the class?
from constants import key


class Adapter:
    def __init__(self, frequency, asset, number_of_entries):
        self.frequency = frequency
        self.asset = asset
        self.number_of_entries = number_of_entries

    def get_data(self):
        frequencies = {
            "daily": "TIME_SERIES_DAILY",
            "weekly": "TIME_SERIES_WEEKLY",
            "monthly": "TIME_SERIES_MONTHLY"
        }

        if self.frequency not in frequencies:
            raise Exception("Wrong frequency. Use 'daily', 'monthly' or 'weekly' ")

        if not self.search_asset():
            raise Exception(f"Asset {self.asset} not found")

        function = frequencies.get(self.frequency)
        request_url = f'https://www.alphavantage.co/query?function={function}&symbol={self.asset}&apikey={key}'

        try:
            request = requests.get(request_url)
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)

        raw_data = request.json()
        data = raw_data
        del data["Meta Data"]

        # needed to get value of the first key in the dict (differs by frequency)
        time_data_key = str(list(data.keys())[0])

        if self.number_of_entries > len(data.get(time_data_key)):
            raise Exception(
                "Requested more entries than available. Available " + str(len(data.get(time_data_key))) + " entries")

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
        request_url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={self.asset}&apikey={key}'

        try:
            request = requests.get(request_url)
            request.raise_for_status()
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)

        data = request.json()
        if len(data["bestMatches"]) == 0:
            return False
        symbol = data["bestMatches"][0].get("1. symbol")

        if symbol == self.asset:
            return True
        else:
            return False
