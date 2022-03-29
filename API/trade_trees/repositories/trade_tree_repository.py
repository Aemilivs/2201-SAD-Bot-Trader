from kink import inject
from API.trade_trees.dbo.trade_tree import *

# Design notes:
# Layer purposed for handling communication API and the database.
@inject()
class TradeTreeRepository:
    def __init__(self, configuration, db) -> None:
        self._configuration = configuration
        self.db = db
        self.db.connect()
        # TODO: Eventually come up with a resolution of whether we should call it or not.
        self.db.create_tables([TradeTreeOutcome, TradeTreeRoot, TradeTreeBranch])

    def create_trade_tree(self, root:TradeTreeRoot):

        # TODO Introduce some meaningful return value.
        rootResult = TradeTreeRoot.create(
            id = root.id,
            title = root.title,
            isActive = root.is_active,
            createdAt = root.created_at,
            updatedAt = root.updated_at,
            child = root.child.id
        )

        outcomes = []

        for outcome in root["outcomes"]:
            entity = TradeTreeOutcome(
                id = outcome["id"],
                operation = outcome["operation"],
                operand = outcome["operand"],
                target = outcome["target"],
                root = root.id
            )
            outcomes.append(entity)

        outcomesResult = TradeTreeOutcome.bulk_create(outcomes)

        return True

    def create_branches(self, branches):
        branchesResult = TradeTreeBranch.bulk_create(branches)

        return True

    def read_trade_tree(self, id):
        # TODO Make this query return a valid trade tree (with a children/branch hierarchy).
        return TradeTreeRoot.select().join(TradeTreeBranch, on= TradeTreeBranch.root == TradeTreeRoot.id).join(TradeTreeOutcome, on = TradeTreeBranch.root == TradeTreeOutcome.root).where(TradeTreeRoot.id == id)

    def read_trade_tree_branches(self, id):
        return TradeTreeBranch.select().where(TradeTreeBranch.root == id)

    def update_trade_tree(self, entity:TradeTreeRoot):
        return TradeTreeRoot.update(
            title = entity.title,
            isActive = entity.is_active,
            updatedAt = entity.updated_at
        ).where(TradeTreeRoot.id == entity.id).execute()

    def delete_trade_tree(self, id):
        return TradeTreeRoot.delete().where(TradeTreeRoot.id == id).execute()

    def delete_trade_tree_branches(self, id):
        return TradeTreeBranch.delete().where(TradeTreeBranch.root == id).execute()