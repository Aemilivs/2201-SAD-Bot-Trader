from enum import Enum


class TradeTreeSchemaOperation(Enum):
    NUMERIC_LESS_COMPARISON = 1
    NUMERIC_LESS_OR_EQUAL_COMPARISON = 2
    NUMERIC_EQUAL_COMPARISON = 3
    NUMERIC_MORE_COMPARISON = 4
    NUMERIC_MORE_OR_EQUAL_COMPARISON = 5
    STRING_EQUAL_COMPARISON = 6
    STRING_STARTS_WITH_COMPARISON = 7
    STRING_CONTAINS_COMPARISON = 8
    STRING_ENDS_WITH_COMPARISON = 9
