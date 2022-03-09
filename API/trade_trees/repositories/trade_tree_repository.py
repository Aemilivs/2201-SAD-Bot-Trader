from kink import inject
from API.trade_trees.dbo.trade_tree import TradeTree

@inject()
class TradeTreeRepository:
    def __init__(self, configuration) -> None:
        self._configuration = configuration
    
    def get_trade_tree(self, id):
        return TradeTree()