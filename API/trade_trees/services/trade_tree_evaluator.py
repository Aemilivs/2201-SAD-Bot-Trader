from cgitb import reset
from functools import reduce


class tradeTreeEvaluator():
    # TODO Inject stock API adaptors using DI.
    def __init__(self) -> None:
        pass

    def evaluate_tree(self, tree):
        root_branch = tree["child"]
        
        result = self.evaluate_branch(root_branch)

        # TODO Introduce better error handling.
        if result == None:
            raise Exception("Invalid rule tree is attempted to be processed.")

        if result:
            # Trigger outcome
            # TODO introduce an execution of an actual outcome.
            print("Triggering an outcome")
            return True

        print("Outcomes have not been triggered.")
        return False

    def evaluate_branch(self, branch):
        discriminator = branch["discriminator"]

        if discriminator.upper() == "AND":
            return self.evaluate_conjuction(branch)

        if discriminator.upper() == "OR":
            return self.evaluate_disjunction(branch)

        if discriminator.upper() == "NOT":
            return self.evaluate_negation(branch)
        
        if discriminator.upper() == "SCHEMA":
            return self.evaluate_schema(branch)

        return None

    # Logical operator AND
    def evaluate_conjuction(self, branch):

        def evaluate(left, right):
            return left and right

        children = branch["children"]

        if len(children) < 1:
            return None
        
        projection = map(self.evaluate_branch, children)
        results = list(projection)
        return reduce(evaluate, results)

    # Logical operator OR
    def evaluate_disjunction(self, branch):
        
        def evaluate(left, right):
            return left or right

        children = branch["children"]

        if len(children) < 1:
            return None

        projection = map(self.evaluate_branch, children)
        results = list(projection)
        return reduce(evaluate, results)

    # Logical operator NOT
    def evaluate_negation(self, branch):
        children = branch["children"]

        if len(children) != 1:
            return None

        child = children[0]
        result = self.evaluate_branch(child)
        return not result
    
    def evaluate_schema(self, branch):
        schema_path = branch["schema_path"]
        discriminant = branch["discriminant"]
        operation = branch["operation"]

        # Placeholder
        value = 1

        if operation.upper() == "NUMERICMOREOREQUALCOMPARISON":
            return value >= float(discriminant)

        return False