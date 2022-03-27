from functools import reduce

from trade_trees.dbo.trade_tree import TradeTreeBranch


class TradeTreeBranchProjector():
    # Deflate the tree structure into a list of 
    def deflate_branch(self, branch, parent = None):
        result = {
            "id": branch.id,
            "discriminator": branch.discriminator,
            "parent": parent
        }

        if(branch.discriminator == 'schema'):
            result["discriminant"] = branch.discriminant
            result["schema_path"] = branch.schema_path
            result["operation"] = branch.operation

        results = []

        if ('children' in branch) and (branch["children"] != None) and (len(branch.children) != 0):
            for child in branch.children:
                results.extend(self.deflate_branch(child, branch.id))
        
        results.append(result)

        return results

    def fold_branches(self, branch, rootId):
        entity = TradeTreeBranch(
                id = branch["id"],
                discriminator = branch["discriminator"],
                root = rootId,
                children = []
            )

        if(entity.discriminator == 'schema'):
            entity.schema_path = branch["schema_path"]
            entity.discriminant = branch["discriminant"]
            entity.operation = branch["operation"]

        if ('children' in branch) and (branch["children"] != None) and (len(branch.children) != 0):
            for child in branch.children:
                deflated_child = self.fold_branches(child, rootId)
                entity.children.append(deflated_child)
        
        return entity

    def deflate_branches(self, branch, parent = None):
        results = []

        if (len(branch.children) != 0):
            for child in branch.children:
                results.extend(self.deflate_branches(child, branch))
        
        branch.parent = parent

        results.append(branch)

        return results