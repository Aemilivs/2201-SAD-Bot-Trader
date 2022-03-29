from cgitb import reset
from functools import reduce

from API.trade_trees.dbo.trade_tree_discriminator import TradeTreeDiscriminator
from API.trade_trees.dbo.trade_tree_schema_operation import TradeTreeSchemaOperation


class TradeTreeEvaluator():
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

        if discriminator.upper() == TradeTreeDiscriminator.AND.name:
            return self.evaluate_conjuction(branch)

        if discriminator.upper() == TradeTreeDiscriminator.OR.name:
            return self.evaluate_disjunction(branch)

        if discriminator.upper() == TradeTreeDiscriminator.NOT.name:
            return self.evaluate_negation(branch)
        
        if discriminator.upper() == TradeTreeDiscriminator.SCHEMA.name:
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

    def get_value(self, payload, path):
        dot_index = path.find('.')

        if dot_index == -1:
            if path in payload:
                return payload[path]
            else:
                return None

        next_path = path[0:dot_index]
        rest = path[dot_index + 1:]

        return self.get_value(payload[next_path], rest)
    
    def evaluate_schema(self, branch):
        schema_path = branch["schema_path"]
        discriminant = branch["discriminant"]
        operation = branch["operation"]

        # Placeholder for a payload returned by an adapter.
        payload = {
            "value": 1,
            "foo": "bar",
            "bug": {
                "value": 1
            }
        }

        value = self.get_value(payload, schema_path)

        # TODO Replace with a better validation; 
        # Case when a payload does not contain the defined schema path.
        if value == None:
            return False

        if operation.upper() == TradeTreeSchemaOperation.NUMERIC_LESS_COMPARISON.name:
            return float(value) < float(discriminant)

        if operation.upper() == TradeTreeSchemaOperation.NUMERIC_LESS_OR_EQUAL_COMPARISON.name:
            return float(value) <= float(discriminant)

        if operation.upper() == TradeTreeSchemaOperation.NUMERIC_EQUAL_COMPARISON.name:
            return float(value) == float(discriminant)

        if operation.upper() == TradeTreeSchemaOperation.NUMERIC_MORE_COMPARISON.name:
            return float(value) > float(discriminant)

        if operation.upper() == TradeTreeSchemaOperation.NUMERIC_MORE_OR_EQUAL_COMPARISON.name:
            return float(value) >= float(discriminant)

        if operation.upper() == TradeTreeSchemaOperation.STRING_EQUAL_COMPARISON.name:
            return value == discriminant

        if operation.upper() == TradeTreeSchemaOperation.STRING_STARTS_WITH_COMPARISON.name:
            return value.startswith(discriminant)

        if operation.upper() == TradeTreeSchemaOperation.STRING_CONTAINS_COMPARISON.name:
            return discriminant in value

        if operation.upper() == TradeTreeSchemaOperation.STRING_ENDS_WITH_COMPARISON.name:
            return value.endswith(discriminant)

        return False