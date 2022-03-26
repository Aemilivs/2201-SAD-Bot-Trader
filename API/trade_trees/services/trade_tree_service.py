from datetime import datetime
import json
from types import SimpleNamespace
import uuid
from kink import inject

from trade_trees.dbo.trade_tree import TradeTreeRoot

# Design notes:
# Layer purposed for handling business logic.
@inject
class TradeTreeService():
    def __init__(self, configuration, trade_tree_repository):
        self.configuration = configuration
        self.repository = trade_tree_repository

    def initialize_trade_tree_table(self):
        self.repository.initialize_trade_tree_table()
        
    def post_trade_tree(self, entity: TradeTreeRoot):
        entity.id = uuid.uuid4()
        entity.created_at = datetime.utcnow()
        entity.updated_at = datetime.utcnow()
        entity.child.id = uuid.uuid4()
        # TODO Introduce error handling in case if operation failed.
        self.repository.create_trade_tree(entity)
        return entity

    def get_trade_tree(self, id):
        return self.repository.read_trade_tree(id)
    
    def put_trade_tree(self, entity: TradeTreeRoot):
        entity.updated_at = datetime.utcnow()
        self.repository.update_trade_tree(entity) > 0
        return entity

    def delete_trade_tree(self, id):
        return self.repository.delete_trade_tree(id)
    