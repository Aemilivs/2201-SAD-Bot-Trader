# bootstrap.py
from kink import di
from API.trade_trees.repositories.trade_tree_repository import TradeTreeRepository
import configparser

def bootstrap_di() -> None:
    config = configparser.ConfigParser()
    config.read('configuration.ini')
    di['configuration'] = config
    di['trade_tree_repository'] = TradeTreeRepository()