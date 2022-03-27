# Design notes:
# Layer purposed for definiton of a contract between the user and API.
import uuid
from trade_trees.dto.trade_tree_branch_parser import TradeTreeBranchParser
from trade_trees.dto.trade_tree_outcome_parser import TradeTreeOutcomeParser
from trade_trees.dto.trade_tree_root_parser import TradeTreeRootParser

class FakeRequest(dict):
        def __setattr__(self, name, value):
            object.__setattr__(self, name, value)

class TradeTreeParser():
    def __init__(self) -> None:
        self.rootParser = TradeTreeRootParser()
        self.branchParser = TradeTreeBranchParser()
        self.outcomeParser = TradeTreeOutcomeParser()

    def parse_args(self):
        root = self.rootParser.parse_args()
        # TODO Parse the children hierarchy to be stored in the database.
        # Possibly the best place to introduce UUID generation?
        child_request = FakeRequest()
        children = root['child']['children']
        root['child']['children'] = None
        setattr(child_request, 'json', root['child'])
        setattr(child_request, 'unparsed_arguments', {})
        branch = self.branchParser.parse_args(req=child_request, strict=False)
        branch.id = uuid.uuid4()
        root.child = branch
        root.child.children = self.parse_children(children, branch)

        return root

    def parse_children(self, input, parent):
        if(len(input) == 0):
            return None

        if(parent.children == None):
            parent.children = []
        
        iterator = map(self.project_child, input)
        return list(iterator)

    # Recursively call parse_children in order to build a proper structure of the tree.
    def project_child(self, branch):
        child_request = FakeRequest()
        children = {}
        if 'children' in branch:
            children = branch['children']
            branch['children'] = None
        setattr(child_request, 'json', branch)
        setattr(child_request, 'unparsed_arguments', {})
        result = self.branchParser.parse_args(req=child_request, strict=False)
        result.id = uuid.uuid4()
        result.children = self.parse_children(children, result)
        return result