from datetime import datetime
from functools import reduce
import json
from playhouse.shortcuts import model_to_dict
from types import SimpleNamespace
import uuid
import flask
from kink import inject

from trade_trees.dbo.trade_tree import TradeTreeRoot
from trade_trees.services.trade_tree_branch_projector import TradeTreeBranchProjector

# Design notes:
# Layer purposed for handling business logic.
@inject
class TradeTreeService():
    def __init__(self, configuration, trade_tree_repository):
        self.configuration = configuration
        self.repository = trade_tree_repository

    def initialize_trade_tree_table(self):
        self.repository.initialize_trade_tree_table()
        
    def post_trade_tree(self, root: TradeTreeRoot):
        # TODO Validation of children:
        # 1. No branch that has no children shall have anything but schema descriminator.
        # 2. No branch that has schema descriminator shall have children.
        root.id = uuid.uuid4()
        root.created_at = datetime.utcnow()
        root.updated_at = datetime.utcnow()

        # Introduce the root into the database.
        self.repository.create_trade_tree(root)

        # Delete all the existing branches associated with the given trade tree root.
        self.repository.delete_trade_tree_branches(root.id)

        # Flatten the tree structure in order to store it in the database.
        projector = TradeTreeBranchProjector()
        folded_branches = projector.fold_branches(root.child, root.id)
        deflated_branches = projector.deflate_branches(folded_branches)
        # Introduce the branches into the database.
        self.repository.create_branches(deflated_branches)

        # TODO Introduce error handling in case if operation failed.
        return root

    def get_trade_tree(self, id):
        result = self.repository.read_trade_tree(id)

        if (len(result) < 1):
            # TODO: Replace with a proper method designed for API response 
            return flask.jsonify({"error": "Not found"}), 404

        raw = model_to_dict(result[0], backrefs=True)
        payload = flask.jsonify(raw)

        projector = TradeTreeBranchProjector()
        deflated_branches = payload.json["root"]
        inflated_branch = projector.inflate_branches(deflated_branches)
        payload.json["root"] = inflated_branch
        return {
            "id": payload.json["id"],
            "title": payload.json["title"],
            "isActive": payload.json["isActive"],
            "child": inflated_branch,
            "createdAt": payload.json["createdAt"],
            "updatedAt": payload.json["updatedAt"]
        }
    
    def put_trade_tree(self, entity: TradeTreeRoot):
        entity.updated_at = datetime.utcnow()
        self.repository.update_trade_tree(entity) > 0
        return entity

    def delete_trade_tree(self, id):
        return self.repository.delete_trade_tree(id)
    