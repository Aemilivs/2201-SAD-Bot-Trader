# Design notes:
# Layer purposed for definiton of a contract between the user and API.
from trade_trees.dto.trade_tree_branch_parser import TradeTreeBranchParser
from trade_trees.dto.trade_tree_root_parser import TradeTreeRootParser

class FakeRequest(dict):
        def __setattr__(self, name, value):
            object.__setattr__(self, name, value)

class TradeTreeParser():
    def __init__(self) -> None:
        self.rootParser = TradeTreeRootParser()
        self.branchParser = TradeTreeBranchParser()

    def parse_args(self):
        root = self.rootParser.parse_args()
        # TODO Parse the children hierarchy to be stored in the database.
        # Possibly the best place to introduce UUID generation?
        child_request = FakeRequest()
        setattr(child_request, 'json', root['child'])
        setattr(child_request, 'unparsed_arguments', {})
        child = self.branchParser.parse_args(req=child_request, strict=True)
        root.child = child
        return root
