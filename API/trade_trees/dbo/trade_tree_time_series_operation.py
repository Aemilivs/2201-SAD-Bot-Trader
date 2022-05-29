from enum import Enum


class TradeTreeTimeSeriesOperation(Enum):
    TIME_SERIES_MIN_LESS_COMPARISON = 1
    TIME_SERIES_MIN_LESS_OR_EQUAL_COMPARISON = 2
    TIME_SERIES_MIN_EQUAL_COMPARISON = 3
    TIME_SERIES_MIN_MORE_COMPARISON = 4
    TIME_SERIES_MIN_MORE_OR_EQUAL_COMPARISON = 5
    TIME_SERIES_AVERAGE_LESS_COMPARISON = 6
    TIME_SERIES_AVERAGE_LESS_OR_EQUAL_COMPARISON = 7
    TIME_SERIES_AVERAGE_EQUAL_COMPARISON = 8
    TIME_SERIES_AVERAGE_MORE_COMPARISON = 9
    TIME_SERIES_AVERAGE_MORE_OR_EQUAL_COMPARISON = 10
    TIME_SERIES_MEAN_LESS_COMPARISON = 11
    TIME_SERIES_MEAN_LESS_OR_EQUAL_COMPARISON = 12
    TIME_SERIES_MEAN_EQUAL_COMPARISON = 13
    TIME_SERIES_MEAN_MORE_COMPARISON = 14
    TIME_SERIES_MEAN_MORE_OR_EQUAL_COMPARISON = 15
    TIME_SERIES_MAX_LESS_COMPARISON = 16
    TIME_SERIES_MAX_LESS_OR_EQUAL_COMPARISON = 17
    TIME_SERIES_MAX_EQUAL_COMPARISON = 18
    TIME_SERIES_MAX_MORE_COMPARISON = 19
    TIME_SERIES_MAX_MORE_OR_EQUAL_COMPARISON = 20