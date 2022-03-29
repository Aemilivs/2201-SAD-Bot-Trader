from enum import Enum


class TradeTreeDiscriminator(Enum):
    AND = 1
    OR = 2
    NOT = 3
    SCHEMA = 4
