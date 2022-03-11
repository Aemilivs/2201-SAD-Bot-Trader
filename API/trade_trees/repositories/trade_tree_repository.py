import datetime
from kink import inject
from API.trade_trees.dbo.trade_tree_root import TradeTreeRoot
from API.trade_trees.dto.trade_tree_dto_root import TradeTreeRootDTO

@inject()
class TradeTreeRepository:
    def __init__(self, configuration, db) -> None:
        self._configuration = configuration
        self.db = db
        self.db.connect()

    def get_trade_trees(self):
        return TradeTreeRoot.select()
    
    def get_trade_tree(self, id):
        return TradeTreeRoot.select().where(TradeTreeRoot.id == id)

    def post_trade_tree(self, dto:TradeTreeRootDTO):
        TradeTreeRoot.create(
            createdAt = datetime.datetime.now(),
            updatedAt = datetime.datetime.now()
        ).save()

    def initialize_database(self):
        self.db.create_tables([TradeTreeRoot])