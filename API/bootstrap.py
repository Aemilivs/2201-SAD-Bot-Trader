# bootstrap.py
from kink import di
from peewee import SqliteDatabase
from API.trade_trees.repositories.trade_tree_repository import TradeTreeRepository
from API.trade_trees.services.trade_tree_service import TradeTreeService
# from API.common.db_schema import create_database_context
import configparser

def bootstrap_di() -> None:
    config = configparser.ConfigParser()
    config.read('configuration.ini')
    di['configuration'] = config
    di['db'] = SqliteDatabase('DatabaseName')
    di['trade_tree_repository'] = TradeTreeRepository()
    di['trade_tree_service'] = TradeTreeService()