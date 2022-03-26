from datetime import datetime, timezone
from kink import inject
from trade_trees.dbo.trade_tree import *

# Design notes:
# Layer purposed for handling communication API and the database.
@inject()
class TradeTreeRepository:
    def __init__(self, configuration, db) -> None:
        self._configuration = configuration
        self.db = db
        self.db.connect()
        # TODO: Eventually come up with a resolution of whether we should call it or not.
        self.db.create_tables([TradeTreeSchemaDiscriminator, TradeTreeOutcome, TradeTreeRoot, TradeTreeBranch])
    
    def create_trade_tree(self, entity:TradeTreeRoot):
        # TODO Introduce some meaningful return value.
        rootResult = TradeTreeRoot.create(
            id = entity.id,
            title = entity.title,
            isActive = entity.is_active,
            createdAt = entity.created_at,
            updatedAt = entity.updated_at
        )

        childResult = TradeTreeBranch.create(
            id = entity.child.id,
            root = entity.id,
            discriminator = entity.child.discriminator
        )

        return 1

    def read_trade_tree(self, id):
        # TODO Make this query return a valid trade tree (with a children/branch hierarchy).
        return TradeTreeRoot.select().join(TradeTreeBranch).where(TradeTreeBranch.root == id)

    def update_trade_tree(self, entity:TradeTreeRoot):
        return TradeTreeRoot.update(
            title = entity.title,
            isActive = entity.is_active,
            updatedAt = entity.updated_at
        ).where(TradeTreeRoot.id == entity.id).execute()

    def delete_trade_tree(self, id):
        return TradeTreeRoot.delete().where(TradeTreeRoot.id == id).execute()