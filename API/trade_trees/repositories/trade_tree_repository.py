from datetime import datetime, timezone
from kink import inject
from API.trade_trees.dbo.trade_tree_root import TradeTreeRoot
from API.trade_trees.dto.trade_tree_dto_root import TradeTreeRootDTO

# Design notes:
# Layer purposed for handling communication API and the database.
@inject()
class TradeTreeRepository:
    def __init__(self, configuration, db) -> None:
        self._configuration = configuration
        self.db = db
        self.db.connect()
    
    def initialize_trade_tree_table(self):
        self.db.create_tables([TradeTreeRoot])

    def create_trade_tree(self, dto:TradeTreeRootDTO):
        return TradeTreeRoot.create(
            createdAt = datetime.utcnow(),
            updatedAt = datetime.utcnow()
        ).save()

    def read_trade_tree(self, id):
        return TradeTreeRoot.select().where(TradeTreeRoot.id == id)

    def update_trade_tree(self, dto:TradeTreeRootDTO):
        return TradeTreeRoot.update(
            updatedAt = datetime.utcnow()
        ).where(TradeTreeRoot.id == dto.id).execute()

    def delete_trade_tree(self, id):
        return TradeTreeRoot.delete().where(TradeTreeRoot.id == id).execute()