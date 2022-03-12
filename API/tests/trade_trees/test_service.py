from kink import inject, di

from API.trade_trees.services.trade_tree_service import TradeTreeService

di['configuration'] = None
di['test_tree_repository'] = None

def test_service():
    sut = TradeTreeService()
    assert sut != None