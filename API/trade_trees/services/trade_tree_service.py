from datetime import datetime
import uuid
from flask_restful import abort
from playhouse.shortcuts import model_to_dict
from uuid import UUID
import flask
from kink import inject

from API.trade_trees.dbo.trade_tree import TradeTreeRoot
from API.trade_trees.services.trade_tree_branch_projector import TradeTreeBranchProjector
from API.trade_trees.services.trade_tree_evaluator import TradeTreeEvaluator

# Design notes:
# Layer purposed for handling business logic.


@inject
class TradeTreeService():
    def __init__(self, configuration, trade_tree_repository, evaluator):
        self.configuration = configuration
        self.repository = trade_tree_repository
        self.projector = TradeTreeBranchProjector()
        self.evaluator = evaluator

    def initialize_trade_tree_table(self):
        self.repository.initialize_trade_tree_table()

    def post_trade_tree(self, root: TradeTreeRoot):
        # TODO Validation of children:
        # 1. No branch that has no children shall have anything but schema descriminator.
        # 2. No branch that has schema descriminator shall have children.
        root.id = uuid.uuid4()
        root.created_at = datetime.utcnow()
        root.updated_at = datetime.utcnow()

        for outcome in root["outcomes"]:
            outcome["id"] = uuid.uuid4()

        # Introduce the root into the database.
        self.repository.create_trade_tree(root)

        # Delete all the existing branches associated with the given trade tree
        # root.
        self.repository.delete_trade_tree_branches(root.id)

        # Flatten the tree structure in order to store it in the database.
        folded_branches = self.projector.fold_branches(root.child, root.id)
        deflated_branches = self.projector.deflate_branches(folded_branches)
        # Introduce the branches into the database.
        self.repository.create_branches(deflated_branches)

        # TODO Introduce error handling in case if operation failed.
        return root

    def get_trade_tree(self, id, user_id):
        self.verify_access(id, user_id)
        result = self.repository.read_trade_tree(id)

        if (len(result) < 1):
            # TODO: Replace with a proper method designed for API response
            return flask.jsonify({"error": "Not found"}), 404

        raw = model_to_dict(result[0], backrefs=True)
        payload = flask.jsonify(raw)

        deflated_branches = payload.json["root"]
        inflated_branch = self.projector.inflate_branches(deflated_branches)
        payload.json["root"] = inflated_branch
        return {
            "id": payload.json["id"],
            "title": payload.json["title"],
            "isActive": payload.json["isActive"],
            "child": inflated_branch,
            "createdAt": payload.json["createdAt"],
            "updatedAt": payload.json["updatedAt"],
            "outcomes": payload.json["tradetreeoutcome_set"]
        }

    def get_user_trade_trees(self, user_id: UUID):
        query = self.repository.read_user_trade_tree_roots(user_id)
        results = [model_to_dict(results) for results in query]
        roots = list(
            map(lambda it: {'id': it['id'], 'title': it['title']}, results))

        if len(roots) == 0:
            abort(404, message="User does not own any trade tree.")
            
        return {'roots': roots}

    def put_trade_tree(self, root: TradeTreeRoot):
        self.verify_access(root.id, root.user_id)

        # Flatten the tree structure in order to store it in the database.
        folded_branches = self.projector.fold_branches(root.child, root.id)
        deflated_branches = self.projector.deflate_branches(folded_branches)

        # Delete all the existing branches associated with the given trade tree
        # root.
        self.repository.delete_trade_tree_branches(root.id)

        # Introduce the branches into the database.
        root.updated_at = datetime.utcnow()

        self.repository.update_trade_tree(root)
        self.repository.create_branches(deflated_branches)

        return root

    def verify_access(self, id, user_id):
        results = self.repository.read_user_trade_tree_roots(user_id)
        trees = list(map(lambda it: str(it.id), results))

        if len(trees) == 0:
            abort(404, message="User does not own requested resource(s).")

        if str(id) not in trees:
            abort(401, message="User is not authorized to change this resource.")

    def delete_trade_tree(self, id, user_id):
        self.verify_access(id, user_id)
        self.repository.delete_trade_tree(id, user_id)
        self.repository.delete_trade_tree_branches(id)
        return True

    def evaluate_trade_tree(self, id, user_id):
        tree = self.get_trade_tree(id, user_id)
        return self.evaluator.evaluate_tree(tree)
