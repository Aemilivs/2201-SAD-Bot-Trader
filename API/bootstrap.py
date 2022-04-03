# bootstrap.py
from kink import di
from peewee import SqliteDatabase
import configparser


def bootstrap_di() -> None:
    config = configparser.ConfigParser()
    config.read('API/configuration.ini')
    di['configuration'] = config
    databaseName = config['DEFAULT']['DatabaseName']
    di['db'] = SqliteDatabase(databaseName + '.sqlite')
    from API.trade_trees.repositories.trade_tree_repository import TradeTreeRepository
    from API.trade_trees.services.trade_tree_service import TradeTreeService
    di['trade_tree_repository'] = TradeTreeRepository()
    di['trade_tree_service'] = TradeTreeService()
