from kink import inject

from API.trade_trees.dto.trade_tree_dto_root import TradeTreeRootDTO

# Design notes:
# Layer purposed for handling business logic.
@inject
class TradeTreeService():
    def __init__(self, configuration, trade_tree_repository):
        self.configuration = configuration
        self.repository = trade_tree_repository

    def post_trade_tree(self, dto: TradeTreeRootDTO):
        return self.repository.create_trade_tree(dto) > 0

    def get_trade_tree(self, id):
        dbo = self.repository.read_trade_tree(id)
        # TODO: Introduce a mapping into DTO in order to decouple database definition from a user contract.
        # dto = TradeTreeRootDTO(dbo.id, dbo.createdAt, dbo.updatedAt)
        return dbo
    
    def put_trade_tree(self, dto: TradeTreeRootDTO):
        return self.repository.update_trade_tree(dto) > 0

    def delete_trade_tree(self, id):
        self.repository.delete_trade_tree(id)
        return True
    