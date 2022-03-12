from kink import inject

from API.trade_trees.dto.trade_tree_dto_root import TradeTreeRootDTO

# Design notes:
# Layer purposed for handling business logic.
@inject
class TradeTreeService():
    def __init__(self, configuration, trade_tree_repository):
        self.configuration = configuration
        self.repository = trade_tree_repository

    def initialize_trade_tree_table(self):
        self.repository.initialize_trade_tree_table()
        
    def post_trade_tree(self, dto: TradeTreeRootDTO):
        return self.repository.create_trade_tree(dto) > 0

    def get_trade_tree(self, id):
        return self.repository.read_trade_tree(id)
    
    def put_trade_tree(self, dto: TradeTreeRootDTO):
        return self.repository.update_trade_tree(dto) > 0

    def delete_trade_tree(self, id):
        return self.repository.delete_trade_tree(id)
    