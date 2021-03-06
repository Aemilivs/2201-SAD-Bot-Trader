# bootstrap.py
"""This module bootstraps the API according to the configuration"""
import configparser
from kink import di
from peewee import SqliteDatabase


def bootstrap_di() -> None:
    """This function bootstraps the API with respect to the configuration"""
    config = configparser.ConfigParser()
    config.read('API/configuration.ini')
    # pylint: disable=no-value-for-parameter
    di['configuration'] = config
    database_name = config['DEFAULT']['DatabaseName']
    di['db'] = SqliteDatabase(database_name + '.sqlite')
    # Unfortunately, this is the only way DI can be introduced into application components.
    # if from import expressions are put to the top of the file -
    # an exception messaging about missing service in the DI container is
    # thrown.
    from API.trade_trees.repositories.trade_tree_repository import TradeTreeRepository
    di['trade_tree_repository'] = TradeTreeRepository()
    from API.trading_api.trading_api_adapter import Adapter
    di['adapter'] = Adapter()
    from API.trade_trees.services.trade_tree_evaluator import TradeTreeEvaluator
    di['evaluator'] = TradeTreeEvaluator()
    from API.trade_trees.services.trade_tree_service import TradeTreeService
    di['trade_tree_service'] = TradeTreeService()
    from API.users.repositories.user_repository import UserRepository
    di['user_repository'] = UserRepository()
    from API.users.services.user_service import UserService
    di['user_service'] = UserService()
