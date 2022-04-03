# bootstrap.py
"""This module bootstraps the API according to the configuration"""
import configparser
from kink import di
from peewee import SqliteDatabase
from API.trade_trees.repositories.trade_tree_repository import TradeTreeRepository
from API.trade_trees.services.trade_tree_service import TradeTreeService


def bootstrap_di() -> None:
    """This function bootstraps the API with respect to the configuration"""
    config = configparser.ConfigParser()
    config.read('API/configuration.ini')
    # pylint: disable=no-value-for-parameter
    di['configuration'] = config
    database_name = config['DEFAULT']['DatabaseName']
    di['db'] = SqliteDatabase(database_name + '.sqlite')
    di['trade_tree_repository'] = TradeTreeRepository()
    di['trade_tree_service'] = TradeTreeService()
